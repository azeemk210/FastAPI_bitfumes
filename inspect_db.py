import sqlite3

conn = sqlite3.connect("blog.db")
cursor = conn.cursor()

# View tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# View schema for 'blogs'
cursor.execute("PRAGMA table_info(blogs);")
schema = cursor.fetchall()
print("\nSchema of 'blogs':")
for col in schema:
    print(col)

# View data from 'blogs'
cursor.execute("SELECT * FROM blogs;")
rows = cursor.fetchall()
print("\nData in 'blogs':")
for row in rows:
    print(row)

conn.close()
