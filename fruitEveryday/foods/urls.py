from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name='index'), 
    url(r'^register/$', register, name='register'),
    url(r'^registerHandler/$', registerHandler, name='registerHands'),
    url(r'^login/$', login, name='login'),
    url(r'^loginHandler/$', loginHandler, name='loginHandler'),
    url(r'^loginOut/$', loginOut, name='loginOut'),
    
    url(r'^detail([0-9]*)/$', detail, name='detail'),
    url(r'^intoCart/$', intoCart, name='intoCart'),
    url(r'^lists([0-9]*)/$', lists, name='lists'),
    url(r'^cartNum/$',cartNum ,name='cartNum'),


    url(r'^userCenterInfo([0-9]*)/$', userCenterInfo, name='userCenterInfo'),
    url(r'^recentMap/$', recentMap, name='recentMap'),
    url(r'^userCenterOrder/page([0-9]*)/$',
        userCenterOrder, name='userCenterOrder'),
    url(r'^userCenterSite/$', userCenterSite, name='userCenterSite'),
    url(r'^userCenterSiteHandle/$', userCenterSiteHandle, name='userCenterSiteHandle'),
    
    url(r'^cart/$', cart, name='cart'),
    url(r'^subBill/$', subBill, name='subBill'),
    url(r'^placeOrder/$', placeOrder, name='placeOrder'),

    url(r'^base/$', base, name='base'),
    url(r'^baseBottom/$', baseBottom, name='bottom'),
    url(r'^userCenterBase/$',userCenterBase,name='userCenterBase'),
]

