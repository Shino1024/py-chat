#!/usr/bin/python

import socket
import sys
from select import select
import subprocess

host = ""
port = -1
name = ""
sock = None

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
	if msg.find("\BK/") != -1 and msg.fiRnd("/BK\\") == -1:
		msg += "\033[25m"
	msg.replace("\BK/", "\033[5m")
	msg.replace("/BK\\", "\033[25m")
	msg += "\033[0m"
	return msg

def getArgs():
	global host, port, name, ttyChat, ttyUsers
	with open("TMUX_RESULT_TTY", "r+") as infoFile:
		allData = infoFile.readlines()
		host = allData[0]
		port = allData[1]
		user = allData[2]

def logToFile(msg):
	try:
		with open("dragonchat.log", "a+") as logFile:
			logFile.write(msg + "\n")
	except IOError:
		subprocess.call(["chmod", "0600", "dragonchat.log"])

def cleanUp():
	global sock
	sock.close()
	subprocess.call(["tmux", "kill-session", "-t", "dragonchat"])

def printToAnotherConsole(msg, tty):
	subprocess.call(["./redirection.sh", "REDIRECTION_FILE_" + tty])

def clearScreen():
	subprocess.call("clear")

def connect():
	global host, port, name, sock
	try:
		print "Connecting to the server..."
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
		getArgs()
		if connect() == 1:
			return 1
		interact()
	except KeyboardInterrupt:
		cleanUp()

if __name__ == "__main__":
	sys.exit(main())