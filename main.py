# -*- coding: UTF-8 -*-
import requests
import websocket
import threading
import base64
import time
import json
import re
import os
from mcstatus import MinecraftServer

fuckmozhengb = {}
fuckSpamDog = {}
fanyitimes = {}
joinlists = {}
adminList = [1790194105,1584784496,2734583]
hypban_cookie = None
hypban_isChecking = False

def SpamCheck(group,qq,msgid):
	return

def blockList_get(number):
	return os.path.isfile("C:\\Users\\guimc\\Desktop\\qqbots\\mirai\\ntlist\\{}".format(number))

def on_message2(ws, message):
	global hypban_cookie
	global hypban_isChecking
	try:
		# print(message)
		a = json.loads(message)
		message_text = ""
		message_id = 0
		ad = a["data"]
		if ad["type"] == "GroupMuteAllEvent":
			print(requests.post("http://127.0.0.1:8080/unmuteAll",data=json.dumps({"target":ad["group"]["id"]})))
		if ad["type"] == "MemberJoinRequestEvent":
			aaa = "有人正在申请入群!\n申请用户:{0}({1})".format(ad["nick"],ad["fromId"])
			sendGroupmsg2(ad["groupId"],aaa)
			joinlists[ad["eventId"]] = [ad["fromId"],ad["groupId"]]
		if ad["type"] == "MemberLeaveEventKick":
			aaa = "{0}({1})被移出了本群！\n操作人:{2}({3})".format(ad["member"]["memberName"],ad["member"]["id"],ad["operator"]["memberName"],ad["operator"]["id"])
			sendGroupmsg2(ad["operator"]["group"]["id"],aaa)
		if ad["type"] == "MemberJoinEvent":
			sendGroupmsg2(ad["member"]["group"]["id"],"Welcome! {0}({1})".format(ad["member"]["memberName"],ad["member"]["id"]))
		if ad["type"] == "GroupMessage":
			message_list1 = ad["messageChain"]
			for i in message_list1:
				it = i["type"]
				if it == "Quote": message_text += "(回复了一条消息)"
				if it == "At": message_text += "@{}".format(i["target"])
				if it == "AtAll": message_text += "@All"
				if it == "Face": message_text += "[表情:{}]".format(i["name"])
				if it == "Plain": message_text += i["text"]
				if it == "Image": message_text += "[图片]"
				if it == "FlashImage": message_text += "[动图?]"
				if it == "Voice": message_text += "[语音]"
				if it == "Xml": message_text += "[卡片信息:Xml]"
				if it == "Json": message_text += "[卡片信息:Json]"
				if it == "Poke": message_text += "[戳一戳]"
				if it == "Dice": message_text += "[Dice:{}]".format(i["value"])
				if it == "MusicShare": message_text += "[音乐分享:{0} ({1})]".format(i["title"],i["jumpUrl"])
				if it == "ForwardMessage": message_text += "[合并转发消息]"
				if it == "File": message_text += "[文件:{}]".format(i["name"])
				if it == "Source": message_id = i["id"]
		else:
			return
		sender_qqnumber = ad["sender"]["id"]
		sender_name = ad["sender"]["memberName"]
		group_number = ad["sender"]["group"]["id"]
		group_name = ad["sender"]["group"]["name"]
		SpamCheck(group_number,sender_qqnumber,message_id)
		if message_text == "":
			return
		command_list = message_text.split(" ")
		if message_text.find("[表情:呲牙]") != -1:
			sendGroupmsg3(group_number,sender_qqnumber,"为什么要呲牙咧嘴?:(((((")
			recall(message_id)
		if sender_qqnumber in [] and message_text[0] == "#":
			sendGroupmsg(group_number,message_id,sender_qqnumber,"你好,你已经被禁止使用这部分功能!")
			return
		print("[{0}({1})] {2}({3}) {4}".format(group_name,group_number,sender_name,sender_qqnumber,message_text))
		if message_text == "#test":
			sendGroupmsg(group_number,message_id,sender_qqnumber,"Hello!")
		if len(command_list) == 2 and command_list[0] == "#get_skin":
			try:
				uuid1 = requests.get("https://api.mojang.com/users/profiles/minecraft/"+command_list[1])
				if uuid1.status_code != 200:
					sendGroupmsg(group_number,message_id,sender_qqnumber,"获取信息失败,可能是没有这 个玩家?")
					return
				uuid1 = uuid1.json()["id"]
				# https://crafatar.com/renders/body/{uuid}
				data1 = {
					"target": group_number,
					"quote": message_id,
					"messageChain": [
						{"type":"At","target":sender_qqnumber},
						{"type":"Plain","text":"\nUsername: {0}\nUUID: {1}".format(command_list[1],uuid1)},
						{"type":"Image","url":"https://crafatar.com/renders/body/{0}".format(uuid1)}
					]
				}
				print(requests.post("http://localhost:8080/sendGroupMessage",data=json.dumps(data1)).text)
			except Exception as e:
				sendGroupmsg(group_number,message_id,sender_qqnumber,"ERR: {}:{}".format(type(e),e))
		if command_list[0] == "#help":
			sendGroupmsg(group_number,message_id,sender_qqnumber,"请访问: http://bot.guimc.ltd/")
		if message_text == "#sjyy":
			sendGroupmsg(group_number,message_id,sender_qqnumber,requests.get("http://api.muxiuge.cn/API/society.php").json()["text"])
		if command_list[0] == "/mcping":
			try:
				server = MinecraftServer.lookup(command_list[1]).status()
				aaa = "Motd:\n{0}\n在线人数:{1}/{2}\nPing:{3}\nVersion:{4} (protocol:{5})".format(re.sub(re.compile(r"§."),"",server.description),server.players.online,server.players.max,server.latency,server.version.name,server.version.protocol)
				data1 = {
					"target": group_number,"quote": message_id,
					"messageChain": [
						{"type":"At","target":sender_qqnumber},
						{"type":"Plain","text":aaa}
					]
				}
				# {"type":"Image","base64":server.favicon.replace("data:image/png;base64,","")}
				if server.favicon != None:
					data1["messageChain"].append({"type":"Image","base64":server.favicon.replace("data:image/png;base64,","")})
				print(requests.post("http://localhost:8080/sendGroupMessage",data=json.dumps(data1)).text)
			except Exception as e:
				sendGroupmsg(group_number,message_id,sender_qqnumber,"ERR: {}:{}".format(type(e),e))
		if command_list[0] == "折磨":
			if ad["sender"]["permission"] in ["OWNER","ADMINISTRATOR"] or sender_qqnumber in adminList:
				sendGroupmsg(group_number,message_id,sender_qqnumber,"Starting...")
				if int(command_list[3]) <= 0 and int(command_list[2]) > 10:
					sendGroupmsg(group_number,message_id,sender_qqnumber,"You can't do it! The number is wrong!")
					return
				for i in range(int(command_list[2])):
					time.sleep(int(command_list[3]))
					mutePerson(group_number,int(command_list[1]),60)
					time.sleep(int(command_list[3]))
					unmutePerson(group_number,int(command_list[1]))
				sendGroupmsg(group_number,message_id,sender_qqnumber,"Finish!!!")
			else:sendGroupmsg(group_number,message_id,sender_qqnumber,"You can't do it!!!")
		if command_list[0] == "#hypban":
			try:
				userName = command_list[1]
				BanID = command_list[2].replace("#","")
				print("Username:{} BanID:{}".format(userName,BanID))
				if hypban_cookie != None:
					b = requests.get("http://127.0.0.1/hypban.php?name={0}&banid={1}&type=api".format(userName,BanID),headers={'Host':'api.xgstudio.xyz'},cookies=requests.utils.dict_from_cookiejar(hypban_cookie))
				else:
					b = requests.get("http://127.0.0.1/hypban.php?name={0}&banid={1}&type=api".format(userName,BanID),headers={'Host':'api.xgstudio.xyz'})
				a = b.text
				hypban_cookie = b.cookies
				print(a)
				if a == "SparklingWater:Wait some time to Use":
					a = "Please Wait some time to use"
				elif a.find("<b>Warning</b>:  sizeof():") != -1:
					a = "Error:We can't get banInfo!"
				sendGroupmsg(group_number,message_id,sender_qqnumber,a)
			except Exception as e:
				sendGroupmsg(group_number,message_id,sender_qqnumber,"ERR: {}:{}".format(type(e),e))
		if len(message_text) < 35 and re.search("qq:[1-9]([0-9]{4,10})|(花雨庭|hyp|hyt)|暴打|拿捏|配置|暴击|杀戮|.*内部|\\dR|\\n元|破甲|[0-9]{2,4}-[0-9]{2,4}|天花板|工具箱|[0-9]{2,4}/[0-9]{2}/[0-9]{2}|绕更新|attach|cl14|cl8|开端|不封号|外部|.* toolbox|替换au|绕过(盒子)vape检测|外部|防封|封号|waibu|晋商|禁商|盒子更新后|跑路|小号机|群(号)[0-9]{5,10}", message_text) != None:
			sendGroupmsg3(group_number,sender_qqnumber,"你好像在发广告 :(((((")
			recall(message_id)
			sendTempMsg(group_number,1584784496,"{0}({1})匹配成功了正则,并且消息字数大于了35\n消息:\n{2}")
		if command_list[0] == "#fdpinfo":
			# https://bstats.org/api/v1/plugins/11076/charts/<Type>/data
			try:
				if command_list[1] == "online":
					url = "https://bstats.org/api/v1/plugins/11076/charts/minecraftVersion/data"
					a = requests.get(url=url).json()
					onlinePlayer = 0
					for i in a:
						onlinePlayer += i["y"]
					sendGroupmsg(group_number,message_id,sender_qqnumber,"OnlinePlayers: {}".format(onlinePlayer))
				elif command_list[1] == "versions":
					url = "https://bstats.org/api/v1/plugins/11076/charts/pluginVersion/data"
					a = requests.get(url=url).json()
					onlineVersion = []
					for i in a:
						onlineVersion.append("{}: {}".format(i["name"],i["y"]))
					sendGroupmsg(group_number,message_id,sender_qqnumber,"OnlineVersionsInfo:\n{}".format("\n".join(onlineVersion)))
				elif command_list[1] == "systems":
					url = "https://bstats.org/api/v1/plugins/11076/charts/os/data"
					a = requests.get(url=url).json()
					onlineSystem = []
					for i in a["seriesData"]:
						onlineSystem.append("{}: {}".format(i["name"],i["y"]))
					sendGroupmsg(group_number,message_id,sender_qqnumber,"OnlineSystms:\n{}".format("\n".join(onlineSystem)))
				elif command_list[1] == "countrys":
					url = "https://bstats.org/api/v1/plugins/11076/charts/location/data"
					a = requests.get(url=url).json()
					onlineCountry = []
					for i in a:
						onlineCountry.append("{}: {}".format(i["name"],i["y"]))
					sendGroupmsg(group_number,message_id,sender_qqnumber,"OnlineCountrys:\n{}".format("\n".join(onlineCountry)))
			except Exception as e:
				sendGroupmsg(group_number,message_id,sender_qqnumber,"ERR: {}:{}".format(type(e),e))
	except Exception as e:
		print(e)

