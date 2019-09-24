from django.contrib import admin
from home.models import CategoryModel,ArticleModel,CommentModel
# Register your models here.
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','parent_id']
    list_per_page = 20

class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','content','category','user','status','read_count','comments','publish_time']
    list_per_page = 20

class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id','content','article','user','parent','create_time']
    list_per_page = 20

admin.site.register(CategoryModel,CategoryModelAdmin)
admin.site.register(ArticleModel,ArticleModelAdmin)
admin.site.register(CommentModel,CommentModelAdmin)

