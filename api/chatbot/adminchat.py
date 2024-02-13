import socket
import time
from dhooks import Webhook
import threading


class AdminChat:
    def __init__(self,port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = socket.gethostname()
        self.text = ""
        self.clients = []
        self.nicknames = []
        self.should_reload = False
        
    def broadcast(self, message):
        for client in self.clients:
            client.send(message)
    def handle(self,client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                self.broadcast(message)
            except:
                # Removing And Closing Clients
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('ascii'))
                self.nicknames.remove(nickname)
                break
    def receive(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        while True:
            # Accept Connection
            client, address = self.socket.accept()
            print("Connected with {}".format(str(address)))
            # Request And Store Nickname
            client.send('hello'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')  # Receive and store the nickname sent by the client
            
            print(nickname)
            if self.text != nickname:
                self.text = nickname
                self.should_reload = True
                
            # Print And Broadcast Nickname
            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
    def should_reload(self):
        self.should_reload = False
        return self.should_reload

# IT WORKS BUT IS LAGGY AF Check txt for real check logs. Js should only get the text from the txt.

def main():
    admin = AdminChat(55555)
    threading.Thread(target=admin.receive, args=()).start()
    print("aware")

        

if __name__ == "__main__":
    main()