import sqlite3

def insertUser(email ,paswword):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (email, paswword) VALUES (?,?)", (email,paswword))
    con.commit()
    con.close()


def retrieveUsers():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT email, paswword FROM users")
	users = cur.fetchall()
	con.close()
	return users
