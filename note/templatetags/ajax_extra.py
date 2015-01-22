from django import template

register = template.Library()


@register.simple_tag
def ajax():
    """
    Inline ajax js include
    """
    return '<script type="text/javascript" src="{url}"></script>'.format(url='/incul/static/js/ajax.js')