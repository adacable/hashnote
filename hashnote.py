import cherrypy
import display
import json
def CORS(): 
  cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
  cherrypy.response.headers['Access-Control-Allow-Methods'] = "GET,PUT,POST,DELETE"
  cherrypy.response.headers['Access-Control-Allow-Headers'] = "Content-Type"
  #cherrypy.response.headers['Content-Type'] = "application/json; charset=utf-8"
  cherrypy.response.headers['Allow'] = "GET,PUT,POST,DELETE"

cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS) 
def size_text(num):
    return 16*(num**0.5)
class HelloWorld(object):
    def bookmarkletloader(self):
        return file("jquery.js").read() + file("bookmarklet.js").read()
    bookmarkletloader.exposed = True
    def savepage(self,note=False,url = ""):
        if note:
            display.write(note)
            return "sucess"
        else:
            print "error"
            return "error"
    savepage.exposed = True
    def partialhashtags(self,term=None,numberOfHashtags=3):
        hashtags = [i for i in display.display("").keys() if term in i]
        returnstring = "["
        for hashtag in hashtags:
            returnstring +='"%s",'%hashtag
        return returnstring[:-1] + "]"
    partialhashtags.exposed = True
    def notes(self,searchterm=None):
        if searchterm == None:
            searchterm = ""
            rawkey = None
        else:
            rawkey = searchterm
            searchterm = [str(i) for i in searchterm.split(",")]
        return json.dumps([display.displayify(i,"") for i in display.filterForHashtags(searchterm)])
    notes.exposed = True
    def commonhashtags(self,key=None,numberOfHashtags=3):
        if key == None:
            key = ""
        else:
            key = key.split(",")
        adict = display.display(key) 
        returnstring = "["
        for i in range(int(numberOfHashtags)):
            try:
                m = max(adict, key=adict.get)
                returnstring = returnstring + '"%s",'%(m)
                del adict[m]
            except ValueError:
                break
        returnstring = returnstring[:-1]
        return returnstring + "]"
    commonhashtags.exposed = True
    def index(self,key= None):
        returnstring = """
            <html>
            <head>
            <script>""" + file('jquery.js').read() + """</script>
            <style>
            """ + file('style.css').read() + """
            </style>
            </head>
            <body>
            """
        if key == None:
            key = ""
            rawkey = None
        else:
            rawkey = key
            key = [str(i) for i in key.split(",")]
            returnstring += "<a class=homelink href='/' >home</a>"
        tagsdict = display.display(key)
        returnstring += "<nav class=keys>"
        for dictkey in tagsdict.keys():
            returnstring += "<a class=scale href='?key=%s' style='font-size:%s px' >%s</a>"%(dictkey,size_text(tagsdict[dictkey]),str(dictkey))
        returnstring += "</nav ><div class=notes>"
        for note in display.filterForHashtags(key):
            returnstring += "<article class=note>%s</article>"%(display.displayify(note,rawkey))
        returnstring += """
            </body>
            </html>
            """
        return returnstring
    index.exposed = True
    def bookmarklet(self):
        return file("loadthis.html").read()
    bookmarklet.exposed = True
    def bookmarkletstyle(self):
        return file("bookmarkletstyle.css").read()
    bookmarkletstyle.exposed = True
cherrypy.quickstart(HelloWorld())
