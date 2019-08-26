from django.conf.urls import url
from . import views

urlpatterns = [
    # 注册
    url(r'^users/register/$', views.RegisterView.as_view(), name='register'),
]