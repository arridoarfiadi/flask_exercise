import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

#users = [(1,"ant", "asdf"), (2,"bob","gfds"), (3,"clair", "qwer")]
#insert_query = "INSERT INTO users VALUES (?,?,?)"
#cursor.executemany(insert_query,users)


create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)
cursor.execute("INSERT INTO items VALUES ('test', 11.12)")


connection.commit()
connection.close()