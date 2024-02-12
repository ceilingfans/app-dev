import socket
import time
from dhooks import Webhook
import threading


class AdminChat:
    def __init__(self,port,username, filename):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.port = port
        self.host = socket.gethostname()
        self.text = ""
        self.filename = filename
        self.toggled = True
        self.reply = ""
        
    def receive(self):
        while True:
            if self.text == "":
                continue
            message = self.text
            with open(self.filename, "a") as file:
                file.write(f'{self.username}:{message}\n')
            message = message.encode('ascii')
            self.conn.send(message)
            self.text = ""
            # If admin says bye the chat gets logged to discord and ends.
            if message.decode('ascii') == "bye":
                with open(self.filename, "r") as file:
                    contents = file.read()
                    hook = Webhook(
        "https://discord.com/api/webhooks/1198939240235532358/Gu5Dw7cmkupwqo9yg-PgdSKXlj1toWbCHsSqQUabIJc-A3dOlHfDdVkkqwurh34wXdaR")
                    hook.send(contents)
                self.conn.close()
                break
            incoming_message = self.conn.recv(1024).decode('ascii')
            print(f"User:{incoming_message}")
            self.reply = incoming_message
            
    def connect(self):
        while True:
            try:
                self.socket.bind((self.host, self.port))
                self.socket.listen()
                self.conn , self.addr = self.socket.accept()
                print(f"Connected with {self.addr}")
                break
            except: 
                print("reconnecting staff")
                time.sleep(1)
        print(f"Connected with {self.addr}")
        self.receive()
    
    def set_text(self, text):
        self.text = text
        return self.text
    
    def get_reply(self):
        return self.reply


# IT WORKS BUT IS LAGGY AF Check txt for real check logs. Js should only get the text from the txt.

def main():
    admin = AdminChat(55555,"Admin","text.txt")
    admin_thread = threading.Thread(target=admin.connect, args=())
    admin_thread.start()
    while True:
        text = input("Admin:")
        admin.set_text(text)

if __name__ == "__main__":
    main()