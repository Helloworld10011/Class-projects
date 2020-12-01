class Node:
    def __init__(self, Id, IP, Port):
        self.Id = Id
        self.IP = IP
        self.Port = Port
        self.Socket= (IP, Port)
    def __repr__(self):
        return 'Node ' + self.Id + \
               ' with IP:' + self.IP+ ' and Port: ' + self.Port


class Message:
    def __init__(self, ):