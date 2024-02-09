import socket
import time
import threading

class UserChat:
    def __init__(self,port,username, filename):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.port = port
        self.filename = filename
        self.text = ""
        self.reply = ""
    
    def receive(self):
        while True:
            incoming_message = self.client.recv(1024)
            incoming_message = incoming_message.decode('ascii')
            print(f"Admin:{incoming_message}")
            while self.text == "":
                message = self.text
            with open(self.filename, "a") as file:
                file.write(f'{self.username}:{message}\n')
            message = message.encode('ascii')
            self.client.send(message)
            self.text = ""
            self.reply = incoming_message

    def connect(self):
        while True:
            try:
                self.client.connect((socket.gethostname(), self.port))
                print("connected")
                break
            except:
                print("reconnecting cus")
                time.sleep(1)
        self.receive()
        
        
    def set_text(self, text):
        self.text = text
        return self.text
    
    def get_reply(self):
        return self.reply


# IT WORKS BUT IS LAGGY AF Check txt for real check logs. Js should only get the text from the txt.

def main():
    user = UserChat(55555,"User","text.txt")
    user_thread = threading.Thread(target=user.connect, args=())
    user_thread.start()
    while True:
        text = input("User:")
        user.set_text(text)

if __name__ == "__main__":
    main()