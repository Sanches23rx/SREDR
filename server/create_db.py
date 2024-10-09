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
         CREATE TABLE IF NOT EXISTS Linux (
             logs TEXT
         )
     ''')
    # Добавим несколько записей для примера
    conn.commit()
    conn.close()