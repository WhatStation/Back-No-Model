from django.urls import path
from rate import views

app_name = 'rate'

urlpatterns = [
    path('', views.RateView.as_view(), name = 'rate'),
    path('wall/', views.RateWallView.as_view(), name = 'wall'),
]
