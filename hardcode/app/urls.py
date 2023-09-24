from django.urls import path
from app import views as v

app_name = 'app'

urlpatterns = [
	path('', v.index, name='index'),
	path('all/', v.get_all, name='get_all'),
	path('product/', v.get_all_from_product, name='get_all_from_product'),
	path('statistic/', v.statistic, name='statistic')
]