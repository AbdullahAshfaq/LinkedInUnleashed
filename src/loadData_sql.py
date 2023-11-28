import pandas as pd
from utils.sql_utils import *


data_dir = './data/' # / at the end necessary

# sql creds
creds = {
    'db':"postgresdb",
    'user':"postgres",
    'password':"postgres",
    'host':"localhost",
    'port':"5439"
}

file_list = [
    # (table_name, file_path)
    # People
    ('uspeople_pc','people/us_profiles/10000_random_us_people_profiles.csv'),
    # Jobs
    ('job_postings','companies/company+jobs/job_postings.csv'),
    ('job_skills','companies/company+jobs/job_details/formatted_job_skills.csv'),
    ('job_benefits','companies/company+jobs/job_details/benefits.csv'),
    ('job_industries','companies/company+jobs/job_details/formatted_job_industries.csv'),
    ('job_salaries','companies/company+jobs/job_details/salaries.csv'),
    # Companies
    ('companies','companies/company+jobs/company_details/companies.csv'),
    ('company_industries','companies/company+jobs/company_details/company_industries.csv'),
    ('company_specialities','companies/company+jobs/company_details/company_specialities.csv'),
    ('company_counts','companies/company+jobs/company_details/employee_counts.csv'),
    ('company_pc','companies/us_companies_proxycurl/10000_united_states_companies_profiles.csv')
]

# Creating a SQL connection
pgsql = PostgreSQL_Connector(creds)

# data_dir should end with /
if data_dir[-1] != '/':
    data_dir = data_dir+'/'

# Loop over all files and upload to db
for sql_table, filepath in file_list:
    df = pd.read_csv(data_dir+filepath)
    pgsql.pandas2SQL(input_df=df, dst_table_name=sql_table)





