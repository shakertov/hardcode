from rest_framework import serializers
from app.models import ProductModel, LessonModel, ViewsModel, UserModel
from django.db.models import Sum
import datetime

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
		fields = ['id', 'title', 'description', 'lessons']


class ListProductsSerializer(serializers.ModelSerializer):
	total_views = serializers.SerializerMethodField()
	total_duration = serializers.SerializerMethodField()
	total_students = serializers.SerializerMethodField()
	total_purchase = serializers.SerializerMethodField()

	class Meta:
		model = ProductModel
		fields = ['id', 'title', 'description', 'total_views', 'total_duration', 'total_students', 'total_purchase']

	def get_total_views(self, obj):
		views = 0
		for lesson in obj.lessons.all():
			views += lesson.views.count()
		return views

	def get_total_duration(self, obj):
		duration = 0
		for lesson in obj.lessons.all():
			for v in lesson.vws.all():
				duration += v.duration.total_seconds()
		return str(datetime.timedelta(seconds=duration))

	def get_total_students(self, obj):
		students = obj.access.count()
		return students

	def get_total_purchase(self, obj):
		users_all_amount = UserModel.objects.count()
		students = obj.access.count()
		try:
			total_purchase = students / users_all_amount
		except ZeroDivisionError:
			return 0
		return str(total_purchase * 100) + ' %'

