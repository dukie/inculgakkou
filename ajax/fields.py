from ajax_select import get_lookup
from django.core.urlresolvers import reverse
from django.forms.widgets import Select
from django.template.defaultfilters import force_escape
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

try:
    import json
except ImportError:
    from django.utils import simplejson as json


def plugin_options(channel, channel_name, widget_plugin_options, initial):
    """ Make a JSON dumped dict of all options for the jquery ui plugin itself """
    po = {}
    if initial:
        po['initial'] = initial
    po.update(getattr(channel, 'plugin_options', {}))
    po.update(widget_plugin_options)
    if not po.get('min_length'):
        # backward compatibility: honor the channel's min_length attribute
        # will deprecate that some day and prefer to use plugin_options
        po['min_length'] = getattr(channel, 'min_length', 1)
    if not po.get('source'):
        po['source'] = reverse('ajax_lookup', kwargs={'channel': channel_name})

    # allow html unless explicitly false
    if po.get('html') is None:
        po['html'] = True

    return {
            'plugin_options': mark_safe(json.dumps(po)),
            'data_plugin_options': force_escape(json.dumps(po)),
            'lookup_url': po['source'],
            'min_length': po['min_length']
            }


class AjaxSelectWidget(Select):

    #  Widget bounded to another select threw ajax

    add_link = None

    def __init__(self,
                 channel,
                 masterSelectId,
                 choices=(),
                 attrs=None, alphanumericID=False):
        self.plugin_options={}
        super(AjaxSelectWidget, self).__init__(attrs, choices)
        self.channel = channel
        self.masterSelectId = masterSelectId
        self.alphanumericID = alphanumericID

    def render(self, name, value, attrs=None, choices=()):

        if self.alphanumericID:
            value = ''
        else:
            value = '' or value

        finalAttributes = self.build_attrs(attrs)
        self.html_id = finalAttributes.pop('id', name)

        current_repr = ''
        initial = None
        lookup = get_lookup(self.channel)
        if value:
            print(value)
            objects = lookup.get_objects([value])
            try:
                obj = objects[0]
            except IndexError:
                raise Exception("{0} cannot find object:{1]".format(lookup, value))
            current_repr = lookup.format_item_display(obj)
            initial = [current_repr, obj.pk]
        options = self.render_options(choices, [value])

        context = {
            'name': name,
            'html_id': self.html_id,
            'current_id': value,
            'current_repr': current_repr,
            'func_slug': self.html_id.replace("-", ""),
            'add_link': self.add_link,
            'options': mark_safe(options),
        }
        self.plugin_options['masterSelectId'] = self.masterSelectId
        self.plugin_options['boundSelectId'] = self.html_id
        context.update(plugin_options(lookup, self.channel, self.plugin_options, initial))

        return mark_safe(render_to_string("ajaxFields/selectWidget.html", context))

    def value_from_datadict(self, data, files, name):
        got = data.get(name, None)
        try:
            return int(got)
        except ValueError:
            return got

    def id_for_label(self, id_):
        return '%s' % id_

