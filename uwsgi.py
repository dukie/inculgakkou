import os
#import newrelic.agent
#newrelic.agent.initialize('/tmp/newrelic/newrelic.ini')
#substitute mysite with the name of your project !!!
os.environ['DJANGO_SETTINGS_MODULE'] = 'incul.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
