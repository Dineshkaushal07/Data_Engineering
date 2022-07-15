# SPARKIFY

## Intro

A startup called Sparkify wanted to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
To solve their problem this particular data engineering solution was created.

## Languages and tools used

Below are the tools used in this project -

- Jupyter Notebook
- Python Language
- PostgreSQL

## Elements of the project

There are below elements in the project

SQL_QUERIES - This file  basically contins all the postgres SQL script as it is a python executable file so we are just creating a tuple of string which actually is a SQL script.

CREATE_TABLES - This file contains python code to create the basic setup. It is responsible to create connection to Postgres sql and further it creates Database and tables. Every time this file is run existing tables are dropped and new tables are created in the Database.

ETL - This file does all the Extracting Transforming and loading part. 

1. Our Source data is json so first of all we need to read that json file.

2. Then mending the data as per requirement is handled using functios 

3. Then the transformed data is loaded into the tables.

Then we are anble to perform queries to data and get information.

## Flow of Code 

1. First file to be compiled should be sql_queries.py

2. Then comes the turn of create_tables.py because it uses sql_queries.py

3. In the third step we run our etl.py file which uses create_tables.py

4. Then we can run tests on our data.

## Conclusion

Creating data solutions is essential part of any company before moving to data analytics part data engineering part always come so one should be proficient with right set of skills to ace those challenges