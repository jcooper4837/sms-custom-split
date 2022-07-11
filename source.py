#sms-custom-split
#split timer with reorderable splits on the fly

import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import cv2
import math
import time as clock
from datetime import timedelta

def toScore(x):
    times = list(())
    times.append(x[:1])
    times.append(x[2:4])
    times.append(x[5:7])
    times.append(x[8:])
    mils = int(times[3])
    secs = int(times[2]) * 1000
    mins = int(times[1]) * 60000
    hrs = int(times[0]) * 3600000
    return mils + secs + mins + hrs

def toTime(x):
    x = abs(x)
    mil2 = str(math.floor(x % 1000))
    sec2 = str(math.floor(x / 1000 % 60))
    min2 = str(math.floor(x / (1000 * 60) % 60))
    hr2 = str(math.floor(x / (1000 * 3600)))
    while len(mil2) < 3:
        mil2 = "0" + mil2
    while len(sec2) < 2:
        sec2 = "0" + sec2
    while len(min2) < 2:
        min2 = "0" + min2
    return hr2 + ":" + min2 + ":" + sec2 + "." + mil2

def totalizer(x, s):
    x_score = list(())
    for i in range(s):
        x_score.append(toScore(x[i]))
    total = 0
    for i in range(s):
        total = total + x_score[i]
    return toTime(total)

def getCat(cat):
    if cat == "any" or cat == "79":
        return cat
    if cat == "0":
        cat = "any"
    elif cat == "1":
        cat = "79"
    else:
        cat = "any"
    return cat

def getTrack(track,lvl,used):
    if len(track) < 1:
        return -1
    if track[0] == "1":
        track = "bh" + track[1:]
    if track[0] == "2":
        track = "rh" + track[1:]
    if track[0] == "3":
        track = "gb" + track[1:]
    if track[0] == "4":
        track = "pp" + track[1:]
    if track[0] == "5":
        track = "sb" + track[1:]
    if track[0] == "6":
        track = "nb" + track[1:]
    if track[0] == "7":
        track = "pv" + track[1:]
    if track in lvl:
        return lvl.index(track)
    if track == "lvl":
        print("[ ",end="")
        for i in range(len(lvl)):
            if used[i] == 0:
                print(lvl[i]+", ",end="")
        print("]")
    return -1

def reset():
    out = open("output.txt", "w")
    string = " PB:  "+pb_total
    string = string+"\n+/-:    "+pb_sign+str(toTime(pb_delta)[3:])
    string = string+"\nSOB:  "+sob_total
    string = string+"\n WR:  "+wr_total
    string = string+"\n+/-:    "+wr_sign+str(toTime(wr_delta)[3:])
    string = string+"\n\nTIME  "+str(toTime(live_total))
    string = string+"\nLEVEL "+str(current+1)
    print(string)
    out.write(string)
    out.close()

cat = input("category: ")
cat = getCat(cat) + ".txt"
print(cat)
f = open(cat, "r")
size = eval(f.readline())
pb, sob, wr, live, used = list(()), list(()), list(()), list(()), list(())
for i in range(size):
    pb.append(f.readline())
f.readline()
for i in range(size):
    sob.append(f.readline())
f.readline()
for i in range(size):
    wr.append(f.readline())
for i in range(size):
    pb[i] = pb[i][:len(pb[i])-1]
    sob[i] = sob[i][:len(sob[i])-1]
    wr[i] = wr[i][:len(wr[i])-1]
    live.append("0:00:00.000")
    used.append(0)

catlvl = cat[:len(cat)-4] + "lvl.txt"
f2 = open(catlvl, "r")
size = eval(f2.readline())
lvl = list(())
for i in range(size):
    lvl.append(f2.readline())
for i in range(size):
    lvl[i] = lvl[i][:len(lvl[i])-1]

pb_total = totalizer(pb, size)
sob_total = totalizer(sob, size)
wr_total = totalizer(wr, size)
print(pb_total, sob_total, wr_total)
current = 0
track = 0
live_total = 0
pb_delta = 0
wr_delta = 0
pb_sign = "+"
wr_sign = "+"
update = False
confirm = "-"
mkw2 = ""
icon = '\u25b5'
esc = 0
rand = input("rand: ")
if len(rand) == 0:
    rand = True
else:
    rand = False
input("Enter to Start Timer: ")
start_time = clock.time()
split_time = round((clock.time() - start_time),3)
prev_time = split_time
print(start_time)
print(round((clock.time()-start_time),3))

reset()

while current < size:
    current = current + 1
    while len(confirm) > 0:
        if rand:
            track = -1
            while track == -1 or track > size - 1 or used[track] == 1:
                track = input("track: ")
                track = getTrack(track,lvl,used)
                if current == size:
                    track = size-1
        else:
            track = current - 1
        print(lvl[track])
        split = input("split: ")
        old_time = prev_time
        prev_time = split_time
        split_time = round((clock.time() - start_time),3)
        delta_time = round(split_time - prev_time,3)
        print(split_time, delta_time)
        if split == "c":
            esc = 1
            break
        elif split == "r":
            esc = 2
            current = 0
            live_total = 0
            pb_delta = 0
            wr_delta = 0
            input("Enter to Start Timer: ")
            start_time = clock.time()
            split_time = round((clock.time() - start_time),3)
            prev_time = split_time
            print(start_time)
            print(round((clock.time()-start_time),3))
            reset()
            break

        time = str(timedelta(seconds=delta_time))
        time = time[:len(time)-3]
        print(time)
        if len(time) != 11:
            confirm = "fail"
        else:
            confirm = input("confirm: ")
        if len(confirm) > 0:
            split_time = prev_time
            prev_time = old_time
    if esc > 0:
        if esc == 1:
            break
        elif esc == 2:
            esc = 0
            continue
    confirm = "-"
    used[track] = 1

    live[track] = time
    pb_split = toScore(time) - toScore(pb[track])
    wr_split = toScore(time) - toScore(wr[track])
    pb_delta = pb_delta + pb_split
    wr_delta = wr_delta + wr_split
    if toScore(time) < toScore(sob[track]) and (not rand or current > 1):
        print("gold!")
        sob[track] = time
        sob_total = totalizer(sob, size)
    print(pb[track])
    print(lvl[track])
        
    live_total = live_total + toScore(time)

    if pb_delta < 0:
        pb_sign = "-"
    else:
        pb_sign = "+"
    if wr_delta < 0:
        wr_sign = "-"
    else:
        wr_sign = "+"
        
    out = open("output.txt", "w")
    string = " PB:  "+pb_total
    string = string+"\n+/-:    "+pb_sign+str(toTime(pb_delta)[3:])
    string = string+"\nSOB:  "+sob_total
    string = string+"\n WR:  "+wr_total
    string = string+"\n+/-:    "+wr_sign+str(toTime(wr_delta)[3:])
    string = string+"\n\nTIME  "+str(toTime(live_total))
    string = string+"\nLEVEL "+str(current+1)
    print(string)
    out.write(string)
    out.close()

live_total = totalizer(live, size)
print(live_total)
out2 = open("finish.txt", "w")
out2.write(str(size))
out2.write("\n")
for i in range(size):
    out2.write(live[i])
    out2.write("\n")
out2.write("sob\n")
for i in range(size):
    out2.write(sob[i])
    out2.write("\n")
out2.write("wr\n")
for i in range(size):
    out2.write(wr[i])
    out2.write("\n")
out2.write("0")
out2.close()

