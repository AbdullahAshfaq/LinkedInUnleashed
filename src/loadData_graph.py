import pandas as pd
import json
from utils import mongo_utils, pandas_utils, neo4j_utils

# Generate JSON from Mongo DB
# ('save_as', 'collection', query)
data_dir = './LinkedInUnleashed/data/for_neo4j/'

mongo_creds = {
    'user': 'root',
    'password': 'example',
    'db': 'LUapp',
    'host':'localhost',
    'port': '27017'
}

queries = [
    ('similar_companies.json', 'companies',[
        {"$addFields": {"size_sim_comps": {"$size": "$similar_companies"}}},
        {"$match": {"size_sim_comps": {"$gt": 0}}},
        {"$project": {"name": 1, "similar_companies": 1, "_id": 0}}
    ]),
    ('company_locations.json', 'companies', [
        {"$addFields": {"size_loc": {"$size": "$locations"}}},
        {"$match": {"size_loc": {"$gt": 0}}},
        {"$project": {"name": 1, "locations": 1, "_id": 0}}
    ]),
    ('company_spec.json', 'companies', [
        {"$addFields": {"size_spec": {"$size": "$specialities"}}},
        {"$match": {"size_spec": {"$gt": 0}}},
        {"$project": {"name": 1, "specialities": 1, "_id": 0}}
    ]),
    ('people_experiences.json', 'people',[
        {"$addFields": {"size_exp": {"$size": "$experiences"}}},
        {"$match": {"size_exp": {"$gt": 0}}},
        {"$project": {"public_identifier": 1, "full_name":1, "experiences": 1, "_id":0}}
    ]),
    ('people_education.json', 'people',[
        {"$addFields": {"size_edu": {"$size": "$education"}}},
        {"$match": {"size_edu": {"$gt": 0}}},
        {"$project": {"public_identifier": 1, "full_name":1, "education": 1, "_id":0}}
    ])
]


# Do not edit below here
########################

# data_dir should end with /
if data_dir[-1] != '/':
    data_dir = data_dir+'/'

# Establish a connection to MongoDB
mongoCon = mongo_utils.Mongo_Connector(creds=mongo_creds)

for dest, col, q in queries:
    print(f"Getting data for {dest} from Mongo collection {col} ... ", end=' ')
    result_lst = mongoCon.Mongo2json(collection_name=col, query=q)
    print(f"{len(result_lst)} loaded ...", end=' ')
    with open(data_dir+dest,'w') as f:
        json.dump(result_lst, f)
    print("Saved to file")

print(f"--------------------------------")
print(f"---Running Neo4j Queries now (May take time)")
print(f"--------------------------------")

neo_creds = {
    'host': 'localhost',
    'port': '7687',
    'user': 'neo4j',
    'password': 'neo4j1'
}

neoCon = neo4j_utils.neo_connector(creds=neo_creds)

# One query per list value
neo_queries = [
    # Constraints 1: No duplicate companies
    "CREATE CONSTRAINT on (c:Company) assert c.name IS UNIQUE;",
    "CREATE CONSTRAINT on (i:Industry) assert i.name IS UNIQUE;",
    "CREATE CONSTRAINT on (s:State) assert s.name IS UNIQUE;",
    "CREATE CONSTRAINT on (p:People) assert p.public_identifier IS UNIQUE;",
    "CREATE CONSTRAINT on (e:Edu_Institution) assert e.name IS UNIQUE;",

    # To import nodes Companies
    '''
    load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
    with row where row.name is Not NULL
    merge (c:Company {name: row.name})
    ''',

    # To import Industries
    '''
    load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
    with row where row.industry is Not NULL
    merge (i:Industry {name: row.industry})
    ''',

    # To import Company-Industry relations
    '''
    load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
    Match (c:Company {name: row.name})
    Match (i:Industry {name: row.industry})
    merge (c)-[:WORKS_IN]->(i);
    ''',

    # To import Company-Company relations
    '''
    call apoc.load.json("file:///similar_companies.json") yield value
    match (c:Company{name: value.name})
    unwind value.similar_companies as sim_comp
    merge (d:Company{name:sim_comp.name})
    merge (c)-[:SIMILAR_TO]->(d);
    ''',
    # Check for duplicate nodes
    # match (n)-[:SIMILAR_TO]-(m:Company{name:'adidas'}) return *;

    # To import States and State-Company relations
    '''
    call apoc.load.json("file:///company_locations.json") yield value
    match (c:Company{name: value.name})
    unwind value.locations as loc
    merge (l:State {name: coalesce(loc.state,'UNK')})
    merge (l)<-[r:LOCATED_AT {is_hq: loc.is_hq}]-(c)
    set r.pc = coalesce(loc.postal_code,'0'),
        r.city =  coalesce(loc.city,'')
    ;
    ''',

    # Loading Company Specialities (27k specialities)
    '''
    call apoc.load.json("file:///company_spec.json") yield value
    match (c:Company{name: value.name})
    unwind value.specialities as spec
    merge (s:Speciality {name: spec})
    merge (c)-[:SPECIALIZES_IN]->(s);
    ''',
    # To see a speciality
    # match (s:Speciality {name: 'Google Ads'})-[r]-(m) return *;
    # match (s:Speciality)-[r]-(m) where s.name =~ '.*Google Ads.*' return *;

    # Creating People nodes
    '''
    call apoc.load.json("file:///people_experiences.json") yield value
    merge (p:People {full_name: value.full_name, public_identifier: value.public_identifier});
    ''',

    # Attaching experiences to people
    '''
    call apoc.load.json("file:///people_experiences.json") yield value
    match (p:People {full_name: value.full_name, public_identifier: value.public_identifier})
    unwind value.experiences as exp
    merge (c:Company {name: exp.company})
    merge (p)-[r:EMPLOYEE_IN]->(c)
    set r.is_active = (case when exp.ends_at is NULL then true else false end)
    set r.starts_at = toString(coalesce(exp.starts_at.year,'0000'))+'-'+ toString(coalesce(exp.starts_at.month,'00'))+'-'+ toString(coalesce(exp.starts_at.day, '00'))
    set r.ends_at = toString(coalesce(exp.ends_at.year,'0000'))+'-'+ toString(coalesce(exp.ends_at.month,'00'))+'-'+ toString(coalesce(exp.ends_at.day, '00'))
    set r.title = coalesce(exp.title,'')
    set r.description = coalesce(exp.description,'');

    ''',

    # Create Edu_Institutions and attaching to People
    '''
    call apoc.load.json("file:///people_education.json") yield value
    match (p:People {full_name: value.full_name, public_identifier: value.public_identifier})
    unwind value.education as edu
    merge (u:Edu_Institution {name: coalesce(edu.school,'')})
    set u.linkedin_profile=coalesce(edu.school_linkedin_profile_url,'')
    merge (p)-[r:STUDIED_IN]->(u)
    set r.field_of_study=coalesce(edu.field_of_study,'')
    set r.degree_name=coalesce(edu.degree_name,'')
    set r.starts_at = toString(coalesce(edu.starts_at.year,'0000'))+'-'+ toString(coalesce(edu.starts_at.month,'00'))+'-'+ toString(coalesce(edu.starts_at.day, '00'))
    set r.ends_at = toString(coalesce(edu.ends_at.year,'0000'))+'-'+ toString(coalesce(edu.ends_at.month,'00'))+'-'+ toString(coalesce(edu.ends_at.day, '00'));
    '''
    # In 1st merge, constrain is on u.name so we merge on only that and set remaining properties



]


for q in neo_queries:
    print(f"Running query: \n {q}")
    neoCon.runQuery(q)