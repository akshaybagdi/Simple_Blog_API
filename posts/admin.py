from django.contrib import admin
from .models.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date', 'status', 'journal', 'volume', 'website')
    search_fields = ('title', 'author__username', 'journal')
    list_filter = ('publication_date', 'status', 'journal')
