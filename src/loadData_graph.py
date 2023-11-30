


# Generate JSON from Mongo DB
# ('save_as', query)
data_dir = './data/for_neo4j/'
queries = [
    ('similar_companies.json',[
    {"$addFields": {"size_sim_comps": {"$size": "$similar_companies"}}},
    {"$match": {"size_sim_comps": {"$gt": 0}}},
    {"$project": {"name": 1, "similar_companies": 1, "_id": 0}}
]),
    ('company_locations.json', [
    {"$addFields": {"size_loc": {"$size": "$locations"}}},
    {"$match": {"size_loc": {"$gt": 0}}},
    {"$project": {"name": 1, "locations": 1, "_id": 0}}
]),
    ('company_spec.json',[
    {"$addFields": {"size_spec": {"$size": "$specialities"}}},
    {"$match": {"size_spec": {"$gt": 0}}},
    {"$project": {"name": 1, "specialities": 1, "_id": 0}}
])

]















# Constraints 1: No duplicate companies
'''
CREATE CONSTRAINT on (c:Company) assert c.name IS UNIQUE
CREATE CONSTRAINT on (i:Industry) assert i.name IS UNIQUE
CREATE CONSTRAINT on (s:State) assert s.name IS UNIQUE
'''

# To import nodes Companies
'''
load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
with row where row.name is Not NULL
merge (c:Company {name: row.name})
'''

# To import Industries
'''
load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
with row where row.industry is Not NULL
merge (i:Industry {name: row.industry})
'''

# To import Company-Industry relations
'''
load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
Match (c:Company {name: row.name})
Match (i:Industry {name: row.industry})
merge (c)-[:WORKS_IN]->(i);
'''

# To import Company-Company relations
'''
call apoc.load.json("file:///similar_companies.json") yield value
match (c:Company{name: value.name})
unwind value.similar_companies as sim_comp
merge (d:Company{name:sim_comp.name})
merge (c)-[:SIMILAR_TO]->(d);
'''
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
'''

# Loading Company Specialities (27k specialities)
'''
call apoc.load.json("file:///company_spec.json") yield value
match (c:Company{name: value.name})
unwind value.specialities as spec
merge (s:Speciality {name: spec})
merge (c)-[:SPECIALIZES_IN]->(s);
'''
# To see a speciality
# match (s:SPECIALITY {name: 'Google Ads'})-[r]-(m) return *;