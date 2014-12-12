import socket
try:
    import cPickle as pickle
except:
    import pickle
from integer import Integer

port = 5006
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("", port))
print "waiting on port:", port
while 1:
    data, addr = server_socket.recvfrom(1024)
    data_by = pickle.loads(data)
    print data_by.get()



# import threading
# import time
# import SocketServer

# class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
#     def handle(self):
#         data = self.request[0].strip()
#         socket = self.request[1]
#         cur_thread = threading.current_thread().name
#         print("{} wrote: ".format(cur_thread))
#         print(data)
#         socket.sendto(data.upper(), self.client_address)

# class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
#         pass

# if __name__ == "__main__":
#     # Port 0 means to select an arbitrary unused port
#     HOST, PORT = "127.0.0.1", 8000

#     udpserver = ThreadedUDPServer((HOST,PORT+1), ThreadedUDPRequestHandler)
#     udp_thread = threading.Thread(target=udpserver.serve_forever)
#     udp_thread.setDaemon(True)
#     print("UDP serving at port", PORT+1)
#     udp_thread.start()

#     client_interface = ThreadedUDPServer((HOST,PORT), ThreadedUDPRequestHandler)
#     client_thread = threading.Thread(target=client_interface.serve_forever)
#     client_thread.setDaemon(True)
#     print("Client interface serving at port", PORT)
#     client_thread.start()

#     while 1:
#     	time.sleep(1)
