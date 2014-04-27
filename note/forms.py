# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets
from note.models import Sensei, Lesson, Topic, Example, Book, Level, KanjiLesson, Kanji, KanjiWord


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level

    def __init__(self, *args, **kwargs):
        super(LevelForm, self).__init__(*args, **kwargs)
        self.fields['startPeriod'].widget = widgets.AdminDateWidget()
        self.fields['endPeriod'].widget = widgets.AdminDateWidget()


class SenseiForm(forms.ModelForm):
    class Meta:
        model = Sensei

    def __init__(self, *args, **kwargs):
        super(SenseiForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget = widgets.AdminDateWidget()


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['chapterNumber', 'book', 'date', 'sensei']

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description', 'topicType']


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['kanji', 'furigana', 'translateRus']

    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.fields['furigana'].widget.is_required = False


class BookForm(forms.ModelForm):
    class Meta:
        model = Book


class KanjiLessonForm(forms.ModelForm):
    class Meta:
        model = KanjiLesson

    def __init__(self, *args, **kwargs):
        super(KanjiLessonForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget = widgets.AdminDateWidget()


class KanjiForm(forms.ModelForm):
    class Meta:
        model = Kanji
        fields = ['number', 'symbol', 'reading', 'meaning']


class KanjiWordsForm(forms.ModelForm):
    class Meta:
        model = KanjiWord
        fields = ['writing', 'reading', 'translation', 'shikenLevel']

    def __init__(self, *args, **kwargs):
        super(KanjiWordsForm, self).__init__(*args, **kwargs)
        self.fields['shikenLevel'].widget.is_required = False
