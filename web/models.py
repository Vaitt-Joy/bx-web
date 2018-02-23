from django.db import models


# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=30, verbose_name='菜单名称')
    hrefLink = models.CharField(verbose_name='跳转链接')
    allow = models.IntegerField(default=-1, verbose_name='权限')
    sort = models.IntegerField(verbose_name='排序')
    parentId = models.IntegerField(verbose_name='父节点id')
