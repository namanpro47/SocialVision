# TEMP -- this is going to be replaced with Pi's client which sends the image to the server
import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import matplotlib.pyplot as plt

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '172.30.24.46'  # PC's ip address
PORT = 3141

client_socket.connect((HOST, PORT))

connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320)
cam.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    try:
        # TODO: code to process image

        # assume `frame`. the following code will send it to server.
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        img_counter += 1
        # assume `frame`. the following code will send it to server.

        # @Aydin: replace this whatever procedure we have for waiting for next inference
        time.sleep(10)
    except:
        print("son of a bitch!!!")


cam.release()
