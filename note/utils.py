# -*- coding: utf-8 -*-
import datetime
import logging
import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models.fields import FieldDoesNotExist
from django.http import HttpResponseRedirect

from note.models import Kanji, TopicType, Topic, EnglishWordsChapter, TestSuit, TestTopics, TestEntity, UserSettings, Level, KanjiLesson
from note.settings import CORRECT, WRONG


logger = logging.getLogger('Utils')


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def getActualKanjiList(userSettings):
    try:
        currentKanjiLesson = KanjiLesson.objects.get(pk=userSettings.currentKanjiLesson)
    except KanjiLesson.DoesNotExist:
        currentKanjiLesson = KanjiLesson.objects.all()[0]
    return Kanji.objects.filter(lesson=currentKanjiLesson)


def getUserSettings(user):
    try:
        return UserSettings.objects.get(user=user)
    except UserSettings.DoesNotExist:
        return None


def createTopicsList(trainingType):
    dictType = TopicType.objects.get(name=trainingType)
    topics = Topic.objects.select_related('lesson').filter(topicType=dictType).order_by('lesson__date')
    return topics


def createEnglishChaptersList(trainingType):
    dictType = EnglishWordsChapter.objects.all()
    #topics = Topic.objects.filter(topicType=dictType)
    return dictType


def goHome():
    redirectAdr = reverse('note.views.home')
    return HttpResponseRedirect(redirectAdr)


def goToSettings():
    return HttpResponseRedirect(reverse('userSettings'))


class TrainingFactory(object):
    def __init__(self, user):
        self.user = user
        try:
            self.testSuit = TestSuit.objects.get(user=self.user, isActive=True)
        except TestSuit.DoesNotExist:
            self.testSuit = None

    def isTestInProgress(self):
        if self.testSuit:
            return True
        return False

    def createSuit(self, theme):
        try:
            with transaction.atomic():
                tTopic = TestTopics.objects.get(pk=theme)
                topicCT = tTopic.topicCT
                if self.isTestInProgress():
                    self.testSuit.delete()
                self.testSuit = TestSuit.create()
                self.testSuit.topic = tTopic
                self.testSuit.user = self.user
                self.testSuit.testingEntityCT = topicCT
                self.testSuit.currentQuestion.answer = '-1'
                self.testSuit.currentQuestion.question = '-1'
                self.testSuit.currentQuestion.hint = '-1'
                self.testSuit.isActive = True
                self.testSuit.save()
                userSet = getUserSettings(self.user)
                behaviorManager = tTopic.createBehaviorObject()
                entQuerySet = behaviorManager.getEntities(tTopic, userSet)
                #TODO maybe Bulk create will be better
                for entry in entQuerySet:
                    te = TestEntity()
                    te.testSuit = self.testSuit
                    te.entityId = entry.id
                    te.save()
                return self.testSuit

        except TestTopics.DoesNotExist:
            print("Create Factory Topic doesn't exist")
            return None

    def restoreSuit(self):
        return self.testSuit

    def destroySuit(self):
        if self.testSuit:
            self.testSuit.delete()
            return True
        else:
            return False


class TrainingEngine(object):
    def __init__(self, testSuit):
        self.testSuit = testSuit

    def getNewQuestion(self):
        entities = TestEntity.objects.filter(testSuit=self.testSuit, points__lt=3)
        length = len(entities) - 1

        choose = random.randint(0, length)
        chosen = entities[choose]
        manager = self.testSuit.testingEntityCT.model_class().objects
        realQObject = manager.get(pk=chosen.entityId)
        self.testSuit.currentQuestion.question = realQObject.__dict__[self.testSuit.topic.questionField]
        self.testSuit.currentQuestion.answer = realQObject.__dict__[self.testSuit.topic.answerField]
        self.testSuit.currentQuestion.hint = realQObject.__dict__[self.testSuit.topic.hintField]
        self.testSuit.currentQuestion.entityId = chosen
        self.testSuit.currentStep += 1
        self.testSuit.save()
        return self.testSuit.currentQuestion

    def getPreviousInfo(self):
        info = dict()
        info['answer'] = self.testSuit.currentQuestion.answer
        info['question'] = self.testSuit.currentQuestion.question
        return info

    def getCurrentQuestion(self):
        return self.testSuit.currentQuestion

    def checkAnswer(self, answer):
        result = None
        rightAnswer = self.testSuit.currentQuestion.answer
        entity = self.testSuit.currentQuestion.entityId
        if answer == rightAnswer:
            entity.points += 1
            result = CORRECT
        else:
            entity.points -= 1
            result = WRONG
        entity.save()
        return result

    def __fillUpQuestion(self):
        pass