import hashlib

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from users.models import User


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')

    def post(self,request):
        """
        1.获取请求数据
        2.验证请求数据
        3.保存用户信息
        4.设置登陆状态
        5.返回相应
        """
        # 1.获取请求数据
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # 2.验证请求数据
        if not all([username,password1,password2]):
            context = {
                'username':username,
                'password1':password1,
                'password2':password2,
                'errmsg':'参数不全'
            }
            return render(request,'register.html',context=context)
        # 3.保存用户信息
        try:
            user = User.objects.create(
                username=username,
                password=hashlib.md5(password1.encode()).hexdigest()
            )
        except Exception as e:
            context = {
                'username': username,
                'password1': password1,
                'password2': password2,
                'errmsg': '创建失败'
            }
            return render(request,'register.html',context=context)
        # 4.设置登陆状态
        request.session['id'] = user.id
        request.session['name'] = user.username
        # 5.返回相应
        return redirect(reverse('home:index'))
