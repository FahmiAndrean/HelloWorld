# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, subprocess, random, requests, sys, time, urllib.parse

listApp = ["CHROMEOS", "DESKTOPWIN", "DESKTOPMAC", "IOSIPAD", "WIN10"]
try:
	for app in listApp:
		try:
			try:
				with open("authToken.txt", "r") as token:
					authToken = token.read()
					if not authToken:
						client = LINE()
						with open("authToken.txt","w") as token:
							token.write(client.authToken)
						continue
					client = LINE(authToken, speedThrift=False, appName="{}\t8.8.1\tHelloWorld\t11.2.5".format(app))
				break
			except Exception as error:
				print(error)
				if error == "REVOKE":
					exit()
				elif "auth" in error:
					continue
				else:
					exit()
		except Exception as error:
			print(error)
except Exception as error:
	print(error)
with open("authToken.txt", "w") as token:
    token.write(str(client.authToken))
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)
namefoot = "「SETTINGS」"

languageOpen = codecs.open("language.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ INFO ] BOT RESETTED")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Bulan" % (months)
	if weeks != 0: text += " %02d Minggu" % (weeks)
	if days != 0: text += " %02d Hari" % (days)
	if hours !=  0: text +=  " %02d Jam" % (hours)
	if mins != 0: text += " %02d Menit" % (mins)
	if secs != 0: text += " %02d Detik" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuHelp =	"╭──「 Help Message 」" + "\n" + \
				"│ " + key + "Help" + "\n" + \
				"│ " + key + "Translate" + "\n" + \
				"│ " + key + "TextToSpeech" + "\n" + \
				"│──「 Status Command 」" + "\n" + \
				"│ MyKey" + "\n" + \
				"│ " + key + "Logout" + "\n" + \
				"│ " + key + "Restart" + "\n" + \
				"│ " + key + "Runtime" + "\n" + \
				"│ " + key + "Speed" + "\n" + \
				"│ " + key + "Status" + "\n" + \
				"│──「 Settings Command 」" + "\n" + \
				"│ SetKey 「On/Off」" + "\n" + \
				"│ " + key + "AutoAdd 「On/Off」" + "\n" + \
				"│ " + key + "AutoJoin 「On/Off」" + "\n" + \
				"│ " + key + "AutoJoinTicket 「On/Off」" + "\n" + \
				"│ " + key + "AutoRead 「On/Off」" + "\n" + \
				"│ " + key + "AutoRespon 「On/Off」" + "\n" + \
				"│ " + key + "CheckContact 「On/Off」" + "\n" + \
				"│ " + key + "CheckPost 「On/Off」" + "\n" + \
				"│ " + key + "CheckSticker 「On/Off」" + "\n" + \
				"│ " + key + "DetectUnsend 「On/Off」" + "\n" + \
				"│ " + key + "SetKey: 「text」" + "\n" + \
				"│ " + key + "SetAutoAddMessage: 「text」" + "\n" + \
				"│ " + key + "SetAutoResponMessage: 「text」" + "\n" + \
				"│ " + key + "SetAutoJoinMessage: 「Text」" + "\n" + \
				"│──「 Self Command 」" + "\n" + \
				"│ " + key + "ChangeName: 「Text」" + "\n" + \
				"│ " + key + "ChangeBio: 「Text」" + "\n" + \
				"│ " + key + "Me" + "\n" + \
				"│ " + key + "MyMid" + "\n" + \
				"│ " + key + "MyName" + "\n" + \
				"│ " + key + "MyBio" + "\n" + \
				"│ " + key + "MyPicture" + "\n" + \
				"│ " + key + "MyVideoProfile" + "\n" + \
				"│ " + key + "MyCover" + "\n" + \
				"│ " + key + "MyProfile" + "\n" + \
				"│ " + key + "GetMid @Mention" + "\n" + \
				"│ " + key + "GetName @Mention" + "\n" + \
				"│ " + key + "GetBio @Mention" + "\n" + \
				"│ " + key + "GetPicture @Mention" + "\n" + \
				"│ " + key + "GetVideoProfile @Mention" + "\n" + \
				"│ " + key + "GetCover @Mention" + "\n" + \
				"│ " + key + "CloneProfile @Mention" + "\n" + \
				"│ " + key + "RestoreProfile" + "\n" + \
				"│ " + key + "BackupProfile" + "\n" + \
				"│ " + key + "FriendList" + "\n" + \
				"│ " + key + "FriendInfo 「Number」" + "\n" + \
				"│ " + key + "BlockList" + "\n" + \
				"│ " + key + "FriendBroadcast" + "\n" + \
				"│ " + key + "ChangePictureProfile" + "\n" + \
				"│──「 Group Command 」" + "\n" + \
				"│ " + key + "ChangeGroupName: 「Text」" + "\n" + \
				"│ " + key + "SendContact 「mid」" + "\n" + \
				"│ " + key + "GroupCreator" + "\n" + \
				"│ " + key + "GroupID" + "\n" + \
				"│ " + key + "GroupName" + "\n" + \
				"│ " + key + "GroupPicture" + "\n" + \
				"│ " + key + "OpenQR" + "\n" + \
				"│ " + key + "CloseQR" + "\n" + \
				"│ " + key + "GroupList" + "\n" + \
				"│ " + key + "MemberList" + "\n" + \
				"│ " + key + "PendingList" + "\n" + \
				"│ " + key + "GroupInfo" + "\n" + \
				"│ " + key + "GroupBroadcast: 「Text」" + "\n" + \
				"│ " + key + "ChangeGroupPicture" + "\n" + \
				"│──「 Special Command 」" + "\n" + \
				"│ " + key + "Mimic 「On/Off」" + "\n" + \
				"│ " + key + "MimicList" + "\n" + \
				"│ " + key + "MimicAdd @Mention" + "\n" + \
				"│ " + key + "MimicDel @Mention" + "\n" + \
				"│ " + key + "Mention" + "\n" + \
				"│ " + key + "Lurking 「On/Off」" + "\n" + \
				"│ " + key + "Lurking" + "\n" + \
				"│──「 Media Command 」" + "\n" + \
				"│ " + key + "InstaInfo 「Username」" + "\n" + \
				"│ " + key + "InstaStory 「Username」" + "\n" + \
				"│ " + key + "Quotes" + "\n" + \
				"│ " + key + "SearchImage 「Search」" + "\n" + \
				"│ " + key + "SearchMusic 「Search」" + "\n" + \
				"│ " + key + "SearchLyric 「Search」" + "\n" + \
				"│ " + key + "SearchYoutube 「Search」" + "\n" + \
				"│ " + key + "YoutubeMp3 「Link」" + "\n" + \
				"│ " + key + "YoutubeMp4 「Link」" + "\n" + \
				"│ " + key + "SendVideo 「Link」" + "\n" + \
				"│ " + key + "SendPicture 「Link」" + "\n" + \
				"╰─────「 @!」"
	return menuHelp

