from dosdefence import isDos, reload, dos_defence
from os import getenv
from function import *
import sqlite3
from interact_with_imgur import uploadAndGetPhoto
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


# preparation
userStatus = {}
imgName = {}
userUpdate = {}

def isAttack(text):
    if '*' in text or '?' in text or '%' in text or '+' in text or '_' in text:
        return True
    if "\"" in text or '\'' in text:
        return True
    return False

def startbot(update, bot):
    if(isDos(update)): return
    Send(update, "hihi")
    Send(update, "按 /help ")

def help(update, bot):
    if(isDos(update)): return
    Send(update, "/help\n" \
                +"/cal\n"\
                +"/add\n"\
                +"/del\n"\
                +"/list\n"\
                +"/find\n")

def list(update, bot):
    if(isDos(update)): return
    userID = str(update.message.from_user.id)
    sql = sqlite3.connect("KaTsu.db")
    cur = sql.cursor()
    
    cur.execute("Select Name from Data")

    text = []
    allPhoto = cur.fetchall()
    for result in allPhoto:
        text.append( result[0])
    cur.close()
    sql.close()


    if(len(allPhoto)==0):
        Send(update, "沒東西")
    else:
        userUpdate.update({userID: update})
        update.message.reply_text("現在有：",
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(s, callback_data = "{0} {1}".format(s, userID)) for s in text[0::2]],
            [InlineKeyboardButton(s, callback_data = "{0} {1}".format(s, userID)) for s in text[1::2]]
            
        ]))


