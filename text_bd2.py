import sqlite3

# Создание связующей таблицы
conn = sqlite3.connect('mydatabase.db')
cur = conn.cursor()

ready_text_table = cur.execute("""CREATE TABLE IF NOT EXISTS ready_text_time(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   id_category INTEGER,
   title TEXT,
   text TEXT);
""")

print("++++++++++")
