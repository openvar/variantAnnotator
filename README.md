# HGVS Variant Database
Building an interactive app that validates genomic variant descriptions in the HGVS format and adds them to a database 
in a suitable format for publication. The process of generating c. and p. descriptions is automated. Note: This app 
should only be used for variants identified by DNA sequencing techniques

### Running the app
```bash
$ streamlit run app.py
```

### Tasks
- Fix the SQL queries in the search terms, Insert statement and create table
- Once fixed and working, move the SQL statements from the app into the db_mysql MySql object
- Take a look at the insert code. The way inserts are carried out is important. The structure is 
cursor.execute(query, values) and prevents 
[SQL injection](https://stackoverflow.com/questions/49193680/improve-sql-insert-query-to-avoid-sql-injections) 