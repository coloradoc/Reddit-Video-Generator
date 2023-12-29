import sqlite3
con = sqlite3.connect('urls.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS url
                        (urls text)''')




rows=[]
for row in cur.execute('''SELECT * FROM url'''):
    print(row)
    rows.append(row)

print(rows)