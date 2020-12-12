import socket
import threading
import json
import time

Header_Size = 20


class Message:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return str({"type": self.type, "value": self.value})


class Server:
    def __init__(self, IP, Port, ID, list):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((IP, Port))
        self.s.listen(1)
        self.Id= ID
        self.list_in= list
        print(self.Id + "Server running...")

        while True:
            c, a = self.s.accept()
            sThread = threading.Thread(target=self.handler, args=(c, a))
            sThread.daemon = True
            sThread.start()
            print(str(a[0]) + ': ' + str(a[1]) + ' connected')

    def handler(self, c, a):
        full_msg = ''
        new_msg = True
        while True:
            try:
                data = c.recv(1024)
                if data:
                    if new_msg:
                        msglen = int(data[:Header_Size])
                        new_msg = False

                    full_msg += data.decode("utf-8")
                    if (len(full_msg) - Header_Size) == msglen:
                        msg = full_msg[Header_Size:]
                        new_msg = True
                        full_msg = ''
                        m = Message(**json.loads(msg, encoding="utf-8"))
                        print("Server " + self.Id + " received "+ str(m))
                        self.list_in.append(m)

            except:
                print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
                break

    def shotdown(self):
        self.s.close()



class Client:
    def __init__(self, IP, Port, my_ID, ID):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.s).connect((IP, Port))
        print(my_ID + " Connected to " + ID)
        self.Id= my_ID

    def SendMessage(self, sock, message):
        print("Client " + self.Id + " sent " + str(message))
        m = json.dumps(message.__dict__)
        m = f'{len(m):<{Header_Size}}' + m
        data = sock.send(bytes(m, 'utf-8'))

    def getinput(self, message):
        cThread = threading.Thread(target=self.SendMessage, args=(self.s, message,))
        cThread.daemon = True
        cThread.start()

    def shotdown(self):
        self.s.close()



class Node:
    def __init__(self, Id, IP, Port, Neigh_Id, Neigh_IP, Neigh_Port):
        self.list_in = []
        self.count_in = 0
        self.Id = Id
        self.IP = IP
        self.Port = Port
        self.Neigh_Id = Neigh_Id
        self.Neigh_IP = Neigh_IP
        self.Neigh_Port = Neigh_Port

        sThread = threading.Thread(target=self.make_Server, args=())
        sThread.daemon = True
        sThread.start()

        self.ctrlThread = threading.Thread(target=self.controller, args=())
        self.ctrlThread.start()


    def make_Server(self):

        self.server = Server(self.IP, self.Port, self.Id, self.list_in)


    def run_Client(self):
        self.client = Client(self.Neigh_IP, self.Neigh_Port, self.Id, self.Neigh_Id)

    def send_message(self, message):
        self.client.getinput(message)

    def controller(self):
        while True:
            l = len(self.list_in)
            if (l > self.count_in):
                for i in range(self.count_in, l):
                    message = self.list_in[i].__dict__

                    if message['type'] == 'start' and message['value'] == 'hello':
                        self.send_message(Message('start', 'hi'))

                    elif message['type'] == 'start' and message['value'] == 'hi':
                        pass

                    elif message['type'] == 'end' and message['value'] == 'goodbye':
                        self.send_message(Message('end', 'bye'))
                        time.sleep(1)
                        self.client.shotdown()
                        print("Client of node " + self.Id + " to " + self.Neigh_Id + " finished!")

                    elif message['type'] == 'end' and message['value'] == 'bye':
                        self.client.shotdown()
                        print("Client of node " + self.Id + " to " + self.Neigh_Id + " finished!")
                    else:
                        print("Wrong type of message for " + self.Id + "!!!")

                self.count_in = len(self.list_in)


    def send_hello(self):
        sendm = Message('start', 'hello')
        self.send_message(sendm)

    def send_end(self):
        sendm = Message('end', 'goodbye')
        self.send_message(sendm)

    def __repr__(self):
        return 'Node ' + self.Id + \
               ' with IP:' + self.IP + ' and Port: ' + self.Port



inp= input()
data= inp.split(" ")

Node1= Node("1" , data[1], int(data[2]), "2" , data[3], int(data[4]))
Node2= Node("2", data[3], int(data[4]), "1", data[1], int(data[2]))

Node1.run_Client()
Node2.run_Client()

inp2= input()
data2= inp2.split(" ")

if data2[2]==data[2]:
    Node1.send_hello()
    time.sleep(3)
    Node1.send_end()
else:
    Node2.send_hello()
    time.sleep(3)
    Node2.send_end()