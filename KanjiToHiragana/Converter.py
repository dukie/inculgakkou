# -*- coding: utf-8 -*-
import urllib
from KanjiToHiragana.htmlBase import Taker
import bs4 as BeautifulSoup
#import urllib
#from htmlBase import Taker
#import BeautifulSoup
__author__ = 'dukie'


class Converter(object):
    dataTemplate = {
            "uniqid": "ccff2960280404a4ae4319198eda7d2103b0de26",
            "Submit": "Translate Now",
            "kanji_parts": "unchanged",
            "converter": "spacedrollover",
            "kana_output": "hiragana",
    }
    def __init__(self):
        self.htmlTaker = Taker()

    def getHiragana(self, kanji):
        headers = [
                       {
                            "name" : "Content-Type",
                            "value": "application/x-www-form-urlencoded",

                        },

        ]
        data = Converter.dataTemplate
        data['kanji'] = kanji
        data = urllib.parse.urlencode(data)
        data = bytes(data, 'utf-8')
        rawHtml = self.htmlTaker.postHtml(data, url="http://nihongo.j-talk.com/",headers=headers)
        soup = BeautifulSoup.BeautifulSoup(rawHtml)
        elements = soup.find('div', {"id": "rollover", "class":"hiragana"})
        res = ""
        for element in elements:
            if type(element) == BeautifulSoup.NavigableString:
                res += element
            elif type(element) == BeautifulSoup.Tag:
                trg = element.find('trg')
                if trg:
                    res += trg.findAll(text=True)[0]
        return res.strip(' ')

if __name__ == '__main__':
    import sys
    print(type("食べ物"))
    print(type(sys.argv[1]))
    con = Converter()
    print (con.getHiragana("食べ物"))
    print (con.getHiragana(sys.argv[1]))