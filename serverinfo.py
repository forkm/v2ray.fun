#! /usr/bin/env python
# -*- coding: utf-8 -*-

import readjson, urllib2, base64, os, json
# 获取本机IP地址
myip = urllib2.urlopen('http://api.ipify.org').read()
myip = myip.strip()

# 判断传输配置
mystreamnetwork = str(readjson.ConfStreamNetwork)

if readjson.ConfStreamNetwork == "kcp":
    if(readjson.ConfStreamHeader == "utp"):
        mystreamnetwork = "mKCP utp BT下载流量"
    elif(readjson.ConfStreamHeader == "srtp"):
        mystreamnetwork = "mKCP srtp 伪装FaceTime通话"
    elif(readjson.ConfStreamHeader == "wechat-video"):
        mystreamnetwork = "mKCP wechat-video 伪装微信视频流量"
    else:
        mystreamnetwork = "mKCP"
elif readjson.ConfStreamNetwork == "http":
    mystreamnetwork = "HTTP/2"
elif readjson.ConfStreamNetwork == "ws":
    mystreamnetwork = "WebSocket"

if (readjson.ConfStreamSecurity == "tls"):
    mystreamsecurity = "TLS：开启"
else:
    mystreamsecurity = "TLS：关闭"

# 输出信息
print("服务器IP：%s") % str(myip)
print("主端口：%s") % str(readjson.ConfPort)
print("UUID：%s") % str(readjson.ConfUUID)
print("alter ID: %s") % str(readjson.ConfAlterId)
print("加密方式：%s") % str(readjson.ConfSecurity)
print("传输方式：%s") % str(mystreamnetwork)
# print("路径：%s") % str(readjson.ConfPath)
if readjson.ConfigDynPortRange:
    print("动态端口范围:%s") % str(readjson.ConfigDynPortRange)
else:
    print("动态端口:禁止")

# config["host"] = str(readjson.ConfPath)

def clientPort():
    global PortUrl
    if readjson.ConfListeningLocal == "127.0.0.1" and readjson.ConfStreamNetwork == "ws":
        PortUrl = str(443)
    else:
        PortUrl = str(readjson.ConfPort)

def GetVmessUrl():
    config = {
        "v": "2",
        "ps": "v2rayN V2.x",
        "add": "",
        "port": "",
        "id": "",
        "aid": "",
        "net": "",
        "type": "none",
        "host": "",
        "path": "",
        "tls": "",
    }
    config["add"] = str(myip)
    clientPort()
    config["port"] = PortUrl
    config["id"] = str(readjson.ConfUUID)
    config["aid"] = str(readjson.ConfAlterId)
    config["net"] = str(mystreamnetwork)
    if mystreamnetwork == "kcp":
        config["type"] = str(readjson.ConfStreamHeader)
    if (readjson.ConfSecurity == "tls") or (readjson.ConfListeningLocal == "127.0.0.1" and readjson.ConfStreamNetwork == "ws"):
        config["tls"] = "tls"
    base64Str = base64.encodestring(json.dumps(config))
    base64Str = ''.join(base64Str.split())
    vmessurl = "vmess://" + base64Str
    return vmessurl

def GetVmessUrlPepi():
    mystreamnetwork = str(readjson.ConfStreamNetwork)
    if readjson.ConfStreamNetwork == "http":
        mystreamnetwork = "http"
    elif readjson.ConfStreamNetwork == "ws":
        mystreamnetwork = "websocket"
    else:
        mystreamnetwork = "none"
    clientPort()
    base64Str = base64.urlsafe_b64encode(str(readjson.ConfSecurity) + ":" + str(
        readjson.ConfUUID) + "@" + str(myip) + ":" + PortUrl)
    vmessurl = "vmess://" + base64Str + "?obfs=" + str(mystreamnetwork)
    return vmessurl

def GreenShow(string):
    print("\033[32m")
    print("%s") % string
    print("\033[0m")

def GenQRCode(name, string):
    os.system("qrcode -w 200 -o ~/" + name + " " + string)

def ShowQRCode(string):
    os.system("qrcode -w 200 " + string)

print("=====  V2rayN v2.x =====")
GreenShow(GetVmessUrl())
GenQRCode("config_v2rayN.png", GetVmessUrl())

print("=====  Pepi(ios) 1.0.7(87) =====")
GreenShow(GetVmessUrlPepi())
GenQRCode("config_pepi.png", GetVmessUrlPepi())
