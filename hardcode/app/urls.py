from django.urls import path
from app import views as v

app_name = 'app'

urlpatterns = [
	path('', v.index, name='index'),
	path('all/', v.get_all, name='get_all')
]