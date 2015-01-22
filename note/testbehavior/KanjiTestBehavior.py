from note.models import Kanji

__author__ = 'dukie'


class Behavior():
    def __init__(self):
        pass

    def getEntities(self, TestTopicObject, userSettings):
        entityClass = TestTopicObject.topicCT.model_class()
        #TODO: Temporary solution for fetching all Kanji to test suit
        if userSettings.currentKanjiLesson != 0:
            kanjiSet = Kanji.objects.filter(lesson=userSettings.currentKanjiLesson)
        else:
            kanjiSet = Kanji.objects.all()
        entQuerySet = entityClass.objects.filter(relatedKanji__in=kanjiSet)
        return entQuerySet