from django.contrib import admin

from .models import Book, Comment

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'is_active', 'recommended', 'datetime_created',)