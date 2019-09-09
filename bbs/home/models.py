from django.db import models

# Create your models here.
class CategoryModel(models.Model):

    name=models.CharField(unique=True,max_length=20,verbose_name='分类名')
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='父级分类id')


    def __str__(self):
        return self.name

    class Meta:
        db_table='tb_category'
        verbose_name='分类管理'
        verbose_name_plural=verbose_name