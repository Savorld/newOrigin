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
     ====
    '''
    if dic['username']:

        user = UserInfo.objects.get(uName=dic['username'])
        cart = CartList.objects.filter(cUser=user.id)
        countDate = cart.aggregate(Count('id'))
        count = countDate['id__count']
    else:
        count = 0


    dic['count'] = count
    pro = Sort.objects.all()
    dic['proList'] = pro
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
    cNumNew = int(request.POST['cNum'])
    cUserNew = UserInfo.objects.get(uName=dic['username'])
    cProductNew = ProductInfo.objects.get(pk=request.POST['cProduct'])
    cPriceNew = cProductNew.pPrice
    try:
        oldCart = CartList.objects.get(
            cUser_id=cUserNew, cProduct_id=cProductNew)
    except:
        oldCart = 0
    if oldCart != 0:
        cNumNew += oldCart.cNum
        oldCart.delete()
    CartList.objects.create(
        cUser=cUserNew,
        cProduct=cProductNew,
        cPrice=cPriceNew,
        cNum=cNumNew,
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
    if dic['username']:

        user = UserInfo.objects.get(uName=dic['username'])
        cart = CartList.objects.filter(cUser=user.id)
        countDate = cart.aggregate(Count('id'))
        count = countDate['id__count']
    else:
        count = 0


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
        'count' : count,
    }
    dic2 = dict(dic, **dic1)

    return render(request, 'foods/lists.html', dic2)


@decorate.loginName
def detail(request, dic, *args):
    '''
    某个商品的详细信息页面
    '''
    id = args[0]
    if dic['username']:
        userid = UserInfo.objects.get(uName=dic['username']).id
        cartNum = len(CartList.objects.filter(cUser=userid))
    else:
        cartNum = 0
    detail = ProductInfo.objects.get(pk=id)
    recom = ProductInfo.objects.all()[0:2]
    dic1 = {
        'detailPro': detail,
        'recomPro': recom,
        'cartNumData': cartNum,
    }
    dic2 = dict(dic, **dic1)

    return render(request, 'foods/detail.html', dic2)

@decorate.loginName
def addCart(request, dic, *args):
    
    id = int(request.POST['id'])
    user = UserInfo.objects.get(uName=dic['username'])
    cart = CartList.objects.filter(cUser = user.id ,cProduct = id )
    if len(cart) == 0:
        pro = ProductInfo.objects.get(pk= id)
        
        CartList.objects.create(
                cNum = 1,
                cUser = user,
                cProduct = pro ,
                cPrice = pro.pPrice,
        )
    else:
        cart = CartList.objects.get(cUser = user.id ,cProduct = id )
        # num = cart.cNum + 1
        cart.cNum += 1
        cart.save()

    return HttpResponse('ok')



@decorate.loginYz
@decorate.loginName
def userCenterInfo(request, dic, *args):
    '''
    用户中心个人信息
    '''
    pageNum = args[0]
    users = UserInfo.objects.get(uName=dic['username'])
    Recent = RencentMap.objects.filter(rUser_id=users)
    goodsRecent = []
    for re in Recent[::-1]:
        new = ProductInfo.objects.get(pk=re.rProName.id)
        if new not in goodsRecent:
            goodsRecent.append(new)
    # goodsRecent =list(set(goodsRecent))[::-1]
    dic1 = {
        'users': users,
        'goodsRecent': goodsRecent
    }
    dic2 = dict(dic, **dic1)
    return render(request, 'foods/userCenterInfo.html', dic2)


@decorate.loginYz
@decorate.loginName
def recentMap(request, dic, *args):
    pro = ProductInfo.objects.get(pk=request.POST['pro'])
    usr = UserInfo.objects.get(uName=dic['username'])
    RencentMap.objects.create(
        rUser=usr,
        rProName=pro,
    )


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


def subBill(request):
    """
    购物车数据提交后台处理
    """
    userSession = UserInfo.objects.get(pk=5)
    ProductNumbers = request.POST.get('saleSum')  # 购物车商品总价
    OrderID = OrderList.objects.create(oSum=ProductNumbers, oIspay=False, oUser=userSession)
    ProductID = json.loads(request.POST['goodsIds']) # 购物车每个商品id
    ProductNum = json.loads(request.POST['goodsNum']) # 每个商品购买的数量
    
    # 使用下标取值
    for i in range(len(ProductID)):
        pNum = ProductNum[i]
        pId = ProductID[i]
        detailOrder = DetailOrder.objects.create(dNum=pNum, dPrice=ProductInfo.objects.get(pk=pId).pPrice,
                                                 dMain=OrderList.objects.get(pk=OrderID.id),
                                                 dProduct=ProductInfo.objects.get(pk=int(pId)))

    return redirect('/userCenterSite/')

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

    return redirect('/userCenterSite/')
