import socket
from select import select
import sys
from termcolor import colored

socks = []
names = []
sock = None
port = 8191

maxusers = 8
maxbuf = 4096

def start():
	global sock, port, maxusers, socks, maxbuf
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCKSTREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.REUSE_ADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, naxbuf)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, maxbuf)
		sock.bind((localhost, port))
		sock.listen(maxusers)
		socks.append(sock)
		return 0
	except:
		return 1

def announce(msg):
	global socks, sock
	for x in socks:
		if x == sock:
			continue
		try:
			x.send(msg)
		except:
			x.close()
			if x in socks:
				socks.remove(x)

def handleConnections():
	global sock, socks, maxbuf, names
	newUser = False
	while True:
		reader, writer, error = select(socks, [], [])
		for x in reader:
			if x == sock:
				connection, address = sock.accept()
				socks.append(connection)
				names.append(list(address, "\n"))
			else:
				if sock.getpeername() 

def main():
	if start() == 1:
		return 1

if __name__ == "__main__":
	sys.exit(main())