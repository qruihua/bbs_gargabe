from django.urls import path
from . import views

urlpatterns = [
    # 注册
    path(r'', views.IndexView.as_view(), name='index'),
]