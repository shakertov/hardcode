from django.shortcuts import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.models import ProductModel, UserModel

def index(request):
	return HttpResponse('sdfsdf', 200)

@api_view(['GET', 'POST'])
def get_all(request):
	"""
	Отдаёт пользователю список всех уроков,
	к которому имеет доступ. Получает от
	пользователя его ID методом POST
	"""
	if request.method == 'POST':
		try:
			user = UserModel.objects.get(id=3)
			products = ProductModel.objects.filter(acc__user_id=user.id, acc__value=True)
			data = {
				'ID': 'ID пользователя ' + str(request.data['ID']),
				'DATA': str(products)
			}
			return Response(data, status=status.HTTP_200_OK)
		except KeyError:
			return Response(
				{'error': 'Необходимо отправить идентификатор пользователя'},
				status=status.HTTP_401_UNAUTHORIZED
			)
	data = {
		'error': 'Необходимо отправить идентификатор пользователя'
	}
	return Response(data, status=status.HTTP_401_UNAUTHORIZED)

def get_all_from_product(request):
	"""
	Отдает пользователю список всех уроков
	доступного ему продукта.
	Получает от пользователя его ID и
	идентификатор продукта PRODUCT ID.
	"""

def statistic(request):
	"""
	Отдает пользователю статистику
	по всей платформе
	"""