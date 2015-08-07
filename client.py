#!/usr/bin/python

import socket
from argparse import ArgumentParser, ArgumentTypeError
import sys
from select import select
import subprocess

host = ""
port = -1
name = ""
sock = None

parser = None

ttyChat, ttyUsers = -1, -1

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
	return "\033[1m" + string + "\033[21m"

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
	def checkPort(val):
		val2 = int(val)
		if val2 < 1024 or val2 > 65536:
			raise ArgumentTypeError("The port is beyond the acceptable domain.")
		return val2
	def checkName(val):
		if len(val) == 0 or len(val) > 16:
			raise ArgumentTypeError("The length of the name should be between 1 and 16 characters.")
		elif val.find("\\") != -1:
			raise ArgumentTypeError("No backslashes in the name, please.")
		return val
	global parser
	parser = ArgumentParser()
	parser.add_argument("--host", help="Provide the server's host.", dest="host", action="store", default="localhost", required=True)
	parser.add_argument("--port", help="Provide the port.", dest="port", action="store", default=4402, required=True, type=checkPort)
	parser.add_argument("--name", help="Provide the name.", dest="name", action="store", required=True, type=checkName)
	parser.parse_args()

def setUpWindows():

def cleanUp():

def printToAnotherConsole():

def clearScreen():
	subprocess.call("clear")

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
		printToAnotherConsole(colored("Connected!", "green"))
		sys.stdout.write(colored("> ", "yellow"))
		sys.stdout.flush()
	except:
		print bold(colored("Couldn't reach the server, exiting..."))
		return 1

def interact():
	global sock, name
	thePair = [sys.stdin, sock]
	while 1:
		read, write, error = select(thePair, [], [])
		for x in read:
			if x == sys.stdin:
				msg = sys.stdin.readline()
				length = len(msg) + 2
				msg = parseMsg(msg)
				x.send(msg)
			else:
				printToAnotherConsole()
				clearScreen()
				sys.stdout.write("> ")
				sys.stdout.flush()

def main():
	try:
		parseArgs()
		if connect() == 1:
			return 1
		setUpWindows()
		interact()
	except KeyboardInterrupt:
		cleanUp()

if __name__ == "__main__":
	sys.exit(main())