def menuTextToSpeech():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTextToSpeech =	"╭──「Text To Speech 」" + "\n" + \
						"│ " + key + "af : Afrikaans" + "\n" + \
						"│ " + key + "sq : Albanian" + "\n" + \
						"│ " + key + "ar : Arabic" + "\n" + \
						"│ " + key + "hy : Armenian" + "\n" + \
						"│ " + key + "bn : Bengali" + "\n" + \
						"│ " + key + "ca : Catalan" + "\n" + \
						"│ " + key + "zh : Chinese" + "\n" + \
						"│ " + key + "zh-cn : Chinese (Mandarin/China)" + "\n" + \
						"│ " + key + "zh-tw : Chinese (Mandarin/Taiwan)" + "\n" + \
						"│ " + key + "zh-yue : Chinese (Cantonese)" + "\n" + \
						"│ " + key + "hr : Croatian" + "\n" + \
						"│ " + key + "cs : Czech" + "\n" + \
						"│ " + key + "da : Danish" + "\n" + \
						"│ " + key + "nl : Dutch" + "\n" + \
						"│ " + key + "en : English" + "\n" + \
						"│ " + key + "en-au : English (Australia)" + "\n" + \
						"│ " + key + "en-uk : English (United Kingdom)" + "\n" + \
						"│ " + key + "en-us : English (United States)" + "\n" + \
						"│ " + key + "eo : Esperanto" + "\n" + \
						"│ " + key + "fi : Finnish" + "\n" + \
						"│ " + key + "fr : French" + "\n" + \
						"│ " + key + "de : German" + "\n" + \
						"│ " + key + "el : Greek" + "\n" + \
						"│ " + key + "hi : Hindi" + "\n" + \
						"│ " + key + "hu : Hungarian" + "\n" + \
						"│ " + key + "is : Icelandic" + "\n" + \
						"│ " + key + "id : Indonesian" + "\n" + \
						"│ " + key + "it : Italian" + "\n" + \
						"│ " + key + "ja : Japanese" + "\n" + \
						"│ " + key + "km : Khmer (Cambodian)" + "\n" + \
						"│ " + key + "ko : Korean" + "\n" + \
						"│ " + key + "la : Latin" + "\n" + \
						"│ " + key + "lv : Latvian" + "\n" + \
						"│ " + key + "mk : Macedonian" + "\n" + \
						"│ " + key + "no : Norwegian" + "\n" + \
						"│ " + key + "pl : Polish" + "\n" + \
						"│ " + key + "pt : Portuguese" + "\n" + \
						"│ " + key + "ro : Romanian" + "\n" + \
						"│ " + key + "ru : Russian" + "\n" + \
						"│ " + key + "sr : Serbian" + "\n" + \
						"│ " + key + "si : Sinhala" + "\n" + \
						"│ " + key + "sk : Slovak" + "\n" + \
						"│ " + key + "es : Spanish" + "\n" + \
						"│ " + key + "es-es : Spanish (Spain)" + "\n" + \
						"│ " + key + "es-us : Spanish (United States)" + "\n" + \
						"│ " + key + "sw : Swahili" + "\n" + \
						"│ " + key + "sv : Swedish" + "\n" + \
						"│ " + key + "ta : Tamil" + "\n" + \
						"│ " + key + "th : Thai" + "\n" + \
						"│ " + key + "tr : Turkish" + "\n" + \
						"│ " + key + "uk : Ukrainian" + "\n" + \
						"│ " + key + "vi : Vietnamese" + "\n" + \
						"│ " + key + "cy : Welsh" + "\n" + \
						"╰─────「 @!」" + "\n" + "\n\n" + \
						"Contoh : " + key + "say-id chiken"
	return menuTextToSpeech

