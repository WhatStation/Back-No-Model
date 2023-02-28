from django.contrib import admin

from .models import Stores, Search, SearchWithFeedBack

# Register your models here.
admin.site.register(Stores)
admin.site.register(Search)
admin.site.register(SearchWithFeedBack)