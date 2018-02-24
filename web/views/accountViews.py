from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout

from web.forms import AccountForm
from web.models import Account
from web.tools.PyTools import get_client_ip


def account(req, method=''):
    if method == 'list':
        return account_list(req)
    elif method == 'add':
        return account_add(req)
    elif method == 'login':
        return login(req)
    elif method == 'logout':
        return logout_views(req)
    else:
        return render(req, "tempfile/baseImpl.html", {"html": "error/403.html", "title": "403", "nav_active": "403"})


def login(req):
    if req.method == 'GET':
        af = AccountForm()
        return render(req, 'user/login.html', {'af': af})
    else:
        af = AccountForm(req.POST)
        if af.is_valid():
            username = req.POST.get("username", '')
            password = req.POST.get("password", '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(req, user)
                account = Account.objects.filter(username=username)
                if account:
                    ip = get_client_ip(req)
                    account = Account.objects.get(username=username)
                    account.lastIp = ip
                    req.session['nickName'] = account.nickName
                    req.session['userType'] = account.user_type
                    response = HttpResponseRedirect('/web')
                    # 将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('username', username, 3600)
                    account.save()
                    return response
                else:
                    return render(req, 'user/login.html', {'af': af, 'password_is_wrong': True, 'message': '用户不存在！'})
            else:
                return render(req, 'user/login.html',
                              {'af': af, 'password_is_wrong': True, 'message': '用户名或密码错误,请重新登录'})
        else:
            return render(req, 'user/login.html', {'af': af})


def logout_views(req):
    logout(req)
    login(req)


def account_add(req):
    return render(req, "user/account_add.html", {"nav_active": "account-add"})


def account_list(req):
    return render(req, "user/account_list.html", {"nav_active": "account-list"})
