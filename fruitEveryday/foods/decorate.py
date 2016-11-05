from django.shortcuts import *
from django.http import *


def loginName(fn):
    def fun(request, *args):
        username = request.session.get('username', default='')
        dic = {
            'username': username
        }
        res = fn(request, dic, *args)
        return res

    return fun


def loginYz(fn):
    def fun(request, *args):
        if request.session.has_key('username'):
            res = fn(request, *args)
        else:
            res = redirect('/login/')
        return res

    return fun
