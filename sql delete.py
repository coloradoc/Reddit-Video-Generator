import sqlite3
con = sqlite3.connect('titles.db')
cur = con.cursor()


sql_Delete_query = """Delete from title where '''SELECT * FROM title''' = 'If brands were brutally honest, what brand would have what slogan?' """
cur.execute(sql_Delete_query)
con.commit() 

rows=[]
for row in cur.execute('''SELECT * FROM title'''):
    print(row)

    rows.append(row)

print(rows)