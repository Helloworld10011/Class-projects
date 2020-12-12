import socket
import threading
import json
import time

Header_Size = 20


class Message:
    def __init__(self, nid, type, value):
        self.nid = nid
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return str(self.nid) + " " + self.type + " " + str(self.value)


class Server:
    def __init__(self, IP, Port, ID, list):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((IP, Port))
        self.s.listen(1)
        self.Id= ID
        self.list_in= list
        #print("%i's Server running..." %(self.Id))

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

    def SendMessage(self, sock, message):
        time.sleep(self.delay)
        # print("Client " + self.Id + " sent " + str(message))
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
    def __init__(self, Id, Neigh_list, delays, timeouts):
        self.list_in = []
        self.count_in = 0
        self.Id = Id
        self.IP = '127.0.0.1'
        self.Port = self.Id + 1040
        self.Neighs = Neigh_list
        self.Neigh_delays= delays
        self.clients= []
        assert len(self.Neighs) == len(self.Neigh_delays)
        self.deg= len(self.Neighs)
        self.timeout1, self.timeout2, self.timeout3= timeouts
        self.time= time.time()
        self.state= 0
        self.ballot= 0
        self.proposed= -1
        self.ballot_proposed= 0
        self.value= None
        self.do= 0


        sThread = threading.Thread(target=self.make_Server, args=())
        sThread.daemon = True
        sThread.start()

        self.ldrThread = threading.Thread(target=self.leader_part, args=())
        self.ldrThread.start()

        self.ctrlThread = threading.Thread(target=self.controller, args=())
        self.ctrlThread.start()

    def make_Server(self):
        self.server = Server(self.IP, self.Port, self.Id, self.list_in)


    def run_Client(self):

        for i in range(self.deg):
            self.clients.append(Client('127.0.0.1', self.Neighs[i] + 1040, self.Id, self.Neigh_delays[i]))
        #print("Node #%i is connected" %(self.Id))


    def send_message(self, message, id_list):
        for id in id_list:
            index= self.Neighs.index(id)
            self.clients[index].getinput(message)


    def leader_part(self):
        while True:
            if self.state==3:
                break

            if self.state==0 and (time.time()-self.time> self.timeout1) and self.do == 0:
                self.state= 1
                self.ballot+= 1
                self.pot_ack= 0
                self.do= 1
                self.prop_value= self.proposed
                self.ballot_prop_value= self.ballot_proposed
                mess= Message(self.Id, "POTENTIAL_LEADER", self.ballot)
                self.send_message(mess, self.Neighs)
                self.time= time.time()

            elif self.state==1:
                if (time.time()-self.time)> self.timeout2:
                    self.state= 0
                    self.time= time.time()
                elif self.pot_ack> (self.deg+1)/2-1:
                    self.state= 2
                    self.prop_ack= 0
                    if self.prop_value is -1:
                        self.prop_value= (self.deg+1)*self.Id
                    mess= Message(self.Id, "V_PROPOSE", (self.ballot, self.prop_value))
                    self.send_message(mess, self.Neighs)
                    self.time= time.time()
                    self.ballot_proposed= self.ballot
                    self.proposed= self.prop_value

            elif self.state==2:
                if (time.time()-self.time)> self.timeout3:
                    self.state= 0
                    self.time= time.time()
                elif self.prop_ack> (self.deg+1)/2-1:
                    mess= Message(self.Id, "V_DECIDE", self.prop_value)
                    self.send_message(mess, self.Neighs)
                    self.state= 3
                    print("Node %i Decided on %i and halted!" %(self.Id, self.prop_value))


    def controller(self):
        while True:
            if self.state==3:
                break

            l = len(self.list_in)
            if (l > self.count_in):
                #self.time= time.time()

                for i in range(self.count_in, l):
                    message = self.list_in[i].__dict__

                    if message['type'] == 'POTENTIAL_LEADER':
                        if message['value']>self.ballot and self.state == 0:
                            print("node %i: " %(self.Id) + str(self.list_in[i]))
                            self.time= time.time()
                            id= message['nid']
                            self.ballot= message["value"]
                            value= (self.ballot_proposed, self.proposed)
                            mess= Message(self.Id, "POTENTIAL_LEADER_ACK", value)
                            self.send_message(mess, [id])

                    elif message['type'] == "V_PROPOSE":
                        if message['value'][0]>= self.ballot and self.state == 0:
                            print("node %i: " % (self.Id) + str(self.list_in[i]))
                            self.time = time.time()
                            id = message['nid']
                            self.ballot = message["value"][0]
                            self.ballot_proposed= self.ballot
                            self.proposed= message["value"][1]
                            mess= Message(self.Id, "V_PROPOSE_ACK", -1)
                            self.send_message(mess, [id])

                    elif message['type'] == "V_DECIDE":
                        print("node %i: " % (self.Id) + str(self.list_in[i]))
                        self.time = time.time()
                        self.value= message["value"]
                        self.state= 3

                    elif message['type'] == "POTENTIAL_LEADER_ACK" and self.state == 1:
                        print("node %i: " % (self.Id) + str(self.list_in[i]))
                        self.pot_ack += 1
                        ballot= message["value"][0]
                        if ballot> self.ballot_prop_value:
                            self.ballot_prop_value= ballot
                            self.prop_value= message["value"][1]

                    elif message['type'] == "V_PROPOSE_ACK" and self.state == 2:
                        print("node %i: " % (self.Id) + str(self.list_in[i]))
                        self.prop_ack += 1

                    #else:
                    #    print(message)
                    #    print("Wrong type of message for " + str(self.Id) + "!!!")

                self.count_in = len(self.list_in)



    def __repr__(self):
        return 'Node ' + self.Id + \
               ' with IP:' + self.IP + ' and Port: ' + self.Port


n= int(input())
Nodes= []
ids= []
Neighs = []
delays = []
timeouts= []

for _ in range(n):
    id, timeout1, timeout2, timeout3= input().split()
    id= int(id)
    timeout= (float(timeout1), float(timeout2), float(timeout3))
    Neigh= []
    delay= []
    for _ in range(n-1):
        Neigh_id, Neigh_delay= input().split()
        Neigh.append(int(Neigh_id))
        delay.append(float(Neigh_delay))
    ids.append(id)
    Neighs.append(Neigh)
    delays.append(delay)
    timeouts.append(timeout)

for i in range(n):
    Nodes.append(Node(ids[i], Neighs[i], delays[i], timeouts[i]))

time.sleep(0.5)

for i in range(n):
    Thread = threading.Thread(target=Nodes[i].run_Client, args=())
    Thread.start()
