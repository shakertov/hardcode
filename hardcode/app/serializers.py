from rest_framework import serializers
from app.models import ProductModel, LessonModel, ViewsModel


class LessonSerializer(serializers.ModelSerializer):
	status = serializers.SerializerMethodField()
	last_seen = serializers.SerializerMethodField()
	class Meta:
		model = LessonModel
		fields = ['title', 'description', 'link', 'duration', 'status', 'last_seen']

	def get_status(self, obj):
		request = self.context.get('request')
		if request and hasattr(request, 'data'):
			data = request.data
			try:
				view = ViewsModel.objects.get(user_id=data['ID_U'], lesson_id=obj.id)
				duration_coefficient = view.duration.total_seconds() / obj.duration.total_seconds()
				if duration_coefficient > 0.8:
					return 'Просмотрено'
				else:
					return 'Не просмотрено'
			except ViewsModel.DoesNotExist:
				return 'Нет данных'
		return 'Нет данных'

	def get_last_seen(self, obj):
		request = self.context.get('request')
		if request and hasattr(request, 'data'):
			data = request.data
			try:
				view = ViewsModel.objects.get(user_id=data['ID_U'], lesson_id=obj.id)
				if view.date:
					return view.date
			except ViewsModel.DoesNotExist:
				return 'Нет данных'
		return 'Нет данных'



class ProductSerializer(serializers.ModelSerializer):
	lessons = LessonSerializer(read_only=True, many=True)
	class Meta:
		model = ProductModel
		fields = ['title', 'description', 'lessons']


class ListProductsSerializer(serializers.ModelSerializer):
	total_views = 0
	total_duration = 0
	total_students = 0
	total_purchase = 0

	class Meta:
		model = ProductModel
		fields = ['title', 'description', 'total_views', 'total_duration', 'total_students', 'total_purchase']

	def get_total_views(self, obj):
		pass
	
