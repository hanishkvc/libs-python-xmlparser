#!/usr/bin/env python3

import sys


class XMLParser():
    TAGSTARTMARKERAGAIN = "TagStartMarkerAgain"
    TAGENDMARKERALONE = "TagEndMarkerAlone"
    sFile = None
    hFile = None
    handler = None
    def __init__(self):
        self.sFile = None
        self.hFile = None
        self.handler = None

    def open(self, sFile):
        self.hFile = open(sFile)

    def parse(self, handler):
        bTagMarkerStart = False
        bTagTypeStart = True
        iTagMarkerOffset = 0
        sCurTag = None
        for l in self.hFile:
            for c in l:
                if c == '<':
                    if bTagMarkerStart:
                        handler.error(l, self.TAGSTARTMARKERAGAIN)
                    else:
                        bTagMarkerStart = True
                        bTagTypeStart = True
                        iTagMarkerOffset = 0
                        sCurTag = ""
                elif c == '>':
                    if bTagMarkerStart:
                        if bTagTypeStart:
                            handler.tag_start(l, sCurTag)
                        else:
                            handler.tag_end(l, sCurTag)
                        bTagMarkerStart = False
                    else:
                        handler.error(l, self.TAGENDMARKERALONE)
                elif c == '/':
                    if bTagMarkerStart:
                        bTagTypeStart = False
                else:
                    if bTagMarkerStart:
                        sCurTag += c


    def reset(self):
        hFile.seek(0)

class XMLParserHandler:
    def error(self, sLine, errType):
        print(errType)

    def tag_start(self, sLine, sTag):
        print("<{}>".format(sTag))

    def tag_end(self, sLine, sTag):
        print("</{}>".format(sTag))


myParser = XMLParser()
myHandler = XMLParserHandler()
myParser.open(sys.argv[1])
myParser.parse(myHandler)



