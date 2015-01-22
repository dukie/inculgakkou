# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets
from django.forms import widgets as normalWidgets
from ajax.fields import AjaxSelectWidget
from note.models import Sensei, Lesson, Topic, Example, Book, Level, KanjiLesson, Kanji, KanjiWord, EnglishWordsChapter, EnglishWord, TestTopics, UserSettings
from note.settings import NEW_TEST_ACTION, RESTORE_TEST_ACTION, ANSWER_ACTION, DESTROY_TEST, behaviorsClasses


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LevelForm, self).__init__(*args, **kwargs)
        self.fields['startPeriod'].widget = widgets.AdminDateWidget()
        self.fields['endPeriod'].widget = widgets.AdminDateWidget()


class SenseiForm(forms.ModelForm):
    class Meta:
        model = Sensei
        fields = '__all__'

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


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['currentLevel', 'currentHomeClassChapter', 'currentKanjiLesson']


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
        fields = '__all__'


class KanjiLessonForm(forms.ModelForm):
    class Meta:
        model = KanjiLesson
        fields = '__all__'

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
    contentName = forms.CharField(required=True, label="言葉番号範囲",
                                  widget=forms.TextInput(attrs={'placeholder': '選択した本の言葉番号範囲'}))

    class Meta:
        model = EnglishWordsChapter
        fields = ['book', 'contentName']

    def __init__(self, *args, **kwargs):
        super(EnglishWordsChapterForm, self).__init__(*args, **kwargs)
        #self.fields['date'].widget.is_required = False
        self.fields['book'].label = '本を選択してください'


class EnglishWordForm(forms.ModelForm):
    verbEng = forms.CharField(required=True, label="英語の動詞", widget=forms.TextInput(attrs={'placeholder': '英語の動詞'}))
    verbJp = forms.CharField(required=True, label="日本語の動詞", widget=forms.TextInput(attrs={'placeholder': '日本語の動詞'}))
    nounEng = forms.CharField(required=False, label="英語の名詞", widget=forms.TextInput(attrs={'placeholder': '語の名詞'}))
    nounJp = forms.CharField(required=False, label="日本語の名詞", widget=forms.TextInput(attrs={'placeholder': '日本語の名詞'}))
    adjEng = forms.CharField(required=False, label="英語の形容詞", widget=forms.TextInput(attrs={'placeholder': '英語の形容詞'}))
    adjJp = forms.CharField(required=False, label="日本語の形容詞", widget=forms.TextInput(attrs={'placeholder': '英語の形容詞'}))
    exampleEng = forms.CharField(required=True, label="英語の例", widget=forms.TextInput(attrs={'placeholder': '英語の例'}))
    exampleJp = forms.CharField(required=True, label="日本語の例", widget=forms.TextInput(attrs={'placeholder': '日本語の例'}))

    class Meta:
        model = EnglishWord
        fields = ['verbEng', 'verbJp', 'nounEng', 'nounJp', 'adjEng', 'adjJp', 'exampleEng', 'exampleJp']

    def __init__(self, *args, **kwargs):
        super(EnglishWordForm, self).__init__(*args, **kwargs)


#Admin Forms


class TestTopicAdminForm(forms.ModelForm):
    class Media:
        js = ('js/ajax.js',)

    mokChoices = ()
    questionField = forms.CharField(required=True,
                                    widget=AjaxSelectWidget(channel='fieldsLookup',
                                                            masterSelectId='id_topicCT',
                                                            choices=mokChoices,
                                                            alphanumericID=True))
    answerField = forms.CharField(required=True,
                                  widget=AjaxSelectWidget(channel='fieldsLookup',
                                                          masterSelectId='id_topicCT',
                                                          choices=mokChoices,
                                                          alphanumericID=True))
    hintField = forms.CharField(required=True,
                                widget=AjaxSelectWidget(channel='fieldsLookup',
                                                        masterSelectId='id_topicCT',
                                                        choices=mokChoices,
                                                        alphanumericID=True))

    behaviorChoices = tuple(((k,k) for k in behaviorsClasses.keys()))
    testBehaviorClass = forms.CharField(label='Choose behavior:', widget=normalWidgets.Select(choices=behaviorChoices))

    class Meta:
        model = TestTopics
        fields = '__all__'


#Forms for Training

class NewTestForm(forms.Form):
    CHOICES = TestTopics.objects.all().values_list('id', 'title')
    theme = forms.IntegerField(label='Choose test topic:', widget=normalWidgets.Select(choices=CHOICES))
    action = forms.CharField(widget=forms.HiddenInput(), initial=NEW_TEST_ACTION)


class RestoreTestForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput(), initial=RESTORE_TEST_ACTION)


class AnswerTestForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput(), initial=ANSWER_ACTION)
    answer = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Answer'}))


class RemoveTestForm(forms.Form):
    action = forms.CharField(widget=forms.HiddenInput(), initial=DESTROY_TEST)