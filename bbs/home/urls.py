from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path(r'', views.IndexView.as_view(), name='index'),
    #列表页面
    path(r'<int:category_id>/', views.ListView.as_view(), name='list'),
    #发帖页面
    path('publish/', views.PublishView.as_view(), name='publish'),
    #详情页面
    path('detail/<int:id>/',views.DetailView.as_view(),name='detail'),
]