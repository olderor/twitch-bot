#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from datetime import datetime
import socket, string, sys, time, os.path
import commands as t

NICK = "olderor"#olderor2
CHANNEL = "zerxam"#olderor2
BotIndex = 0

# Method for sending a message
def SendMessage(message):
	res = "PRIVMSG #" + CHANNEL + " :/me _bot " + message + "\r\n"
	Print("bot: " + res)
	s.send(res)

def Print(output):
	strm = str(output)
	toPrint = str(datetime.utcnow()) + " " + strm
	print toPrint
	toPrint = toPrint.replace("\n", "{N}") + "\n"
	f = open('logs/chatlog' + str(BotIndex) + '.txt', 'a')
	f.write(toPrint)
	f.close()

def GetIndex():
	if (os.path.exists('times.txt')):
		f = open('times.txt', 'r')
		inpt = f.read()
		f.close()
		if not inpt == "":
			global BotIndex
			BotIndex = int(inpt)
			t.BotIndex = BotIndex
	
GetIndex()
print BotIndex
Print("")
Print("")
Print("")
Print("Starting bot")
Print("")
Print("")
	
# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
PORT = 6667
PASS = "oauth:"
readbuffer = ""
MODT = False

# Connecting to Twitch IRC by passing credentials and joining a certain channel
s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS " + PASS + "\r\n")
s.send("NICK " + NICK + "\r\n")
s.send("JOIN #" + CHANNEL + " \r\n")

SendMessage("Bot is connected")
start = 0

def CheckUser(username):
	if username == NICK or username == CHANNEL or username == "gotthit":
		return True
	return False

ENABLED = True


thread = Thread(target = t.PrintInfo, args = (s, ))
thread.start()

