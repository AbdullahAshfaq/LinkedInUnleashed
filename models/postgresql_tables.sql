----------------
-- Job Tables --
----------------
DROP TABLE IF EXISTS job_postings;
CREATE TABLE IF NOT EXISTS job_postings (
    job_id                         bigserial primary key,
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
    scraped                         int
);

DROP TABLE IF EXISTS job_benefits;
CREATE TABLE IF NOT EXISTS job_benefits (
    job_id       bigserial,
    inferred     int,
    type        varchar(50)
);
CREATE INDEX job_benefits_idx ON job_benefits(job_id);

DROP TABLE IF EXISTS job_industries;
CREATE TABLE IF NOT EXISTS job_industries (
    job_id       bigserial,
    industry_id    int,
    industry_name  varchar(100)
);
CREATE INDEX job_industries_idx ON job_industries(job_id);

DROP TABLE IF EXISTS job_skills;
CREATE TABLE IF NOT EXISTS job_skills (
    job_id        bigserial,
    skill_abr    varchar(10),
    skill_name   varchar(50)

);
CREATE INDEX job_skills_idx ON job_skills(job_id);

DROP TABLE IF EXISTS job_salaries;
CREATE TABLE IF NOT EXISTS job_salaries (
    salary_id              bigserial,
    job_id                 bigserial,
    max_salary           decimal,
    med_salary           decimal,
    min_salary           decimal,
    pay_period            varchar(20),
    currency              varchar(20),
    compensation_type     varchar(20)
);
CREATE INDEX job_salaries_idx ON job_salaries(job_id);

--------------------
-- Company Tables --
--------------------

DROP TABLE IF EXISTS companies;
CREATE TABLE IF NOT EXISTS companies (
    company_id        bigserial primary key,
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
    company_id     bigserial,
    industry      varchar(100)
);
CREATE INDEX company_industries_idx ON company_industries(company_id);

DROP TABLE IF EXISTS company_specialities;
CREATE TABLE IF NOT EXISTS company_specialities (
    company_id     bigserial,
    speciality    text
);
CREATE INDEX company_specialities_idx ON company_specialities(company_id);

DROP TABLE IF EXISTS company_counts;
CREATE TABLE IF NOT EXISTS company_counts (
    company_id     bigserial,
    employee_count      int,
    follower_count      int,
    time_recorded     decimal
);
CREATE INDEX company_counts_idx ON company_counts(company_id);

-- Company Proxycurl tables

DROP TABLE IF EXISTS company_pc;
CREATE TABLE IF NOT EXISTS company_pc (
    linkedin_internal_id           varchar(20),
    description                    text,
    website                        varchar(500),
    industry                       varchar(50),
    company_size                   varchar(50),
    company_size_on_linkedin      int,
    -- hq                             varchar(50),
    company_type                   varchar(50),
    founded_year                  int,
    -- specialities                   varchar(200),
    -- locations                      varchar(500),
    name                           varchar(200),
    tagline                        varchar(500),
    universal_name_id              varchar(500),
    profile_pic_url                text,
    background_cover_image_url     text,
    search_id                      varchar(200),
    -- similar_companies              text,
    -- updates                        text,
    follower_count                int
);

-----------------------------
-- People Proxycurl tables --
-----------------------------

DROP TABLE IF EXISTS uspeople_pc;
CREATE TABLE IF NOT EXISTS uspeople_pc (
public_identifier                varchar(200),
profile_pic_url                  text,
background_cover_image_url       text,
first_name                       varchar(200),
last_name                        varchar(200),
full_name                        varchar(400),
occupation                       varchar(300),
headline                         varchar(300),
summary                          text,
country                          varchar(10), -- This 2 letter country code
country_full_name                varchar(200),
city                             varchar(200),
state                            varchar(100),
-- experiences                      object,
-- education                        object,
-- languages                        object,
-- accomplishment_organisations     object,
-- accomplishment_publications      object,
-- accomplishment_honors_awards     object,
-- accomplishment_patents           object,
-- accomplishment_courses           object,
-- accomplishment_projects          object,
-- accomplishment_test_scores       object,
-- volunteer_work                   object,
-- certifications                   object,
connections                     decimal,
-- people_also_viewed               object,
-- recommendations                  object,
-- activities                       object,
-- similarly_named_profiles         object,
-- articles                         object,
-- groups                           object,
skills                           text [],
inferred_salary                  varchar(50),
github                           varchar(200),
facebook                         varchar(200),
gender                           varchar(200),
birth_date                       date,
industry                         varchar(20) [],
interests                        varchar(20) []
-- PRIMARY KEY (public_identifier, full_name)
);

select public_identifier, full_name,count(*) from uspeople_pc group by 1,2 having count(*)>1;

select * from uspeople_pc;
where public_identifier like '%alissonslp%';

select * from company_pc where lower(name) like '%nike%';
select * from company_pc;