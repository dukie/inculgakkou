# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


class Sex(models.Model):
    sexName = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = 'incul_sex'
        ordering = ['sexName', ]

    def __unicode__(self):
        return self.sexName


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

    def get_absolute_url(self):
        return reverse('note.views.lessons', args=[str(self.id)])


class Lesson(models.Model):
    level = models.ForeignKey('Level')
    chapterNumber = models.PositiveIntegerField(max_length=5, null=True)
    book = models.ForeignKey('Book', null=True)
    date = models.DateField(null=False)
    sensei = models.ForeignKey('Sensei')

    class Meta:
        db_table = 'incul_lesson'
        ordering = ['chapterNumber']

    def __unicode__(self):
        return unicode(self.chapterNumber)

    def get_absolute_url(self):
        return reverse('note.views.topics', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('note.views.lessons', args=[str(self.level.id), str(self.id)])


class TopicType(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.name)


class Topic(models.Model):
    lesson = models.ForeignKey('Lesson')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    topicType = models.ForeignKey('TopicType', null=False)

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
        return reverse('note.kanjiviews.kanjiWords', args=[str(self.id)])

    def get_edit_url(self):
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