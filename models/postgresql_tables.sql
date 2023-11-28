----------------
-- Job Tables --
----------------
DROP TABLE IF EXISTS job_postings;
CREATE TABLE IF NOT EXISTS job_postings (
    job_id                         int primary key,
    company_id                    decimal,
    title                          varchar(300),
    description                    text,
    max_salary                    decimal,
    med_salary                    decimal,
    min_salary                    decimal,
    pay_period                     varchar(20),
    formatted_work_type            varchar(20),
    location                       varchar(100),
    applies                       decimal,
    original_listed_time          decimal,
    remote_allowed                decimal,
    views                         decimal,
    job_posting_url                varchar(200),
    application_url                text,
    application_type               varchar(50),
    expiry                        decimal,
    closed_time                   decimal,
    formatted_experience_level     varchar(50),
    skills_desc                    text,
    listed_time                   decimal,
    posting_domain                 varchar(100),
    sponsored                       int,
    work_type                      varchar(20),
    currency                       varchar(10),
    compensation_type              varchar(50),
    scraped                         int,
);

DROP TABLE IF EXISTS job_benefits;
CREATE TABLE IF NOT EXISTS job_benefits (
    job_id       int primary key,
    inferred     int,
    type        varchar(50)
);

DROP TABLE IF EXISTS job_industries;
CREATE TABLE IF NOT EXISTS job_industries (
    job_id       int primary key,
    industry_id    int,
    industry_name  varchar(100)
);

DROP TABLE IF EXISTS job_skills;
CREATE TABLE IF NOT EXISTS job_skills (
    job_id        int primary key,
    skill_abr    varchar(10),
    skill_name   varchar(50)
);

DROP TABLE IF EXISTS job_skills;
CREATE TABLE IF NOT EXISTS job_skills (
    salary_id              int primary key,
    job_id                 int,
    max_salary           decimal,
    med_salary           decimal,
    min_salary           decimal,
    pay_period            varchar(20),
    currency              varchar(20),
    compensation_type     varchar(20)
);

--------------------
-- Company Tables --
--------------------

DROP TABLE IF EXISTS companies;
CREATE TABLE IF NOT EXISTS companies (
    company_id        int primary key,
    name             varchar(200),
    description      text,
    company_size    decimal,
    state            varchar(100),
    country          varchar(10),
    city             varchar(200),
    zip_code         varchar(100),
    address          varchar(200),
    url              varchar(300)
);

DROP TABLE IF EXISTS company_industries;
CREATE TABLE IF NOT EXISTS company_industries (
    company_id     int primary key,
    industry      varchar(100)
);

DROP TABLE IF EXISTS company_specialities;
CREATE TABLE IF NOT EXISTS company_specialities (
    company_id     int primary key,
    speciality    text
);

DROP TABLE IF EXISTS company_counts;
CREATE TABLE IF NOT EXISTS company_counts (
    company_id     int primary key,
    employee_count      int,
    follower_count      int,
    time_recorded     decimal
);

-- Company Proxycurl tables


DROP TABLE IF EXISTS company_pc;
CREATE TABLE IF NOT EXISTS company_pc (
    linkedin_internal_id           varchar(20) primary key,
    description                    text,
    website                        varchar(500),
    industry                       varchar(50),
    company_size                   varchar(50),
    company_size_on_linkedin      int
    -- hq                             varchar(50)
    company_type                   varchar(50)
    founded_year                  int
    -- specialities                   varchar(200)
    -- locations                      varchar(500)
    name                           varchar(200)
    tagline                        varchar(500)
    universal_name_id              varchar(500)
    profile_pic_url                text
    background_cover_image_url     text
    search_id                      varchar(200)
    -- similar_companies              text
    -- updates                        text
    follower_count                int
);

