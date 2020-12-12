import json
import threading
import sys
from stream import Stream


class Node:
    def __init__(self,
                 uid=None,
                 next=None):

        ''' Network Variables '''
        self.stream = Stream()
        self.address = (self.stream.ip, self.stream.port)
        
        ''' Algorithm Variables '''
        self.uid = uid
        print('node', uid, 'initialized successfully with address:', self.address)

    def run(self):
        while True:
            stream_in_buff = self.stream.read_in_buf()
            for message in stream_in_buff:
                self.handle_message(message)

    def handle_message(self, message):
        print('node', self.uid, "received: ", message)
        self.send_message(message)
        """
        ***note that the initializer itself set the delays during making add_sender by Sender(server_address, delay)
        and the stream Class use sender to send message.
        """
        # DO SOMETHING WITH MESSAGE
        # USE 'self.send_message' FOR SENDING MESSAGES
        # REMEMBER THAT CHANNELS HAVE DELAYS

    def send_message(self, msg):
        self.stream.add_message_to_out_buff(msg)
        self.stream.send_messages()