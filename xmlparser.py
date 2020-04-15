#!/usr/bin/env python3
# A simple minded stupid xml parser
# v20200415IST1850, HanishKVC

import sys


class XMLParser:
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

    def _process_tag(self, sIn):
        try:
            sTag,sRemain = sIn.split(' ',1)
        except ValueError:
            sTag = sIn
            sRemain = ""
        dAttribs = {}
        sKey = ""
        sData = ""
        bKey = True
        bInString = False
        for c in sRemain:
            if c == '"':
                if bInString:
                    bInString = False
                else:
                    bInString = True
            elif c == '=':
                if not bInString:
                    bKey = False
            elif str.isspace(c):
                if bInString:
                    if bKey:
                        sKey += c
                    else:
                        sData += c
                else:
                    if not bKey:
                        if sKey != "":
                            dAttribs[sKey] = sData
                            sKey = ""
                            sData = ""
                            bKey = True

            else:
                if bKey:
                    sKey += c
                else:
                    sData += c
        if sKey != "":
            dAttribs[sKey] = sData
        return sTag, dAttribs

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
                        sTag, dAttribs = self._process_tag(sCurTag)
                        if bTagTypeStart:
                            handler.tag_start(sTag, dAttribs, self.iTagLvl, sCurTag, l)
                            self.iTagLvl += 1
                        if (not bTagTypeStart) or (iTagMarkerOffset == SELFCONTAINEDTAGSPECIALOFFSET):
                            self.iTagLvl -= 1
                            handler.tag_end(sTag, dAttribs, self.iTagLvl, sCurData, sCurTag, l)
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

    def tag_start(self, sTag, dAttribs, iTagLvl, sRawTag, sLine):
        self._printalign2taglvl(iTagLvl)
        print("DBUG:<{}>".format(sRawTag))
        self._printalign2taglvl(iTagLvl)
        print("<{} {}>".format(sTag, dAttribs))

    def tag_end(self, sTag, dAttribs, iTagLvl, sData, sRawTag, sLine):
        self._printalign2taglvl(iTagLvl)
        print(sData)
        self._printalign2taglvl(iTagLvl)
        print("</{}>".format(sRawTag))


if __name__ == "__main__":
    myParser = XMLParser()
    myHandler = XMLParserHandler()
    myParser.open(sys.argv[1])
    myParser.parse(myHandler)


