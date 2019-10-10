from django.contrib import admin
from .models import *

# Register your models here.


# 用来将模型注册到admin管理界面中
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # 利用prepopulated_fields属性指定某些字段，其中对应值利用其它字段自动设置
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']    # 展示字段
    list_filter = ['available', 'created', 'updated']     # 可筛选的字段
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}