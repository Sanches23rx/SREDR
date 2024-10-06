import socket


# Параметры сервера
HOST = '192.168.12.77'
PORT = 61


# Сервер TCP
def tcp_server_for_win_logs():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if not data:
                        break
                    print('Received:', data)
                except Exception as e:
                    pass
                    #print(f"Ошибка при приеме данных: {e}")
            conn.close()