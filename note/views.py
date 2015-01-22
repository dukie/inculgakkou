# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from KanjiToHiragana import Converter
from note.forms import LevelForm, SenseiForm, LessonForm, TopicForm, ExampleForm, BookForm, EnglishWordsChapterForm, EnglishWordForm, UserSettingsForm
from note.models import Level, Lesson, Topic, Example, Sensei, Book, KanjiWord, EnglishWordsChapter, EnglishWord, UserSettings
from note.utils import getUserSettings, goToSettings


def home(request):
    level = Level.objects.all().order_by('-name')[0]
    return redirect(level)


def lessons(request, lessonId=None):
    userSet = getUserSettings(request.user)
    if not userSet:
        return goToSettings()
    level = userSet.currentLevel
    lessons = Lesson.objects.select_related('level', 'sensei').filter(level=level).order_by('date')
    context = {
        'levelName': level.name,
        'lessonsList': lessons,
        'levels': Level.objects.all(),
    }
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            if lessonId:
                lessonObj = Lesson.objects.get(pk=lessonId)
                form = LessonForm(request.POST, instance=lessonObj)
            else:
                form = LessonForm(request.POST)
            lesson = form.save(commit=False)
            lesson.level = level
            lesson.save()
            return redirect('lessons')
    else:
        if lessonId:
            lesson = Lesson.objects.get(pk=lessonId)
            form = LessonForm(instance=lesson)
        else:
            form = LessonForm()

    return render(request, 'lessons.html',
                  {
                      'form': form,
                      'content': context
                  })


def topics(request, lessonId, topicId=None):
    lesson = get_object_or_404(Lesson, pk=lessonId)
    topics = Topic.objects.select_related('lesson', 'topicType').filter(lesson=lesson)
    context = {
        'levelName': lesson.level.name,
        'lessonNumber': lesson.chapterNumber,
        'topicsList': topics,
        'levels': Level.objects.all(),
    }
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            if topicId:
                topicObj = Topic.objects.get(pk=topicId)
                form = TopicForm(request.POST, instance=topicObj)
            else:
                form = TopicForm(request.POST)
            topic = form.save(commit=False)
            topic.lesson = lesson
            topic.save()
            return redirect('topics', str(lesson.pk))
    else:
        if topicId:
            topic = Topic.objects.get(pk=topicId)
            form = TopicForm(instance=topic)
        else:
            form = TopicForm()

    return render(request, 'topics.html',
                  {
                      'content': context,
                      'form': form
                  })


def examples(request, topicId, exampleId=None):
    topic = get_object_or_404(Topic, pk=topicId)
    examples = Example.objects.select_related('topic').filter(topic=topic)
    context = {
        'levelName': topic.lesson.level.name,
        'levels': Level.objects.all(),
        'lessonNumber': topic.lesson.chapterNumber,
        'topicName': topic.name,
        'examplesList': examples,
    }
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            if exampleId:
                exampleObj = Example.objects.get(pk=exampleId)
                form = ExampleForm(request.POST, instance=exampleObj)
            else:
                form = ExampleForm(request.POST)
            example = form.save(commit=False)
            example.topic = topic
            example.save()
            return redirect('examples', str(topic.pk))
    else:
        if exampleId:
            example = Example.objects.get(pk=exampleId)
            form = ExampleForm(instance=example)
        else:
            form = ExampleForm()
    return render(request, 'examples.html',
                  {
                      'content': context,
                      'form': form
                  })


def search(request, searchString):
    if len(searchString) < 2:
        redirectAdr = reverse('note.views.home')
        if request.META.get('HTTP_REFERER'):
            redirectAdr = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(redirectAdr)
    bunpouResults = Example.objects.filter(Q(kanji__contains=searchString) | Q(furigana__contains=searchString) | Q(
        translateEng__icontains=searchString) | Q(translateRus__contains=searchString))
    kanjiResults = KanjiWord.objects.filter(
        Q(writing__contains=searchString) | Q(reading__contains=searchString) | Q(translation__contains=searchString))
    context = {
        'bunpouResults': bunpouResults,
        'kanjiResults': kanjiResults,
        'searchString': searchString,
        'levelName': "Search"
    }
    return render(request, 'searchResults.html',
                  {
                      'content': context
                  })


