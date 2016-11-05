from django.db import models
from tinymce.models import HTMLField


class UserInfo(models.Model):
    uName = models.CharField(max_length=20)
    uPwd = models.CharField(max_length=100)
    uEmail = models.EmailField()
    uPhone = models.DecimalField(max_digits=11, decimal_places=0, null=True)
    uAddr = models.CharField(max_length=200, null=True)
    uTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%d'%self.id




# class cartsManager(models.Manager):

#     def create_cart(self, User, Product, Price, Num):
#         # cart = self.model()
#         # cart.cUser = User
#         # cart.cProduct = Product
#         # cart.cPrice = Price
#         # cart.cNum = Num
#         cart = self.create(cUser=User, cProduct=Product,
#                            cPrice=Price, cNum=Num)
#         return cart


class CartList(models.Model):
    cPrice = models.DecimalField(max_digits=5, decimal_places=2)
    cNum = models.IntegerField()
    cUser = models.ForeignKey('UserInfo')
    cProduct = models.ForeignKey('ProductInfo')

    def __str__(self):
        return '%d'%self.id


class OrderList(models.Model):
    oUser = models.ForeignKey('UserInfo')
    oSum = models.DecimalField(max_digits=6, decimal_places=2)
    oIspay = models.BooleanField()
    oTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%d'%self.id


class DetailOrder(models.Model):
    dProduct = models.ForeignKey('ProductInfo')
    dNum = models.IntegerField()
    dPrice = models.DecimalField(max_digits=4, decimal_places=2) #error

    dMain = models.ForeignKey('OrderList')

    def __str__(self):
        return '%d'%self.id


class ProductInfo(models.Model):
    pName = models.CharField(max_length=50)
    pPrice = models.DecimalField(max_digits=4, decimal_places=2)
    pStock = models.IntegerField()
    pDesc = models.CharField(max_length=1000)
    pDetail = HTMLField()
    pTime = models.DateTimeField(auto_now_add=True)
    pImg = models.ImageField(upload_to='upload/')
    pClass = models.ForeignKey('Sort')
    pUnit = models.CharField(max_length=20)

    def __str__(self):
        return '%d'%self.id


class Sort(models.Model):
    sClass = models.CharField(max_length=20)
    # sImg = models.ImageField(upload_to='upload/')

    def __str__(self):
        return self.sClass.encode('utf-8')



class RencentMap(models.Model):
    rUser = models.ForeignKey('UserInfo')
    rProName = models.ForeignKey('ProductInfo')
    rTime = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return '%d'%self.id