# DROP TABLE STATEMENTS
indeedjobs_table_drop = "DROP TABLE IF EXISTS IndeedJobs"
company_table_drop = "DROP TABLE IF EXISTS Company"
job_table_drop = "DROP TABLE IF EXISTS Job"
date_table_drop = "DROP TABLE IF EXISTS Date"
description_table_drop = "DROP TABLE IF EXISTS Description"

# CREATE TABLE STATEMENTS
indeedjobs_table_create = ("""CREATE TABLE IF NOT EXISTS 
                                         IndeedJobs(indeed_id int PRIMARY KEY,
                                                    co_id int REFERENCES Company(co_id),
                                                    job_id int REFERENCES Job(job_id), 
                                                    date_id int REFERENCES Date(date_id),
                                                    des_id int REFERENCES Description(des_id), 
                                                    no_of_reviews int, 
                                                    no_of_star float);
""")

company_table_create = ("""CREATE TABLE IF NOT EXISTS 
                                        Company(co_id int PRIMARY KEY, 
                                                co_name varchar, 
                                                location varchar(25),
                                                revenue varchar(25), 
                                                employees varchar(20), 
                                                industry varchar);
""")

job_table_create = ("""CREATE TABLE IF NOT EXISTS 
                                        Job(job_id int PRIMARY KEY, 
                                            job_title varchar, 
                                            job_type varchar(25),
                                            no_of_skill int, 
                                            skills varchar, 
                                            salary varchar(25));
""")

date_table_create = ("""CREATE TABLE IF NOT EXISTS 
                                        Date(date_id int PRIMARY KEY, 
                                             date_since_posted int);
""")

description_table_create = ("""CREATE TABLE IF NOT EXISTS 
                                        Description(des_id int PRIMARY KEY, 
                                                    link varchar, 
                                                    description varchar);
""")

# INSERT STATEMENTS
indeedjobs_table_insert = ("""INSERT INTO IndeedJobs(co_id, job_id, date_id, des_id, no_of_reviews, no_of_star)
                        VALUES(%s,%s,%s,%s,%s,%s)
                        ON CONFLICT
                        DO NOTHING;
""")

company_table_insert = ("""INSERT INTO Company(co_id, co_name, location, revenue, employees, industry)
                        VALUES(%s,%s,%s,%s,%s,%s)
                        ON CONFLICT
                        DO NOTHING;
""")

job_table_insert = ("""INSERT INTO Job(job_id, job_title, job_type, no_of_skill, skills, salary)
                        VALUES(%s,%s,%s,%s,%s,%s)
                        ON CONFLICT
                        DO NOTHING;
""")

date_table_insert = ("""INSERT INTO Date(date_id, date_since_posted)
                          VALUES(%s,%s)
                          ON CONFLICT
                          DO NOTHING;
""")

description_table_insert = ("""INSERT INTO Description(des_id, link, description)
                        VALUES(%s,%s,%s)
                        ON CONFLICT
                        DO NOTHING;
""")


# QUERY LISTS FOR EXECUTION
create_table_queries = [company_table_create, job_table_create, date_table_create, description_table_create,indeedjobs_table_create]
drop_table_queries = [company_table_create, job_table_create, date_table_create, description_table_create,indeedjobs_table_create]