def menuTranslate():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTranslate =	"╭──「 Translate 」" + "\n" + \
					"│ " + key + "af : afrikaans" + "\n" + \
					"│ " + key + "sq : albanian" + "\n" + \
					"│ " + key + "am : amharic" + "\n" + \
					"│ " + key + "ar : arabic" + "\n" + \
					"│ " + key + "hy : armenian" + "\n" + \
					"│ " + key + "az : azerbaijani" + "\n" + \
					"│ " + key + "eu : basque" + "\n" + \
					"│ " + key + "be : belarusian" + "\n" + \
					"│ " + key + "bn : bengali" + "\n" + \
					"│ " + key + "bs : bosnian" + "\n" + \
					"│ " + key + "bg : bulgarian" + "\n" + \
					"│ " + key + "ca : catalan" + "\n" + \
					"│ " + key + "ceb : cebuano" + "\n" + \
					"│ " + key + "ny : chichewa" + "\n" + \
					"│ " + key + "zh-cn : chinese (simplified)" + "\n" + \
					"│ " + key + "zh-tw : chinese (traditional)" + "\n" + \
					"│ " + key + "co : corsican" + "\n" + \
					"│ " + key + "hr : croatian" + "\n" + \
					"│ " + key + "cs : czech" + "\n" + \
					"│ " + key + "da : danish" + "\n" + \
					"│ " + key + "nl : dutch" + "\n" + \
					"│ " + key + "en : english" + "\n" + \
					"│ " + key + "eo : esperanto" + "\n" + \
					"│ " + key + "et : estonian" + "\n" + \
					"│ " + key + "tl : filipino" + "\n" + \
					"│ " + key + "fi : finnish" + "\n" + \
					"│ " + key + "fr : french" + "\n" + \
					"│ " + key + "fy : frisian" + "\n" + \
					"│ " + key + "gl : galician" + "\n" + \
					"│ " + key + "ka : georgian" + "\n" + \
					"│ " + key + "de : german" + "\n" + \
					"│ " + key + "el : greek" + "\n" + \
					"│ " + key + "gu : gujarati" + "\n" + \
					"│ " + key + "ht : haitian creole" + "\n" + \
					"│ " + key + "ha : hausa" + "\n" + \
					"│ " + key + "haw : hawaiian" + "\n" + \
					"│ " + key + "iw : hebrew" + "\n" + \
					"│ " + key + "hi : hindi" + "\n" + \
					"│ " + key + "hmn : hmong" + "\n" + \
					"│ " + key + "hu : hungarian" + "\n" + \
					"│ " + key + "is : icelandic" + "\n" + \
					"│ " + key + "ig : igbo" + "\n" + \
					"│ " + key + "id : indonesian" + "\n" + \
					"│ " + key + "ga : irish" + "\n" + \
					"│ " + key + "it : italian" + "\n" + \
					"│ " + key + "ja : japanese" + "\n" + \
					"│ " + key + "jw : javanese" + "\n" + \
					"│ " + key + "kn : kannada" + "\n" + \
					"│ " + key + "kk : kazakh" + "\n" + \
					"│ " + key + "km : khmer" + "\n" + \
					"│ " + key + "ko : korean" + "\n" + \
					"│ " + key + "ku : kurdish (kurmanji)" + "\n" + \
					"│ " + key + "ky : kyrgyz" + "\n" + \
					"│ " + key + "lo : lao" + "\n" + \
					"│ " + key + "la : latin" + "\n" + \
					"│ " + key + "lv : latvian" + "\n" + \
					"│ " + key + "lt : lithuanian" + "\n" + \
					"│ " + key + "lb : luxembourgish" + "\n" + \
					"│ " + key + "mk : macedonian" + "\n" + \
					"│ " + key + "mg : malagasy" + "\n" + \
					"│ " + key + "ms : malay" + "\n" + \
					"│ " + key + "ml : malayalam" + "\n" + \
					"│ " + key + "mt : maltese" + "\n" + \
					"│ " + key + "mi : maori" + "\n" + \
					"│ " + key + "mr : marathi" + "\n" + \
					"│ " + key + "mn : mongolian" + "\n" + \
					"│ " + key + "my : myanmar (burmese)" + "\n" + \
					"│ " + key + "ne : nepali" + "\n" + \
					"│ " + key + "no : norwegian" + "\n" + \
					"│ " + key + "ps : pashto" + "\n" + \
					"│ " + key + "fa : persian" + "\n" + \
					"│ " + key + "pl : polish" + "\n" + \
					"│ " + key + "pt : portuguese" + "\n" + \
					"│ " + key + "pa : punjabi" + "\n" + \
					"│ " + key + "ro : romanian" + "\n" + \
					"│ " + key + "ru : russian" + "\n" + \
					"│ " + key + "sm : samoan" + "\n" + \
					"│ " + key + "gd : scots gaelic" + "\n" + \
					"│ " + key + "sr : serbian" + "\n" + \
					"│ " + key + "st : sesotho" + "\n" + \
					"│ " + key + "sn : shona" + "\n" + \
					"│ " + key + "sd : sindhi" + "\n" + \
					"│ " + key + "si : sinhala" + "\n" + \
					"│ " + key + "sk : slovak" + "\n" + \
					"│ " + key + "sl : slovenian" + "\n" + \
					"│ " + key + "so : somali" + "\n" + \
					"│ " + key + "es : spanish" + "\n" + \
					"│ " + key + "su : sundanese" + "\n" + \
					"│ " + key + "sw : swahili" + "\n" + \
					"│ " + key + "sv : swedish" + "\n" + \
					"│ " + key + "tg : tajik" + "\n" + \
					"│ " + key + "ta : tamil" + "\n" + \
					"│ " + key + "te : telugu" + "\n" + \
					"│ " + key + "th : thai" + "\n" + \
					"│ " + key + "tr : turkish" + "\n" + \
					"│ " + key + "uk : ukrainian" + "\n" + \
					"│ " + key + "ur : urdu" + "\n" + \
					"│ " + key + "uz : uzbek" + "\n" + \
					"│ " + key + "vi : vietnamese" + "\n" + \
					"│ " + key + "cy : welsh" + "\n" + \
					"│ " + key + "xh : xhosa" + "\n" + \
					"│ " + key + "yi : yiddish" + "\n" + \
					"│ " + key + "yo : yoruba" + "\n" + \
					"│ " + key + "zu : zulu" + "\n" + \
					"│ " + key + "fil : Filipino" + "\n" + \
					"│ " + key + "he : Hebrew" + "\n" + \
					"╰─────「 @!」" + "\n" + "\n\n" + \
					"Contoh : " + key + "tr-id chiken"
	return menuTranslate

def youtubeMp4(to, link):
    subprocess.getoutput('youtube-dl --format mp4 --output TeamAnuBot.mp4 {}'.format(link))
    try:
        client.sendVideo(to, "TeamAnuBot.mp4")
        time.sleep(2)
        os.remove('TeamAnuBot.mp4')
    except Exception as e:
        client.sendMessage(to, ' 「 ERROR 」\nMungkin Link Nya Salah GaN~', contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+client.getContact(clientMid).pictureStatus, 'AGENT_NAME': '「 ERROR 」', 'AGENT_LINK': 'https://line.me/ti/p/{}'.format(client.getUserTicket().id)})

def youtubeMp3(to, link):
    subprocess.getoutput('youtube-dl --extract-audio --audio-format mp3 --output TeamAnuBot.mp3 {}'.format(link))
    try:
        client.sendAudio(to, 'TeamAnuBot.mp3')
        time.sleep(2)
        os.remove('TeamAnuBot.mp3')
    except Exception as e:
        client.sendMessage(to, ' 「 ERROR 」\nMungkin Link Nya Salah GaN~', contentMetadata = {'AGENT_ICON': 'http://dl.profile.line-cdn.net/'+client.getContact(clientMid).pictureStatus, 'AGENT_NAME': '「 ERROR 」', 'AGENT_LINK': 'https://line.me/ti/p/{}'.format(client.getUserTicket().id)})

