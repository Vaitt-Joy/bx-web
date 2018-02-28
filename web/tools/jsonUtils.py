import json

from django.http import HttpResponse


def response_json(msg=-1, param="请求数据失败!", data=None):
    return HttpResponse(json.dumps({'msg': msg, 'param': param, 'data': data}), content_type="application/json")


def load_json(data):
    try:
        return json.loads(str(data))
    except Exception as e:
        print(e)
        return None
