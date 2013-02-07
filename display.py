import re
def display(hashtagsin):
    inlines  = filterForHashtags(hashtagsin)
    hashtagsdict = dict()
    for line in inlines:
        for hashtag in hashtags(line):
            if hashtag in hashtagsdict.keys():
                hashtagsdict[hashtag] += 1
            else:
                hashtagsdict[hashtag] = 1
    return hashtagsdict
def hashtags(stringin):
    return re.findall("#(\w+)",stringin)
def filterForHashtags(hashtagsin):
    infile = open("out.txt")
    stringlist = infile.readlines()
    for hashtagin in hashtagsin:
        stringlist =  [i for i in stringlist if hashtagin in hashtags(i)]
    return stringlist 
def replHashTag(matchObject):
    if currenta == "None":
        return "<a href=?key=%s>%s</a>"%(matchObject.group()[1:],matchObject.group())
    else:
        if matchObject.group()[1:] in currenta:
            return "<a target='_blank' href=/?key=%s>%s</a>"%(matchObject.group()[1:],matchObject.group())
        else:
            return "<a target='_blank' class=straight href=/?key=%s>%s</a><a class=plus href=/?key=%s,%s>+</a>"%(matchObject.group()[1:],matchObject.group(),matchObject.group()[1:],currenta)
def replLink(matchObject):
    return "<a target='_blank' class=external href=%s>%s</a>"%(matchObject.group(),matchObject.group()[:20])
def displayify(stringin,current):
    global currenta
    currenta = str(current)
    return re.sub("http://(\S+)",replLink,re.sub("#(\w+)",replHashTag,stringin))
def write(note):
    open("out.txt","a").write(note + "\n")
