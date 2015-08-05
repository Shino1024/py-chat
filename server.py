#/usr/bin/python

import socket
from select import select
import sys

socks = []
users = []
sock = None
port = 4402
host = "localhost"

maxusers = 8
maxbuf = 4096

def colored(string, color):
	normalizer = "\033[0m"
	if color == "red":
		return "\033[91m" + string + normalizer
	elif color == "green":
		return "\033[92m" + string + normalizer
	elif color == "yellow":
		return "\033[93m" + string + normalizer
	elif color == "blue":
		return "\033[94m" + string + normalizer

def bold(string):
	return "\e[1m" + string + "\e[21m"

def start():
	global sock, port, maxusers, socks, maxbuf, host
	try:
		print "Creating the server..."
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print "dbg"
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#		sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, naxbuf)
#		sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, maxbuf)
		sock.bind((host, port))
		sock.listen(maxusers)
		socks.append(sock)
		print colored("Server active!", "green")
		return 0
	except:
		print bold(colored("Encountered an error, exiting...", "red"))
		return 1

def announce(msg, kind):
	global socks, sock, users
	for x in socks:
		if x == sock or users[socks.index(x.getpeername())] == "\n":
			continue
		try:
			if kind == "msg":
				x.send(colored(msg, "blue"))
			elif kind == "off":
				x.send(colored(msg, "red"))
			elif kind == "onl":
				x.send(colored(msg, "green"))
		except:
			x.close()
			if x in socks:
				name = users[socks.index(x)][1]
				announce("User %s has gone offline." % name, "off")
				socks.remove(x)

def handleConnections():
	global sock, socks, maxbuf, users
	try:
		newUser = False
		while True:
			reader, writer, error = select(socks, [], [], 0)
			for x in reader:
				if x == sock:
					connection, address = sock.accept()
					socks.append(connection)
					users.append(list(address, "\n"))
				else:
					try:
						name = users[socks.index(x)][1]
#						if name == "\n":
#							name = "\Anonymous"
						data = x.recv(maxbuf)
						if data:
							addrs, names = list(zip(*users))[0], list(zip(*users))[1]
							if names[addrs.index(x.getpeername())] == "\n":
								if data in names:
									x.send("\n")
								else:
									users[addrs.index(x.getpeername())][1] = data
									announce("User %s has joined." % data, "onl")
							else:
								announce(bold(names[addrs.index(x.getpeername())]) + ": " + data, "msg")
						else:
							if x in socks:
								socks.remove(x)
							announce("User %s has gone offline." % name, "off")
					except:
						announce("User %s has gone offline." % name, "off")
	except KeyboardInterrupt:
		print colored("Closing the server...", "red")
		announce("The server has been interrupted.", "off")
		sock.close()
		return 0

def main():
	if start() == 1:
		return 1
	return handleConnections()

if __name__ == "__main__":
	sys.exit(main())