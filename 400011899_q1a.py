
#Jakub Pawlikowski
#Monday, January 27th 2020.

import socket

print("Socket Client Active!")
print("Available commands:")
print("CONN : connect to ftp.cdc.gov via FTP via port 21 - DO THIS FIRST")
print("USER <username> : user authentication (note 'anonymous' is accepted user)")
print("PASS <email> : password authentication via an email address")
print("pwd : display current active directory")
print("cwd : change current active directory")
print("help : display instructional docs")
print("cdup : change active directory to parent")
print("syst : display system information")
print("quit : disconnect from server\n")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverName = socket.gethostname()

serverPort = 9999

clientSocket.connect((serverName, serverPort))

while True:
	command = input("Enter FTP command: ")

	#wrap command input in HTTP GET message format
	httpMsg = "GET " + command + " HTTP/1.1\r\n"
	
	clientSocket.send(httpMsg.encode())
	
	serverMsgHttp = clientSocket.recv(1024)

	#unwrap command from HTTP response message format
	serverMsgTemp = serverMsgHttp.decode().split('HTTP/1.1')
	serverMsg = serverMsgTemp[1].split("200 OK")
	serverMsg = serverMsg[0].strip()
	
	if serverMsg == "quit":
		print("Quiting client")
		break

clientSocket.close()