def setVal(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    if str(userID) not in getenv('DEVELOPER_ID'): return
    text = ' '.join(update.message.text.split(' ')[1:])
    sql = sqlite3.connect("KaTsu.db")
    sql.execute(text)
    sql.commit()
    sql.close()
    reload()
    return

def add(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    if str(userID) == getenv('DEVELOPER_ID'):
        userStatus.update({userID:"waitName"})
        Send(update, "輸入名字", force=True)

def finding(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    text = update.message.text.split(' ')
    if(len(text)==1):
        userStatus.update({userID:"findName"})
        Send(update, "輸入名字", force=True)
        return
    text = text[1]
    if isAttack(text):
        Send(update, '不要攻擊我啦')
        try:
            del userStatus[userID]
        except:
            pass
        return

    sql = sqlite3.connect("KaTsu.db")
    cur = sql.cursor()
    cur.execute("Select Image from Data where Name GLOB '{0}'".format(text))
    allPhoto = cur.fetchall()
    cur.close()
    sql.close()
    for result in allPhoto:
        # Send(update, result[0])
        SendPhoto(update, result[0])
    if(len(allPhoto)==0):
        Send(update, "查無結果")

def delete(update, bot):
    if(isDos(update)): 
        print(dos_defence)
        return
    userID = update.message.from_user.id
    if str(userID) == getenv('DEVELOPER_ID'):
        userStatus.update({userID:"delName"})
        Send(update, "輸入名字", force=True)

def select(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    text = update.message.text
    nums = text.split(' ')[1:]
    try:
        if(len(nums)==3):
            for i in range(len(nums)):
                nums[i] = int(nums[i])
                if(nums[i]>10 or nums[i]<1):
                    return
            count1(update, nums, [1, 1, 1])
        elif(len(nums)==7 and nums[3]=='from'):
            for i in range(len(nums)):
                if(i==3):
                    continue
                nums[i] = int(nums[i])
                if(nums[i]>10 or nums[i]<1):
                    return
            count1(update, nums[:3], nums[4:])
        else:
            Send(update, '輸入指令\n%d %d %d (from %d %d %d)', True)
            userStatus.update({userID:"calculate"})

    except:
        return
def callback(update, bot):
    text, userID = update.callback_query.data.split(" ")
    update2 = userUpdate[userID]
    if(isDos(update2)): return
    update.callback_query.edit_message_text(text)

    sql = sqlite3.connect("KaTsu.db")
    cur = sql.cursor()
    cur.execute("Select Image from Data where Name GLOB '{0}'".format(text))
    allPhoto = cur.fetchall()
    cur.close()
    sql.close()
    print(text)
    for result in allPhoto:
        # Send(update, result[0])
        SendPhoto(update2, result[0])
    if(len(allPhoto)==0):
        Send(update2, "查無結果")


def getText(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    text = update.message.text
    print(text)
    if isAttack(text):
        Send(update, '不要攻擊我啦')
        try:
            del userStatus[userID]
        except:
            pass
        return
    try:
        if userID in userStatus:
            state = userStatus[userID]
            if state == 'waitName' or state == 'waitPhoto':
                sql = sqlite3.connect("KaTsu.db") 
                cur = sql.cursor()
                cur.execute("select count(*) from Data where Name = '{0}'".format(text))
                num = cur.fetchone()[0]
                print(num)
                cur.close()
                sql.close()

                if(num!=0):
                    Send(update, '名字重複', force=True)
                    return

                imgName.update({userID:text})
                Send(update, '名字好了')
                Send(update, '給我照片', force=True)
            elif state == 'delName':
                sql = sqlite3.connect("KaTsu.db") 
                cur = sql.cursor()
                cur.execute("delete from Data where Name = '{0}'".format(text))
                sql.commit()
                cur.close()
                sql.close()
                Send(update, "刪除 {0}".format(text))
                del userStatus[userID]
            elif state == 'findName':
                sql = sqlite3.connect("KaTsu.db")
                cur = sql.cursor()
                cur.execute("Select Image from Data where Name GLOB '{0}'".format(text))
                try:
                    allPhoto = cur.fetchall()
                    cur.close()
                    sql.close()
                    for result in allPhoto:
                        # Send(update, result[0])
                        SendPhoto(update, result[0])
                    if(len(allPhoto)==0):
                        Send(update, "查無結果")
                except:
                    try:
                        cur.close()
                        sql.close()
                    except:
                        pass
                    Send(update, "查無結果")

                del userStatus[userID]
            elif state == 'calculate':
                nums = text.split(' ')
                try:
                    if(len(nums)==3):
                        for i in range(len(nums)):
                            nums[i] = int(nums[i])
                            if(nums[i]>10 or nums[i]<1):
                                return
                        count1(update, nums, [1, 1, 1])
                    elif(len(nums)==7 and nums[3]=='from'):
                        for i in range(len(nums)):
                            if(i==3):
                                continue
                            nums[i] = int(nums[i])
                            if(nums[i]>10 or nums[i]<1):
                                return
                        count1(update, nums[:3], nums[4:])
                    else:
                        Send(update, "輸入無效")
                except:
                    Send(update, "輸入無效")
                    del userStatus[userID]
                    return
                del userStatus[userID]

    except:
        pass
    # else:
    #     sql = sqlite3.connect("KaTsu.db")
    #     cur = sql.cursor()
    #     cur.execute("Select Image from Data where Name GLOB '{0}'".format(text))
    #     allPhoto = cur.fetchall()
    #     cur.close()
    #     sql.close()
    #     for result in allPhoto:
    #         Send(update, result[0])
    #     # for result in allPhoto:
    #     #     SendPhoto(update, result[0])
        

def getPhoto(update, bot):
    if(isDos(update)): return
    Send(update, '不要壓縮，傳檔案', True)

def getFile(update, bot):
    if(isDos(update)): return
    userID = update.message.from_user.id
    path = uploadAndGetPhoto(update.message.document.file_id)
    
    sql = sqlite3.connect("KaTsu.db") 
    cur = sql.cursor()
    command = "insert into Data values('{0}', '{1}')".format(imgName[userID], path)

    print(path)
    print(command)
    cur.execute(command)
    sql.commit()

    cur.close()
    sql.close()

    Send(update, "新增 {0}".format(imgName[userID]))
    del userStatus[userID]