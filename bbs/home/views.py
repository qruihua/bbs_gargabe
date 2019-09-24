from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
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

class PublishView(View):

    def get(self,request):
        #查询分类信息
        categories=CategoryModel.objects.all()
        #组织上下文
        context={
            'categories':categories
        }
        #模板数据渲染
        return render(request,'publish.html',context=context)

    def post(self, request):

        user_id = request.session.get('id')
        if user_id is None:
            return redirect(reverse('users:login'))

        category_id = request.POST.get('category_id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not all([category_id, title, content]):
            return render(request, 'publish.html', context={'参数不全'})

        try:
            category = CategoryModel.objects.get(pk=category_id)
        except CategoryModel.DoesNotExist:
            return render(request, 'publish.html', context={'参数不正确'})

        article = ArticleModel.objects.create(
            title=title,
            content=content,
            category=category,
            user_id=user_id
        )
        return redirect(reverse('home:list',kwargs={'category_id':category_id}))