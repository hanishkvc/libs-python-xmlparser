#!/usr/bin/env python3

import sys


class XMLParser():
    TAGSTARTMARKERAGAIN = "TagStartMarkerAgain"
    TAGENDMARKERALONE = "TagEndMarkerAlone"
    sFile = None
    hFile = None
    handler = None
    iTagLvl = 0
    #iTagId = 0
    def __init__(self):
        self.sFile = None
        self.hFile = None
        self.handler = None

    def open(self, sFile):
        self.hFile = open(sFile)
        self.iTagLvl = 0

    def parse(self, handler):
        bTagMarkerStart = False
        bTagTypeStart = True
        iTagMarkerOffset = 0
        sCurTag = None
        sCurData = ""
        SELFCONTAINEDTAGSPECIALOFFSET=1000
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
                            handler.tag_start(l, sCurTag, self.iTagLvl)
                            self.iTagLvl += 1
                        if (not bTagTypeStart) or (iTagMarkerOffset == SELFCONTAINEDTAGSPECIALOFFSET):
                            self.iTagLvl -= 1
                            handler.tag_end(l, sCurTag, self.iTagLvl, sCurData)
                            sCurData = ""
                        bTagMarkerStart = False
                    else:
                        handler.error(l, self.TAGENDMARKERALONE)
                elif c == '/':
                    if bTagMarkerStart:
                        if (iTagMarkerOffset == 0):
                            #print("DBUG:parse:Found /")
                            bTagTypeStart = False
                        else:
                            iTagMarkerOffset = SELFCONTAINEDTAGSPECIALOFFSET
                elif c == ' ': # Need to check if this is required
                    if bTagMarkerStart:
                        if (iTagMarkerOffset == 0) or (iTagMarkerOffset == SELFCONTAINEDTAGSPECIALOFFSET):
                            pass
                        else:
                            sCurTag += c
                    else:
                        sCurData += c
                else:
                    if bTagMarkerStart:
                        iTagMarkerOffset += 1
                        sCurTag += c
                    else:
                        sCurData += c

    def reset(self):
        hFile.seek(0)
        self.iTagLvl = 0

class XMLParserHandler:
    def _printalign2taglvl(self, iTagLvl):
        for i in range(iTagLvl):
            print("--", end="")
        #print("iTagLvl:{}".format(iTagLvl))

    def error(self, sLine, errType):
        print(errType)

    def tag_start(self, sLine, sTag, iTagLvl):
        self._printalign2taglvl(iTagLvl)
        print("<{}>".format(sTag))

    def tag_end(self, sLine, sTag, iTagLvl, sData):
        self._printalign2taglvl(iTagLvl)
        print(sData)
        self._printalign2taglvl(iTagLvl)
        print("</{}>".format(sTag))


myParser = XMLParser()
myHandler = XMLParserHandler()
myParser.open(sys.argv[1])
myParser.parse(myHandler)



