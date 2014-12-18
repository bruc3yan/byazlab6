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
import signal
try:
    import cPickle as pickle
except:
    import pickle
#usage: python server.py (servername)

os.system('clear')
# Hard coded a list of servers & ports
SERVERS = {}
SERVERS["s1"] = ('localhost', 1000)
SERVERS["s2"] = ('localhost', 2000)
NUM_SERVERS = 2

# Dict of integers
DATA_LIBRARY = {} 

COUNTER = Integer('meow')
COUNTER.set(0)

# Server name of this server
THIS_SERVER = sys.argv[1]

# The waiting queue for this server
# the key is the HOST,PORT of the client
# then it gives back an array: [jobNumber, remaining waiting servers]
JOB_QUEUE = {}

class ClientRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Client listener")
        cur_thread_name = threading.current_thread().getName()
        data_by = pickle.loads(data) # de-serialize
        # data_by = data
        print("{} hears (out of {}) from {} : ".format(cur_thread_name, threading.active_count(), self.client_address))
        print(data_by)

        # if this is a ACK from the servers for previous requests
        client_port = self.client_address[1]
        if (client_port == 1000) or (client_port == 2000):
            print "OOOOH ITS AN ALLYYY"
            # getting # [SERVERname, (HOST,PORT), jobNumber]
            try:
                receivedServer = data_by[0]
                receivedClient = data_by[1]
                receivedJobnum = data_by[2]
                print JOB_QUEUE
                value = JOB_QUEUE[receivedClient]
                value[1] = value[1] -1
                if (value[1] == 0):
                    socket.sendto(pickle.dumps('Success.'), receivedClient)
            except StandardError:
                print '...'

        
        # if this request comes from actual client
        else:
            # [CLIENT, INTEGER, CREATE, ARG0]
            jobNumber = COUNTER.get()
            COUNTER.set(jobNumber+1)
            newJob = [THIS_SERVER, self.client_address, jobNumber, data_by]
            newJob_pickled = pickle.dumps(newJob)
            JOB_QUEUE[self.client_address] = [jobNumber, NUM_SERVERS]
            print 'making new job : ', jobNumber
            print 'increased counter to be :    ', COUNTER.get()
            for server in SERVERS.keys():
                HOST, PORT = SERVERS[server][0], SERVERS[server][1]
                print 'HOST, PORT', (HOST, PORT)
                socket.sendto(newJob_pickled, (HOST,PORT))


        #socket.sendto(data.upper(), self.client_address)


class ServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        data_by = pickle.loads(data)
        socket = self.request[1]
        threading.current_thread().setName("Server listener")
        cur_thread = threading.current_thread().getName()
        print("{} hears (out of {}) from server {} : ".format(cur_thread, threading.active_count(), self.client_address))
        print(data_by)
        server_address = (self.client_address[0], self.client_address[1])

        response = [THIS_SERVER]
        try:
            # getting # [THIS_SERVER, self.client_address, jobNumber, data_by]
            # forming # [SERVERname, (HOST,PORT), jobNumber]
            if data_by[0] in SERVERS.keys():
                response.append(data_by[1])
                response.append(data_by[2])
        except 'StandardError':
            response.append(None)
            response.append(None)
        # response = 'ACK from '+THIS_SERVER
        response_pickle = pickle.dumps(response)
        socket.sendto(response_pickle, server_address)
        print 'Just sent response to ', server_address
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