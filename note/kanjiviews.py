# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from note.forms import KanjiLessonForm, KanjiForm, KanjiWordsForm
from note.models import KanjiLesson, Kanji, KanjiWord
from note import utils
from note.utils import goToSettings


def kanjiLessons(request, lessonId=None):
    lessons = KanjiLesson.objects.select_related('sensei').all()

    context = {
        'lessonsList': lessons,
    }
    if request.method == 'POST':
        form = KanjiLessonForm(request.POST)
        if form.is_valid():
            if lessonId:
                lessonObj = KanjiLesson.objects.get(pk=lessonId)
                form = KanjiLessonForm(request.POST, instance=lessonObj)
            else:
                form = KanjiLessonForm(request.POST)
            form.save()
            return redirect('kanjiLessons')
    else:
        if lessonId:
            lesson = KanjiLesson.objects.get(pk=lessonId)
            form = KanjiLessonForm(instance=lesson)
        else:
            form = KanjiLessonForm()
    userSet = utils.getUserSettings(request.user)
    if not userSet:
        return goToSettings()


    return render(request, 'kanjilessons.html',
                  {
                      'form': form,
                      'content': context,
                      'actualKanji': utils.getActualKanjiList(userSet)
                  })


def kanjiList(request, lessonId, kanjiId=None):
    lesson = get_object_or_404(KanjiLesson, pk=lessonId)
    kanji = Kanji.objects.select_related('lesson').filter(lesson=lesson)
    total = len(KanjiWord.objects.filter(relatedKanji__in=kanji))

    context = {
        'lessonDate': lesson.date,
        'kanjiList': kanji,
        'totalKanji': total
    }
    if request.method == 'POST':
        form = KanjiForm(request.POST)
        if form.is_valid():
            if kanjiId:
                kanjiObj = Kanji.objects.get(pk=kanjiId)
                form = KanjiForm(request.POST, instance=kanjiObj)
            else:
                form = KanjiForm(request.POST)
            editableKanji = form.save(commit=False)
            editableKanji.lesson = lesson
            editableKanji.save()
            return redirect('kanjiList', str(lesson.pk))
    else:
        if kanjiId:
            kanjiObj = Kanji.objects.get(pk=kanjiId)
            form = KanjiForm(instance=kanjiObj)
        else:
            form = KanjiForm()

    userSet = utils.getUserSettings(request.user)
    if not userSet:
        return goToSettings()

    return render(request, 'kanjilist.html',
                  {
                      'content': context,
                      'form': form,
                      'actualKanji': utils.getActualKanjiList(userSet)
                  })


def kanjiWords(request, kanjiId, kanjiWordId=None):
    kanji = get_object_or_404(Kanji, pk=kanjiId)
    kanjiWords = KanjiWord.objects.select_related('relatedKanji').filter(relatedKanji=kanji)
    context = {
        'kanji': kanji,
        'kanjiWords': kanjiWords,
    }
    if request.method == 'POST':
        form = KanjiWordsForm(request.POST)
        if form.is_valid():
            if kanjiWordId:
                kanjiWordObj = KanjiWord.objects.get(pk=kanjiWordId)
                form = KanjiWordsForm(request.POST, instance=kanjiWordObj)
            else:
                form = KanjiWordsForm(request.POST)
            editableKanjiWord = form.save(commit=False)
            editableKanjiWord.relatedKanji = kanji
            editableKanjiWord.save()
            return redirect('kanjiWords', str(kanji.pk))
    else:
        if kanjiWordId:
            kanjiWordObj = KanjiWord.objects.get(pk=kanjiWordId)
            form = KanjiWordsForm(instance=kanjiWordObj)
        else:
            form = KanjiWordsForm()

    userSet = utils.getUserSettings(request.user)
    if not userSet:
        return goToSettings()

    return render(request, 'kanjiwords.html',
                  {
                      'content': context,
                      'form': form,
                      'actualKanji': utils.getActualKanjiList(userSet)
                  })




