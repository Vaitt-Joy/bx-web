# coding=utf-8
from django.db import models


# Create your models here.

class Menu(models.Model):
    """
    菜单信息
    """
    name = models.CharField(max_length=30, verbose_name='菜单名称')
    hrefLink = models.CharField(verbose_name='跳转链接', max_length=255)
    allow = models.IntegerField(default=-1, verbose_name='权限')
    sort = models.IntegerField(verbose_name='排序')
    parentId = models.IntegerField(verbose_name='父节点id')
    menuNumber = models.IntegerField(verbose_name='节点层级', default=1)

    createTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True, editable=False)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)


# Create your models here.
class Account(models.Model):
    """
    用户信息
    """

    class Meta:
        db_table = "account"

    user_type_choice = (
        (0, u'超级管理员'),
        (1, u'开发人员'),
        (2, u'测试人员'),
        (3, u'业主'),
        (4, u'业主测试'),
        (5, u'other'),
    )
    username = models.CharField(verbose_name='用户账号', max_length=30, unique=True)
    password = models.CharField(verbose_name='用户密码', max_length=255)
    email = models.EmailField(verbose_name='邮箱', null=True, blank=True)
    user_type = models.IntegerField(choices=user_type_choice, default=4, verbose_name='用户类型')
    nickName = models.CharField(verbose_name='用户昵称', max_length=30, default='')
    code = models.CharField(verbose_name='邀请码', max_length=30, default='')

    lastIp = models.CharField(max_length=30, default='')

    createTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True, editable=False)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __unicode__(self):
        return self.nickName


class YeZhuInfo(models.Model):
    """业主信息"""

    class Meta:
        db_table = "yezhuinfo"

    name = models.CharField(verbose_name='业主名称', max_length=30)
    website = models.CharField(verbose_name='website', max_length=20, unique=True)
    s3_access_id = models.CharField(verbose_name='s3 s3_access_id', max_length=100, default='')
    s3_access_key = models.CharField(verbose_name='s3 s3_access_key', max_length=130, default='')
    s3_access_url = models.CharField(verbose_name='s3 s3_access_url', max_length=130, default='')
    jiguang_accout = models.CharField(verbose_name='jiguang_accout', max_length=130, default='')
    jiguang_pwd = models.CharField(verbose_name='jiguang_pwd', max_length=130, default='')

    createTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True, editable=False)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    def __unicode__(self):
        return self.name


# Create your models here.

class AppInfo(models.Model):
    """app 信息"""

    class Meta:
        db_table = "appInfo"

    yezhuId = models.IntegerField(default=-1)
    appName = models.CharField(max_length=50)
    appId = models.CharField(max_length=50)
    logoImg = models.FileField(upload_to='upload/%Y/%m/%d', verbose_name='logo 图', blank=False)
    startImg = models.FileField(upload_to='upload/%Y/%m/%d', verbose_name='start 图', blank=False)

    createTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True, editable=False)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)


class AppUpdateLog(models.Model):
    """app 或者插件升级log"""

    class Meta:
        db_table = 'app_update_log'

    appInfoId = models.IntegerField(default=-1)
    versionCode = models.IntegerField()
    versionName = models.CharField(max_length=10)
    baleStatus = models.IntegerField(default=0, verbose_name='打包状态')
    s3_repo_url = models.CharField(default='', max_length=255)
    oss_repo_url = models.CharField(default='', max_length=255)
    env = models.IntegerField(default=1)
    desc = models.CharField(default="", max_length=255)
    type = models.IntegerField(default=1, verbose_name='强更类型')  # 强更类型
    size = models.CharField(verbose_name='大小', max_length=20)
    md5 = models.CharField(verbose_name='md5', max_length=50)

    # 插件使用
    plugin = models.IntegerField(default=-1)
    fileName = models.FileField(verbose_name='插件名称', max_length=100, )
    fileType = models.CharField(verbose_name='plugin后缀名', max_length=20)

    createTime = models.DateTimeField(verbose_name='发表时间', auto_now_add=True, editable=False)
    updateTime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
