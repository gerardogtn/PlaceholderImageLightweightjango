import hashlib
import os
import sys

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)

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
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
    ),
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        },
    ),
    STATICFILES_DIRS=(
        os.path.join(BASE_DIR, 'static'),
    ),
    STATIC_URL='/static/',
)

from io import BytesIO
from PIL import Image, ImageDraw
from django import forms
from django.conf.urls import url
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        image = Image.new('RGB', (width, height))
        content = BytesIO()
        self.drawText(width, height, image)
        image.save(content, image_format)
        content.seek(0)
        self.addCaching(width, height, image_format, content)
        return content

    def drawText(self, width, height, image):
        draw = ImageDraw.Draw(image)
        text = '{} x {}'.format(width, height)
        textWidth, textHeight = draw.textsize(text)
        if (textWidth < width and textHeight < height):
            leftCoor = (width - textWidth) // 2
            topCoor = (height - textHeight) // 2
            draw.text((leftCoor, topCoor), text, fill=(255, 255, 255))

    def addCaching(self, width, height, image_format, content):
        key = '{}.{}.{}'.format(width, height, image_format)
        HOUR_LENGTH = 60*60
        cache.set(key, content, HOUR_LENGTH)

def index(request):
    example = reverse('placeholder', kwargs={'width': 50, 'height': 50})
    context = {
        'example': request.build_absolute_uri(example)
    }
    return render(request, 'home.html', context)

## TODO: Add implementation.
def placeholder(request, width, height):
    form = ImageForm({'height': height, 'width': width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
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