def addLevel(request):
    levels = Level.objects.all()
    context = {
        'levels': levels
    }
    if request.method == 'POST':
        form = LevelForm(request.POST)
        if form.is_valid():
            form.save()
    form = LevelForm()

    return render(request, 'addLevel.html',
                  {
                      'form': form,
                      'content': context
                  })


def userSettings(request):
    context = {}
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            try:
                userSet = UserSettings.objects.get(user=request.user)
                form = UserSettingsForm(request.POST, instance=userSet)
                updateSettings = form.save(commit=False)
            except UserSettings.DoesNotExist:
                updateSettings = form.save(commit=False)
                updateSettings.user = request.user
            updateSettings.save()
    else:
        try:
            userSet = UserSettings.objects.get(user=request.user)
            form = UserSettingsForm(instance=userSet)
        except UserSettings.DoesNotExist:
            form = UserSettingsForm()

    return render(request, 'userSettings.html',
                  {
                      'form': form,
                      'content': context
                  })


def sensei(request, senseiId):
    senseis = Sensei.objects.select_related('sex').all()
    context = {
        'senseis': senseis
    }
    if request.method == 'POST':
        form = SenseiForm(request.POST)
        if form.is_valid():
            if senseiId:
                senseiObj = Sensei.objects.get(pk=senseiId)
                form = SenseiForm(request.POST, instance=senseiObj)
            else:
                form = SenseiForm(request.POST)
            form.save()
            return redirect('senseis')
    if senseiId:
        sensei = Sensei.objects.get(pk=senseiId)
        form = SenseiForm(instance=sensei)
    else:
        form = SenseiForm()

    return render(request, 'sensei.html',
                  {
                      'form': form,
                      'content': context
                  })


def convert(request):
    if request.method == 'POST':
        kanji = request.POST['kanji']
    converter = Converter.Converter()
    hiragana = converter.getHiragana(kanji)
    response_data = {}
    if hiragana:
        response_data['result'] = 'Success'
        response_data['message'] = hiragana
    else:
        response_data['result'] = 'Failed'
        response_data['message'] = ""
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def addBooks(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
    form = BookForm()

    return render(request, 'addBooks.html',
                  {
                      'form': form,
                      'content': context
                  })


def englishWordsChapter(request, chapterId=None):
    chapters = EnglishWordsChapter.objects.select_related('book').all()
    context = {
        'chapters': chapters
    }
    if request.method == 'POST':
        form = EnglishWordsChapterForm(request.POST)
        if form.is_valid():
            if chapterId:
                englishWordsChapterObj = EnglishWordsChapter.objects.get(pk=chapterId)
                form = EnglishWordsChapterForm(request.POST, instance=englishWordsChapterObj)
            form.save()
            return redirect('englishWordsChapter')
    else:
        if chapterId:
            englishWordsChapterObj = EnglishWordsChapter.objects.get(pk=chapterId)
            form = EnglishWordsChapterForm(instance=englishWordsChapterObj)
        else:
            form = EnglishWordsChapterForm()
    return render(request, 'englishChapter.html',
                  {
                      'form': form,
                      'content': context
                  })


def englishWords(request, chapterId=None, wordId=None):
    chapter = get_object_or_404(EnglishWordsChapter, pk=chapterId)
    context = {
        'words': EnglishWord.objects.select_related('chapter').filter(chapter=chapter)
    }
    if request.method == 'POST':
        form = EnglishWordForm(request.POST)
        if form.is_valid():
            if wordId:
                word = get_object_or_404(EnglishWord, pk=wordId)
                form = EnglishWordForm(request.POST, instance=word)
            else:
                form = EnglishWordForm(request.POST)
                form = form.save(commit=False)
                form.chapter = chapter
            form.save()
            return redirect('englishWords', str(chapter.pk))
    else:
        if wordId:
            word = EnglishWord.objects.get(pk=wordId)
            form = EnglishWordForm(instance=word)
        else:
            form = EnglishWordForm()

    return render(request, 'englishWord.html',
                  {
                      'form': form,
                      'content': context
                  })
