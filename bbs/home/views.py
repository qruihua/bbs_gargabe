from django.shortcuts import render
from django.views import View

# Create your views here.


class IndexView(View):

    def get(self,request):
        #获取session数据
        id = request.session.get('id')
        username=request.session.get('name')
        #组织上下文数据
        context = {
            'id':id,
            'username':username
        }

        return render(request,'index.html',context=context)