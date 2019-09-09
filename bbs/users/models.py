from django.db import models

# Create your models here.
class User(models.Model):

    username=models.CharField(max_length=20,unique=True)
    password=models.CharField(max_length=32)

    def __str__(self):
        return self.username

    class Meta:
        db_table='tb_user'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name