# coding=utf-8
from django.shortcuts import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.http import *
from models import *
import hashlib
from . import decorate
from django.db.models import *


@decorate.loginName
def index(request, dic, *args):
    '''
    首页，登录后用装饰器函数实现username的传值，*args 为可变参数
    模板内部双层循环取值先

    '''
    # user = UserInfo.objects.get(uName=dic['username'])
    # cart = CartList.objects.filter(cUser=user.id)
    # countDate = cart.aggregate(Count('id'))

    pro = Sort.objects.all()
    dic['proList'] = pro
    # dic['count'] = countDate['id__count']
    return render(request, 'foods/index.html', dic)


def register(request):
    """
    注册

    """
    return render(request, 'foods/register.html')


def registerHandler(request):
    """
    注册执行
    :param request:
    :return:
    """
    if request.method == 'POST':
        uName = request.POST['user_name']
        uPwd = request.POST['pwd']
        eMail = request.POST['email']
        # 对密码进行md5加密
        encrypt = hashlib.md5()
        encrypt.update(uPwd)
        # isEmpty = UserInfo.objects.get(uName=uName)
        # 在数据库中查找是否用户名已存在
        try:
            UserInfo.objects.get(uName=uName)
        except Exception:
            UserInfo.objects.create(
                uName=uName, uPwd=encrypt.hexdigest(), uEmail=eMail)
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect("用户名存在了")


def login(request):
    """
    登录页面渲染

    """
    return render(request, 'foods/login.html')


def loginHandler(request):
    """
    登录操作执行验证
    """
    if request.method == 'POST':
        uName = request.POST['username']
        uPwd = request.POST['pwd']
        # uReb = request.POST['reb']
        encrypt = hashlib.md5()
        encrypt.update(uPwd)
        user = UserInfo.objects.filter(
            uName__exact=uName, uPwd__exact=encrypt.hexdigest())
        if user:
            # 比较成功，跳转index
            # user = UserInfo.objects.get(uName=uName)
            request.session['username'] = uName
            response = redirect('/')
            # response = render_to_response('weblogin/index.html', {'user': user})

            # response.set_cookie('username', uName, 3600)
            return response
        else:
            return HttpResponseRedirect('/login/')


def loginOut(request):
    """
    退出登录
    :param request:
    :return:
    """
    response = HttpResponseRedirect('/')
    # response.delete_cookie('username')
    del request.session['username']
    return response


@decorate.loginName
def intoCart(request, dic, *args):
    '''
    加入购物车
    '''
    cNum = request.POST.get('cNum')
    pro = request.POST.get('cProduct')
    cUser = UserInfo.objects.get(uName=dic['username'])
    cProduct = ProductInfo.objects.get(pk=int(pro))
    cPrice = cProduct.pPrice

    CartList.objects.create(
        cUser=cUser,
        cProduct=cProduct,
        cPrice=cPrice,
        cNum=cNum,
    )
    return HttpResponse(cNum)


def cartNum(request):
    '''
    接收post请求，返回某个用户的购物车数量
    '''
    userid = 1
    cartNum = len(CartList.objects.filter(cUser=userid))
    return JsonResponse({'cartNumData': cartNum})


@decorate.loginName
def lists(request, dic, *args):
    '''
    某类商品的列表,通过id实现商品类的选择，通过index实现翻页的功能
    '''
    index = args[0]
    id = request.GET.get('id')
    subList = ProductInfo.objects.filter(pClass=int(id))
    sortList = ProductInfo.objects.order_by('pPrice')
    page = Paginator(subList, 2)
    sortPage = Paginator(sortList, 2)
    pageList = page.page_range
    sortPageList = sortPage.page_range
    recom = subList[0:2]
    if index == '':
        index = '1'
    currentList = page.page(int(index))
    sortList = sortPage.page(int(index))
    dic1 = {
        'id': id,
        'recomPro': recom,
        'subList': subList,
        'pageList': pageList,
        'pIndex': int(index),
        'sortList': sortList,
        'currentList': currentList,
        'sortPageList': sortPageList,
    }
    dic2 = dict(dic, **dic1)

    return render(request, 'foods/lists.html', dic2)


@decorate.loginName
def detail(request, dic, *args):
    '''
    某个商品的详细信息页面
    '''
    id = args[0]
    user = UserInfo.objects.get(uName=dic['username'])

    userid = user.id
    cartNum = len(CartList.objects.filter(cUser=userid))
    detail = ProductInfo.objects.get(pk=id)
    recom = ProductInfo.objects.all()[0:2]
    dic1 = {
        'detailPro': detail,
        'recomPro': recom,
        'cartNumData': cartNum,
    }
    dic2 = dict(dic, **dic1)

    return render(request, 'foods/detail.html', dic2)


@decorate.loginYz
@decorate.loginName
def userCenterInfo(request, dic, *args):
    '''
    用户中心个人信息
    '''
    pageNum = args[0]
    goodsRecent = ProductInfo.objects.all()[0:5]
    users = UserInfo.objects.get(uName=dic['username'])
    dic1 = {
        'users': users,
        'goodsRecent': goodsRecent
    }
    dic2 = dict(dic, **dic1)
    return render(request, 'foods/userCenterInfo.html', dic2)


