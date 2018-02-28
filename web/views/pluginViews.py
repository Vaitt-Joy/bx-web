# coding=utf-8
import os

from django.db import transaction
from django.shortcuts import render

from BxWeb import settings
from web.forms import PluginForm
from web.models import Plugin, FileSystem
from web.tools.PyTools import approximate_size


def plugin(req, method=''):
    if method == 'add':
        return plugin_add(req)
    elif method == 'list':
        return plugin_list(req)
    elif method == 'delete':
        return plugin_delete(req)
    else:
        return render(req, "tempfile/baseImpl.html", {"html": "error/403.html", "title": "403", "nav_active": "403"})


@transaction.atomic
def plugin_add(req):
    message = ''
    if req.method == 'GET':
        lf = PluginForm()
    else:
        lf = PluginForm(req.POST, req.FILES)
        message = '文件格式有误！'
        if lf.is_valid():
            data = lf.cleaned_data  # 获取数据
            env = data['pluginEnvSelect']  # 选择的环境
            url = data['pluginFile']  # 选择的文件
            desc = data['desc']  # 选择的文件
            name, ext = os.path.splitext(url.name)
            # 获取code
            strings = name.split("_")
            if (ext == '.apk' or ext == '.jar') and len(strings) == 3:
                if strings:
                    plugin_name = strings[1]
                    package_name = strings[0]
                    code = strings[len(strings) - 1]
                    # 开启事务
                    sid = transaction.savepoint()
                    try:
                        # 存 本地
                        file_sys = FileSystem(localUrl=url, fileTableName=Plugin._meta.db_table)
                        file_sys.save()
                        plugin = Plugin(packageName=package_name, pluginName=plugin_name, version=int(code), desc=desc,
                                        env=int(env), fileType=ext, md5=file_sys.uuidOrMd5)
                        plugin.save()
                        transaction.savepoint_commit(sid)
                        message = '上传成功!'
                    except Exception as e:
                        transaction.savepoint_rollback(sid)
                        message = '文件上传失败!'
                        print(e)
                        pass
    return render(req, "plugin/plugin_add.html",
                  {"nav_active": "plugin-add", 'lf': lf, 'error_is_true': True, 'message': message})


def plugin_delete(req):
    if req.method == 'GET':
        value = req.GET['value']
        plugin = Plugin.objects.get(id=value[0])
        if plugin:
            file = FileSystem.objects.get(uuidOrMd5=plugin.md5)
            if file:
                file.delete()
            plugin.delete()
    return plugin_list(req)


def plugin_list(req, page=0, pagecount=10):
    table = ['id', 'packageName', 'pluginName', 'md5', 'size', 'env', 'code', 'desc', 'url', 's3_repo_url',
             'oss_repo_url', 'operating']
    operating_btn = ['delete']  # edit
    data = []
    try:
        plugins = Plugin.objects.order_by("version")[page: pagecount * (page + 1)]
        for value in plugins:
            file = FileSystem.objects.get(uuidOrMd5=value.md5)
            if file:
                if value.env == 1:
                    env = '强制更新'
                else:
                    env = '推荐更新'
                size = approximate_size(file.size, False)
                mapping = [value.id, value.packageName, value.pluginName, value.md5, size, env, value.version,
                           value.desc, file.localUrl, file.s3_url, file.oss_url, 'btn']
                data.append(mapping)
    except Exception as e:
        print(e)
    return render(req, "plugin/plugin_list.html",
                  {"nav_active": "plugin-list", "data": data, "table": table, "operatingBtn": operating_btn})
    # return render(req, "plugin/plugin_list.html", {"nav_active": "plugin-list"})
