import socket
import threading


class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 55556
        self.server = None
        self.clients = []
        self.nicknames = []

        self.gui = None
        self.chat_area = None

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        print('Serwer nasłuchuje na {}:{}'.format(self.host, self.port))

        while True:
            client, address = self.server.accept()
            print('Nowe połączenie: {}'.format(address))

            nickname = client.recv(1024).decode('utf-8')

            self.nicknames.append(nickname)
            self.clients.append(client)

            self.broadcast('[SERVER]: {} dołączył do czatu!'.format(nickname))
            self.send_user_list()

            threading.Thread(target=self.handle_client, args=(client,)).start()

    def broadcast(self, message):
        for client in self.clients:
            client.send(message.encode('utf-8'))

    def send_user_list(self):
        user_list = '[USERS]' + ', '.join(self.nicknames)
        self.broadcast(user_list)

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message == 'koniec':
                    self.handle_client_exit(client)
                    break
                else:
                    self.broadcast('[{}]: {}'.format(self.get_nickname(client), message))
            except:
                self.handle_client_exit(client)
                break

    def handle_client_exit(self, client):
        index = self.clients.index(client)
        nickname = self.nicknames[index]
        self.clients.remove(client)
        self.nicknames.remove(nickname)
        self.broadcast('[SERVER]: {} opuścił czat!'.format(nickname))
        client.close()
        self.send_user_list()

    def stop(self):
        for client in self.clients:
            client.close()
        self.server.close()

    @staticmethod
    def get_nickname(client):
        index = server.clients.index(client)
        return server.nicknames[index]


if __name__ == '__main__':
    server = ChatServer()
    server.start()
