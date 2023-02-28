from django.db import models
from django.utils.timezone import datetime

class Stores(models.Model) :
    # category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank = True, null = True) # 연결된 카테고리가 사라지면 null 로 변경
    # tags = models.ManyToManyField('Tag', blank = True) # blank 랑 null 은 False 가 디폴트

    name = models.CharField('NAME', max_length=50, unique=True) # 식당이름, 비어있을수없음
    category = models.CharField('CATEGORY', max_length=50, blank=True, null=True) # 카테고리
    address = models.CharField('ADDRESS', max_length=100) # 주소지, 비어있을수없음
    star = models.FloatField('STAR', blank=True, null=True) # 평균 별점
    comment = models.CharField('COMMENT', max_length=150, blank=True, null=True) # 한줄요약
    naver_services = models.CharField('SERVICES', max_length=150, blank=True, null=True) # 네이버서비스 str
    station = models.CharField('STATION', max_length=20, blank=True, null=True) # 지하철역
    out = models.CharField('OUT', max_length=20, blank=True, null=True) # 몇출
    meter = models.FloatField('METER', blank=True, null=True) # 출구부터 거리
    lines = models.CharField('LINES', max_length=100, blank=True, null=True) # 호선
    walking_time = models.FloatField('WALKING_TIME', blank=True, null=True) # 걷는시간

    price = models.FloatField('PRICE_CLASS', blank=True, null=True) # 가성비
    cute = models.FloatField('CUTE_CLASS', blank=True, null=True) # 귀여운
    wide = models.FloatField('WIDE_CLASS', blank=True, null=True) # 넓은
    corps = models.FloatField('CORPS_CLASS', blank=True, null=True) # 단체
    satisfaction = models.FloatField('SATISFACTION_CLASS', blank=True, null=True) # 만족
    modern = models.FloatField('MODERN_CLASS', blank=True, null=True) # 모던
    ambience = models.FloatField('AMBIENCE_CLASS', blank=True, null=True) # 분위기
    visual = models.FloatField('VISUAL_CLASS', blank=True, null=True) # 비주얼
    cozy = models.FloatField('COZY_CLASS', blank=True, null=True) # 아늑
    clean = models.FloatField('CLEAN_CLASS', blank=True, null=True) # 위생
    service = models.FloatField('SERVICE_CLASS', blank=True, null=True) # 응대
    exoticfood = models.FloatField('EXOTICFOOD_CLASS', blank=True, null=True) # 이색음식
    exotictheme = models.FloatField('EXOTICTHEME_CLASS', blank=True, null=True) # 이색테마
    classic = models.FloatField('CLASSIC_CLASS', blank=True, null=True) # 클래식
    alone = models.FloatField('ALONE_CLASS', blank=True, null=True) # 혼자



    tags = models.CharField('TAGS', max_length=300, blank=True, null=True) # 태그

    def __str__(self) :
        return self.name

class Search(models.Model) :
    content = models.CharField('CONTENT', max_length=200) # 검색어, 비어있을수없음
    result_tag = models.CharField('RESULT_TAG', max_length=200, blank=True, null=True) # 검색어에 모델이 달아주는 태그 (,로 구분된 str)
    create_date = models.DateTimeField('CREATE_DATE', default=datetime.now) # 생성날짜

    @property
    def short_content(self) :
        return self.content[:10]

    def __str__(self) :
        return self.short_content

class SearchWithFeedBack(models.Model) :
    content = models.CharField('CONTENT', max_length=200) # 검색어, 비어있을수없음
    create_date = models.DateTimeField('CREATE_DATE', default=datetime.now) # 생성날짜
    thumbs = models.BooleanField('THUMBS') # 비어있을수없음

    price = models.BooleanField('PRICE_CLASS', blank=True, null=True) # 가성비
    cute = models.BooleanField('CUTE_CLASS', blank=True, null=True) # 귀여운
    wide = models.BooleanField('WIDE_CLASS', blank=True, null=True) # 넓은
    corps = models.BooleanField('CORPS_CLASS', blank=True, null=True) # 단체
    satisfaction = models.BooleanField('SATISFACTION_CLASS', blank=True, null=True) # 만족
    modern = models.BooleanField('MODERN_CLASS', blank=True, null=True) # 모던
    ambience = models.BooleanField('AMBIENCE_CLASS', blank=True, null=True) # 분위기
    visual = models.BooleanField('VISUAL_CLASS', blank=True, null=True) # 비주얼
    cozy = models.BooleanField('COZY_CLASS', blank=True, null=True) # 아늑
    clean = models.BooleanField('CLEAN_CLASS', blank=True, null=True) # 위생
    service = models.BooleanField('SERVICE_CLASS', blank=True, null=True) # 응대
    exoticfood = models.BooleanField('EXOTICFOOD_CLASS', blank=True, null=True) # 이색음식
    exotictheme = models.BooleanField('EXOTICTHEME_CLASS', blank=True, null=True) # 이색테마
    classic = models.BooleanField('CLASSIC_CLASS', blank=True, null=True) # 클래식
    alone = models.BooleanField('ALONE_CLASS', blank=True, null=True) # 혼자

    @property
    def short_content(self) :
        return self.content[:10]

    def __str__(self) :
        return self.short_content