def mutePerson(group,qqnumber,mutetime):
	data1 = {
		"target":group,
		"memberId":qqnumber,
		"time":mutetime
	}
	print(requests.post("http://localhost:8080/mute",data=json.dumps(data1)).text)

def unmutePerson(group,qqnumber):
	data1 = {
		"target":group,
		"memberId":qqnumber
	}
	print(requests.post("http://localhost:8080/unmute",data=json.dumps(data1)).text)

def recall(msgid):
	data1 = {
		"target":msgid
	}
	print(requests.post("http://localhost:8080/recall",data=json.dumps(data1)).text)

def sendGroupmsg2(target1,text):
	data1 = {
		"target": target1,
		"messageChain": [
			{"type":"Plain","text":text}
		]
	}
	print(requests.post("http://localhost:8080/sendGroupMessage",data=json.dumps(data1)).text)

def sendGroupmsg3(target1,senderqq,text):
	data1 = {
		"target": target1,
		"messageChain": [
			{"type":"At","target":senderqq},
			{"type":"Plain","text":" {}".format(text)}
		]
	}
	print("[Bot -> Group]{}".format(text))
	print(requests.post("http://localhost:8080/sendGroupMessage",data=json.dumps(data1)).text)

def sendGroupmsg(target1,msgid,senderqq,text):
	data1 = {
		"target": target1,
		"quote": msgid,
		"messageChain": [
			{"type":"At","target":senderqq},
			{"type":"Plain","text":" {}".format(text)}
		]
	}
	print("[Bot -> Group]{}".format(text))
	print(requests.post("http://localhost:8080/sendGroupMessage",data=json.dumps(data1)).text)

def urlget(url):
	headers = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'}
	temp=requests.get(url, headers=headers)
	return(temp.text)

def sendTempMsg(target1,target2,text):
	data1 = {
		"qq": target2,
		"group": target1,
		"messageChain": [
			{"type":"Plain","text":text}
		]
	}
	print(requests.post("http://localhost:8080/sendTempMessage",data=json.dumps(data1)).text)

# 定义一个用来接收监听数据的方法
def on_message(ws, message):
	threading.Thread(target=on_message2, args=(ws, message)).start()

# 定义一个用来处理错误的方法
def on_error(ws, error):
	print("-----连接出现异常，异常信息如下-----")
	print(error)

# 定义一个用来处理关闭连接的方法
def on_close(ws):
	print("-------连接已关闭------")


if __name__ == "__main__":
	ws = websocket.WebSocketApp("ws://127.0.0.1:8080/all?verifyKey=uThZyFeQwJbD&qq=3026726134",
				on_message=on_message,
				on_error=on_error,
				on_close=on_close,
				)
	ws.run_forever()