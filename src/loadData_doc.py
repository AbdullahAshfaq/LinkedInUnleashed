import pandas as pd


data_dir = "./data/"  # / at the end necessary


file_list = [
    # (Collection,cols, filepath)
    (
        "People",
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
        "Companies",
        "companies/company+jobs/company_details/companies.csv",
        ["hq", "specialities", "locations", "similar_companies", "updates"],
    )
]
