import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO jobs (title, location, postalcode, contract, worktime, userstate,description, salary, category_id, company_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ('title jobs', 'location for the first jobs' ,'postalcode for the first job','contract for the first job','worktime for the first job','userstate for the first job','description for the first job','salary for the first job','category_id for the first job','company_id for the first job')
            )

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )

connection.commit()
connection.close()
