from datetime import datetime
from time import timezone

import collections
from django.shortcuts import render

from web.models import AppUpdateLog


def plugin(req, method=''):
    if method == 'add':
        return plugin_add(req)
    elif method == 'list':
        return plugin_list(req)
    else:
        return render(req, "tempfile/baseImpl.html", {"html": "error/403.html", "title": "403", "nav_active": "403"})


def plugin_add(req):
    if req.method == 'POST':
        print(req.FILES)
    # else:
    return render(req, "plugin/plugin_add.html", {"nav_active": "plugin-add"})


def plugin_list(req, page=0, pageCount=10):
    table = ['id', 'fileName', 'md5', 'size', 'env', 'desc', 's3_repo_url', 'oss_repo_url']
    # for i in range(1, 20):
    #     app = AppUpdateLog(id=i, fileModel=2, versionCode=i, fileName='xxxx', md5='ahsdksjdsa', env=1, desc='3232',
    #                        s3_repo_url='http://',
    #                        oss_repo_url='http://', updateTime=datetime.now(), createTime=datetime.now())
    #     app.save()
    # AppUpdateLog.objects.all().delete()
    # 获取插件 数据

    pluginLogs = AppUpdateLog.objects.all()
    return render(req, "plugin/plugin_list.html",
                  {"nav_active": "plugin-list", "data": pluginLogs, "table": table})
    # return render(req, "plugin/plugin_list.html", {"nav_active": "plugin-list"})
