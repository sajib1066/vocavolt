from django.contrib import admin

from .models import Category, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'slug', 'is_active', 'created_at', 'updated_at'
    ]
    list_filter = ['is_active']
    search_fields = ['name', 'slug']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'slug', 'is_active', 'view_count', 'like_count',
        'created_at', 'updated_at'
    ]
    list_filter = ['is_active']
    search_fields = ['title', 'slug']