#Jakub Pawlikowski
#Monday, January 27th 2020.

import socket

host = socket.gethostname()

serverPort = 9999

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((host, serverPort))

serverSocket.listen(1)

print("The server is ready to receive")

connectionSocket,addr = serverSocket.accept()

while True:
	httpMsgIn = connectionSocket.recv(1024).decode()

	#unwrap command from HTTP GET message format
	msgTemp = httpMsgIn.split('HTTP')
	msg = msgTemp[0].split('GET')
	msg = msg[1].strip()

	#CONN command initiates FTP connection with ftp.cdc.gov
	if msg == "CONN":
		print("Connecting to ftp.cdc.gov..")
		tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		hostIP = "198.246.117.106"
		connPort = 21
		tcpClient.connect((hostIP, connPort))
		response = tcpClient.recv(1024).decode()
		print(" -> ", response)
	else:
		ftpCommand = msg + "\r\n"
		tcpClient.send(ftpCommand.encode())
		response = tcpClient.recv(1024).decode()
		print(" --> ", response)
		if msg == "quit":
			httpMsgOut = "HTTP/1.1" + msg + "200 OK"
			connectionSocket.send(httpMsgOut.encode())
			break
	
	httpMsgOut = "HTTP/1.1" + msg + "200 OK"
	connectionSocket.send(httpMsgOut.encode())

connectionSocket.close()
