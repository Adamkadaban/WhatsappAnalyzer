myName="ExampleName" #Your first name (or however your name is stored in your contacts)
fileName="example.txt" #The name of your file should preferably be the first name of their contact


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import math
import os
from emoji import UNICODE_EMOJI
from matplotlib.font_manager import FontProperties
import datetime


Name=fileName[:-4]
def timeKey(t):
    d={'5 AM':0, '6 AM':1, '7 AM':2, '8 AM':3, '9 AM':4, '10 AM':5, '11 AM':6, '12 PM':7, '1 PM':8, '2 PM':9, '3 PM':10, '4 PM':11, '5 PM':12, '6 PM':13, '7 PM':14, '8 PM':15, '9 PM':16, '10 PM':17, '11 PM':18, '12 AM':19, '1 AM':20, '2 AM':21, '3 AM':22, '4 AM':23}
    return d[t]
def convertTime(t):
    time=t.split()[0]
    type=t.split()[1]
    hours=time.split(":")[0]
    minutes=time.split(":")[1]
    return int(hours), int(minutes), type
def timeAnalyzer(m):
    r={}
    for i in m:
        hs, mins, tp=convertTime(i[0][1])
        time=str(hs)+" "+tp
        if time not in r:
            r[time]=1
        else:
            r[time]+=1
    # plt.xticks(np.arange(24), ('5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM', '12 AM', '1 AM', '2 AM', '3 AM', '4 AM'))
    r=sortDictTimes(r)
    times=list(r.keys())
    frequencies=list(r.values())
    plt.bar(times, frequencies)
    plt.xlabel("Time of day")
    plt.ylabel("Number of messages")
    plt.title("Frequency of messages at different times with "+Name)
    plt.show()

def getDeleted(m):
    youDeleted = 0
    theyDeleted = 0
    for i in range(len(m)):
        try:
            mX = m[i][1][1]
            if mX == "You deleted this message":
                youDeleted += 1
            if mX == "This message was deleted":
                theyDeleted += 1
        except:
            pass
    return youDeleted, theyDeleted
def countWord(m, word):
    c=0
    for i in m:
        ms = i[1][1].lower()
        ps = i[1][0]
        if myName in ps:
            c+=ms.count(word)
            if word in ms:
                print(ms)
    return c
def wordFrequency(m):
    r={}
    for i in m:
        ms=i[1][1]
        ps=i[1][0]
        if Name in ps:
            words=ms.split(" ")
            for j in words:
                if j not in r:
                    r[j]=1
                else:
                    r[j]=r[j]+1
    if " " in r:
        r[" "]=0
    r=sortDict(r)
    words=list(r.keys())[:20]
    nums=list(r.values())[:20]
    plt.bar(words, nums)
    plt.xlabel("Word")
    plt.ylabel("Number of times used")
    plt.title("Most frequently used words by "+Name)
    plt.show()

def countMessages(m):
    Me = 0
    Them = 0
    for i in messages:
        if Name in i[1][0]:
            Them += 1
        if myName in i[1][0]:
            Me += 1

    return Me, Them
def sortDict(r):
    r=sorted(r.items(), key=lambda x: x[1], reverse=True)
    newR={}
    for i in r:
        newR[i[0]]=i[1]
    return newR
def sortDictTimes(r):
    r=sorted(r.items(), key=lambda x: timeKey(x[0]))
    newR={}
    for i in r:
        newR[i[0]]=i[1]
    return newR

def is_emoji(s):
    return s in UNICODE_EMOJI

def drawEmojiFrequency(m):
    r={}
    for i in m:
        mes=i[1][1]
        for j in mes:
            if is_emoji(j):
                if j not in r:
                    r[j]=1
                else:
                    r[j]=r[j]+1
    r=sortDict(r)
    emojis=list(r.keys())[:10]
    frequencies=list(r.values())[:10]
    # print(emojis)
    # print(frequencies)
    plt.bar(emojis, frequencies)
    # plt.xticks(font="Arial")
    plt.xlabel("Emoji")
    plt.ylabel("Number times used")
    plt.title("Frequency of emojis used with "+Name)
    plt.show()
def dateToNum(a):
    x=a.split("/")
    tot=0
    tot+=int(x[2])*365
    tot+=int(x[0])*30
    tot+=int(x[1])
    return tot
def drawDates(a):
    vals=analyzeDates(a)
    datesV=list(vals.keys())
    datesV=[matplotlib.dates.datestr2num(i) for i in datesV]
    # datesV=[matplotlib.dates.num2timedelta(dateToNum(i)) for i in datesV]
    frequencies=list(vals.values())
    plt.plot_date(datesV, frequencies, "-", color="#3285a8")
    plt.title(("Frequency of messages with "+Name))
    plt.xlabel("Date")
    plt.ylabel("Frequency of Messages")
    # slope, b = np.polyfit(datesV, frequencies, 1)
    # plt.plot(np.unique(datesV), np.poly1d(np.polyfit(datesV, frequencies, 1))(np.unique(datesV)), color="red")
    plt.show()


# def analyzeDates(m):
#     dates=[i[0][0] for i in m]
#     dateVals=[dateToNum(i) for i in dates]
#     small= min([i for i in dateVals if i!=0])
#     dateVals=[i-small for i in dateVals]
#     r={}
def analyzeDates(m):
    # dates=[i[0][0] for i in m]
    r={}
    for i in m:
        date=i[0][0]
        if date not in r:
            r[date]=1
        else:
            r[date]=r[date]+1
    return r
def fixMessages(m):
    r=[i for i in m if i.split(" - ", 1)[0].count("/")==2]
    r=[i for i in r if len(i)>1]
    return r

fin = open(fileName, encoding='utf-8')
messages=[]
for i in fin:
    stuffything=i.split(" - ", 1)[0]
    if stuffything.count("/")==2 and stuffything.count(":")==1 and stuffything.count("//")==0:
        messages.append(i.rstrip())
    else:
        messages[-1]=messages[-1]+" "+i.rstrip()

fin.close()

messages=[i.rstrip() for i in messages]
messages=fixMessages(messages)



#Split messages into [date/time, message]
for i in range(len(messages)):
    messages[i]=messages[i].split(" - ", 1)

#split into [date, time[
for i in range(len(messages)):
    messages[i][0]=messages[i][0].split(", ")

#split into [sender, message]
#Lol ill fix it later
for i in range(len(messages)):
    try:
        messages[i][1]=messages[i][1].split(": ", 1)
    except:
        pass

# c=0
# for i in messages:
#     if len(i)<2:
#         print(i)

# for i in range(100):
#     print(messages[i])

# messages=[i for i in messages if i[1][1]!="<Media omitted>"]


newM=[]
for i in range(len(messages)):
    try:
        mX=messages[i][1][1]
        if mX!="<Media omitted>" and mX!="You deleted this message" and mX!="This message was deleted":
            newM.append(messages[i])
    except:
        pass
messages=newM


# print(analyzeDates(messages[]))
# print(messages)


#Start options:


drawDates(messages)
drawEmojiFrequency(messages)
wordFrequency(messages)
timeAnalyzer(messages)

