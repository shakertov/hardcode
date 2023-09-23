from django.db import models


class UserModel(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)


class ProductModel(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	owner = models.ForeignKey(
		'UserModel',
		on_delete=models.CASCADE,
		related_name='products'
	)
	lessons = models.ManyToManyField(
		'LessonModel',
		through='LessonProductModel',
		related_name='products'
	)
	access = models.ManyToManyField(
		'UserModel',
		through='AccessModel'
	)


class LessonModel(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	link = models.SlugField()
	duration = models.DurationField()
	views = models.ManyToManyField(
		'UserModel',
		through='ViewsModel'
	)


class LessonProductModel(models.Model):
	product = models.ForeignKey(
		'ProductModel',
		on_delete=models.CASCADE,
		related_name='plm'
	)
	lesson = models.ForeignKey(
		'LessonModel',
		on_delete=models.CASCADE,
		related_name='plm'
	)


class AccessModel(models.Model):
	user = models.ForeignKey(
		'UserModel',
		on_delete=models.CASCADE,
		related_name='acc'
	)
	product = models.ForeignKey(
		'ProductModel',
		on_delete=models.CASCADE,
		related_name='acc'
	)
	value = models.BooleanField(
		default=False
	)


class ViewsModel(models.Model):
	user = models.ForeignKey(
		'UserModel',
		on_delete=models.CASCADE,
		related_name='vws'
	)
	lesson = models.ForeignKey(
		'LessonModel',
		on_delete=models.CASCADE,
		related_name='vws'
	)
	duration = models.DurationField()
	date = models.DateTimeField(auto_now_add=True)
