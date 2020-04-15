#!/usr/bin/env python3


class XMLParser():
    sFile = None
    hFile = None
    handler = None
    def __init__(self):
        self.sFile = None
        self.hFile = None
        self.handler = None

    def open(self, sFile):
        hFile = open(sFile)

    def parse(self, handler):
        bTagMarkerStart = False
        sCurTag = None
        for l in self.hFile:
            for c in l:
                if c == '<':
                    if bTagMarkerStart:
                        handler.error(l, self.TAGSTARTMARKERAGAIN)
                    else:
                        bTagMarkerStart = True
                        sCurTag = c
                if c == '>':
                    if bTagMarkerStart:
                        sCurTag += c
                        handler.tag_start(l, sCurTag)
                        bTagMarkerStart = False
                    else:
                        handler.error(l, self.TAGENDMARKERALONE)
