# -*- coding: utf-8 -*-
"""
Created on Feb 7, 2012

@author: dukie
"""

import urllib.request as urllib2
#import urllib2
coding = "UTF-8"

headersDict = {
    "LIVESCORE": [
        {
            "name": "X-Fsign",
            "value": "SW9D1eZo"
        },
    ],
    "FONBET_GET": [
        {
            "name": "Referer",
            "value": "http://toto-info.fonbet.com/ru/Default.aspx"
        }
    ],
    "FONBET_POST": [
        {
            "name": "X-Requested-With",
            "value": "XMLHttpRequest"
        },
        {
            "name": "Referer",
            "value": "http://toto-info.fonbet.com/ru/650/Detail.aspx"
        },
        {
            "name": "Content-Type",
            "value": "application/json; charset=utf-8"
        }
    ],
    "USER-AGENT":
        {
            "name": "User-Agent",
            "value": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1"
        }
}


class Taker(object):
    def __init__(self, url=None):
        if url:
            self.url = url

            self.opener = urllib2.Request(self.url)
        else:
            self.url = "http://www.vkursax.ru"

    def getHTML(self, url=None, headers=None):
        if url is not None:
            self.url = url
            self.opener = urllib2.Request(self.url)
            if headers:
                self.setupHeaders(headers)

        self.opener.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1")
        self.opener.add_header("X-Fsign", "SW9D1eZo")
        try:
            htmlResult = urllib2.urlopen(self.opener)
            byteText = htmlResult.read()
            htmlResult.close()
            text = byteText.decode(coding)
            return text

        except urllib2.HTTPError:
            print("404 not found")
            return '404'
        except urllib2.URLError:
            # TODO: need to prevent stack overflow
            print("Address temporary not available, retry")
            return self.getHTML(url, headers)

    def postHtml(self, data, url=None, headers=None):
        if url is not None:
            self.url = url
            self.opener = urllib2.Request(self.url)
            if headers:
                self.setupHeaders(headers)

        try:
            htmlResult = urllib2.urlopen(self.opener, data)
            byteText = htmlResult.read()
            htmlResult.close()
            text = byteText.decode(coding)
            return text

        except urllib2.HTTPError:
            print("404 not found")
            return '404'
        except urllib2.URLError:
            # TODO: need to prevent stack overflow
            print("Address temporary not available, retry")

    def setupHeaders(self, headers=None):
        self.opener.add_header(headersDict['USER-AGENT']['name'], headersDict['USER-AGENT']['value'])
        if headers is not None:
            for header in headers:
                self.opener.add_header(header['name'], header['value'])
            return True
        return False


