import socket
from argparse import ArgumentParser
import sys
from select import select

host = ""
port = -1
name = ""
sock = None

parser = None

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

def parseMsg(msg):
	msg.replace("\BL/", "\033[94m")
	msg.replace("/BL\\", "\033[94m")
	msg.replace("\YE/", "\033[93m")
	msg.replace("/YE\\", "\033[93m")
	msg.replace("\RE/", "\033[91m")
	msg.replace("/RE\\", "\033[91m")
	msg.replace("\GR/", "\033[92m")
	msg.replace("/GR\\", "\033[92m")
	if msg.find("\BO/") != -1 and msg.find("/BO\\") == -1:
		msg += "\033[21m"
	msg.replace("\BO/", "\033[1m")
	msg.replace("/BO\\", "\033[21m")
	if msg.find("\UN/") != -1 and msg.find("/UN\\") == -1:
		msg += "\033[24m"
	msg.replace("\UN/", "\033[4m")
	msg.replace("/UN\\", "\033[24m")
	if msg.find("\BK/") != -1 and msg.find("/BK\\") == -1:
		msg += "\033[25m"
	msg.replace("\BK/", "\033[5m")
	msg.replace("/BK\\", "\033[25m")
	msg += "\033[0m"
	return msg

def parseArgs():
	global parser
	parser = ArgumentParser()
	parser.add_argument("--host", help="Provide the server's host.", dest="host", action="store", required=True)
	parser.add_argument("--port", help="Provide the port.", dest="port", action="store", required=True, type=int)
	parser.add_argument("--name", help="Provide the name.", dest="name", action="store", required=True)
	parser.parse_args()

def connect():
	global host, port, name, sock
	try:
		print "Connecting to the server..."
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		host = parser.host
		port = parser.port
		name = parser.name
		sock.settimeout(10)
		sock.connect((host, port))
		print colored("Connected!", "green")
	except:
		return 1

def interact():

def main():
	if connect() == 1:
		return 1
	return interact()

if __name__ == "__main__":
	sys.exit(main())