from django.shortcuts import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app.models import ProductModel, UserModel
from app.serializers import ProductSerializer, LessonSerializer, ListProductsSerializer

def index(request):
	return HttpResponse('Привет! Это API приложение!', 200)

@api_view(['GET', 'POST'])
def get_all(request):
	"""
	Отдаёт пользователю список всех уроков,
	к которому имеет доступ. Получает от
	пользователя его ID методом POST
	"""
	if request.method == 'POST':
		try:
			user_id = request.data['ID_U']
			user = UserModel.objects.get(id=user_id)
			products = ProductModel.objects.filter(acc__user_id=user.id, acc__value=True)
			products = ProductSerializer(products, many=True, context={'request': request})
			return Response(products.data, status=status.HTTP_200_OK)
		except KeyError:
			return Response(
				{'error': 'Необходимо отправить идентификатор пользователя'},
				status=status.HTTP_401_UNAUTHORIZED
			)
		except UserModel.DoesNotExist:
			return Response(
				{'error': 'Такого пользователя не существует'},
				status=status.HTTP_404_NOT_FOUND
			)

	data = {
		'error': 'Необходимо отправить идентификатор пользователя'
	}
	return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def get_all_from_product(request):
	"""
	Отдает пользователю список всех уроков
	доступного ему продукта.
	Получает от пользователя его ID и
	идентификатор продукта PRODUCT ID.
	"""
	if request.method == 'POST':
		try:
			user_id = request.data['ID_U']
			product_id = request.data['ID_P']
			user = UserModel.objects.get(id=user_id)
			lessons = ProductModel.objects.get(id=product_id, acc__user_id=user.id, acc__value=True).lessons
			lessons = LessonSerializer(lessons, many=True, context={'request': request})
			return Response(lessons.data, status=status.HTTP_200_OK)
		except KeyError:
			return Response(
				{'error': 'Необходимо отправить идентификатор пользователя и идентификатор продукта'},
				status=status.HTTP_401_UNAUTHORIZED
			)
		except UserModel.DoesNotExist:
			return Response(
				{'error': 'Такого пользователя не существует'},
				status=status.HTTP_404_NOT_FOUND
			)
		except ProductModel.DoesNotExist:
			return Response(
				{'error': 'Такого продукта не существует или у пользователя нет доступа к нему'},
				status=status.HTTP_404_NOT_FOUND
			)

	data = {
		'error': 'Необходимо отправить идентификатор пользователя и идентификатор продукта'
	}
	return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def statistic(request):
	"""
	Отдает пользователю статистику
	по всей платформе
	"""
	products = ProductModel.objects.all()
	products = ListProductsSerializer(products, many=True)
	return Response(products.data, status.HTTP_200_OK)