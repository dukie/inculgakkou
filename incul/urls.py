from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Base
                       url(r'^bunpou/(?P<levelId>\d+)/$', 'note.views.lessons', name='lessons'),
                       url(r'^bunpou/lesson/(?P<lessonId>\d+)/$', 'note.views.topics', name='topics'),
                       url(r'^bunpou/topic/(?P<topicId>\d+)/$', 'note.views.examples', name='examples'),
                       url(r'^kanji/kanjilist/(?P<lessonId>\d+)/$', 'note.kanjiviews.kanjiList', name='kanjiList'),
                       url(r'^kanji/kanjiwords/(?P<kanjiId>\d+)/$', 'note.kanjiviews.kanjiWords', name='kanjiWords'),
                       url(r'^search/(?P<searchString>\w+)/$', 'note.views.search', name='search'),
                       url(r'^$', 'note.views.home'),

                       #Add views
                       url(r'^addLevel/$', 'note.views.addLevel', name='addLevel'),
                       url(r'^sensei/(?P<senseiId>\w+){0,1}$', 'note.views.sensei', name='senseis'),
                       url(r'^bunpou/(?P<levelId>\d+)/(?P<lessonId>\d+)/$', 'note.views.lessons', name='lessonsEdit'),
                       url(r'^bunpou/lesson/(?P<lessonId>\d+)/(?P<topicId>\d+)/$', 'note.views.topics',
                           name='topicsEdit'),
                       url(r'^bunpou/topic/(?P<topicId>\d+)/(?P<exampleId>\d+)/$', 'note.views.examples',
                           name='examplesEdit'),
                       url(r'^addBook/$', 'note.views.addBooks', name='addBook'),

                        url(r'^kanji/(?P<lessonId>\w+){0,1}$', 'note.kanjiviews.kanjiLessons', name='kanjiLessons'),
                        url(r'^kanji/kanjilist/(?P<lessonId>\d+)/(?P<kanjiId>\d+)/$', 'note.kanjiviews.kanjiList', name='kanjiEdit'),
                        url(r'^kanji/kanjiwords/(?P<kanjiId>\d+)/(?P<kanjiWordId>\d+)/$', 'note.kanjiviews.kanjiWords', name='kanjiWordEdit'),
                       #Post views
                       url(r'^convert/$', 'note.views.convert', name='convert'),

                       #Main
                       url(r'^admin/', include(admin.site.urls)),
)
