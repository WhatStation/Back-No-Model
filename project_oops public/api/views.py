from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from main.models import Search, SearchWithFeedBack
from rate.models import Rate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from api.apps import SearchConfig
import pandas as pd
from config import CFG
import torch


# from blog.models import Post
# from api.utils import obj_to_post # 시리얼라이저

class ApiSearch(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiSearch, self).dispatch(request, *args, **kwargs)
    
    def post(self, request) :
        """
        로드 되어있는 모델과 식당 정보를 이용
        사용자 인풋 -> 모델 -> 식당정보와 연산해서 정렬 -> 식당정보 top 5 리턴?
        사용자 인풋 db에 저장
        """

        r_dict = json.loads(request.body)
        
        # request json 형식 확인
        if not set(r_dict.keys()) == set(['search']) : 
            print(r_dict.keys())
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400) # status Bad Request

        # 입력 문장
        search=r_dict['search']
   
        # input에 대한 모델 연산

        vectorized = SearchConfig.s_bert.encode(search).reshape((1, -1))
        result = SearchConfig.classifier(torch.Tensor(vectorized))
        result = torch.sigmoid(result)
        result = result.cpu().detach().numpy()

        res = pd.DataFrame(result, columns=CFG.CLASS_NAMES).T
        res = res.rename(columns={0: 'Probability'})
        tagged_store = SearchConfig.tagged_store
        convert_col = dict(zip(tagged_store.iloc[:, -16:-1].columns, CFG.CLASS_NAMES))
        tagged_store = tagged_store.rename(columns=convert_col)

        store_tag_prob = pd.concat([tagged_store['name'], tagged_store.iloc[:, -16:-1] * res['Probability']], axis=1)
        store_tag_prob['sum'] = store_tag_prob.iloc[:, -16:-1].sum(axis=1, numeric_only=True)


        tags = res[res['Probability']>0.5].index # 이건 이대로 괜찮은가
        tag_change = {'가성비':'#가성비있는',
         '귀여운':'#귀여운',
         '넓은':'#넓은',
         '단체':'#단체모임',
         '만족':'#만족도가높은',
         '모던':'#모던한',
         '분위기':'#분위기있는',
         '비주얼':'#비주얼이좋은',
         '아늑':'#아늑한',
         '위생':'#깔끔한',
         '응대':'#서비스가좋은',
         '이색음식':'#음식이 특이한',
         '이색테마':'#이색테마인',
         '클래식':'#고급스러운',
         '혼자':'#혼자오기좋은'}
        
        lat_long = {
            '가좌역':[37.568782058, 126.914762449],
            '경의중앙 신촌역':[37.559901686, 126.942906303],
            '망원역':[37.556034031, 126.910131170],
            '상수역':[37.547767159, 126.922543620],
            '서강대역':[37.552502661, 126.934998613],
            '신촌역':[37.555184166, 126.936910322],
            '이대역':[37.556797076, 126.946268566],
            '합정역':[37.550061507, 126.914638072],
            '홍대입구역':[37.556739534, 126.923599596]
        }
        
        # print(f"{', '.join(tags)} 태그를 가진 식당들을 보여줍니다")
        input_tags = list(tags)
        changed_tags = []
        for t in input_tags :
            changed_tags.append(tag_change[t])

        print(f"검색어 : {search}")
        if len(tags) == 0:
            print("태그 없음")
            return HttpResponse('NO TAGS. DETAILED INPUT REQUIRED', status = 321)


        # if store_tag_prob['sum'].max() < 1: # 이거 수치 조정이 좀 필요
        #     print("좀 더 자세한 분위기가 나타나게 작성해주세요!")
        #     return HttpResponse('DETAILED INPUT REQUIRED', status = 321)
            
        store_tag_prob = store_tag_prob.sort_values('sum', ascending=False)
        store_tag_prob = store_tag_prob.T.iloc[:, :5]

        store_tag_prob.columns = store_tag_prob.iloc[0]
        store_tag_prob = store_tag_prob.drop(store_tag_prob.index[0])
        top_5_store_name = list(store_tag_prob.columns)
        main_store_dict = (tagged_store[tagged_store['name'] == top_5_store_name[0]]).to_dict('records')[0]

        latlong = lat_long[main_store_dict['station']]
        res_dict = {
            "result_tags" : changed_tags,
            "main_store" : {
                "name" : main_store_dict['name'],
                "station" : main_store_dict['station'],
                "line" : main_store_dict["lines"].split(','),
                "tags" : main_store_dict["tags"].split(','),
                "walking_time" : main_store_dict["walking_time"]
            },
            "sub_stores" : top_5_store_name[1:],
            "lat" : latlong[0],
            "long" : latlong[1],
        }
        print(changed_tags)
        # print(res_dict)

        new_search = { 'content' : search,
                       'result_tag' : ','.join(input_tags)}
        Search.objects.create(**new_search)

        return JsonResponse(data = res_dict, safe = True, status = 200)
    
    def put(self, request) :
        """
        평가 받은 리뷰들을 따로 한번 더 저장
        """
        r_dict = json.loads(request.body)

        column_list = ['price','cute','wide','corps','satisfaction','modern','ambience','visual','cozy','clean','service','exoticfood','exotictheme','classic','alone']
        
        # request json 형식 확인
        if not set(r_dict.keys()) == set(['search', 'thumbs_up']+column_list) : 
            print(r_dict.keys())
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400) # status Bad Request

        # db 저장
        try :
            new_search = { 'content' : r_dict['search'],'thumbs': r_dict['thumbs_up']}
            for c in column_list :
                new_search[c] = r_dict[c]
            SearchWithFeedBack.objects.create(**new_search)
            return JsonResponse(data = {'success':True}, safe = True, status = 200)
        except :
            return JsonResponse(data = {'success':False}, safe = True, status = 400)



