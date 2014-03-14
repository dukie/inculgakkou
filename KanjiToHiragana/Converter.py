# -*- coding: utf-8 -*-
import urllib
from html import Taker
import BeautifulSoup
__author__ = 'dukie'


class Converter(object):
    dataTemplate = {
            u"uniqid": u"ccff2960280404a4ae4319198eda7d2103b0de26",
            u"kanji": u"",
            u"Submit": u"Translate Now",
            u"kanji_parts": u"unchanged",
            u"converter": u"spacedrollover",
            u"kana_output": u"hiragana",
    }
    def __init__(self):
        self.htmlTaker = Taker()

    def getHiragana(self, kanji):
        headers = [
                       {
                            "name" : u"Content-Type",
                            "value": u"application/x-www-form-urlencoded"
                        }
        ]
        data = Converter.dataTemplate
        if type(kanji) == str:
            data[u'kanji'] = kanji
        elif type(kanji) == unicode:
            data[u'kanji'] = kanji.encode("utf-8")

        data = urllib.urlencode(data)
        rawHtml = self.htmlTaker.postHtml(data, url="http://nihongo.j-talk.com/",headers=headers)
        soup = BeautifulSoup.BeautifulSoup(rawHtml)
        elements = soup.find('div', {"id": "rollover", "class":"hiragana"})
        res = u""
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

    con = Converter()
    print con.getHiragana(u"食べ物")
    print con.getHiragana(sys.argv[1])