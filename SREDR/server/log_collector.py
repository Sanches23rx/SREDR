import socket
import threading
import sqlite3
import datetime

# Параметры сервера
#HOST = '192.168.12.77'
#PORT = 61

HOST_WIN = '192.168.1.11'
PORT_WIN = 61

HOST_LNX = '192.168.1.11'
PORT_LNX = 60

def write_host_info(log_type, addr):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    if len(cursor.execute(f"SELECT ip FROM endpoints WHERE ip == '{addr}'").fetchall()) == 0:
        cursor.execute(f"INSERT INTO endpoints VALUES (?, ?)", (addr,log_type))
        print('New ip added')

    conn.commit()
    conn.close()


def write_log_to_db(log_type, data):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO {log_type} VALUES (?)", (data,))
    #print('Data wirited:', data[:30])
    #print(cursor.execute(f"SELECT COUNT(*) FROM {log_type}").fetchall())

    conn.commit()
    conn.close()

# Обработчик подключения, поток забирает себе эту функцию
def handle_client(conn, addr, log_type):
    print('[NEW CONNECTION] - Connected by:', addr)
    write_host_info(log_type, addr[0])
    connected = True
    try:
        while connected:
            print('wait:', str(datetime.datetime.now()))
            try:
                data = conn.recv(6096).decode('utf-8')
                if not data:
                    break
                if data == '!DISCONNECT':
                    connected = False
                write_log_to_db(log_type, addr[0])
                print('Received:', data[:30], ' - ', data[-30:], ', ip:', str(addr))
            except Exception as e:
                print('Ошибка получения данных:', e)
                pass
    except socket.timeout:
                print(f"Тайм-аут соединения с {addr}. Закрытие соединения.")
    finally:
        conn.close()
        print(f"Соединение с {addr} закрыто.")


# Перехватчик подключений
def initial_connect_handler(HOST, PORT, os_type):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    while True:
        conn, addr = server.accept()
        conn.settimeout(100)
        thread = threading.Thread(target=handle_client, args=(conn, addr, os_type))
        thread.start()


# Сервер TCP
def start_log_collector():  
    print(f'Server listening on\n Windows logs:{HOST_WIN}:{PORT_WIN}\n Linux logs:{HOST_LNX}:{PORT_LNX}')

    threading.Thread(target=initial_connect_handler, args=(HOST_WIN, PORT_WIN, 'windows')).start()
    threading.Thread(target=initial_connect_handler, args=(HOST_LNX, PORT_LNX, 'linux')).start()