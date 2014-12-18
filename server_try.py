import threading
import time
import SocketServer
import sys
from integer import Integer
from simpledict import SimpleDict
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
DATA_LIB = {}

TOTAL_ORDERING = Integer('server_order')

COUNTER = Integer('meow')
COUNTER.set(0)

# Server name of this server
THIS_SERVER = sys.argv[1]

# The waiting queue for this server
# the key is the HOST,PORT of the client
# then it gives back an array: [jobNumber, remaining waiting servers, actual commands]
JOB_QUEUE = {}

# locks
lock = threading.Lock()

class ClientRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        threading.current_thread().setName("Client listener")
        cur_thread_name = threading.current_thread().getName()
        data_by = pickle.loads(data) # de-serialize
        print("{} hears (out of {}) from {} : ".format(cur_thread_name, threading.active_count(), self.client_address))
        print(data_by)

        # if this is a ACK from the servers for previous requests
        client_port = self.client_address[1]
        if (client_port == 1000) or (client_port == 2000):
            print "This is a response from server"
            # getting # [SERVERname, (HOST,PORT), jobNumber]
            try:
                receivedServer = data_by[0]
                receivedClient = data_by[1]
                receivedJobnum = data_by[2]
                receivedSuccess = data_by[3]
                print JOB_QUEUE
                value = JOB_QUEUE[receivedClient]
                value[1] = value[1] -1
                if not receivedSuccess:
                    socket.sendto(pickle.dumps('Failed.'), receivedClient)
                    del JOB_QUEUE[receivedClient]
                if (value[1] == 0):
                    socket.sendto(pickle.dumps('Success.'), receivedClient)
                    del JOB_QUEUE[receivedClient]
            except StandardError:
                print '...'

        
        # if this request comes from actual client
        else:
            # [CLIENT, INTEGER, CREATE, ARG0]
            jobNumber = COUNTER.get()
            COUNTER.set(jobNumber+1)
            newJob = [THIS_SERVER, self.client_address, jobNumber, TOTAL_ORDERING.get(), data_by]
            newJob_pickled = pickle.dumps(newJob)
            JOB_QUEUE[self.client_address] = [jobNumber, NUM_SERVERS, data_by]

            print 'making new job : ', jobNumber
            print 'increased counter to be :    ', COUNTER.get()
            for server in SERVERS.keys():
                HOST, PORT = SERVERS[server][0], SERVERS[server][1]
                print 'HOST, PORT', (HOST, PORT)
                socket.sendto(newJob_pickled, (HOST,PORT))



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

        # total ordering
        order = data_by[-2]
        print 'total order:     ', TOTAL_ORDERING.get()
        if TOTAL_ORDERING.get() < order:
            TOTAL_ORDERING.set(order)
            print 'total order:     ', TOTAL_ORDERING.get()

        success = 0
        request = data_by[-1]
        if 'CLIENT' in request[0].upper():
            if 'INTEGER' in request[1].upper():
                if 'CREATE' in request[2].upper():
                    try:
                        name = request[3]
                        DATA_LIB[name] = Integer(name)
                        DATA_LIB[name].set_owner(self.client_address)
                        print 'DATA_LIB : ', DATA_LIB
                        print 'Successfully create integer with name : ', name
                        success  = 1
                    except StandardError:
                        print 'Failed to retrieve name to create Integer.'
                        
                if 'SET' in request[2].upper():
                    try:
                        name = request[3]
                        new_value = request[4]
                        DATA_LIB[name].set(new_value)
                        print 'DATA_LIB : ', DATA_LIB
                        print 'Successfully set integer with name ', name, ' to be ', DATA_LIB[name].get()
                        success = 1
                    except StandardError:
                        print 'Failed to set value to integer.'
                        

        response = [THIS_SERVER]
        try:
            # getting # [THIS_SERVER, self.client_address, jobNumber,#totalOrdering, data_by]
            # forming # [SERVERname, (HOST,PORT), jobNumber, success]
            if data_by[0] in SERVERS.keys():
                response.append(data_by[1])
                response.append(data_by[2])
                response.append(success)
        except 'StandardError':
            response.append(None)
            response.append(None)
            response.append(success)
        response_pickle = pickle.dumps(response)
        socket.sendto(response_pickle, server_address)
        current_order = TOTAL_ORDERING.get()
        TOTAL_ORDERING.set(current_order+1)
        print 'Just sent response to ', server_address


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
