import socket
import time
import threading

class UserChat:
    def __init__(self,port):
        
        self.port = port
        self.text = ""
        self.reply = ""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), port))
        print("Connected to server!")
    
    def receive(self,message1):
        message = self.client.recv(1024).decode('ascii')
        self.client.send(message1.encode('ascii'))
        self.client.close()
            


# IT WORKS BUT IS LAGGY AF Check txt for real check logs. Js should only get the text from the txt.

def main():
    user = UserChat(55555)
    user.receive("hel3")

if __name__ == "__main__":
    main()