from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('search/', views.ApiSearch.as_view(), name='search'),
    path('rate/', views.ApiRate.as_view(), name='rate'),
    path('rate/page/<int:page>/', views.ApiRatePage.as_view(), name='ratePage'),
    path('rate/<int:id_num>/', views.ApiRateID.as_view(), name='rateID')
]