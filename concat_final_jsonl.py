import json
import jsonlines
import pandas as pd


def textifynum(basenum, chartotal):
    bsnum = str(basenum)
    while len(bsnum) < chartotal:
        bsnum = "0" + bsnum
    return bsnum

def blogchckOS(url):
    checker = url[:15]
    #print(checker)
    if checker == "https://bits.de":
        return ("debian", "de")
    elif checker == "https://communi":
        return ('Fedora', 'fe')
    elif checker == "https://news.op":
        return ('openSUSE', 'su')
    elif checker == "https://blog.li":
        return ('linuxmint', 'lm')
    elif checker == "https://forum.m":
        return ('ManjaroLinux', 'mj')
    elif checker == "https://www.red":
        return ('redhat', 'rh')
    elif checker == "https://ubuntu.":
        return ('Ubuntu', 'ub')
    elif checker == "":
        return ('pop_os', 'po')
    else:
        return ('NO','NOTHING')

shortos = ['de', 'fe', 'su', 'lm', 'mj', 'rh', 'ub', 'po']

# for my manual work with the Reddit API and RSS feeds I liked the formatted Json files
# After reading on Scrapy I understand why json lines are much easier to parse / feed as we can read 1 line at a time

#Grab the Wiki Json files
with open('WebFocusedCrawlWorkV001/wikiitems.json') as wiki_json_file:
    wikijson = json.load(wiki_json_file)

#Grab BlogNews WebCrawl
with open('WebFocusedCrawlWorkV001/blognewsitems.json') as blognews_json_file:
    newsjson = json.load(blognews_json_file)

#Grab Rss suplement to newsjson
with open('RSSparser/rssfeeds.json') as rss_json_file:
    rssjson = json.load(rss_json_file)

# Grab Reddit Social Media Posts
with open('RedditAPI/redditHot150.json') as reddit_json_file:
    redditjson = json.load(reddit_json_file)


print("--------------------------------------------------------------------")
print("----------           High Level Document Totals          -----------")
print("--------------------------------------------------------------------")

print("Wiki pages Total Documents: " + str(len(wikijson)))
print("NewsBlog Sites Total Documents: " + str(len(newsjson)))
print("RSS news suplement Total Documents: " + str(len(rssjson)))
print("Reddit Total Documents: " + str(len(redditjson)))


"""
# End Structure Look
    id:
       1st char: r - Reddit, w - wikipdedia, b - blog,
       2nd: -
       3rd & 4th char: de - debian, fe - 'Fedora' su - 'openSUSE', lm - 'linuxmint', mj - 'ManjaroLinux', rh - 'redhat', ub - 'Ubuntu', po - 'pop_os'
       5th running 4 digit number

"""
opus_dict = []

UniqueID = 0

#//////////////////WIKIPEDIA//////////////////////////////
for doc in wikijson:
    tempdict = {
        "ID": "",
        "URL": "",
        "TITLE": "",
        "BODY": "",
        "os": "",
        "tags" : [],
        }
    UniqueID = UniqueID + 1
    IDnum = textifynum(UniqueID, 4)

    if doc["tags"][2]=="ubuntu":
        tempdict["os"]='Ubuntu'
        tempdict["ID"]='w-ub' + IDnum
    elif doc["tags"][2]=="opensuse":
        tempdict["os"]='openSUSE'
        tempdict["ID"]='w-su' + IDnum
    elif doc["tags"][2]=="red":
        tempdict["os"]='redhat'
        tempdict["ID"]='w-rh' + IDnum
    elif doc["tags"][2]=="manjaro":
        tempdict["os"]='ManjaroLinux'
        tempdict["ID"]='w-mj' + IDnum
    elif doc["tags"][2]=="linux":
        tempdict["os"]='linuxmint'
        tempdict["ID"]='w-lm' + IDnum
    elif doc["tags"][2]=="pop":
        tempdict["os"]='pop_os'
        tempdict["ID"]='w-po' + IDnum
    elif doc["tags"][2]=="fedora":
        tempdict["os"]='Fedora'
        tempdict["ID"]='w-fe' + IDnum
    elif doc["tags"][2]=="debian":
        tempdict["os"]='debian'
        tempdict["ID"]='w-de' + IDnum
    tempdict["URL"] = doc["url"]
    tempdict["TITLE"] = doc["title"]
    tempdict["BODY"] = doc["text"]
    tempdict["tags"] = doc["tags"]

    opus_dict.append(tempdict.copy())


