import sqlite3

def create_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    # Создаем таблицу, если она не существует
    #cursor.execute('''
    #    CREATE TABLE IF NOT EXISTS records (
    #        id INTEGER PRIMARY KEY AUTOINCREMENT,
    #        data TEXT NOT NULL,
    #        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #    )
    #)
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS windows (
             logs TEXT
         )
     ''')
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS linux (
             logs TEXT
         )
     ''')
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS endpoints (
             ip TEXT, os_type TEXT, hostname TEXT, os_ver_info TEXT, userID TEXT
         )
     ''')
    # Добавим несколько записей для примера
    conn.commit()
    conn.close()