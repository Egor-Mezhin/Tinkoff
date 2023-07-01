import sqlite3
import test_bd

conn = sqlite3.connect("orders.db")
cursorsed = conn.cursor()


# cursorsed.executemany("INSERT INTO ready_text(id_category, title, text) VALUES (?, ?, ?)", 1111)
# conn.commit()


# x = "Прив"
# select_text = cursorsed.execute(f"""
# SELECT ready_text.title, ready_text.text 
# FROM ready_text
# JOIN ready_category ON 
# ready_category.id = ready_text.id_category
# WHERE ready_category.title = "{x}";
# """)
# one_result = cursorsed.fetchall()
# print(one_result)


cursorsed.execute("""
UPDATE counter 
SET count = count - 1""")

cursorsed.execute("SELECT count FROM counter")
x = cursorsed.fetchone()
print(x)
conn.commit()