#//////////////////////////////////////NewsBlogs///////////////////////////////
for doc in newsjson:
    tempdict = {
        "ID": "",
        "URL": "",
        "TITLE": "",
        "BODY": "",
        "os": "",
        "tags" : [],
        }
    UniqueID = UniqueID + 1
    IDnum = textifynum(UniqueID, 4)
    OStup = blogchckOS(doc["url"])
    tempdict["os"]=OStup[0]
    tempdict["ID"]='b-'+ OStup[1] + IDnum
    tempdict["URL"] = doc["url"]
    tempdict["TITLE"] = doc["title"]
    tempdict["BODY"] = doc["text"]
    tempdict["tags"] = doc["tags"]

    opus_dict.append(tempdict.copy())

#//////////////////////////////////////RSS Feeds Blog Suplement///////////////////////////////
for doc in rssjson:
    tempdict = {
        "ID": "",
        "URL": "",
        "TITLE": "",
        "BODY": "",
        "os": "",
        "tags" : [],
        }
    UniqueID = UniqueID + 1
    IDnum = textifynum(UniqueID, 4)
    OStup = blogchckOS(doc["url"])
    tempdict["os"]=OStup[0]
    tempdict["ID"]='b-'+ OStup[1] + IDnum
    tempdict["URL"] = doc["url"]
    tempdict["TITLE"] = doc["title"]
    tempdict["BODY"] = doc["text"]
    tempdict["tags"] = doc["tags"]

    opus_dict.append(tempdict.copy())


#//////////////////////////////////////Reddit///////////////////////////////
for doc in redditjson:
    tempdict = {
        "ID": "",
        "URL": "",
        "TITLE": "",
        "BODY": "",
        "os": "",
        "tags" : [],
        }
    UniqueID = UniqueID + 1
    IDnum = textifynum(UniqueID, 4)
    OStup = blogchckOS(doc["url"])
    tempdict["os"]=doc["os"]
    if doc["os"][:2].lower() in shortos:
        tempdict["ID"]='r-'+ doc["os"][:2].lower() + IDnum
    elif doc["os"][:2] == 'op':
        tempdict["ID"]='r-'+ 'su' + IDnum
    elif doc["os"][:2] == 'li':
        tempdict["ID"]='r-'+ 'lm' + IDnum
    elif doc["os"][:2] == 'Ma':
        tempdict["ID"]='r-'+ 'mj' + IDnum
    elif doc["os"][:2] == 're':
        tempdict["ID"]='r-'+ 'rh' + IDnum
    else:
        tempdict["ID"]='r-'+ 'UNKNOWN' + IDnum

    tempdict["URL"] = doc["url"]
    tempdict["TITLE"] = doc["title"]
    tempdict["BODY"] = doc["text"]
    tempdict["tags"] = ["redditpost"]

    opus_dict.append(tempdict.copy())


#Write out to the opus.jl file
with open('opus.jl', "w", encoding='utf-8') as opus_file:
    for line in opus_dict:
        json_record = json.dumps(line, ensure_ascii=False)
        opus_file.write(json_record + '\n')




