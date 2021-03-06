#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
from datetime import datetime
import socket, string, random, sys, time, os.path
from time import sleep
import urllib2, json
import requests, validators
import json
import codecs



# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
PORT = 6667
PASS = "oauth:"
readbuffer = ""
MODT = False

NICK = "olderor" # Bot nickname.
CHANNEL = "shtan_udachi" # Channel name.
BOT_INDEX = 0 # Bot lobby index.
ENABLED = True # Flag if bot should work (answer to the commands).




# Method for sending a message with /me tag
def SendMessage(message):
	res = "PRIVMSG #" + CHANNEL + " : _bot " + message + "\r\n"
	Print("bot: " + res)
	s.send(res)

# Method for sending a message without /me tag. Use for twitch chat commands (ex. /ban)
def SendMessageAnonymous(message):
	res = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
	Print("bot anon: " + res)
	s.send(res)

# Method for doing logs. Prints info into file and console.
def Print(output):
	strm = str(output)
	toPrint = str(datetime.utcnow()) + " " + strm[:-1]
	print toPrint
	toPrint = toPrint
	f = open(CHANNEL + '/logs/chatlog' + str(BOT_INDEX) + '.txt', 'a')
	f.write(toPrint+ "\n")
	f.close()
	

# Check if user is admin.
def CheckUser(username):
	f = open(CHANNEL + '/admins.txt', 'r')
	data = f.readlines()
	return username + '\n' in data

# Get current bot lobby index (used for logging).
def GetIndex():
	if (os.path.exists(CHANNEL + '/times.txt')):
		f = open(CHANNEL + '/times.txt', 'r')
		inpt = f.read()
		f.close()
		if not inpt == "":
			global BOT_INDEX
			BOT_INDEX = int(inpt)

# Force bot to stop writing in the chat (bot still works and doing chat logs).
def Exit():
	SendMessage("Bye!")
	global ENABLED
	ENABLED = False
	global BOT_INDEX 
	BOT_INDEX += 1
	f = open(CHANNEL + '/times.txt', 'w')
	f.write(str(BOT_INDEX))
	f.close()


# Parse message from the user and do commands if need.
def ParseMessage(username, messageParts):
	messageParts[0] = messageParts[0].decode('utf-8')
	f = open(CHANNEL + '/commands.json', 'r')
	commands = json.load(f)
	f.close()
	if messageParts[0] != "any":
		exec(commands.get(messageParts[0].lower(), ""))
	
# Parse message from the user and do commands if need.
def ParseAny(username, messageParts):
	f = open(CHANNEL + '/commands.json', 'r')
	commands = json.load(f)
	f.close()
	exec(commands.get("any", ""))
	
# Set number of points to the user.
def SetPoints(nick, count):
	f = open(CHANNEL + '/points.json', 'r')
	data = json.load(f)
	f.close()
	data[nick] = count
	f = open(CHANNEL + '/points.json', 'w')
	json.dump(data, f)
	f.close()
	return count

# Add points to the user.
def AddPoints(nick, count):
	f = open(CHANNEL + '/points.json', 'r')
	data = json.load(f)
	f.close()
	val = data.get(nick, 0) + count
	data[nick] = val
	f = open(CHANNEL + '/points.json', 'w')
	json.dump(data, f)
	f.close()
	return val







# Starting bot.
# Get bot lobby index.
# Notify that bot is connected.
GetIndex()
print BOT_INDEX
Print(" ")
Print(" ")
Print(" ")
Print("Starting bot ")
Print(" ")
Print(" ")


# Connecting to Twitch IRC by passing credentials and joining a certain channel.
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #" + CHANNEL + " \r\n")

#SendMessage("Bot is connected DatSheffy 7")














# Send info about the channel into chat with some delay.
def PrintInfo():
	f = open(CHANNEL + '/info.txt', 'r')
	info = f.readlines()
	i = 450
	while False: #True
		if ENABLED:
			i += 1
			if i == 1000:
				i = 0
				SendMessage(info[random.randint(0, len(info) - 1)][:-1])
		sleep(1)

thread = Thread(target = PrintInfo, args = ())
thread.start()




start = 0

while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		# Checks whether the message is PING because its a method of Twitch to check if you're afk
		if (line[0:4] == "PING"):
			Print("ping-pong ")
			s.send("PONG tmi.twitch.tv\r\n")
		else:
			# Splits the given string so we can work with it better
			Print(str(line))
			parts = string.split(line, ":")

			if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
				try:
					message = parts[2]
					for i in range(3, len(parts)):
						message = message + ":" + parts[i]
					message = message[:len(message) - 1]
				except:
					message = ""
				
				# Sets the username variable to the actual username
				usernamesplit = string.split(parts[1], "!")
				username = usernamesplit[0]
				
				# Only works after twitch is done announcing stuff (MODT = Message of the day)
				if MODT:
					try:
						end = time.time()
						messageParts = string.split(message, " ")
						if not ENABLED:
							if (messageParts[0] == "_botstart" or messageParts[0] == "start") and CheckUser(username):
								#SendMessage("Hello! I'm here")
								ENABLED = True
						else:
							if end - start >= 1 or CheckUser(username):
								start = end
								ParseMessage(username, messageParts)
							ParseAny(username, messageParts)
							
					except Exception as e:
						Print("\n\n\n !!! Exception: " + str(e) + " !!! \n\n\n")

				for l in parts:
					if "End of /NAMES list" in l:
						MODT = True