from datetime import datetime

import collections

import os
from django.shortcuts import render

from web.forms import PluginForm
from web.models import Plugin, FileSystem


def plugin(req, method=''):
    if method == 'add':
        return plugin_add(req)
    elif method == 'list':
        return plugin_list(req)
    else:
        return render(req, "tempfile/baseImpl.html", {"html": "error/403.html", "title": "403", "nav_active": "403"})


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
            newName = os.path.basename(name)
            # 获取code
            strings = name.split("_")
            if ext == '.apk' or ext == '.jar':
                if strings:
                    code = strings[len(strings) - 1]
                    newName = newName.replace("_" + code, "")

                    try:
                        # 存 本地
                        fileSys = FileSystem(localUrl=url, fileTableName=Plugin._meta.db_table)
                        fileSys.save()

                        plugin = Plugin(fileName=newName, version=int(code), desc=desc,
                                        env=int(env), fileType=ext, md5=fileSys.uuidOrMd5)
                        plugin.save()
                        message = '上传成功!'
                    except Exception as e:
                        message = '文件上传失败!'
                        print(e)
                        pass
    return render(req, "plugin/plugin_add.html",
                  {"nav_active": "plugin-add", 'lf': lf, 'error_is_true': True, 'message': message})


def plugin_list(req, page=0, pagecount=10):
    table = ['id', 'fileName', 'md5', 'size', 'env', 'desc', 's3_repo_url', 'oss_repo_url']
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
                mapping = [value.id, value.fileName, value.md5, file.size, env, value.desc, file.s3_url,
                           file.oss_url]
                data.append(mapping)
    except Exception as e:
        print(e)
    return render(req, "plugin/plugin_list.html",
                  {"nav_active": "plugin-list", "data": data, "table": table})
    # return render(req, "plugin/plugin_list.html", {"nav_active": "plugin-list"})