# Reddit Struct
"""
        "id": "redditq4qfch",
        "os": "debian",
        "url": "https://www.reddit.com/r/debian/comments/q4qfch/",
        "title": "Debian -- News -- Updated Debian 11: 11.1 released",
        "text": " Sorry for going meta, and I know votes don't really mean anything, but I'm curious. To the people who upvoted, why ignore my earlier post to the archive of the official announcement email, and then upvote this later post to the reposted announcement on the website? Dang it... I was really hoping for libsane to get fixed within this timeframe, oh well... This post was higher in the feed, it's mostly random. Don't take it seriously Why do you think people who upvoted this could be read your question? If you want to understand reddit you must understand how reddit works first. A lot of users don't read anything but title. Bug number? I'm curious, what's the current issue with it right now?"
# Rss Struct
        "os": "manjaro",
        "url": "https://forum.manjaro.org/t/stable-update-2021-10-08-kernels-mesa-browsers-python-ukui-php-thunderbird-pipewire/85608",
        "title": "[Stable Update] 2021-10-08 - Kernels, Mesa, Browsers, Python, UKUI, PHP, Thunderbird, Pipewire",
        "text": "Hello community,\nAnother stable branch update with some usual updates for you.\n\nimage980\u00d7438 49.7 KB\n\nDon\u2019t miss out on our new merch!\n\nWe updated our Kernels. Note that 5.13 series is marked EOL and 5.12 got removed!\nMesa is now at 21.2.3\n\n\nPipewire got renewed to 0.3.38\n\nWe updated browsers like Vivaldi, Brave and Firefox\n\n\nThunderbird is now at 91.1.2\n\nOther regular upstream updates including Python\n\n\nGet our latest daily developer images now from Github: Plasma, Gnome, XFCE. You get the latest stable releases of Manjaro from CDN77.\n\nOur current supported kernels\n\nlinux44 4.4.284\nlinux49 4.9.283\nlinux414 4.14.248\nlinux419 4.19.208\nlinux54 5.4.150\nlinux510 5.10.70\nlinux513 5.13.19 [EOL]\nlinux514 5.14.10\nlinux515 5.15-rc3\nlinux510-rt 5.10.52_rt47\n\nPackage Updates (Tue Oct 5 09:21:03 CEST 2021)\n\nstable community x86_64:  614 new and 605 removed package(s)\nstable core x86_64:  26 new and 26 removed package(s)\nstable extra x86_64:  373 new and 520 removed package(s)\nstable kde-unstable x86_64:  311 new and 308 removed package(s)\nstable multilib x86_64:  20 new and 19 removed package(s)\n\nA detailed list of all package changes can be found here.\n\n\n\n\nNo issue, everything went smoothly\nYes there was an issue. I was able to resolve it myself.(Please post your solution)\nYes i am currently experiencing an issue due to the update. (Please post about it)\n\n\n\n\n0\nvoters\n\n\n\n\nBefore trying to upgrade, please check if your mirror has already synced:\n\n\nMirror-Check Service\n\n\n\nMy mirror(s) is (are) not yet updated\nPlease note that mirrors are not under the control of the Manjaro team and your first port of call when having mirror problems is to try to update your mirrors  then try pamac upgrade again.\n\n\nThe quick solution:\nsudo pacman-mirrors --geoip &amp;&amp; sudo pacman -Syyu\n\n\n\nThe long-term solution:\n\n\nCheck the mirrors for your country and the closest neighbouring country\n\n\nExecute:\nsudo pacman-mirrors --country YourCountry,NeighbouringCountry --interactive\n\n\n\nIn the list of presented mirrors, select the green mirrors that are fastest with \u2191 and \u2193 on your keyboard and space to select them\n\n\nTab to the OK button\n\n\nPress Enter\n\n\nExecute:\nsudo pacman -Syyu\npamac upgrade\n\n\n\nCheck again for no errors, hit Y Enter\n\n\n \n\n\n\n\n\n            28 posts - 12 participants\n            Read full topic",
        "tags": [
            "Fri, 08 Oct 2021 09:57:11 +0000",
            "Stable Updates"
        ]
#Wiki Sample struct
    {"url": "https://en.wikipedia.org/wiki/Debian",
    "title": "Debian",
    "text": "Linux distribution based on free and open-source s Authority File (Germany)National librariesFrance(data)United States\n\nRetrieved from \"https://en.wikipedia.org/w/index.php?title=Debian&oldid=1045180123\"", "tags": ["en.wikipedia.org", "wiki", "debian"]}
#BlogNews Struct
    {"url": "https://www.redhat.com/en/blog/extending-automation-across-organization-how-we-can-create-new-culture-automation-legacy-it-siloes",
    "title": "Extending automation across the organization: How we can create a new culture of automation from legacy IT siloes",
    "text": "\n        Automation is about empowering people to do initiative.\n\n    ",
    "tags": ["Wed, 29 Sep 2021 13:00:01 GMT", "Tags:", "Automation", ", ", "Cloud management"]},


"""

# Lets get some general info about our dictionary:
opusdf = pd.DataFrame.from_dict(opus_dict)
opusdf['SourceType'] = opusdf['ID'].str[:1]
opusdf['OrigWordCount'] = opusdf['BODY'].str.split().apply(len)

print("--------------------------------------------------------------------")
print("----------    Summary Statistics before Data Cleaning    -----------")
print("--------------------------------------------------------------------")

print(opusdf.groupby(['os','SourceType']).agg({'OrigWordCount': ['count','median','mean','min','max']}))
print("")
print("--------------------------------------------------------------------")
print("----------           Sample of the Parsed Data           -----------")
print("--------------------------------------------------------------------")
print(opusdf.sample(10))
