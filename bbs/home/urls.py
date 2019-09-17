from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path(r'', views.IndexView.as_view(), name='index'),
    #列表页面
    path(r'<category_id>/', views.ListView.as_view(), name='list'),

]