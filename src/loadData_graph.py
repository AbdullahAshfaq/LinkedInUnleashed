

# To import nodes
'''
load csv with headers from"file:///10000_united_states_companies_profiles.csv" as row
with row where row.name is Not NULL
merge (c:Company {name: row.name})
'''

