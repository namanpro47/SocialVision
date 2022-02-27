# looks for a new file in local file system. If it exists, runs inference and sends it to the server.
# the server will be the Pi.
import socket
import sys
import cv2
import pickle
import numpy as np
import struct  # new
import zlib
import os

from model import run_inference
from utils import SiameseNetwork, send_sms

HOST = '172.30.24.46'  # Pi's ip address
PORT = 3142
DATA_FOLDER = 'data/dump/'

# socket configuration
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')


def is_file_present():
    return os.path.isfile(DATA_FOLDER + 'img.jpeg')


while True:

    if is_file_present():
        data, score = run_inference(DATA_FOLDER + 'img.jpeg')
        # encode data (which is a dictionary) as a bytestream
        b_data = pickle.dumps(data, 0)
        size = len(b_data)
        client_socket.sendall(struct.pack(">L", size) + b_data)

        # remove image from local file system
        os.remove(DATA_FOLDER + 'img.jpeg')
        print("Image removed")
        print("Attempting to send SMS...")
        send_sms(data)
