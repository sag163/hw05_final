from django.contrib import admin
from posts.models import Comment

from .models import Post, Group
class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author") 
    search_fields = ("text",) 
    list_filter = ("pub_date",)
    empty_value_display = '-пусто-'

class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description")
    list_filter = ("title",)
    empty_value_display = '-пусто-'    

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'post', 'author', 'text', 'created')
    list_filter = ('author',)
    search_fields = ('author', 'created')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)

