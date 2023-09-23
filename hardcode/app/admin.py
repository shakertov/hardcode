from django.contrib import admin
from app.models import (
	UserModel,
	ProductModel,
	LessonModel,
	AccessModel,
	ViewsModel,
	LessonProductModel
)

@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'owner']

@admin.register(LessonModel)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'link', 'duration']

@admin.register(AccessModel)
class AccessModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'value']

@admin.register(ViewsModel)
class ViewsModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'duration']

@admin.register(LessonProductModel)
class LessonProductModelAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'product']