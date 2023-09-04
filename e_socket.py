import socket
import sys
import os


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def server(ip, port):
    sock.bind((ip, port))
    sock.listen(1)
    run_server()


def client(ip, port):
    sock.connect((ip, port))


def find_local_servers(): # ChatGpt
    # Создаем UDP сокет
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Включаем опцию широковещательной отправки пакетов
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Устанавливаем тайм-аут приема пакетов
    udp_socket.settimeout(5)

    # Отправляем широковещательное сообщение
    # в формате "SERVER_DISCOVERY_REQUEST"
    udp_socket.sendto(b"CL_SERVER_DISCOVERY_REQUEST", ("<broadcast>", 8085))

    # Пытаемся получить ответные сообщения
    try:
        while True:
            # Принимаем пакет и сохраняем адрес отправителя
            data, address = udp_socket.recvfrom(1024)

            # Проверяем, является ли полученное сообщение
            # ответом от локального сервера
            if data == b"CL_SERVER_DISCOVERY_RESPONSE":
                print("Найден сервер: ", address)
                return address
    except socket.timeout:
        print("Поиск серверов завершен.")


def run_server():
    # Создаем UDP сокет и привязываем его к порту
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", 8085))  # Пустой IP означает привязку ко всем интерфейсам на сервере

    print("Сервер запущен и ожидает запросов...")

    while True:
        # Принимаем пакет и сохраняем адрес отправителя
        data, address = udp_socket.recvfrom(1024)

        # Проверяем, является ли полученное сообщение запросом об обнаружении сервера
        if data == b"CL_SERVER_DISCOVERY_REQUEST":
            print("Обнаружен запрос от клиента: ", address)

            # Отправляем ответное сообщение о нашем сервере
            udp_socket.sendto(b"CL_SERVER_DISCOVERY_RESPONSE", address)
            return

    # Закрываем сокет
    udp_socket.close()


conn_old = None
addr_old = None


class multiplayer_socket:
    def __init__(self, ip, port, type: str, listen=2, action_on_disconnect=None):
        self.sock = sock
        self.type = type  # 1 for server, 2 for client
        self.data = 'TEST'
        self.data_input = 'STRING'
        self.conn_old = None
        self.addr_old = None
        self.ip = ip
        self.port = port
        self.listen = listen
        self.action_on_disconnect = action_on_disconnect
        if self.type == "1":
            server(self.ip, self.port)
            self.sock.listen(self.listen)
            self.conn_old, self.addr_old = self.sock.accept()
        elif self.type == "2":
            print(self.ip, self.port)
            client(self.ip, self.port)
        else:
            print("Invalid input")
            exit(-1)

    def update(self, prinim=1):  # ret
        self.conn = self.conn_old
        self.addr = self.addr_old
        try:
            if self.type == "1":
                self.conn.send(self.data.encode())
                if prinim == 1:
                    self.data_input = self.conn.recv(1024).decode()
            elif self.type == "2":
                sock.send(self.data.encode())
                if prinim == 1:
                    self.data_input = self.sock.recv(1024).decode()
        except:
            '''print('ALL USERS DISCONECTED')
            print('WAIT NEW USERS')
            self.conn_old, self.addr_old = self.sock.accept()'''
            self.action_on_disconnect()
        return self.data_input
