# -*- coding: utf-8 -*-
import json

with open('MyActivity.json','r',encoding="utf8") as myfile:
        data=myfile.read()
#with open('MyActivity2.json','r',encoding="utf8") as myfile2:
        data=myfile.read()
obj = json.loads(data)
#obj2 = json.loads(data2)
raw = json.loads(data)
watchedObj = []
songObj = []
url = {}


terms = open("Filter.txt",'r',encoding="utf8")
filters = terms.read().splitlines()
terms.close()
good = open("gFilters.txt",'r',encoding='utf8')
clear = good.read().splitlines()
#remove useless data
for i in obj:
    if 'subtitles' in dict.keys(i):
        channel = i['subtitles'][0]['name']
        dict.pop(i, 'subtitles')
        i['channel'] = channel
    if 'activityControls' in dict.keys(i):
        dict.pop(i, 'activityControls')
    if 'products' in dict.keys(i):
        dict.pop(i, 'products')
    if 'header' in dict.keys(i):
        dict.pop(i, 'header')
    #only keep watched
    if i['title'][:7] == 'Watched':
        tempTitle = i['title'][8:]
        i['title'] = tempTitle
        watchedObj.append(i)
watchedObj.reverse()
for i in watchedObj:
    skip = False
    for f in filters: #filter out
        if i['title'].find(f) != -1:
            skip = True
            break
        if 'channel' in dict.keys(i):
            if i['channel'].find(f) != -1:
                skip = True
                break
    if skip:
        continue
    if i['title'] in dict.keys(url):
        continue
    if 'channel' in dict.keys(i):
        channel = i['channel']
        index = channel.find(' - ')
        if index != -1:
            i['channel'] = i['channel'][:index]
            songObj.append(i)
            url[i['title']] = i['titleUrl']
            continue
    title = i['title'] 
    index = title.find(' - ')
    if index < -1:
        i['channel'] = i['title'][0:index]
        i['title'] = i['title'][index+3:]
        songObj.append(i)
        url[i['title']] = i['titleUrl']
        continue
    for f in clear:
        if 'channel' in dict.keys(i):
            if i['channel'].find(f) != -1:
                songObj.append(i)
                url[i['title']] = i['titleUrl']
                break
f = open("Songs.csv", "w",encoding="utf8")
f.write('Name,Artist,Discovery Date,Genre,Link\n')
f.close()
f = open("Songs.csv", "a",encoding="utf8")
for i in songObj:
    i['title'] = i['title'].replace(",",'')
    i['time'] = i['time'][5:7]+'/'+i['time'][8:10]+'/'+i['time'][0:4] #time
    row = i['title'] + ',' +i['channel'] +','+i['time']+','+''+','+i['titleUrl']+'\n'
    f.write(row)
f.close()