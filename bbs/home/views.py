from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

# Create your views here.
from home.models import CategoryModel, ArticleModel, CommentModel


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

        current_page = request.GET.get('page')
        if current_page is None:
            current_page = 1

        category = CategoryModel.objects.get(pk=category_id)

        total_count = ArticleModel.objects.filter(category=category).count()

        today = timezone.localdate()
        today_count = ArticleModel.objects.filter(category=category,
                                                  publish_time__gte=today).count()

        articles = ArticleModel.objects.filter(category=category).order_by('-publish_time')

        for article in articles:
            comments = CommentModel.objects.filter(article=article).order_by('-create_time')
            cm = comments.first()
            if cm is not None:
                article.last_comment_time = cm.create_time
            else:
                article.last_comment_time = '暂无回复'

            article.comments = len(comments)
            article.save()

        hot_articles = ArticleModel.objects.filter(category=category).order_by('-comments')[:3]

        pagination = Paginator(articles, per_page=5)
        current_articles = pagination.get_page(current_page)
        page_num = current_page
        total_page = pagination.num_pages

        context = {
            'category': category,
            'total_count': total_count,
            'today_count': today_count,
            'articles': current_articles,
            'hot_articles': hot_articles,
            'page_num': page_num,
            'total_page': total_page,
            'id':request.session.get('id'),
            'username':request.session.get('name')
        }

        return render(request,'list.html',context=context)

class PublishView(View):

    def get(self,request):
        category_id = request.GET.get('category_id')
        try:
            category = CategoryModel.objects.get(pk=category_id)
        except CategoryModel.DoesNotExist:
            return render(request, '404.html')

        #查询分类信息
        categories=CategoryModel.objects.all()
        #组织上下文
        context={
            'category':category,
            'categories':categories,
            'id':request.session.get('id'),
            'username':request.session.get('name')
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
            return render(request, '404.html')

        try:
            category = CategoryModel.objects.get(pk=category_id)
        except CategoryModel.DoesNotExist:
            return render(request, '404.html')

        article = ArticleModel.objects.create(
            title=title,
            content=content,
            category=category,
            user_id=user_id
        )
        return redirect(reverse('home:list',kwargs={'category_id':category_id}))

class DetailView(View):

    def get(self,request,id):

        current_page = request.GET.get('page')
        if current_page is None:
            current_page = 1

        try:
            article=ArticleModel.objects.get(pk=id)
        except ArticleModel.DoesNotExist:
            return render(request,'404.html')
        else:
            article.read_count+=1
            article.save()

        comments=CommentModel.objects.filter(article=article).order_by('create_time')
        i=0
        for comment in comments:
            i+=1
            comment.floor=i

        pagination = Paginator(comments, per_page=5)
        current_comments = pagination.get_page(current_page)
        page_num = current_page
        total_page = pagination.num_pages

        context = {
            'article':article,
            'comments':current_comments,
            'page_num':page_num,
            'total_page':total_page,
            'id':request.session.get('id'),
            'username':request.session.get('name')
        }

        return render(request,'show.html',context=context)

class ReplyView(View):

    def get(self,request):

        article_id=request.GET.get('article_id')

        article=ArticleModel.objects.get(pk=article_id)

        context = {
            'article':article,
            'id':request.session.get('id'),
            'username':request.session.get('name')
        }

        return render(request,'reply.html',context=context)

    def post(self, request):

        article_id = request.GET.get('article_id')
        content = request.POST.get('content')

        user_id=request.session.get('id')
        if user_id is None:
            return redirect(reverse('users:login'))

        try:
            article = ArticleModel.objects.get(pk=article_id)
        except ArticleModel.DoesNotExist:
            return render(request, '404.html')

        CommentModel.objects.create(
            content=content,
            article=article,
            user_id=user_id
        )

        return redirect(reverse('home:detail', kwargs={'id': article_id}))

class QuoteView(View):

    def get(self,request):

        comment_id=request.GET.get('comment_id')

        try:
            comment=CommentModel.objects.get(pk=comment_id)
        except CommentModel.DoesNotExist:
            return render(request,'404.html')

        context = {
            'comment':comment,
            'id': request.session.get('id'),
            'username': request.session.get('name')
        }

        return render(request,'quote.html',context)

    def post(self,request):

        user_id = request.session.get('id')
        if user_id is None:
            return redirect(reverse('users:login'))

        comment_id=request.GET.get('comment_id')
        content=request.POST.get('content')
        try:
            comment = CommentModel.objects.get(pk=comment_id)
        except CommentModel.DoesNotExist:
            return render(request, '404.html')

        CommentModel.objects.create(
            content=content,
            article=comment.article,
            user_id=user_id,
            parent=comment
        )

        return redirect(reverse('home:detail',args=str(comment.article.id)))