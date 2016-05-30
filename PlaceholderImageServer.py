import os
import sys

from django.conf import settings

## Read debug environment variable.
DEBUG = os.environ.get('DEBUG', 'on') == 'on'
## Generate random secret key every time the server starts
SECRET_KEY = os.environ.get('SECRET_KEY', 'coxqbwzh%-0%uw3srnbu3#mtnlpf0vj)9a14j5k+84-a$zt$+v')
## Get allowed hosts (list split by commas) from environment variable.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello world!')

application = get_wsgi_application()

urlpatterns = (
    url(r'^$', index),
)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
