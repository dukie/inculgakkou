from django.contrib import admin

# Register your models here.
from note.models import Sex, Sensei, Book, Level, Lesson, Topic, Example


class SexAdmin(admin.ModelAdmin):
    list_display = ['id', 'sexName']
    ordering = ['id']

admin.site.register(Sex, SexAdmin)


class SenseiAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullName']
    ordering = ['id']

admin.site.register(Sensei, SenseiAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']

admin.site.register(Book, BookAdmin)


class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']

admin.site.register(Level, LevelAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ['date', 'chapterNumber']
    ordering = ['date']

admin.site.register(Lesson, LessonAdmin)


class TopicAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'name', 'description']
    ordering = ['lesson', 'name']

admin.site.register(Topic, TopicAdmin)


class ExampleAdmin(admin.ModelAdmin):
    list_display = ['topic', 'kanji','furigana']
    ordering = ['topic']

admin.site.register(Example,ExampleAdmin)