def clientBot(op):
	try:
		if op.type == 0:
			print ("[ 0 ] END OF OPERATION")
			return

		if op.type == 5:
			print ("[ 5 ] NOTIFIED ADD CONTACT")
			name = "「AUTO RESPON」"
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, name, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			print ("[ 13 ] NOTIFIED INVITE INTO GROUP")
			name = "「AUTO JOIN」"
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, name, settings["autoJoinMessage"], [op.param2])

		if op.type == 25:
			try:
				print("[ 25 ] SEND MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "logout":
							name = "「SHUTDOWN」"
							name2 = "「SUCCESS」"
							client.sendMessageFooter(to, name, "Progress.......")
							time.sleep(5)
							client.sendMessageFooter(to, name, "╭──「LogOut」\n╰──「SUCCESS」")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						elif cmd == "restart":
							name = "「RESTART」"
							client.sendMessageFooter(to, name, "Progress.......")
							restartBot()
						elif cmd == "speed":
							start = time.time()
							client.sendMessage(to, "Request to the server....")
							elapsed_time = time.time() - start
							name = "「SPEED SERVER」"
							client.sendMessageFooter(to, name, "╭──「Speed Message」\n╰──「{} ms」".format(str(elapsed_time)))
						elif cmd == "runtime":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							name = "「RUNNING」"
							client.sendMessageFooter(to, name, "╭──「Running Bot」\n╰──「 {} 」".format(str(runtime)))
						elif cmd.startswith("setkey: "):
							sep = text.split(" ")
							key = text.replace(sep[0] + " ","")
							name = "「KEY COMMAND」"
							if " " in key:
								client.sendMessageFooter(to, name, "╭──「Change Key Command」\n╰──「FAILED」")
							else:
								settings["keyCommand"] = str(key).lower()
								client.sendMessageFooter(to, name, "╭──「Change Key Command」\n╰──「{}」".format(str(key).lower()))
						elif cmd.startswith("youtubemp3"):
							sep = msg.text.split(" ")
							link = msg.text.replace(sep[0] + " ","")
							youtubeMp3(to, link)
						elif cmd.startswith("youtubemp4"):
							sep = msg.text.split(" ")
							link = msg.text.replace(sep[0] + " ","")
							youtubeMp4(to, link)
						elif cmd == "help":
							helpMessage = menuHelp()
							name = "「COMMAND MESSAGE」"
							client.sendMention(to, name, helpMessage, [sender])
						elif cmd == "texttospeech":
							helpTextToSpeech = menuTextToSpeech()
							name = "「TTS」"
							client.sendMention(to, name, helpTextToSpeech, [sender])
						elif cmd == "translate":
							helpTranslate = menuTranslate()
							name = "「TRANSLATE」"
							client.sendMention(to, name, helpTranslate, [sender])


						elif cmd == "status":
							try:
								ret_ = "╭──「 Status 」"
								if settings["autoAdd"] == True: ret_ += "\n│ Auto Add : ON"
								else: ret_ += "\n│ Auto Add : OFF"
								if settings["autoJoin"] == True: ret_ += "\n│ Auto Join : ON"
								else: ret_ += "\n│ Auto Join : OFF"
								if settings["autoJoin"] == True: ret_ += "\n│ Auto Join Ticket : ON"
								else: ret_ += "\n│ Auto Join Ticket : OFF"
								if settings["autoRead"] == True: ret_ += "\n│ Auto Read : ON"
								else: ret_ += "\n│ Auto Read : OFF"
								if settings["autoRespon"] == True: ret_ += "\n│ Auto Respon : ON"
								else: ret_ += "\n│ Auto Respon : OFF"
								if settings["checkContact"] == True: ret_ += "\n│ Check Contact : ON"
								else: ret_ += "\n│ Check Contact : OFF"
								if settings["checkPost"] == True: ret_ += "\n│ Check Post : ON"
								else: ret_ += "\n│ Check Post : OFF"
								if settings["checkSticker"] == True: ret_ += "\n│ Check Sticker : ON"
								else: ret_ += "\n│ Check Sticker : OFF"
								if msg.to in settings["detectUnsend"]: ret_ += "\n│ Detect Unsend : ON"
								else: ret_ += "\n│ Detect Unsend : OFF"
								if settings["setKey"] == True: ret_ += "\n│ Set Key : ON"
								else: ret_ += "\n│ Set Key : OFF"
								ret_ +="\n│ Auto Add Message : {}".format(settings["autoAddMessage"])
								ret_ +="\n│ Auto Join Message : {}".format(settings["autoJoinMessage"])
								ret_ +="\n│ Auto Respon Message : {}".format(settings["autoResponMessage"])
								ret_ += "\n╰─────「 Status 」"
								name = "「STATUS」"
								client.sendMessageFooter(to, name, str(ret_))
							except Exception as error:
								logError(error)
						elif cmd == "autoadd on":
							if settings["autoAdd"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Auto add」\n╰──「Telah Aktif」")
							else:
								settings["autoAdd"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Auto add」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "autoadd off":
							if settings["autoAdd"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Auto add」\n╰──「Telah Nonaktif」")
							else:
								settings["autoAdd"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Auto add」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "autojoin on":
							if settings["autoJoin"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Auto join」\n╰──「Telah Aktif」")
							else:
								settings["autoJoin"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Auto join」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "autojoin off":
							if settings["autoJoin"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Auto join」\n╰──「Telah Nonaktif」")
							else:
								settings["autoJoin"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Auto join」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "autojointicket on":
							if settings["autoJoinTicket"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Auto join ticket」\n╰──「Telah Aktif」")
							else:
								settings["autoJoinTicket"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Auto join ticket」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "autojointicket off":
							if settings["autoJoinTicket"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Auto join ticket」\n╰──「Telah Nonaktif」")
							else:
								settings["autoJoinTicket"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Auto join ticket」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "autoread on":
							if settings["autoRead"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Auto read」\n╰──「Telah Aktif」")
							else:
								settings["autoRead"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Auto read」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "autoread off":
							if settings["autoRead"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Auto read」\n╰──「Telah Nonaktif」")
							else:
								settings["autoRead"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Auto read」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "autorespon on":
							if settings["autoRespon"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon」\n╰──「Telah Aktif」")
							else:
								settings["autoRespon"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "autorespon off":
							if settings["autoRespon"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon」\n╰──「Telah Nonaktif」")
							else:
								settings["autoRespon"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "checkcontact on":
							if settings["checkContact"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Details contact」\n╰──「Telah Aktif」")
							else:
								settings["checkContact"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Details contact」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "checkcontact off":
							if settings["checkContact"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Details contact」\n╰──「Telah Nonaktif」")
							else:
								settings["checkContact"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Details contact」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "checkpost on":
							if settings["checkPost"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Details post」\n╰──「Telah Aktif」")
							else:
								settings["checkPost"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Details post」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "checkpost off":
							if settings["checkPost"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Details post」\n╰──「Telah Nonaktif」")
							else:
								settings["checkPost"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Details post」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "checksticker on":
							if settings["checkSticker"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Details sticker」\n╰──「Telah Aktif」")
							else:
								settings["checkSticker"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Details sticker」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "checksticker off":
							if settings["checkSticker"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Details sticker」\n╰──「Telah Nonaktif」")
							else:
								settings["checkSticker"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Details sticker」\n╰──「Berhasil Menonaktifkan」")
						elif cmd == "detectunsend on":
							if msg.to in settings["detectUnsend"]:
								client.sendMessageFooter(to, namefoot, "╭──「Detect unsend」\n╰──「Telah Aktif」")
							else:
								settings["detectUnsend"].append(msg.to)
								client.sendMessageFooter(to, namefoot, "╭──「Detect unsend」\n╰──「Berhasil Mengaktifkan」")
						elif cmd == "detectunsend off":
							if msg.to not in settings["detectUnsend"]:
								client.sendMessageFooter(to, namefoot, "╭──「Detect unsend」\n╰──「Telah Nonaktif」")
							else:
								settings["detectUnsend"].remove(msg.to)
								client.sendMessageFooter(to, namefoot, "╭──「Detect unsend」\n╰──「Berhasil Menonaktifkan」")
						elif cmd.startswith("setautoaddmessage: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoAddMessage"] = txt
								client.sendMessageFooter(to, namefoot, "╭──「Auto add message」\n╰──「{}」".format(txt))
							except:
								client.sendMessageFooter(to, namefoot, "╭──「Auto add message」\n╰──「FAILED」")
						elif cmd.startswith("setautoresponmessage: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoResponMessage"] = txt
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon message」\n╰──「{}」".format(txt))
							except:
								client.sendMessageFooter(to, namefoot, "╭──「Auto respon message」\n╰──「FAILED」")
						elif cmd.startswith("setautojoinmessage: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoJoinMessage"] = txt
								client.sendMessageFooter(to, namefoot, "╭──「Auto join message」\n╰──「{}」".format(txt))
							except:
								client.sendMessageFooter(to, namefoot, "╭──「Auto join message」\n╰──「FAILED")


						elif cmd.startswith("changename: "):
							sep = text.split(" ")
							name = text.replace(sep[0] + " ","")
							if len(name) <= 20:
								profile = client.getProfile()
								nameee = "「NAME」"
								profile.displayName = name
								client.updateProfile(profile)
								client.sendMessageFooter(to, nameee, "╭──「Change name」\n╰──「{}」".format(name))
						elif cmd.startswith("changebio: "):
							sep = text.split(" ")
							bio = text.replace(sep[0] + " ","")
							if len(bio) <= 500:
								profile = client.getProfile()
								profile.statusMessage = bio
								name = "「BIO」"
								client.updateProfile(profile)
								client.sendMessageFooter(to, name, "╭──「Change bio」\n╰──「{}」".format(bio))
						elif cmd == "me":
							name = "「Ig: fahmiadrn」"
							client.sendMention(to, name, "╭──「Tag」\n│@!\n╰──「My Self」", [sender])
							client.sendContact(to, sender)
						elif cmd == "myprofile":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							name = "「DETAILS PROFILE」"
							result = "╭──「 Details Profile 」"
							result += "\n│ Display Name : @!"
							result += "\n│ Mid : {}".format(contact.mid)
							result += "\n│ Status Message : {}".format(contact.statusMessage)
							result += "\n│ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							result += "\n│ Cover : {}".format(str(cover))
							result += "\n╰─────「 Finish 」"
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							footer = "「IMAGE」"
							client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus), link, icon, footer)
							client.sendMention(to, name, result, [sender])
						elif cmd == "groupcreator":
							groupp = client.getGroup(to)
							gc = groupp.creator.mid
							name = "「GROUP CREATOR」"
							client.sendMention(to, name, "╭──「Group creator」\n╰──「 @!」", [gc])
						elif cmd == "mymid":
							contact = client.getContact(sender)
							name = "「MID」"
							client.sendMention(to, name, "╭──「Mid」\n│@!\n╰──「{}」".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							name = "「DISPLAY NAME」"
							client.sendMention(to, name, "╭──「Name」\n│@!\n╰──「{}」".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							name = "「BIO」"
							client.sendMention(to, name, "╭──「Bio」\n│@!\n╰──「{}」".format(contact.statusMessage), [sender])
						elif cmd == "mypicture":
							contact = client.getContact(sender)
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							footer = "「IMAGE」"
							client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus), link, icon, footer)
						elif cmd.startswith("sendpicture"):
							sep = msg.text.split(" ")
							link = msg.text.replace(sep[0] + " ","")
							linkk = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = link
							footer = "「IMAGE」"
							client.sendImageWithFooter(to, link, linkk, icon, footer)
						elif cmd.startswith("sendcontact"):
							sep = msg.text.split(" ")
							link = msg.text.replace(sep[0] + " ","")
							client.sendContact(to, link)
						elif cmd.startswith("sendvideo"):
							sep = msg.text.split(" ")
							link = msg.text.replace(sep[0] + " ","")
							client.sendVideoWithURL(to, link)
						elif cmd == "myvideoprofile":
							contact = client.getContact(sender)
							name = "「VIDEO PROFILE」"
							if contact.videoProfile == None:
								return client.sendMessageFoter(to, name, "Anda tidak memiliki video profile")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = str(cover)
							footer = "「IMAGE」"
							client.sendImageWithFooter(to, str(cover), link, icon, footer)
						elif cmd.startswith("getmid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									name = "「MID」"
									client.sendMention(to, name, "╭──「Mid」\n│@!\n╰──「{}」".format(ls), [ls])
						elif cmd.startswith("getname "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									name = "「DISPLAY NAME」"
									client.sendMention(to, name, "╭──「Name」\n│@!\n╰──「{}」".format(contact.displayName), [ls])
						elif cmd.startswith("getbio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									name = "「BIO」"
									client.sendMention(to, name, "╭──「Bio」\n│@!\n╰──「{}」".format(contact.statusMessage), [ls])
						elif cmd.startswith("getpicture "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									link = "line://ti/p/{}".format(client.getUserTicket().id)
									icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
									footer = "「IMAGE」"
									client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus), link, icon, footer)
						elif cmd.startswith("getvideoprofile "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									name = "「PROFILE」"
									if contact.videoProfile == None:
										return client.sendMention(to, name, "@!tidak memiliki video profile", [ls])
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("getcover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									link = "line://ti/p/{}".format(client.getUserTicket().id)
									icon = str(cover)
									footer = "「IMAGE」"
									client.sendImageWithFooter(to, str(cover), link, icon, footer)
						elif cmd.startswith("cloneprofile "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.cloneContactProfile(ls)
									name = "「CLONE」"
									client.sendContact(to, sender)
									client.sendMessageFooter(to, name, "Berhasil clone profile")
						elif cmd == "restoreprofile":
							try:
								clientProfile = client.getProfile()
								clientProfile.displayName = str(settings["myProfile"]["displayName"])
								clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
								clientPictureStatus = client.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="LineAPI/tmp/backupPicture.bin")
								coverId = str(settings["myProfile"]["coverId"])
								client.updateProfile(clientProfile)
								client.updateProfileCoverById(coverId)
								client.updateProfilePicture(clientPictureStatus)
								name = "「RESTORE」"
								client.sendMessageFooter(to, name, "Berhasil restore profile")
								client.sendContact(to, sender)
								client.deleteFile(clientPictureStatus)
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal restore profile")
						elif cmd == "backupprofile":
							try:
								clientProfile = client.getProfile()
								settings["myProfile"]["displayName"] = str(clientProfile.displayName)
								settings["myProfile"]["statusMessage"] = str(clientProfile.statusMessage)
								settings["myProfile"]["pictureStatus"] = str(clientProfile.pictureStatus)
								coverId = client.getProfileDetail()["result"]["objectId"]
								settings["myProfile"]["coverId"] = str(coverId)
								name = "「BACKUP」"
								client.sendMessageFooter(to, name, "Berhasil backup profile")
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal backup profile")
						elif cmd == "friendlist":
							contacts = client.getAllContactIds()
							num = 0
							result = "╭──「 Friend List 」"
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n│ {}. {}".format(num, contact.displayName)
							result += "\n╰─────「 Total {} Friend 」".format(len(contacts))
							name = "「FRIEND LIST」"
							client.sendMessageFooter(to, name, result)
						elif cmd.startswith("friendinfo "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							try:
								listContact = contacts[int(query)-1]
								contact = client.getContact(listContact)
								cover = client.getProfileCoverURL(listContact)
								name = "「DETAILS PROFILE」"
								result = "╭──「 Details Profile 」"
								result += "\n│ Display Name : @!"
								result += "\n│ Mid : {}".format(contact.mid)
								result += "\n│ Status Message : {}".format(contact.statusMessage)
								result += "\n│ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								result += "\n│ Cover : {}".format(str(cover))
								result += "\n╰─────「 Finish 」"
								link = "line://ti/p/{}".format(client.getUserTicket().id)
								icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								footer = "「IMAGE」"
								client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus), link, icon, footer)
								client.sendMention(to, name, result, [contact.mid])
							except Exception as error:
								logError(error)
						elif cmd == "blocklist":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "╭──「 List Blocked 」"
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n│ {}. {}".format(num, contact.displayName)
							result += "\n╰─────「 Total {} Blocked 」".format(len(blockeds))
							name = "「BLOCKED LIST」"
							client.sendMessageFooter(to, name, result)
						elif cmd.startswith("friendbroadcast: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							name = "「BROADCAST」"
							for contact in contacts:
								client.sendMessageFooter(contact, name, "╭──「Broadcast」\n╰──「{}」".format(str(txt)))
							client.sendMessageFooter(to, name, "╭──「Broadcast」\n╰──「Success bc to {} friend」".format(str(len(contacts))))


						elif cmd.startswith("changegroupname: "):
							if msg.toType == 2:
								sep = text.split(" ")
								groupname = text.replace(sep[0] + " ","")
								if len(groupname) <= 20:
									group = client.getGroup(to)
									group.name = groupname
									client.updateGroup(group)
									name = "「GROUP NAME」"
									client.sendMessageFooter(to, name, "╭──「Change group name」\n╰──「{}」".format(groupname))
						elif cmd == "openqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								name = "「QR」"
								client.sendMessageFooter(to, name, "╭──「Open QR」\n│line://ti/g/{}\n╰──「SUCCESS」".format(groupUrl))
						elif cmd == "closeqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								name = "「QR」"
								client.sendMessageFooter(to, name, "╭──「Close QR」\n╰──「SUCCESS」")
						elif cmd == "grouppicture":
							if msg.toType == 2:
								group = client.getGroup(to)
								link = "line://ti/p/{}".format(client.getUserTicket().id)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								footer = "「IMAGE」"
								client.sendImageWithFooter(to, groupPicture, link, groupPicture, footer)
						elif cmd == "groupname":
							if msg.toType == 2:
								group = client.getGroup(to)
								name = "「GROUP NAME」"
								client.sendMessageFooter(to, name, "╭──「Group name」\n╰──「{}」".format(group.name))
						elif cmd == "groupid":
							if msg.toType == 2:
								group = client.getGroup(to)
								name = "「ID」"
								client.sendMessageFooter(to, name, "╭──「Group id」\n╰──「{}」".format(group.id))
						elif cmd == "grouplist":
							groups = client.getGroupIdsJoined()
							ret_ = "╭──「 Group List 」"
							no = 0
							for gid in groups:
								group = client.getGroup(gid)
								no += 1
								ret_ += "\n│ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							ret_ += "\n╰─────「 Total {} Groups 」".format(str(len(groups)))
							name = "「GROUP LIST」"
							client.sendMessageFooter(to, name, str(ret_))
						elif cmd == "memberlist":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "╭──「 List Member 」"
								for contact in group.members:
									num += 1
									ret_ += "\n│ {}. {}".format(num, contact.displayName)
								ret_ += "\n╰─────「 Total {} Members 」".format(len(group.members))
								name = "「MEMBER LIST」"
								client.sendMessageFooter(to, name, ret_)
						elif cmd == "pendinglist":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "╭──「 Pending List 」"
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "╭──「Pendingan」\n╰──「Tidak ada list」")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n│ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n╰─────「 Total {} Pending 」".format(str(len(group.invitee)))
									name = "「PENDING LIST」"
									client.sendMessageFooter(to, name, str(ret_))
						elif cmd == "groupinfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "Tidak ditemukan"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "Tertutup"
									groupTicket = "Tidak ada"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "╭──「 Group Information 」"
								ret_ += "\n│ Nama Group : {}".format(group.name)
								ret_ += "\n│ ID Group : {}".format(group.id)
								ret_ += "\n│ Pembuat : @!"
								ret_ += "\n│ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n│ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n│ Group Qr : {}".format(groupQr)
								ret_ += "\n│ Group Ticket : {}".format(groupTicket)
								ret_ += "\n╰─────「 Success 」"
								name = "「DETAILS GROUP」"
								link = "line://ti/p/{}".format(client.getUserTicket().id)
								icon = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								footer = "「IMAGE」"
								client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus), link, icon, footer)
								client.sendMention(to, name, str(ret_), [groupCreator])
							except:
								ret_ = "╭──「 Group Information 」"
								ret_ += "\n│ Nama Group : {}".format(group.name)
								ret_ += "\n│ ID Group : {}".format(group.id)
								ret_ += "\n│ Pembuat : {}".format(groupCreator)
								ret_ += "\n│ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n│ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n│ Group Qr : {}".format(groupQr)
								ret_ += "\n│ Group Ticket : {}".format(groupTicket)
								ret_ += "\n╰─────「 Success 」"
								name = "「DETAILS GROUP」"
								client.sendMessageFooter(to, name, str(ret_))
						elif cmd.startswith("groupbroadcast: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							groups = client.getGroupIdsJoined()
							name = "「BROADCAST」"
							for group in groups:
								client.sendMessageFooter(group, name, "╭──「Broadcast」\n╰──「{}」".format(str(txt)))
							client.sendMessageFooter(to, name, "╭──「Broascast」\n╰──「Success bc to {} group」".format(str(len(groups))))


						elif cmd == 'mentionall':
							name = "「MENTION ALL」"
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//100
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "╭──「 Mention Members 」"
								dataMid = []
								for dataMention in group.members[mentionMembers*100 : (mentionMembers+1)*100]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n│ {}. @!".format(str(no))
								ret_ += "\n╰─────「 Total {} Members 」".format(str(len(dataMid)))
								client.sendMention(to, name, ret_, dataMid)
						elif cmd == "lurking on":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							name = "「READER」"
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessageFooter(to, name, "╭──「Lurking」\n╰──「Telah Aktif」")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessageFooter(to, name, "╭──「Set Lurking」\n╰──「{}」".format(readTime))
						elif cmd == "lurking off":
							tz = pytz.timezone("Asia/Jakarta")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							name = "「READER」"
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessageFooter(to, name, "╭──「Lurking」\n╰──「Telah nonaktif」")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessageFooter(to, name, "╭──「Delete Lurking」\n╰──「{}」".format(readTime))
						elif cmd == "lurking":
							name = "「CHECK READER」"
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessageFooter(to, name, "╭──「Lurking」\n╰──「Tidak ada readers」")
								else:
									no = 0
									result = "╭──「 Reader 」"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n│ {}. @!".format(str(no))
									result += "\n╰─────「 Total {} reader 」".format(str(len(read["readMember"][to])))
									name = "「READERS」"
									client.sendMention(to, name, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "changepictureprofile":
							settings["changePictureProfile"] = True
							name = "「SETTINGS」"
							client.sendMessageFooter(to, name, "╭──「Change picture profile」\n╰──「Send your image」")
						elif cmd == "changegrouppicture":
							if msg.toType == 2:
								name = "「SETTINGS」"
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessageFooter(to, name, "╭──「Change group picture」\n╰──「Send your image」")
						elif cmd == "mimic on":
							if settings["mimic"]["status"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Reply message」\n╰──「Telah Aktif」")
							else:
								settings["mimic"]["status"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Reply message」\n╰──「Berhasil mengaktifkan」")
						elif cmd == "mimic off":
							if settings["mimic"]["status"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Reply message」\n╰──「Telah Nonaktif」")
							else:
								settings["mimic"]["status"] = False
								client.sendMessageFootee(to, namefoot, "╭──「Reply message」\n╰──「Berhasil menonaktifkan」")
						elif cmd == "mimiclist":
							name = "「MIMIC LIST」"
							if settings["mimic"]["target"] == {}:
								client.sendMessageFooter(to, name, "╭──「Mimic list」\n╰──「Tidak ada target」")
							else:
								no = 0
								result = "╭──「 Mimic List 」"
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n│ {}. @!".format(no)
								result += "\n╰─────「 Total {} Mimic 」".format(str(len(target)))
								name = "「MIMIC」"
								client.sendMention(to, name, result, target)
						elif cmd.startswith("mimicadd "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								name = "「MIMIC」"
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessageFooter(to, name, "╭──「Mimic add」\n╰──「Target sudah ada di dalam list」")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessageFooter(to, name, "╭──「Mimic add」\n╰──「Berhasil menambahkan target」")
									except:
										client.sendMessageFooter(to, name, "╭──「Mimic add」\n╰──「Gagal menambahkan target」")
						elif cmd.startswith("mimicdel "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								name = "「MIMIC」"
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessageFooter(to, name, "╭──「Mimic delete」\n╰──「Target tidak ada didalam list」")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessageFooter(to, name, "╭──「Mimic delete」\n╰──「Berhasil menghapus target」")
									except:
										client.sendMessageFooter(to, name, "╭──「Mimic delete」\n╰──「Gagal menghapus target」")


						elif cmd.startswith("instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/instainfo/{}?key=betakey".format(txt))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "「Instagram」"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "╭──「 Instagram Info 」"
							result += "\n│ Name : {}".format(data["result"]["name"])
							result += "\n│ Username: {}".format(data["result"]["username"])
							result += "\n│ Bio : {}".format(data["result"]["bio"])
							result += "\n│ Follower : {}".format(data["result"]["follower"])
							result += "\n│ Following : {}".format(data["result"]["following"])
							result += "\n│ Private : {}".format(data["result"]["private"])
							result += "\n│ Post : {}".format(data["result"]["mediacount"])
							result += "\n╰─────「 Finish 」"
							footer = "「Instagram」"
							client.sendImageWithFooter(to, data["result"]["url"], link, icon, footer)
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									link = "line://ti/p/{}".format(client.getUserTicket().id)
									icon = str(search["link"])
									footer = "「InstaStory」"
									if search["tipe"] == 1:
										client.sendImageWithFooter(to, str(search["link"]), link ,icon, footer)
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "╭──「 Quotes 」"
							result += "\n│ Author : {}".format(data["result"]["author"])
							result += "\n│ Category : {}".format(data["result"]["category"])
							result += "\n│ Quote : {}".format(data["result"]["quote"])
							result += "\n╰─────「 Finish 」"
							name = "「QUOTES TODAY」"
							client.sendMessageFooter(to, name, result)
						elif cmd.startswith("say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("lineAPI/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "lineAPI/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("lineAPI/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("searchyoutube"):
							sep = text.split(" ")
							search = text.replace(sep[0] + " ","")
							params = {"search_query": search}
							r = requests.get("https://www.youtube.com/results", params = params)
							soup = BeautifulSoup(r.content, "html5lib")
							ret_ = "╭──「 Youtube Search 」"
							datas = []
							for data in soup.select(".yt-lockup-title > a[title]"):
								if "&lists" not in data["href"]:
									datas.append(data)
							for data in datas:
								ret_ += "\n│──「  {}  」".format(str(data["title"]))
								ret_ += "\n│ https://www.youtube.com{}".format(str(data["href"]))
							ret_ += "\n╰─────「 Total {} Result 」".format(len(datas))
							text = str(ret_)
							icon = "https://image.ibb.co/f9Rwpy/ic_youtube_logo.png"
							name = "「Youtube」"
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							client.sendFooter(to, text, icon, name, link)
#--+++-----+++-----
#---+---++
						elif cmd.startswith("searchimage "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = random.choice(data["result"])
							footer = "「IMAGE」"
							client.sendImageWithFooter(to, random.choice(data["result"]), link, icon, footer)
						elif cmd.startswith("searchmusic "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							icon = "https://image.ibb.co/fakvhJ/appicon.png"
							name = "「JOOX」"
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							if len(cond) == 1:
								num = 0
								ret_ = "╭──「 Result Music 」"
								for music in data["result"]:
									num += 1
									ret_ += "\n│ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n╰─────「 Total {} Music 」".format(str(len(data["result"])))
								ret_ += "\n\nUntuk mengirim music, silahkan gunakan command {}SearchMusic {}|「number」".format(str(setKey), str(search))
								client.sendFooter(to, str(ret_), icon, name, link)
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									linkk = "line://ti/p/{}".format(client.getUserTicket().id)
									iconn = "https://image.ibb.co/fakvhJ/appicon.png"
									footer = "「JOOX IMAGE」"
									namee = "「JOOX」"
									ret_ = "╭──「 Music 」"
									ret_ += "\n│ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n│ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n│ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n│ Link : {}".format(str(data["result"]["mp3"][0]))
									ret_ += "\n╰─────「 Finish 」"
									client.sendImageWithFooter(to, str(data["result"]["img"]), linkk, iconn, footer)
									client.sendFooter(to, str(ret_), iconn, namee, linkk)
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
						elif cmd.startswith("searchlyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							icon = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnp3q7jWUawGklGWAdIpDXhN5TpUYG889S1GqNy9u8DBneXLXr"
							name = "「MusixMatch」"
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "╭──「 Musixmatch Result 」"
									num = 0
									for title in result:
										num += 1
										ret_ += "\n│ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n╰─────「 Total {} Lyric 」".format(str(len(result)))
									ret_ += "\n\nUntuk melihat lyric, silahkan gunakan command {}SearchLyric {}|「number」".format(str(setKey), str(query))
									client.sendFooter(to, ret_, icon, name, link)
								elif len(cond) == 2:
									num = int(cond[1])
									iconn = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnp3q7jWUawGklGWAdIpDXhN5TpUYG889S1GqNy9u8DBneXLXr"
									namee = "「MusixMatch」"
									linkk = "line://ti/p/{}".format(client.getUserTicket().id)
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
												client.sendFooter(to, lyric, iconn, namee, linkk)
						elif cmd.startswith("tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							name = "「TRANSLATE」"
							result = translator.translate(txt, dest=lang)
							client.sendMessageFooter(to, name, result.text)
						if text.lower() == "mykey":
							name = "「KEY」"
							client.sendMessageFooter(to, name, "╭──「Key command」\n╰──「{}」".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessageFooter(to, namefoot, "╭──「Key command」\n╰──「Telah Aktif」")
							else:
								settings["setKey"] = True
								client.sendMessageFooter(to, namefoot, "╭──「Key command」\n╰──「Berhasil mengaktifkan」")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessageFooter(to, namefoot, "╭──「Key command」\n╰──「Telah Nonaktif」")
							else:
								settings["setKey"] = False
								client.sendMessageFooter(to, namefoot, "╭──「Key command」\n╰──「Berhasil menonaktifkan」")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									name = "「AUTO JOIN TICKET」"
									client.sendMessageFooter(to, name, "Berhasil masuk ke group %s" % str(group.name))
					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							name = "「SUCCESS」"
							client.sendMessageFooter(to, name, "╭──「Change picture profile」\n╰──「SUCCESS」")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								name = "「SUCCESS」"
								client.sendMessageFooter(to, name, "╭──「Change group picture」\n╰──「SUCCESS」")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							name = "「DETAILS STICKER」"
							ret_ = "╭──「 Sticker Info 」"
							ret_ += "\n│ STICKER ID : {}".format(stk_id)
							ret_ += "\n│ STICKER PACKAGES ID : {}".format(pkg_id)
							ret_ += "\n│ STICKER VERSION : {}".format(stk_ver)
							ret_ += "\n│ STICKER URL : line://shop/detail/{}".format(pkg_id)
							ret_ += "\n╰─────「 Finish 」"
							client.sendMessageFooter(to, name, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "╭──「 Details Contact 」"
								ret_ += "\n│ Nama : {}".format(str(contact.displayName))
								ret_ += "\n│ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n│ Bio : {}".format(str(contact.statusMessage))
								ret_ += "\n│ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								ret_ += "\n│ Gambar Cover : {}".format(str(cover))
								ret_ += "\n╰─────「 Finish 」"
								link = "line://ti/p/{}".format(client.getUserTicket().id)
								icon = "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								footer = "「IMAGE」"
								name = "「DETAILS CONTACT」"
								client.sendImageWithFooter(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendMessageFooter(to, name, str(ret_))
							except:
								client.sendMessage(to, "Kontak tidak valid")
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "╭──「 Details Post 」"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n│ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n│ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n│ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n│ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n│ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n│ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n│ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n│ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n│ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n│ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n│ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n╰─────「 Finish 」"
								name = "「DETAILS POST」"
								client.sendMessageFooter(to, name, str(ret_))
							except:
								client.sendMessage(to, "Post tidak valid")
			except Exception as error:
				logError(error)


		if op.type == 26:
			try:
				print("[ 26 ] RECEIVE MESSAGE")
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							name = "「MIMIC」"
							client.sendMessageFooter(to, name, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							link = "line://ti/p/{}".format(client.getUserTicket().id)
							icon = path
							footer = "「MIMIC IMAGE」"
							client.sendImageFooter(to, path, link, icon, footer)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									name = "「AUTO RESPON」"
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, name, settings["autoResponMessage"], [sender])
											break
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									name = "「AUTO JOIN TICKET」"
									client.sendMessageFooter(to, name, "Berhasil masuk ke group %s" % str(group.name))
						if msg.to in settings["detectUnsend"]:
							try:
								unsendTime = time.time()
								unsend[msg_id] = {"text": text, "from": sender, "time": unsendTime}
							except Exception as error:
								logError(error)
					if msg.contentType == 1:
						if msg.to in settings["detectUnsend"]:
							try:
								unsendTime = time.time()
								image = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-image.bin".format(time.time()))
								unsend[msg_id] = {"from": sender, "image": image, "time": unsendTime}
							except Exception as error:
								logError(error)
			except Exception as error:
				logError(error)


		if op.type == 55:
			print ("[ 55 ] NOTIFIED READ MESSAGE")
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)


		if op.type == 65:
			try:
				if op.param1 in settings["detectUnsend"]:
					to = op.param1
					sender = op.param2
					nameee = "「ERROR」"
					if sender in unsend:
						unsendTime = time.time()
						contact = client.getContact(unsend[sender]["from"])
						if "text" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								name = "「UNSEND MESSAGE」"
								ret_ = "╭──「 Unsend Message 」"
								ret_ += "\n│ Sender : @!"
								ret_ += "\n│ Time : {} yang lalu".format(sendTime)
								ret_ += "\n│ Type : Text"
								ret_ += "\n│ Text : {}".format(unsend[sender]["text"])
								ret_ += "\n╰─────「 Finish 」"
								client.sendMention(to, name, ret_, [contact.mid])
								del unsend[sender]
							except:
								del unsend[sender]
						elif "image" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								name2 = "「UNSEND IMAGE」"
								ret_ = "╭──「 Unsend Message 」"
								ret_ += "\n│ Sender : @!"
								ret_ += "\n│ Time : {} yang lalu".format(sendTime)
								ret_ += "\n│ Type : Image"
								ret_ += "\n│ Text : None"
								ret_ += "\n╰─────「 Finish 」"
								link = "line://ti/p/{}".format(client.getUserTicket().id)
								icon = unsend[sender]["image"]
								footer = "「IMAGE」"
								client.sendMention(to, name2, ret_, [contact.mid])
								client.sendImageFooter(to, unsend[sender]["image"], link, icon, footer)
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
							except:
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
					else:
						client.sendMessageFooter(to, nameee, "╭──「Detect unsend」\n╰──「Gagal karena data tidak ditemukan」")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()