class ApiRate(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRate, self).dispatch(request, *args, **kwargs)

    def get(self, request) :
        """
        코멘트 전부다 모아서 list 로 뭉쳐서 반환
        """
        rate_objs = Rate.objects.all()
        res_list = []
        for obj in rate_objs[::-1] :
            temp = model_to_dict(obj)
            del temp['password']
            res_list.append(temp)
        return JsonResponse(data = { "comments" :res_list }, status = 200)


    def post(self, request) :
        """
        입력 받은 코멘트 정보 저장, 성공 여부 반환
        """
        r_dict = json.loads(request.body)

        if not set(r_dict.keys()) == set(['rating','comment','password']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        try :
            Rate.objects.create(**r_dict)
            success = True
        except :
            success = False
        return JsonResponse(data = {'success' : success}, status = 200)


class ApiRatePage(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRatePage, self).dispatch(request, *args, **kwargs)

    def get(self, request, page) :
        """
        페이지네이션
        """
        rate_objs = Rate.objects.all()
        end_page = (len(rate_objs)+5)//8
        paginator = Paginator(rate_objs, 8)
        objs = paginator.get_page(page)
        res_list = []
        for obj in objs :
            temp = model_to_dict(obj) 
            del temp['password']
            res_list.append(temp)
        return JsonResponse(data = { "end_page":end_page, "comments":res_list }, status = 200)

class ApiRateID(View) :
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs): 
        return super(ApiRateID, self).dispatch(request, *args, **kwargs)

    def post(self, request, id_num) :
        """
        id_num 번 코멘트 삭제 요청
        """

        # url id 가 존재하는지 확인
        try :
            m = Rate.objects.get(id=id_num)
        except :
            return HttpResponse("WRONG ID", status = 400)

        r_dict = json.loads(request.body)
        # request 형식 체크
        if not set(r_dict.keys()) == set(['password']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        # 비밀번호 일치 체크해서 삭제
        if m.password == r_dict['password'] :
            m.delete()
            correct = True
        else : correct = False

        return JsonResponse(data = {'delete_success' : correct}, status = 200)


    def put(self, request, id_num) :
        """
        id_num 번 코멘트 수정 요청
        """
        # url id 가 존재하는지 확인
        try :
            m = Rate.objects.get(id=id_num)
        except :
            return HttpResponse("WRONG ID", status = 400)

        r_dict = json.loads(request.body)
        # request 형식 체크
        if not set(r_dict.keys()) == set(['password','comment']) :
            return HttpResponse('REQUEST JSON FIELD ERROR', status = 400)

        # 비밀번호 일치 체크해서 수정
        if m.password == r_dict['password'] :
            m.comment = r_dict['comment']
            m.save()
            correct = True
        else : correct = False

        return JsonResponse(data = {'modify_success' : correct}, status = 200)
