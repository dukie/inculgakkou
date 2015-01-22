# -*- coding: utf-8 -*-
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone, importlib
from note.settings import behaviorsClasses


class Sex(models.Model):
    sexName = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'incul_sex'
        ordering = ['sexName', ]

    def __unicode__(self):
        return self.sexName


class UserSettings(models.Model):
    user = models.ForeignKey(User)
    currentKanjiLesson = models.PositiveIntegerField(max_length=5, default=500)
    currentHomeClassChapter = models.PositiveIntegerField(max_length=5, default=500)
    currentLevel = models.ForeignKey('Level')


class Sensei(models.Model):
    fullName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    fullNameFurigana = models.CharField(max_length=100)
    firstNameFurigana = models.CharField(max_length=50)
    lastNameFurigana = models.CharField(max_length=50)
    sex = models.ForeignKey('Sex')
    birthday = models.DateField(null=True)
    placeFrom = models.CharField(max_length=100)

    class Meta:
        db_table = 'incul_sensei'
        ordering = ['fullName', 'sex']

    def __unicode__(self):
        return self.fullName

    def get_absolute_url(self):
        return reverse('note.views.sensei', args=[str(self.id)])


class Book(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'incul_book'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=10, unique=True)
    startPeriod = models.DateField(null=True)
    endPeriod = models.DateField(null=True)

    class Meta:
        db_table = 'incul_level'
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    level = models.ForeignKey('Level')
    chapterNumber = models.PositiveIntegerField(max_length=5, null=True)
    book = models.ForeignKey('Book', null=True)
    date = models.DateField(null=False)
    sensei = models.ForeignKey('Sensei')

    class Meta:
        db_table = 'incul_lesson'
        ordering = ['chapterNumber']

    def __str__(self):
        return str(self.chapterNumber)

    def get_absolute_url(self):
        return reverse('note.views.topics', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('note.views.lessons', args=[str(self.level.id), str(self.id)])


class TopicType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    lesson = models.ForeignKey('Lesson')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    topicType = models.ForeignKey('TopicType', null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('note.views.examples', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('note.views.topics', args=[str(self.lesson.id), str(self.id)])


class Example(models.Model):
    topic = models.ForeignKey('Topic')
    kanji = models.TextField(null=True)
    furigana = models.TextField(null=True)
    translateEng = models.TextField(null=True)
    translateRus = models.TextField(null=True)

    def __unicode__(self):
        return self.kanji

    def get_edit_url(self):
        return reverse('note.views.examples', args=[str(self.topic.id), str(self.id)])


class KanjiLesson(models.Model):
    sensei = models.ForeignKey('Sensei')
    date = models.DateField(null=True)
    book = models.ForeignKey('Book', null=True)

    class Meta:
        db_table = 'incul_kanjilesson'
        ordering = ['date']

    def __unicode__(self):
        return self.date

    def get_absolute_url(self):
        return reverse('note.kanjiviews.kanjiList', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('note.kanjiviews.kanjiLessons', args=[str(self.id)])


class Kanji(models.Model):
    lesson = models.ForeignKey('KanjiLesson')
    number = models.PositiveIntegerField(max_length=5, null=True)
    symbol = models.CharField(max_length=5)
    reading = models.CharField(max_length=30)
    meaning = models.CharField(max_length=100)

    def __unicode__(self):
        return self.symbol

    class Meta:
        db_table = 'incul_kanji'
        ordering = ['number']

    def get_absolute_url(self):
        #if not hasattr(self, 'absoluteUrl'):
        #    self.absoluteUrl = reverse('note.kanjiviews.kanjiWords', args=[str(self.id)])
        #return self.absoluteUrl
        return reverse('note.kanjiviews.kanjiWords', args=[str(self.id)])

    def get_edit_url(self):
        #if not hasattr(self, 'editUrl'):
        #    self.editUrl = reverse('note.kanjiviews.kanjiList', args=[str(self.lesson.pk), str(self.id)])
        #return self.editUrl
        return reverse('note.kanjiviews.kanjiList', args=[str(self.lesson.pk), str(self.id)])


class KanjiWord(models.Model):
    relatedKanji = models.ForeignKey('Kanji')
    writing = models.CharField(max_length=30)
    reading = models.CharField(max_length=30)
    translation = models.CharField(max_length=30)
    shikenLevel = models.PositiveIntegerField(max_length=1, null=True)

    class Meta:
        db_table = 'incul_kanjiword'
        ordering = ['relatedKanji']

    def get_edit_url(self):
        return reverse('note.kanjiviews.kanjiWords', args=[str(self.relatedKanji.pk), str(self.id)])

    def __unicode__(self):
        return self.writing


class KanjiQuizze(models.Model):
    sessionKey = models.CharField(max_length=30, null=False)
    content = models.CharField(max_length=30, null=False)
    answer = models.CharField(max_length=30, null=False)
    date = models.DateField(null=False)

    class Meta:
        db_table = 'incul_kanjquizze'
        ordering = ['date']


class TrainingAnswer(models.Model):
    sessionKey = models.CharField(max_length=30, null=False)
    content = models.CharField(max_length=300, null=False)
    answer = models.CharField(max_length=300, null=False)
    date = models.DateField(null=False)

    class Meta:
        db_table = 'incul_trainingAnswer'
        ordering = ['date']


class EnglishWordsChapter(models.Model):
    contentName = models.CharField(max_length=20)
    book = models.ForeignKey('Book', null=True)
    date = models.DateField(null=False, default=datetime.date.today)

    class Meta:
        ordering = ['date']

    def get_absolute_url(self):
        return reverse('note.views.englishWords', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('note.views.englishWordsChapter', args=[str(self.id)])


class EnglishWord(models.Model):
    chapter = models.ForeignKey('EnglishWordsChapter', null=False)
    verbEng = models.CharField(max_length=30, null=True)
    verbJp = models.CharField(max_length=100, null=True)
    nounEng = models.CharField(max_length=30, null=True)
    nounJp = models.CharField(max_length=100, null=True)
    adjEng = models.CharField(max_length=30, null=True)
    adjJp = models.CharField(max_length=100, null=True)
    exampleEng = models.CharField(max_length=300, null=True)
    exampleJp = models.CharField(max_length=300, null=True)

    def get_edit_url(self):
        return reverse('note.views.englishWords', args=[str(self.chapter.id), str(self.id)])


class TestEntity(models.Model):
    testSuit = models.ForeignKey('TestSuit')
    entityId = models.PositiveIntegerField(null=False)
    points = models.IntegerField(default=0)

    class Meta:
        db_table = 'incul_TEST_entity'


class TestCurrentQuestion(models.Model):
    creationDate = models.DateTimeField(null=False, default=timezone.now())
    question = models.CharField(max_length=100, null=False)
    answer = models.CharField(max_length=100, null=False)
    hint = models.CharField(max_length=200, null=False)
    entityId = models.ForeignKey('TestEntity', null=True)

    def save(self, *args, **kwargs):
        self.creationDate = timezone.now()
        super(TestCurrentQuestion, self).save(*args, **kwargs)

    class Meta:
        db_table = 'incul_TEST_currentQuestion'
        ordering = ['creationDate']


class TestSuit(models.Model):
    creationDate = models.DateTimeField(null=False, default=timezone.now())
    currentStep = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User)
    isActive = models.BooleanField(default=False)
    testingEntityCT = models.ForeignKey(ContentType, null=False)
    points = models.IntegerField(default=0)
    currentQuestion = models.OneToOneField('TestCurrentQuestion', related_name='testSuit')
    topic = models.ForeignKey('TestTopics')

    class Meta:
        ordering = ['creationDate']
        db_table = 'incul_TEST_suit'

    @classmethod
    def create(cls):
        ts = cls()
        ts.creationDate = timezone.now()
        ts.currentQuestion = TestCurrentQuestion()
        return ts

    def save(self, *args, **kwargs):
        self.currentQuestion.save()
        self.currentQuestion = self.currentQuestion
        super(TestSuit, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.currentQuestion.delete()
        super(TestSuit, self).delete(*args, **kwargs)


class TestTopics(models.Model):
    topicCT = models.ForeignKey(ContentType, null=False)
    title = models.CharField(max_length=30, null=False)
    questionField = models.CharField(max_length=30, null=True)
    answerField = models.CharField(max_length=30, null=True)
    hintField = models.CharField(max_length=30, null=True)
    testBehaviorClass = models.CharField(max_length=30, null=True)

    def createBehaviorObject(self):
        importPath = behaviorsClasses[self.testBehaviorClass]
        behaveModule = importlib.import_module(importPath)
        return behaveModule.Behavior()

    class Meta:
        ordering = ['id']
        db_table = 'incul_TEST_topics'