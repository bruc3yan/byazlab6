#!/usr/bin/env python

# Usage: >> python UDPclient.py localhost filename.txt

# UDP client example
import socket
import sys
import os

try:
    import cPickle as pickle
except:
    import pickle
import pprint # for printing

from integer import Integer

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

# NO LONGER NEEDED BECAUSE THIS IS NOT SERIALIZED DATA - WE ARE NOT SENDING IT
# filename = sys.argv[2]
# example_message = "Start."
# client_socket.sendto(example_message, address)

integer_by = Integer(73)
integer_by.set(37)
data_by = integer_by
# data_by = [ { 'a':'A', 'b':2, 'c':3.0 } ]
# print 'DATA:',
# pprint.pprint(data_by)

data_string_by = pickle.dumps(data_by)
client_socket.sendto(data_string_by, address)
# print 'PICKLE:', data_string_by

client_socket.close()
