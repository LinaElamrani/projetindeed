import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO jobs (title, location, postalcode, contract, worktime, userstate,description, salary, category_id, company_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Developer', 'location for the first job' ,'postalcode for the first job','contract for the first job','worktime for the first job','userstate for the first job','description for the first job','salary for the first job','category_id for the first job','company_id for the first job')
            )

cur.execute("INSERT INTO jobs (title, location, postalcode, contract, worktime, userstate,description, salary, category_id, company_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Data analyst', 'location for the job2' ,'postalcode for the job2','contract for the job2','worktime for the job2','userstate for the job2','description for the job2','salary for the job2','category_id for the job2','company_id for the job2')
            )

cur.execute("INSERT INTO jobs (title, location, postalcode, contract, worktime, userstate,description, salary, category_id, company_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('Community Manager', 'location for the job3' ,'postalcode for the job3','contract for the job3','worktime for the job3','userstate for the job3','description for the job3','salary for the job3','category_id for the job3','company_id for the job3')
            )

connection.commit()
connection.close()
