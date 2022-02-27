# receives json data from client (PC) that is then used by Pi to display data on the OLED screen.
import socket
import sys
import cv2
import pickle
import numpy as np
import struct  # new
import zlib

HOST = '172.30.24.46'  # Pi's ip address
PORT = 3142
DATA_FOLDER = 'data/dump/'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)

    json_data = data[:msg_size]
    data = data[msg_size:]

    json_data = pickle.loads(json_data, fix_imports=True, encoding="bytes")

    # upload to OLED screen
    print("json_data: {}".format(json_data))
