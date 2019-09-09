from django.shortcuts import render
from django.utils import timezone
from django.views import View

# Create your views here.
from home.models import CategoryModel, ArticleModel


class IndexView(View):

    def get(self,request):
        #获取session数据
        id = request.session.get('id')
        username=request.session.get('name')
        #查询分类数据
        categories = CategoryModel.objects.filter(parent__isnull=True)

        for category in categories:
            total_count=ArticleModel.objects.filter(category=category).count()
            category.total_count=total_count

            today=timezone.localdate()
            today_count=ArticleModel.objects.filter(category=category,
                                                    publish_time__gte=today).count()
            category.today_count=today_count
        #组织上下文数据
        context = {
            'id':id,
            'username':username,
            'categories': categories
        }

        return render(request,'index.html',context=context)