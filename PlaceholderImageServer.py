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

from django import forms
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest

class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

def index(request):
    return HttpResponse('Hello world!')

## TODO: Add implementation.
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        return HttpResponse('Ok')
    else:
        return HttpResponseBadRequest('Invalid Image request')

application = get_wsgi_application()

urlpatterns = (
    url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
    url(r'^$', index, name='homepage'),
)

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
