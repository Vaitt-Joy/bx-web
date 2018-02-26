# coding=utf-8
from django.http import HttpResponse

from web.models import Plugin, FileSystem
from web.tools.PyTools import approximate_size
from web.tools.jsonUtils import response_json


def query_plugin(req, list=False):
    global msg, param, data
    msg = 0
    param = '请求成功'
    data = None
    if not list:
        if req.method == 'POST':
            plugin_name = req.POST['pluginName']
            version = req.POST['version']
            env = req.POST['env']
        elif req.method == 'GET':
            plugin_name = req.GET['pluginName']
            version = req.GET['version']
            env = req.GET['env']
        else:
            param = '不支持该请求方式：%s' % req.method
            return response_json(msg, param, data)
        return response_json(msg, param, get_plugin_info(env, version, plugin_name))
    else:

        pass

    return response_json(msg, param, data)


def get_plugin_info(env, version, plugin_name):
    try:
        env = int(env)
        version = int(version)
        plugins = Plugin.objects.filter(pluginName=plugin_name, env=env, version__gt=version).order_by(
            'version')
        if plugins:
            plugin = plugins.first()
            if plugin:
                file = FileSystem.objects.get(uuidOrMd5=plugin.md5)
                data = {'size': approximate_size(file.size, False), 'md5': plugin.md5, 'desc': plugin.desc,
                        's3_url': file.s3_url, 'oss_url': file.oss_url, 'pluginName': plugin_name,
                        'url': file.localUrl.url}
                return data
    except Exception as e:
        print(e)
    return None


def api(req, ac=''):
    if ac == 'queryPlugin':
        return query_plugin(req)
    elif ac == 'queryPluginList':
        return query_plugin(req, True)
    else:
        return HttpResponse("error")
