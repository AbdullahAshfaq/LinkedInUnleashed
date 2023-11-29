import pandas as pd
import json
from utils import mongo_utils, pandas_utils

"""
Defined in mongodb docker-compose.yml
"""

creds = {
    'user': 'root',
    'password': 'example',
    'db': 'LUapp',
    'host':'localhost',
    'port': '27017'
}



data_dir = "./data/"  # / at the end necessary


file_list = [
    # (Collection,cols, filepath)
    (
        "people",
        "people/us_profiles/10000_random_us_people_profiles.csv",
        [
            "public_identifier",
            "full_name",
            "experiences",
            "education",
            "languages",
            "accomplishment_organisations",
            "accomplishment_publications",
            "accomplishment_honors_awards",
            "accomplishment_patents",
            "accomplishment_courses",
            "accomplishment_projects",
            "accomplishment_test_scores",
            "volunteer_work",
            "certifications",
            "people_also_viewed",
            "recommendations",
            "activities",
            "similarly_named_profiles",
            "articles",
            "groups",
        ],
    ),
    (
        "companies",
        "companies/us_companies_proxycurl/10000_united_states_companies_profiles.csv",
        ["linkedin_internal_id","website","industry","hq", "specialities", "locations", "similar_companies", "updates"],
    )
]

# data_dir should end with /
if data_dir[-1] != '/':
    data_dir = data_dir+'/'


for col, filepath, fields in file_list:
    print(f"-----------------------------------")
    print(f"Processing {filepath.split('/')[-1]} ...")
    print(f"-----------------------------------")
    # col, filepath, fields = file_list[1]

    df = pd.read_csv(data_dir+filepath)
    # Keep only the columns we want to transfer to mongodb
    df = df[fields] 

    # Converting strings in columns to json
    df = pandas_utils.cols2json(df)

    # Establish a connection to MongoDB
    mongoCon = mongo_utils.Mongo_Connector(creds=creds)

    # Transfer DF to Mongo. The json columns of DF will be json in MongoDB
    print(f"Loading {filepath.split('/')[-1]} into MongoDB ", end=' ')
    result = mongoCon.df2Mongo(collection_name=col, df=df)
    print(f"{col} collection loaded")
