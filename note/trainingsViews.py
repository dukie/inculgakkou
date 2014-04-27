# -*- coding: utf-8 -*-
import random
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from note import settings, utils
from note.models import KanjiQuizze, KanjiWord, Example, Level, TrainingAnswer


def kanjiQuizze(request, answer=None):
    context = {}
    id = request.COOKIES.get('csrftoken')
    if not id:
        redirectAdr = reverse('note.views.home')
        return HttpResponseRedirect(redirectAdr)
    try:
        quizze = KanjiQuizze.objects.get(sessionKey=id)
        if answer:
            if quizze.answer == answer:
                context["result"] = "Correct"
            else:
                context["result"] = "Wrong"
            context['prev_question'] = quizze.content
            context['prev_answer'] = quizze.answer
    except KanjiQuizze.DoesNotExist:
        quizze = KanjiQuizze()
        quizze.sessionKey = id
    actualK = [item.pk for item in utils.getActualKanji(settings.ACTUAL_KANJI_TO_SHOW)]
    words = KanjiWord.objects.filter(relatedKanji__in=actualK)
    length = len(words) - 1
    random.random()
    choose = random.randint(0,length)
    question = words[choose].writing
    answer = words[choose].reading
    translation = words[choose].translation

    quizze.answer = answer
    quizze.content = question
    quizze.date = datetime.now()
    quizze.save()
    context['translation'] = translation
    context['question'] = question
    context['answer'] = answer
    response = render(request, 'kanjiquizzes.html',
                  {
                      'content': context,
                      'actualKanji': utils.getActualKanji(settings.ACTUAL_KANJI_TO_SHOW)
                  })
    return response


def dictionary(request):
    context = {'levels': Level.objects.all()}
    print request.COOKIES
    print request.POST
    id = request.COOKIES.get('csrftoken')
    if not id:
        return utils.goHome()
    topic = request.COOKIES.get('topic')
    if not topic:
        context['topics'] = utils.createTopicsList(settings.DICTIONARY_TYPE)
        return render(request, 'selectTraining.html',
                    {
                      'content': context,
                    })


    try:
        quizze = TrainingAnswer.objects.get(sessionKey=id)
    except TrainingAnswer.DoesNotExist:
        quizze = TrainingAnswer()
        quizze.sessionKey = id

    if request.method == 'POST':
        print "POST"
        action = request.POST['action']
        if action == settings.ANSWER_ACTION:
                answer = request.POST['answer']
                if answer:
                    if quizze.answer == answer:
                        context["result"] = "Correct"
                    else:
                        context["result"] = "Wrong"
                    context['prev_question'] = quizze.content
                    context['prev_answer'] = quizze.answer
        else:
            currentURL = reverse('note.trainingsViews.dictionary')
            response = HttpResponseRedirect(currentURL)
            response.delete_cookie('topic','/')
            return response

    try:
        examples = Example.objects.filter(topic__id=topic)
        length = len(examples) - 1
        random.random()
        choose = random.randint(0,length)
        example = examples[choose]
        translation = example.translateRus
        question = example.kanji
        ans = example.furigana

        quizze.answer = ans
        quizze.content = question
        quizze.date = datetime.now()
        quizze.save()
        context['translation'] = translation
        context['question'] = question
        context['answer'] = ans
    except KanjiQuizze.DoesNotExist:
                quizze = TrainingAnswer()
                quizze.sessionKey = id
    response = render(request, 'training.html',
                  {
                      'content': context,
                  })
    return response




def grammar(request):
    context = {'levels': Level.objects.all()}
    id = request.COOKIES.get('csrftoken')
    if not id:
        return utils.goHome()
    topic = request.COOKIES.get('topic')
    if not topic:
        context['topics'] = utils.createTopicsList(settings.GRAMMAR_TYPE)
        return render(request, 'selectTraining.html',
                    {
                      'content': context,
                    })

    try:
        examples = Example.objects.filter(topic__id=topic)
        length = len(examples) - 1
        random.random()
        choose = random.randint(0,length)
        example = examples[choose]
        context['translation'] = example.translateRus
        context['question'] = example.kanji
    except:
        pass

    if request.method == 'POST':
        action = request.POST['action']
        if action == settings.ANSWER_ACTION:
            pass
        else:
            currentURL = reverse('note.trainingsViews.grammar')
            response = HttpResponseRedirect(currentURL)
            response.delete_cookie('topic',currentURL)
            return response

    response = render(request, 'training.html',
                  {
                      'content': context,
                  })
    return response

def shikenN3(request):
    context = {'levels': Level.objects.all()}
    id = request.COOKIES.get('csrftoken')
    if not id:
        return utils.goHome()
    topic = request.COOKIES.get('topic')
    if not topic:
        context['topics'] = utils.createTopicsList(settings.SHIKENN3_TYPE)
        return render(request, 'selectTraining.html',
                    {
                      'content': context,
                    })

    try:
        examples = Example.objects.filter(topic__id=topic)
        length = len(examples) - 1
        random.random()
        choose = random.randint(0,length)
        example = examples[choose]
        context['translation'] = example.translateRus
        context['question'] = example.kanji
    except:
        pass

    if request.method == 'POST':
        action = request.POST['action']
        if action == settings.ANSWER_ACTION:
            pass
        else:
            currentURL = reverse('note.trainingsViews.shikenN3')
            response = HttpResponseRedirect(currentURL)
            response.delete_cookie('topic',currentURL)
            return response

    response = render(request, 'training.html',
                  {
                      'content': context,
                  })
    return response


def reset(request):
    topic = request.COOKIES
    response = HttpResponseRedirect(reverse('note.views.home'))
    response.delete_cookie('topic', '/')
    return response