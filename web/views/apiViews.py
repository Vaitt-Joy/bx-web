# coding=utf-8
from django.http import HttpResponse

from web.models import Plugin, FileSystem
from web.tools.PyTools import approximate_size
from web.tools.jsonUtils import response_json


def query_plugin(req):
    global msg, param, data
    msg = 0
    param = '请求成功'
    data = None
    if req.method == 'POST':
        pluginName = req.POST['pluginName']
        version = req.POST['version']
        env = req.POST['env']
    elif req.method == 'GET':
        pluginName = req.GET['pluginName']
        version = req.GET['version']
        env = req.GET['env']
    else:
        param = '不支持该请求方式：%s' % req.method
        return response_json(msg, param, data)
    try:
        env = int(env)
        version = int(version)
        plugins = Plugin.objects.filter(pluginName=pluginName, env=env, version__gt=version).order_by(
            'version')
        if plugins:
            plugin = plugins.first()
            if plugin:
                file = FileSystem.objects.get(uuidOrMd5=plugin.md5)
                data = {'size': approximate_size(file.size, False), 'md5': plugin.md5, 'desc': plugin.desc,
                        's3_url': file.s3_url, 'oss_url': file.oss_url, 'pluginName': pluginName}
    except Exception as e:
        print(e)
        pass
    return response_json(msg, param, data)


def api(req, ac=''):
    if ac == 'queryPlugin':
        return query_plugin(req)
    else:
        return HttpResponse("error")
