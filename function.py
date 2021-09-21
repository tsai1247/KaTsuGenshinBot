import sqlite3
from telegram import ForceReply

def exe(command, value=None, commit = False):
        con = sqlite3.connect("KaTsu.db")
        cur = con.cursor()
        print(command)
        try:
        
            if(value==None):
                cur.execute(command)
            else:
                cur.execute(command, value)

        
            ret = cur.fetchall()
            if(commit):
                con.commit()
        except:
            if(commit):
                return False
            else:
                return None
        finally:
            cur.close()
            con.close()

        if(commit):
            return True
        else:
            return ret

def Send(update, msg, force = False):
    if(force):
        update.message.reply_text(msg, reply_markup = ForceReply(selective=force))
    else:
        update.message.reply_text(msg)
        

def SendPhoto(update, photolink):
    update.message.reply_photo(photolink)


def count1(update, nums, start):
    rets = [0, 0, 0]
    for cur in range(len(nums)):
        if(nums[cur] < start[cur]):
            return
    i = 0
    for num in nums:
        while(num!=start[i]):
            if(num==2):
                rets[0]+=6
            elif(num==3):
                rets[1]+=3
            elif(num==4):
                rets[1]+=4
            elif(num==5):
                rets[1]+=6
            elif(num==6):
                rets[1]+=9
            elif(num==7):
                rets[2]+=4
            elif(num==8):
                rets[2]+=6
            elif(num==9):
                rets[2]+=9
            elif(num==10):
                rets[2]+=12
            num-=1
        i+=1
    Send(update, "怪物素材需要：\n白色 {0}\n綠色 {1}\n藍色 {2}\n".format(rets[0],rets[1],rets[2]))


    rets = [0, 0, 0]
    i = 0
    for num in nums:
        while(num!=start[i]):
            if(num==2):
                rets[0]+=3
            elif(num==3):
                rets[1]+=2
            elif(num==4):
                rets[1]+=4
            elif(num==5):
                rets[1]+=6
            elif(num==6):
                rets[1]+=9
            elif(num==7):
                rets[2]+=4
            elif(num==8):
                rets[2]+=6
            elif(num==9):
                rets[2]+=12
            elif(num==10):
                rets[2]+=16
            num-=1
        i+=1
    Send(update, "天賦書需要：\n綠色 {0}\n藍色 {1}\n紫色 {2}\n".format(rets[0],rets[1],rets[2]))

def GetConfig(name: str):
    sql = sqlite3.connect('KaTsu.db')
    cur = sql.cursor()
    cur.execute("select Val from Config where Name = '{0}'".format(name))
    data = cur.fetchone()
    if(data == None or len(data)==0 ):  # init
        initVal = 20
        cur.close()
        cur = sql.cursor()
        cur.execute("insert into Config values('{0}', {1})".format(name, initVal))
        sql.commit()
        data = initVal
    else:
        data = data[0]
    cur.close()
    sql.close()

    return data