while True:
	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		# Checks whether the message is PING because its a method of Twitch to check if you're afk
		if (line[0:4] == "PING"):
			Print("ping-pong")
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
						Print(username + ": " + message)
						end = time.time()
						messageParts = string.split(message, " ")
						if not ENABLED:
							if (messageParts[0] == "_botstart" or messageParts[0] == "start") and CheckUser(username):
								SendMessage("Hello! I'm here")
								ENABLED = True
								t.thread_run = True
						else:
							if end - start >= 1 or CheckUser(username):
								start = end

								if messageParts[0] == "Kappa":
									t.Kappa(s)

								if messageParts[0].lower() == "!ask":
									if len(messageParts) == 1:
										SendMessage("@" + username + " Сначала задай вопрос")
									else:
										t.MagicBall(s, username)

								if messageParts[0].lower() == "!deck":
									t.GetDeck(s)

								#if messageParts[0].lower() == "!donate" or messageParts[0].lower() == "!money":
									#SendMessage("донатить тут: http://www.donationalerts.ru/r/skyfanbrew")

								if messageParts[0].lower() == "!followage":
									if len(messageParts) == 1:
										t.Followage(s, username)
									elif len(messageParts) == 2:
										t.Followage(s, messageParts[1])
									else:
										t.Followage(s, messageParts[1], messageParts[2])
										
								if messageParts[0].lower() == "!мамка":
									if len(messageParts) == 1:
										t.Mamka(s)
									elif len(messageParts) > 1:
										t.Mamka(s, " ".join(messageParts[1:]))


								#if messageParts[0].lower() == "!железо" or messageParts[0].lower() == "!hardware" or messageParts[0].lower() == "!computer":
									#SendMessage("Notebook: Lenovo G780 i5-3210M NVIDIA GeForce GT 630M")

								#if messageParts[0].lower() == "!skyfan" or messageParts[0].lower() == "!skyfanbrew" or messageParts[0].lower() == "!me":
									#SendMessage("Привіт! Мене звати Юра, мені 21, проживаю в м. Харкові, Україна. В Hearthstone граю з березня 2014")

								if messageParts[0].lower() == "!time" or messageParts[0].lower() == "!время" or messageParts[0].lower() == "!live" or messageParts[0].lower() == "!uptime":
									t.Uptime(s)
									
								if messageParts[0].lower() == "!songrequest" or messageParts[0].lower() == "!request":
									t.AddSong(s, messageParts, username)
								
								if (messageParts[0].lower() == "!clearsong" or messageParts[0].lower() == "!clearsongs" or messageParts[0].lower() == "!clear") and CheckUser(username):
									t.ClearSongs(s)
									
								if (messageParts[0].lower() == "!getsong" or messageParts[0].lower() == "!get") and CheckUser(username):
									t.ExtractSong(s)
									
								if (messageParts[0].lower() == "!songssize" or messageParts[0].lower() == "!listsize" or messageParts[0].lower() == "!size"):
									t.GetSongsCount(s)
								
								if messageParts[0].lower() == "!song":
									t.GetLastSong(s)
									
								#if messageParts[0].lower() == "!quote" or messageParts[0].lower() == "!цитата":
									#t.Quote(s)

								if messageParts[0].lower() == "!topdeck" or messageParts[0].lower() == "!топдек":
									t.Topdeck(s)

								#if messageParts[0].lower() == "!hive":
									#SendMessage("Kreygasm H Kreygasm I Kreygasm V Kreygasm E Kreygasm")

								if messageParts[0].lower() == "!pyramid":
									if len(messageParts) > 1:
										t.SendPyramid(s, " ".join(messageParts[1:]))
									else:
										t.SendPyramid(s)
										
								#if messageParts[0].lower() == "!bot":
								#	m = ""
								#	for i in range(1, len(messageParts)):
								#		m = m + messageParts[i]
								#	t.ChatBot(s, username, m)

								if messageParts[0].lower() == "!vk" or messageParts[0].lower() == "!вк":
									SendMessage("группа в вк: https://vk.com/zerxamtv + zerxam в вк: https://vk.com/id228197148")
									
								if messageParts[0].lower() == "!group" or messageParts[0].lower() == "!группа":
									SendMessage("PogChamp у нас появилась группа в вк PogChamp https://vk.com/zerxamtv PogChamp")
									
								if messageParts[0].lower() == "!help" or messageParts[0].lower() == "!commands":
									SendMessage("Список доступных команд: !ask <вопрос> - спроси магический шар, !deck - текущая дека, !followage - узнай, сколько времени подписан на канал, !vk - связаться с zerxam'ом, !uptime - узнай, сколько времени идет стрим, !мамка - узнай, сколько здоровья у матери любимого тебе человека, !topdeck - зафиксируй топдек, !songrequest - запрос на музыку на стриме, !song - текущая песня")

								#if messageParts[0].lower() == "!help" or messageParts[0].lower() == "!commands":
									#SendMessage("!bot <message> - спілкуйся з ботом англійською, !ask - спитай магічний шар, !deck - поточна дека, !donate - закинь грошенят, !followage - скільки часу ти фолловиш, !hardware - опис барахла з якого ведеться стрім, !skyfan - трішечки про мене, !quote - рандомна моя цитата(18+), !vk - зв'язатися зі мною, !uptime - скільки часу стрім")

							if messageParts[0].lower() == "!modhelp":
								if CheckUser(username):
									SendMessage("_botstart или start - запустить бота, _botexit или exit - выключить бота, !setdeck <url> - обновить текущую деку, !remdeck - удалить текущую деку")
								else:
									SendMessage("@" + username + " недостаточно прав для вызова команды. обратитесь к " + NICK)

							if messageParts[0].lower() == "!remdeck":
								if CheckUser(username):
									t.RemoveDeck(s)
								else:
									SendMessage("@" + username + " недостаточно прав для вызова команды. обратитесь к " + NICK)
							
							if messageParts[0].lower() == "!setdeck":
								if CheckUser(username):
									if len(messageParts) == 1:
										SendMessage("в сообщении необходимо указать ссылку на деку. !setdeck <url>")
									else:
										url = ""
										for i in range(1, len(messageParts)):
											url = url + messageParts[i]
										t.SetDeck(s, url)
								else:
									SendMessage("@" + username + " недостаточно прав для вызова команды. обратитесь к " + NICK)

							if (messageParts[0] == "_botexit" or messageParts[0] == "exit") and CheckUser(username):
									SendMessage("Bye!")
									ENABLED = False
									t.thread_run = False
									BotIndex += 1
									f = open('times.txt', 'w')
									f.write(str(BotIndex))
									f.close()
					except Exception as e:
						Print("\n\n\n !!! Exception: " + str(e) + " !!! \n\n\n")

				for l in parts:
					if "End of /NAMES list" in l:
						MODT = True