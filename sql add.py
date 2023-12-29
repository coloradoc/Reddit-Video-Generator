import sqlite3
con = sqlite3.connect('titles.db')
cur = con.cursor()

cur.execute("INSERT OR IGNORE INTO title VALUES (?)", ("What's an unspoken rule that annoys you when people don't know about it?",)) 

con.commit() 

rows=[]
for row in cur.execute('''SELECT * FROM title'''):
    print(row)

    rows.append(row)

print(rows)