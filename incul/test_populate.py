
#Populate test DB from fixture
from django.core.management import call_command
call_command('loaddata', 'test_data.json', verbosity=0)
