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
        print("%i's Server running..." %(self.Id))

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
                        #print("Server " + str(self.Id) + " received "+ str(m))
                        self.list_in.append(m)

            except:
                print(str(a[0]) + ':' + str(a[1]) + 'disconnected')
                break

    def shotdown(self):
        self.s.close()



class Client:
    def __init__(self, IP, Port, my_ID, delay):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        (self.s).connect((IP, Port))
        print(str(my_ID) + " Connected to the next")
        self.Id= my_ID
        self.delay= delay

    def SendMessage(self, sock, message):
        time.sleep(self.delay)
        #print("Client " + self.Id + " sent " + str(message))
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
    def __init__(self, Id, IP, Port, Neigh_IP, Neigh_Port, delay, state):
        self.list_in = []
        self.count_in = 0
        self.Id = Id
        self.IP = IP
        self.Port = Port
        self.Neigh_IP = Neigh_IP
        self.Neigh_Port = Neigh_Port
        self.delay= delay
        self.state= state

        sThread = threading.Thread(target=self.make_Server, args=())
        sThread.daemon = True
        sThread.start()

        self.ctrlThread = threading.Thread(target=self.controller, args=())
        self.ctrlThread.start()


    def make_Server(self):
        self.server = Server(self.IP, self.Port, self.Id, self.list_in)

    def run_Client(self):
        self.client = Client(self.Neigh_IP, self.Neigh_Port, self.Id, self.delay)

    def send_message(self, message):
        self.client.getinput(message)

    def controller(self):
        while True:
            l = len(self.list_in)
            if (l > self.count_in):
                for i in range(self.count_in, l):
                    message = self.list_in[i].__dict__

                    if message['type'] == 'value':
                        if message['value']< self.Id:
                            print("node %i: ELECTION %i" % (self.Id, message['value']))
                        elif message['value']>self.Id:
                            print("node %i: ELECTION %i" % (self.Id, message['value']))
                            self.send_message(Message('value', message['value']))
                        else:
                            self.state[0]= "leader"
                            print("node %i: ELECTION %i" % (self.Id, message['value']))
                            print("node %i: LEADER %i" %(self.Id, self.Id))
                            self.send_message(Message('leader', self.Id))

                    elif message['type']== 'leader':
                        if self.state[0]== 'unknown':
                            self.state[0] = "chosen"
                            print("node %i: LEADER %i" % (self.Id, message['value']))
                            self.send_message(self.list_in[i])

                    else:
                        print("Wrong type of message for " + str(self.Id) + "!!!")

                self.count_in = len(self.list_in)


    def send_value(self):
        sendm = Message('value', self.Id)
        self.send_message(sendm)

#    def send_end(self):
#        sendm = Message('end', 'goodbye')
#        self.send_message(sendm)


    def __repr__(self):
        return 'Node ' + self.Id + \
               ' with IP:' + self.IP + ' and Port: ' + self.Port



n= int(input())
node_ids=[]
node_delays=[]
Nodes=[]
states= [['unknown'] for k in range(n)]

for k in range(n):
    [id, delay]= (input().split())
    id = int(id)
    delay = int(delay)
    node_ids.append(id)
    node_delays.append(delay)

for k in range(n):
    Nodes.append(Node(node_ids[k], '127.0.0.1', node_ids[k], '127.0.0.1', node_ids[((k+1)%n)], node_delays[k], states[k]))

for k in range(n):
    Nodes[k].run_Client()

for k in range(n):
    Nodes[k].send_value()

while True:
    if all([states[k][0]!= 'unknown' for k in range(n)]):
        if sum(1*[states[k][0]== 'leader' for k in range(n)]):
            index= [states[k][0] for k in range(n)].index('leader')
            node= node_ids[index]
            print("Election is over. Leader UID is %i" %(node))
            break
        else:
            print("Election is over. But something's wrong!")
            break

