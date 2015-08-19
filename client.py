#!/usr/bin/python

import socket
import sys
from select import select
import subprocess
from os import remove

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
	msg.replace("~BL~", "\033[94m").replace("~bL~", "\033[94m").replace("~Bl~", "\033[94m").replace("~bl~", "\033[94m")
	msg.replace("~/BL~", "\033[0m").replace("~/bL~", "\033[0m").replace("~/Bl~", "\033[0m").replace("~/bl~", "\033[0m")
	msg.replace("~YE~", "\033[93m").replace("~yE~", "\033[93m").replace("~Ye~", "\033[93m").replace("~ye~", "\033[93m")
	msg.replace("~/YE~", "\033[0m").replace("~/yE~", "\033[0m").replace("~/Ye~", "\033[0m").replace("~/ye~", "\033[0m")
	msg.replace("~RE~", "\033[91m").replace("~rE~", "\033[91m").replace("~Re~", "\033[91m").replace("~re~", "\033[91m")
	msg.replace("~/RE~", "\033[0m").replace("~/rE~", "\033[0m").replace("~/Re~", "\033[0m").replace("~/re~", "\033[0m")
	msg.replace("~GR~", "\033[92m").replace("~gR~", "\033[92m").replace("~Gr~", "\033[92m").replace("~gr~", "\033[92m")
	msg.replace("~/GR~", "\033[0m").replace("~/gR~", "\033[0m").replace("~/Gr~", "\033[0m").replace("~/gr~", "\033[0m")
	msg.replace("~BO~", "\033[1m").replace("~bO~", "\033[1m").replace("~Bo~", "\033[1m").replace("~go~", "\033[1m")
	msg.replace("~/BO~", "\033[21m").replace("~/bO~", "\033[21m").replace("~/Bo~", "\033[21m").replace("~/bo~", "\033[21m")
	msg.replace("~UN~", "\033[4m").replace("~uN~", "\033[4m").replace("~Un~", "\033[4m").replace("~un~", "\033[4m")
	msg.replace("~/UN~", "\033[24m").replace("~/uN~", "\033[24m").replace("~/Un~", "\033[24m").replace("~/un~", "\033[24m")
	msg.replace("~BK~", "\033[5m").replace("~bK~", "\033[5m").replace("~Bk~", "\033[5m").replace("~bk~", "\033[5m")
	msg.replace("~/BK~", "\033[25m").replace("~/bK~", "\033[25m").replace("~/Bk~", "\033[25m").replace("~/bk~", "\033[25m")
	msg += "\033[0m"
	return msg

def getArgs():
	global host, port, name, ttyChat, ttyUsers
	with open("TMUX_RESULT_TTY", "r+") as infoFile:
		allData = infoFile.readlines()
		host = allData[0]
		port = allData[1]
		user = allData[2]
		ttyChat = allData[3]
		ttyUsers = allData[4]
	remove("TMUX_RESULT_TTY")

def logToFile(msg):
	try:
		with open("dragonchat.log", "a+") as logFile:
			logFile.write(msg + "\n")
	except IOError:
		subprocess.call(["chmod", "0600", "dragonchat.log"])

def cleanUp():
	global sock
	print colored("Exiting...", "blue")
	sock.close()
	subprocess.call(["tmux", "kill-session", "-t", "dragonchat"])
	remove("REDIRECTION_FILE_CHAT")
	remove("REDIRECTION_FILE_USERS")

def printToAnotherConsole(msg, tty):
	with open("REDIRECTION_FILE_" + tty, "w+") as inputFile:
		if tty == "USERS":
			inputFile.write("#!/bin/bash\necho -e '" + repr(msg) + "' > " + ttyUsers)
		elif tty == "CHAT":
			inputFile.write("#!/bin/bash\necho -e '" + repr(msg) + "' > " + ttyChat)
	subprocess.call(["./REDIRECTION_FILE_" + tty])

def clearScreen():
	subprocess.call(["clear"])

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
#				length = len(msg) + 2
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