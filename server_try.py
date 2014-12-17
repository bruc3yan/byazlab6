# import socket
# port = 5006
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind(("", port))
# print "waiting on port:", port
# while 1:
#     data, addr = server_socket.recvfrom(1024)
#     print data
import threading
import time
import SocketServer
import sys
from integer import Integer
import os
#usage: python server.py (servername)

os.system('clear')
# Hard coded a list of servers & ports
SERVERS = {}
SERVERS["s1"] = ('localhost', 1000)
SERVERS["s2"] = ('localhost', 2000)

# Dict of integers
DATA_LIBRARY = {} 

COUNTER = Integer('meow')
COUNTER.set(55)

# Server name of this server
THIS_SERVER = sys.argv[1]

JOB_QUEUE = {}

class ClientRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Client listener")
        cur_thread_name = threading.current_thread().getName()
        print("{} hears (out of {}) from {} : ".format(cur_thread_name, threading.active_count(), self.client_address))
        print(data)
        for server in SERVERS.keys():
            HOST, PORT = SERVERS[server][0], SERVERS[server][1]
            print 'HOST, PORT', (HOST, PORT)
            socket.sendto(data, (HOST,PORT))
        # count = 2
        # if self.client_address[1] == 1000 or self.client_address[1] == 2000:
        #     print 'thread is joining.'
        #     threading.current_thread().terminate()
        #     threading.current_thread().join()
        # while count:
        #     ack = socket.recv(1024)
        #     if 's1' in ack:
        #         count = count -1
        #     if 's2' in ack:
        #         count = count -1
        #     print 'ack from ', ack, '   count is ', count


        socket.sendto(data.upper(), self.client_address)


class ServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Server listener")
        cur_thread = threading.current_thread().getName()
        print("{} hears (out of {}) from server {} : ".format(cur_thread, threading.active_count(), self.client_address))
        print(data)
        server_address = (self.client_address[0], self.client_address[1] -1)
        print 'yoooo    ', server_address
        boo = COUNTER.get()
        COUNTER.set(boo-1)
        print 'boo is ', boo
        print 'The counter is ', COUNTER.get()
        # count = 2
        # while count:
        #     ack = socket.recv(1024)
        #     if 's1' in ack:
        #         count = count -1
        #     if 's2' in ack:
        #         count = count -1
        #     print 'ack receivedd from ', ack, '   count is ', count

        socket.sendto('ack from ' + THIS_SERVER, server_address)
        # socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): 
        pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    this_server = 's1'

    try:
        print SERVERS
    	this_server = SERVERS[THIS_SERVER]
    	HOST, PORT = this_server[0], this_server[1]
        print 'HOST, PORT', HOST, PORT
    except StandardError:
    	print 'No server name is entered.'
    	HOST, PORT = "127.0.0.1", 8000

    thread_name = threading.current_thread().name

    if "MainThread" in thread_name:
    	# port 8001 -> client messages comes here
	    client_interface = ThreadedUDPServer((HOST,PORT+1), ClientRequestHandler)
	    client_listener = threading.Thread(target=client_interface.serve_forever)
	    client_listener.setDaemon(True)
	    client_listener.setName('GotDamnUDP')
	    print client_listener.getName()
	    print threading.active_count()
	    print("Client listener at port", PORT+1)
	    client_listener.start()
	    print threading.active_count()

	    # port 8000 -> server messages comes here
	    server_interface = ThreadedUDPServer((HOST,PORT), ServerRequestHandler) 
	    server_listener = threading.Thread(target=server_interface.serve_forever)
	    server_listener.setDaemon(True)
	    print("Server listener at port", PORT)
	    server_listener.start()
	    print threading.active_count()

    while 1:
    	time.sleep(1)