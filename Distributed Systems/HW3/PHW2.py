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
            #print(str(a[0]) + ': ' + str(a[1]) + ' connected')

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
        #print(str(my_ID) + " Connected to the next")
        self.Id = my_ID
        self.delay = delay
        self.list_out = []
        self.counter = 0

        hThread = threading.Thread(target=self.handler, args=())
        #sThread.daemon = True
        hThread.start()

    def handler(self):
        while True:
            if len(self.list_out) > self.counter:
                mess = self.list_out[self.counter]
                self.SendMessage(self.s, mess)
                self.counter += 1

    def SendMessage(self, sock, message):
        time.sleep(self.delay)
        #print("Client " + self.Id + " sent " + str(message))
        m = json.dumps(message.__dict__)
        m = f'{len(m):<{Header_Size}}' + m
        data = sock.send(bytes(m, 'utf-8'))

    def getinput(self, message):
        self.list_out.append(message)


    def shotdown(self):
        self.s.close()



class Node:
    def __init__(self, Id, Neigh_list, delays):
        self.list_in = []
        self.count_in = 0
        self.Id = Id
        self.IP = '127.0.0.1'
        self.Port = self.Id+1
        self.Neighs = Neigh_list
        self.Neigh_delays= delays
        self.clients= []
        assert len(self.Neighs) == len(self.Neigh_delays)
        self.deg= len(self.Neighs)
        self.parent= None
        self.children= []
        self.nonparents= 0
        self.Mark= False
        self.data= 1
        self.collected_data= 0

        sThread = threading.Thread(target=self.make_Server, args=())
        sThread.daemon = True
        sThread.start()

        self.ctrlThread = threading.Thread(target=self.controller, args=())
        self.ctrlThread.start()


    def make_Server(self):
        self.server = Server(self.IP, self.Port, self.Id, self.list_in)


    def run_Client(self):
        for i in range(self.deg):
            self.clients.append(Client('127.0.0.1', self.Neighs[i]+1, self.Id, self.Neigh_delays[i]))
        print("Node #%i is connected" %(self.Id))


    def send_message(self, message, id_list):
        for id in id_list:
            index= self.Neighs.index(id)
            self.clients[index].getinput(message)


    def controller(self):
        while True:
            l = len(self.list_in)
            if (l > self.count_in):
                for i in range(self.count_in, l):
                    message = self.list_in[i].__dict__

                    if message['type'] == 'search':
                        id = message['value']
                        if self.Mark:
                            self.send_message(Message('nonparent', self.Id), [id])
                        else:
                            print("Node #%i received: search from %i for the first time" %(self.Id, id))
                            self.Mark= True
                            self.parent= id
                            self.send_message(Message('parent', self.Id), [self.parent])

                            if self.deg>1:
                                self.send_message(Message('search', self.Id), list(set(self.Neighs)-{self.parent}))
                            else:
                                self.send_message(Message('data', (self.data, self.Id)), [self.parent])

                    elif message['type'] == 'parent':
                        id= message['value']
                        print("Node #%i received: parent from %i" % (self.Id, id))
                        self.children.append(id)

                    elif message['type'] == 'nonparent':
                        id = message['value']
                        print("Node #%i received: nonparent from %i" % (self.Id, id))
                        self.nonparents += 1
                        if (self.nonparents + self.collected_data) == (self.deg - 1):
                            self.send_message(Message('data', (self.data, self.Id)), [self.parent])

                    elif message['type'] == 'data':
                        (data, id)= message['value']
                        print("Node #%i received: data from %i" % (self.Id, id))
                        self.data += data
                        self.collected_data += 1

                        if self.parent==None and self.collected_data == self.deg:
                            print("FINISHED!, number of nodes relative to node %i is %i" % (self.Id, self.data))

                        if self.parent is not None and (self.nonparents + self.collected_data) == (self.deg-1):
                            self.send_message(Message('data', (self.data, self.Id)), [self.parent])


                    else:
                        print("Wrong type of message for " + str(self.Id) + "!!!")

                self.count_in = len(self.list_in)


    def init_search(self):
        if self.deg>0:
            sendm= Message('search', self.Id)
            self.send_message(sendm, self.Neighs)
            self.Mark= True
        else:
            print("FINISHED!, number of nodes relative to node %i is %i" % (self.Id, 1))

    def __repr__(self):
        return 'Node ' + self.Id + \
               ' with IP:' + self.IP + ' and Port: ' + self.Port


ids=[]
dict= {}
Nodes= {}

while True:
    inp= input()
    if not inp:
        break
    (id1, id2, delay) = inp.split()
    id1= int(id1)
    id2 = int(id2)
    delay= int(delay)

    if id1 not in ids:
        ids.append(id1)
        dict["%i_neighs" % (id1)]= []
        dict["%i_delays" % (id1)] = []
    if id2 not in ids:
        ids.append(id2)
        dict["%i_neighs" % (id2)] = []
        dict["%i_delays" % (id2)] = []

    dict["%i_neighs" % (id1)].append(id2)
    dict["%i_delays" % (id1)].append(delay)

    dict["%i_neighs" % (id2)].append(id1)
    dict["%i_delays" % (id2)].append(delay)

for id in ids:
    Nodes["%i" %(id)]= Node(id, dict["%i_neighs" %(id)], dict["%i_delays" %(id)])

time.sleep(0.5)

for id in ids:
    Nodes["%i" %(id)].run_Client()


Nodes["%i" %(ids[0])].init_search()


