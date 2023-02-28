from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.MainView.as_view(), name = 'main'),
    path('search/', views.SearchView.as_view(), name = 'search'),
    path('result/', views.ResultView.as_view(), name = 'result'),

    path('stores_table_csv_to_db/', views.csv_to_db, name = 'csv_to_db'),
    path('feedback_to_csv/', views.feedback_to_csv, name = 'feedback_to_csv'),
    
]
