# Create your views here.

from django.views.generic import TemplateView

class RateView(TemplateView) :
    template_name = 'rate/rate.html'

class RateWallView(TemplateView) :
    template_name = 'rate/wall.html'
