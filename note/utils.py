# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from note.models import Kanji, TopicType, Topic, EnglishWordsChapter


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def getActualKanji(numberOfKanji):
    return Kanji.objects.all().order_by('-number')[:numberOfKanji]


def createTopicsList(trainingType):
    dictType = TopicType.objects.get(name=trainingType)
    topics = Topic.objects.filter(topicType=dictType)
    return topics


def createEnglishChaptersList(trainingType):
    dictType = EnglishWordsChapter.objects.all()
    #topics = Topic.objects.filter(topicType=dictType)
    return dictType


def goHome():
    redirectAdr = reverse('note.views.home')
    return HttpResponseRedirect(redirectAdr)
