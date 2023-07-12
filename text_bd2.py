import sqlite3

# Создание связующей таблицы
conn = sqlite3.connect('orders.db')
cur = conn.cursor()

cur.execute("SELECT num, title FROM ready_category WHERE title = 'Прив1';")
category_list = cur.fetchall()

print(category_list == [])
