# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets
from note.models import Sensei, Lesson, Topic, Example, Book, Level, KanjiLesson, Kanji, KanjiWord, EnglishWordsChapter, EnglishWord


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


class EnglishWordsChapterForm(forms.ModelForm):
    contentName = forms.CharField(required=True, label=u"言葉番号範囲",
                                  widget=forms.TextInput(attrs={'placeholder': '選択した本の言葉番号範囲'}))

    class Meta:
        model = EnglishWordsChapter
        fields = ['book', 'contentName']

    def __init__(self, *args, **kwargs):
        super(EnglishWordsChapterForm, self).__init__(*args, **kwargs)
        #self.fields['date'].widget.is_required = False
        self.fields['book'].label = u'本を選択してください'


class EnglishWordForm(forms.ModelForm):
    verbEng = forms.CharField(required=True, label=u"英語の動詞", widget=forms.TextInput(attrs={'placeholder': '英語の動詞'}))
    verbJp = forms.CharField(required=True, label=u"日本語の動詞", widget=forms.TextInput(attrs={'placeholder': '日本語の動詞'}))
    nounEng = forms.CharField(required=False, label=u"英語の名詞", widget=forms.TextInput(attrs={'placeholder': '語の名詞'}))
    nounJp = forms.CharField(required=False, label=u"日本語の名詞", widget=forms.TextInput(attrs={'placeholder': '日本語の名詞'}))
    adjEng = forms.CharField(required=False, label=u"英語の形容詞", widget=forms.TextInput(attrs={'placeholder': '英語の形容詞'}))
    adjJp = forms.CharField(required=False, label=u"日本語の形容詞", widget=forms.TextInput(attrs={'placeholder': '英語の形容詞'}))
    exampleEng = forms.CharField(required=True, label=u"英語の例", widget=forms.TextInput(attrs={'placeholder': '英語の例'}))
    exampleJp = forms.CharField(required=True, label=u"日本語の例", widget=forms.TextInput(attrs={'placeholder': '日本語の例'}))

    class Meta:
        model = EnglishWord
        fields = ['verbEng', 'verbJp', 'nounEng', 'nounJp', 'adjEng', 'adjJp', 'exampleEng', 'exampleJp']

    def __init__(self, *args, **kwargs):
        super(EnglishWordForm, self).__init__(*args, **kwargs)