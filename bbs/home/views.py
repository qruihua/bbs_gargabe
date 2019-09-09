from django.shortcuts import render
from django.views import View

# Create your views here.
from home.models import CategoryModel


class IndexView(View):

    def get(self,request):
        #获取session数据
        id = request.session.get('id')
        username=request.session.get('name')
        #查询分类数据
        categories = CategoryModel.objects.filter(parent__isnull=True)

        #组织上下文数据
        context = {
            'id':id,
            'username':username,
            'categories': categories
        }

        return render(request,'index.html',context=context)