from itertools import product
from operator import mod
from statistics import mode
from tkinter import CASCADE
from django.db import models

class Maincategory(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True) 
    name =  models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True) 
    name =  models.CharField(max_length=20)

    def __str__(self):
        return self.name



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20)
    maincategory = models.ForeignKey(Maincategory,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    description = models.TextField()
    stock =  models.CharField(max_length=20 , default="In stock")
    pic1 = models.ImageField("image1", default="noimage.jpg",null=True,blank=True)
    pic2 = models.ImageField("image2", default="noimage.jpg",null=True,blank=True)
    pic3 = models.ImageField("image3" ,default="noimage.jpg",null=True,blank=True)
    pic4 = models.ImageField("image4" ,  default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return str(self.id)+" "+self.name

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=14)
    address1 = models.CharField(max_length=50, default=None,null=True,blank=True)
    address2 = models.CharField(max_length=50, default=None,null=True,blank=True)
    address3 = models.CharField(max_length=50, default=None,null=True,blank=True)
    pin = models.CharField(max_length=10, default=None,null=True,blank=True)
    city = models.CharField(max_length=20, default=None,null=True,blank=True)
    state = models.CharField(max_length=20, default=None,null=True,blank=True)
    pic = models.FileField(upload_to="image",  default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return str(self.id)+" "+self.username

class Buyer(models.Model):
    id = models.AutoField(primary_key=True) 
    name =  models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=14)
    address1 = models.CharField(max_length=50, default=None,null=True,blank=True)
    address2 = models.CharField(max_length=50, default=None,null=True,blank=True)
    address3 = models.CharField(max_length=50, default=None,null=True,blank=True)
    pin = models.CharField(max_length=10, default=None,null=True,blank=True)
    city = models.CharField(max_length=20, default=None,null=True,blank=True)
    state = models.CharField(max_length=20, default=None,null=True,blank=True)
    pic = models.FileField(upload_to="image",  default="noimage.jpg",null=True,blank=True)

    def __str__(self):
        return str(self.id)+" "+self.username

class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)+" "+self.buyer.username

order = ((0,"cancle"),(1,"Not Packed"),(2,"Packed"),(3,"Out Of Delevery"),(4,"Delevered"))
payment = ((1,"Pending"),(2,"Done"))
class Checkout(models.Model):
    id =models.AutoField(primary_key=True)
    total = models.IntegerField()
    shipping = models.IntegerField()
    final = models.IntegerField()
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    mode = models.CharField(max_length=20,default="COD")
    orderstatus = models.IntegerField(choices=order,default=1)
    paymentstatus = models.IntegerField(choices=payment,default=1)
    rppid = models.CharField(max_length=50,default="",null=True,blank=True)
    rpoid = models.CharField(max_length=50,default="",null=True,blank=True)
    rpsid = models.CharField(max_length=50,default="",null=True,blank=True)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+" "+self.buyer.username

class Checkoutproduct(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    pic = models.CharField(max_length=100)
    checkout = models.ForeignKey(Checkout,on_delete=models.CASCADE)

    def __str__(self):
        return "pid = "+str(self.id)+" Checkout Id = "+str(self.checkout.id)

class Newslatter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=80,unique=True)

    def __str__(self):
        return self.email

class Contect(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=80,unique=True)

    def __str__(self):
        return self.email