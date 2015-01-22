from ajax_select import LookupChannel
from django.contrib.contenttypes.models import ContentType
from note.models import UserSettings


class FieldsResponseObject(object):
    def __init__(self, pk, name, value):
        self.pk = pk
        self.value = value
        self.name = name


class TestElementsFieldsLookup(LookupChannel):

    model = ContentType

    def get_query(self, q, request):
        ct = ContentType.objects.get(pk=q)
        fieldsList = ct.model_class()._meta.get_all_field_names()
        res = list()
        for x in range(len(fieldsList)):
            res.append(FieldsResponseObject(fieldsList[x], fieldsList[x], fieldsList[x]))
        return res

    def get_result(self,obj):
        return obj.value

    def format_match(self,obj):
        return self.format_item_display(obj.name)

    def format_item_display(self,obj):
        return "{0}".format(obj)

    def get_objects(self, ids):
        return None


class SettingsFieldsLookup(LookupChannel):

    model = ContentType

    def get_query(self, q, request):
        fieldsList = UserSettings._meta.get_all_field_names()
        res = list()
        for x in range(len(fieldsList)):
            res.append(FieldsResponseObject(fieldsList[x], fieldsList[x], fieldsList[x]))
        return res

    def get_result(self,obj):
        return obj.value

    def format_match(self,obj):
        return self.format_item_display(obj.name)

    def format_item_display(self,obj):
        return "{0}".format(obj)

    def get_objects(self, ids):
        return None