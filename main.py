from boom import *
from pirate import connect
import subprocess, time, sys, re, pyperclip
from subtitles import execute

srch = sys.argv[1]
opt = sys.argv[2]

p = subprocess.Popen('protonvpn-cli c -f', stdout=subprocess.PIPE, shell=True)
print(p.communicate())

time.sleep(2)
xtor = search(srch)
mag = magnet(xtor[1])
title = xtor[0]

ptor = connect(srch)
if ptor:
    print('selected torrent from piratebay\n')
    mag = ptor[1]
    title = ptor[0]

pyperclip.copy(mag)

print(title+'\n')

input('Proceed to find subtitles? ')
filters = re.split('\.| |_|-', title)
query = len(srch.split(' '))
query -= 1
while query!=-1:
    filters.pop(query)
    query-=1

filters = list(filter(None, filters))

print(filters)

removeIndex = input('remove any??: ')

for i in removeIndex:
    filters.remove(i)

print(filters)

execute(srch, opt, filters)

p = subprocess.Popen('protonvpn-cli d', stdout=subprocess.PIPE, shell=True)
print(p.communicate)
time.sleep(2)

# time.sleep(3)
# t = subprocess.Popen('transmission-gtk '+'"'+mag+'"', stdout=subprocess.PIPE, shell=True)
# print(t.communicate)
