# Create your views here.

from django.views.generic import TemplateView
from django.http import HttpResponse
import csv
import pandas as pd
from main.models import Stores, SearchWithFeedBack
from django.forms.models import model_to_dict
from datetime import datetime

class MainView(TemplateView) :
    template_name = 'main.html'

class SearchView(TemplateView) :
    template_name = 'search.html'

class ResultView(TemplateView) :
    template_name = 'result.html'

def csv_to_db(request) :
    # 기존 내용 삭제
    delatable_objects = Stores.objects.all()[:]
    for m in delatable_objects:
        m.delete()
    print("***** 테이블 삭제 완 *****")

    df = pd.read_csv('Stores_update.csv')
    dl = df.to_dict('records')
    for di in dl :
        Stores.objects.create(**di)
        print(f"{di['name']} *** added")
    return HttpResponse('db_in_success')

def feedback_to_csv(request) :
    # SearchWithFeedBack db csv 파일로 저장
    
    search = SearchWithFeedBack.objects.all()
    dict_list = []
    for obj in search :
        obj_dict = model_to_dict(obj)
        obj_dict['create_date'] = str(obj_dict['create_date'])
        dict_list.append(obj_dict)
    df = pd.DataFrame.from_records(dict_list)
    df.to_csv(f"feedback_{datetime.now()}.csv", index=False)

    # 기존 내용 삭제
    for m in search:
        m.delete()
    print("***** 테이블 삭제 완 *****")

    return HttpResponse('feedback_to_csv success')