@decorate.loginYz
@decorate.loginName
def userCenterOrder(request, dic, *args):
    '''
    用户中心全部订单
    '''
    pageNum = args[0]
    user = UserInfo.objects.get(uName=dic['username'])
    goodsOrder = user.orderlist_set.all()
    paginator = Paginator(goodsOrder, 1)
    try:
        shows = paginator.page(pageNum)
    except PageNotAnInteger:
        shows = paginator.page(1)
    except EmptyPage:
        shows = paginator.page(paginator.num_pages)
    oSum = 0
    for order in shows:
        goodsDetail = order.detailorder_set.all()
        for detail in goodsDetail:
            oSum += (detail.dPrice) * (detail.dNum)
    pageNum = int(pageNum)
    dic1 = {
        'oSum': oSum,
        'shows': shows,
        'pageNum': pageNum,
        'paginator': paginator,
        'goodsOrder': goodsOrder,
        'goodsDetail': goodsDetail,
    }
    dic2 = dict(dic, **dic1)
    return render(request, 'foods/userCenterOrder.html', dic2)


@decorate.loginYz
@decorate.loginName
def userCenterSite(request, dic, *args):
    '''
    用户中心收获地址
    '''
    # 如果没有登录就跳到登录界面，根据有没有用户名会话来决定
    if request.session.has_key('username'):
        #将用户的信息传过去 #
        user = UserInfo.objects.get(uName=dic['username'])
        userAddress = user.uAddr
        dic1 = {
            'userAddress': userAddress
        }
        dic2 = dict(dic, **dic1)
        return render(request, 'foods/userCenterSite.html', dic2)
    else:
        return redirect('/login/')


@decorate.loginYz
@decorate.loginName
def userCenterSiteHandle(request, dic, *args):
    '''
    判断提交方式
    '''

    if request.method == 'POST':
        #获取用户ID #

        user = UserInfo.objects.get(uName=dic['username'])
        # 获取表单提交的地址信息

        phone = request.POST['contactTel']
        receiver1 = request.POST['receiver']
        detailAddress1 = request.POST['detailAddress']
        postCode1 = request.POST['postCode']
        user.uAddr = detailAddress1 + "  ( " + receiver1 + " ) " + phone
        user.save()
        # 重定向此页面
        return redirect('/userCenterSite/')
    else:
        return redirect('/userCenterSite/')


@decorate.loginYz
@decorate.loginName
def cart(request, dic, *args):

    # 查询条件
    carts = CartList.objects.all()
    b = len(carts)
    list2 = []
    ProductNumbers = 0
    for i in carts:
        c = ProductInfo.objects.filter(pk=i.cProduct.id)
        for d in c:
            ProductNumber = d.pPrice * i.cNum
            ProductNumbers = ProductNumbers + ProductNumber
            values = {
                'id': i.id,
                'ProductID_id': i.cProduct.id,
                'pImg': d.pImg,
                'pName': d.pName,
                'pPrice': d.pPrice,
                'cNum': i.cNum,
                'ProductNumber': ProductNumber,
                'pUnit': d.pUnit,
                'pStock': d.pStock,
            }
            list2.append(values)

    dic1 = {
        "b": b,
        'list2': list2,
        "ProductNumbers": ProductNumbers,
    }
    dic2 = dict(dic, **dic1)

    return render(request, "foods/cart.html", dic2)


@decorate.loginYz
@decorate.loginName
def placeOrder(request, dic, *args):
    # 修改查询条件

    carts = CartList.objects.all()
    user = UserInfo.objects.get(pk=5)
    f = len(carts)
    ProductNumbers = 0
    for i in carts:
        c = ProductInfo.objects.filter(pk=i.cProduct.id)
        for d in c:
            ProductNumber = d.pPrice * i.cNum
            ProductNumbers = ProductNumbers + ProductNumber
            nums = ProductNumbers + 10

    dic1 = {
        'f': f,
        'user': user,
        'nums': nums,
        'carts': carts,
        "ProductNumbers": ProductNumbers,
    }
    dic2 = dict(dic, **dic1)
    return render(request, 'foods/placeOrder.html', dic2)


# 空视图（备用）
def baseBottom(request):

    return render(request, 'foods/baseBottom.html')


# @decorate.loginName
# def base(request, dic, *args):
#     '''
#     实现购物车的显示 
#     '''
#     user = UserInfo.objects.get(uName=dic['username'])
#     cart = CartList.objects.filter(cUser=user.id)
#     countDate = cart.aggregate(Count('id'))
#     dic1 = {
#         'count': countDate['id__count'],
#     }
#     dic2 = dict(dic, **dic1)

#     return render(request, 'foods/base.html', dic2)


def userCenterBase(request):
    return render(request, 'foods/userCenterBase.html')

def base(request):
    return render(request, 'foods/base.html')

def subBill(request):
    """
    购物车数据提交后台处理
    """
    userSession = UserInfo.objects.get(pk=5)
    ProductNumbers = request.POST['ProductNumbers']
    OrderID = OrderList.objects.create(oSum=ProductNumbers, oIspay=False, oUser=userSession)
    goodsId = request.POST['Checks']
    saleSum = request.POST['saleSum']
    # productPrice = request.POST['unitPrice']  # 原本是浮点型，因数据库字段设计有误，强制整型
    detailOrder = DetailOrder.objects.create(dNum=saleSum, dPrice=ProductInfo.objects.get(pk=goodsId).pPrice,
                                             dMain=OrderList.objects.get(pk=OrderID.id),
                                             dProduct=ProductInfo.objects.get(pk=int(goodsId)))
    return redirect('/userCenterSite/')
