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


class ListView(View):

    def get(self,request,category_id):
        #获取当前分类
        category = CategoryModel.objects.get(pk=category_id)
        #获取当前分类的文章总数量
        total_count = ArticleModel.objects.filter(category=category).count()
        #获取今日发布文章数量
        today = timezone.localdate()
        today_count = ArticleModel.objects.filter(category=category,
                                                  publish_time__gte=today).count()
        #获取分类文章
        articles = ArticleModel.objects.filter(category=category).order_by('-publish_time')

        context = {
            'category':category,
            'total_count':total_count,
            'today_count':today_count,
            'articles':articles,
        }

        return render(request,'list.html',context=context)

