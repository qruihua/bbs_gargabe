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

class ArticleModel(models.Model):

    StatusEnum = (
        (0,'未审核'),
        (1,'已审核'),
        (2,'已下架'),
    )

    title=models.CharField(max_length=50)
    content=models.TextField()
    category=models.ForeignKey(CategoryModel,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey('users.User',on_delete=models.SET_NULL,null=True)
    publish_time=models.DateTimeField(auto_now_add=True)
    status=models.SmallIntegerField(choices=StatusEnum,default=0)
    read_count=models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table='tb_article'
        verbose_name = '文章管理'
        verbose_name_plural = verbose_name

class CommentModel(models.Model):

    content=models.TextField()
    article=models.ForeignKey(ArticleModel,on_delete=models.SET_NULL,null=True)
    user=models.ForeignKey('users.User',on_delete=models.SET_NULL,null=True)
    create_time=models.DateTimeField(auto_now_add=True)
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.article.title

    class Meta:
        db_table='tb_comment'
        verbose_name = '评论管理'
        verbose_name_plural = verbose_name