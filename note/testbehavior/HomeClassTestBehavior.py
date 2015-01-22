from note.models import Topic, Lesson

__author__ = 'dukie'


class Behavior():
    def __init__(self):
        pass

    def getEntities(self, TestTopicObject, userSettings):
        entityClass = TestTopicObject.topicCT.model_class()
        lesson = Lesson.objects.get(level=userSettings.currentLevel, chapterNumber=userSettings.currentHomeClassChapter)
        topicsList = Topic.objects.filter(lesson=lesson)
        entQuerySet = entityClass.objects.filter(topic__in=topicsList)
        return entQuerySet