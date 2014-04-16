import json
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from KanjiToHiragana import Converter
from note.forms import LevelForm, SenseiForm, LessonForm, TopicForm, ExampleForm, BookForm
from note.models import Level, Lesson, Topic, Example, Sensei, Book, KanjiWord



def home(request):
    level = Level.objects.all().order_by('-name')[0]
    return redirect(level)


def lessons(request, levelId, lessonId=None):
    level = get_object_or_404(Level, pk=levelId)
    lessons = Lesson.objects.filter(level=level)
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
            return redirect('lessons', str(level.pk))
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
    topics = Topic.objects.filter(lesson=lesson)
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
    examples = Example.objects.filter(topic=topic)
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
        redirectAdr = '/'
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


def sensei(request, senseiId):
    senseis = Sensei.objects.all()
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
        print request
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