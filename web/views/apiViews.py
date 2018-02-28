# coding=utf-8
from django.http import HttpResponse

from web.models import Plugin, FileSystem
from web.tools.PyTools import approximate_size
from web.tools.jsonUtils import response_json, load_json

token = '8b35ea8d7a844523901863ccff75d3ea'


def check_token(req):
    global plugin_token
    if req.method == 'POST':
        plugin_token = req.POST['plugin_token']
    elif req.method == 'GET':
        plugin_token = req.GET['plugin_token']
    if plugin_token and plugin_token == token:
        return True
    return False


def query_plugin(req):
    if not check_token(req):
        return response_json(-1, 'have token error...', {})
    global msg, param, data
    msg = 0
    param = '请求成功'
    data = None
    data_json = None
    if req.method == 'POST':
        data_json = req.POST['data']
    elif req.method == 'GET':
        data_json = req.GET['data']
    else:
        param = '不支持该请求方式：%s' % req.method
        return response_json(-1, param, data)
    if data_json:
        try:
            data = []
            for d in load_json(data_json):
                package_name = d['packageName']
                version = d['version']
                env = d['env']
                if package_name and version and env:
                    data.append(get_plugin_info(env, version, package_name))
        except Exception as e:
            param = '服务器异常,请稍候重试'
            msg = -1
            print(e)
    return response_json(msg, param, data)


def get_plugin_info(env, version, package_name):
    try:
        env = int(env)
        version = int(version)
        plugins = Plugin.objects.filter(packageName=package_name, env=env, version__gt=version).order_by(
            'version')
        if plugins:
            plugin = plugins.first()
            if plugin:
                file = FileSystem.objects.get(uuidOrMd5=plugin.md5)
                return {'size': approximate_size(file.size, False), 'md5': plugin.md5, 'desc': plugin.desc,
                        's3_url': file.s3_url, 'oss_url': file.oss_url, 'packageName': package_name,
                        'url': file.localUrl.url}
    except Exception as e:
        print(e)
    return None


def api(req, ac=''):
    if ac == 'queryPlugin':
        return query_plugin(req)
    else:
        return HttpResponse("error")
