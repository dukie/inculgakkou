# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Base
                       url(r'^incul/bunpou/(?P<levelId>\d+)/$', 'note.views.lessons', name='lessons'),
                       url(r'^incul/bunpou/lesson/(?P<lessonId>\d+)/$', 'note.views.topics', name='topics'),
                       url(r'^incul/bunpou/topic/(?P<topicId>\d+)/$', 'note.views.examples', name='examples'),
                       url(r'^incul/kanji/kanjilist/(?P<lessonId>\d+)/$', 'note.kanjiviews.kanjiList',
                           name='kanjiList'),
                       url(r'^incul/kanji/kanjiwords/(?P<kanjiId>\d+)/$', 'note.kanjiviews.kanjiWords',
                           name='kanjiWords'),
                       url(r'^incul/search/(?P<searchString>\w*)/$', 'note.views.search', name='search'),
                       url(r'^incul/$', 'note.views.home'),

                       #Add views
                       url(r'^incul/addLevel/$', 'note.views.addLevel', name='addLevel'),
                       url(r'^incul/sensei/(?P<senseiId>\w+){0,1}$', 'note.views.sensei', name='senseis'),
                       url(r'^incul/bunpou/(?P<levelId>\d+)/(?P<lessonId>\d+)/$', 'note.views.lessons',
                           name='lessonsEdit'),
                       url(r'^incul/bunpou/lesson/(?P<lessonId>\d+)/(?P<topicId>\d+)/$', 'note.views.topics',
                           name='topicsEdit'),
                       url(r'^incul/bunpou/topic/(?P<topicId>\d+)/(?P<exampleId>\d+)/$', 'note.views.examples',
                           name='examplesEdit'),
                       url(r'^incul/addBook/$', 'note.views.addBooks', name='addBook'),

                       url(r'^incul/kanji/(?P<lessonId>\d+){0,1}$', 'note.kanjiviews.kanjiLessons',
                           name='kanjiLessons'),
                       url(r'^incul/kanji/kanjilist/(?P<lessonId>\d+)/(?P<kanjiId>\d+)/$', 'note.kanjiviews.kanjiList',
                           name='kanjiEdit'),
                       url(r'^incul/kanji/kanjiwords/(?P<kanjiId>\d+)/(?P<kanjiWordId>\d+)/$',
                           'note.kanjiviews.kanjiWords', name='kanjiWordEdit'),
                       #English Part
                       url(r'^incul/english/(?P<chapterId>\d+){0,1}$', 'note.views.englishWordsChapter',
                           name='englishWordsChapter'),
                       url(r'^incul/english/words/(?P<chapterId>\d+){1}/(?P<wordId>\d+){0,1}$',
                           'note.views.englishWords', name='englishWords'),
                       url(r'^incul/english/training/words/$', 'note.trainingsViews.englishWords',
                           name='englishWordsTraining'),
                       url(r'^incul/english/training/examples/$', 'note.trainingsViews.englishExamples',
                           name='englishExamplesTraining'),
                       #TrainingViews
                       url(r'^incul/kanji/quizze/(?P<answer>\w*)[/]?$', 'note.trainingsViews.kanjiQuizze',
                           name='kanjiQuizze'),
                       url(r'^incul/bunpou/training/dictionary/$', 'note.trainingsViews.dictionary',
                           name='dictionaryTraining'),
                       url(r'^incul/bunpou/training/grammar/$', 'note.trainingsViews.grammar', name='grammarTraining'),
                       url(r'^incul/bunpou/training/N3/$', 'note.trainingsViews.shikenN3', name='shikenN3Training'),

                       #Post views
                       url(r'^incul/convert/$', 'note.views.convert', name='convert'),

                       #Main
                       url(r'^incul/admin/', include(admin.site.urls)),
)
