#!/usr/bin/env python

# Usage: >> python client.py localhost 8001

# UDP client example
import socket
import sys
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.connect(("localhost", 5006))
# Comment 1: We don't want the above line because unlike TCP, which needs to maintain a solid connection, we don't need to do that with UDP.  UDP is meant to be used as opening a connection and sending stuff over, then closing the connection when done.  Don't need to keep it open
# to create a binary file use: dd if=/dev/random of=file2.bin bs=1m count=200

host = sys.argv[1]
try:
	port = int(sys.argv[2])
except StandardError:
	port = 5006
address = (host,port)

BLOCK_SIZE = 1024
INDEX_SIZE = 8
buf = BLOCK_SIZE - INDEX_SIZE

data = "Hello world!"
client_socket.sendto(data, address)
received = client_socket.recv(1024)

print "Sent:     {}".format(data)
print "Received: {}".format(received)
client_socket.close()
