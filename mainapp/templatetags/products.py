from mainapp.models import Checkout 
from mainapp.models import Checkoutproduct  
from django import template
register = template.Library()

@register.filter("checkcolor")
def checkcolor(color , item):
    flag = False
    for i in color.split(","):
        if(i==item):
            flag = True
            break
    return flag

@register.filter("checksize")
def checksize(size , item):
    flag = False
    for i in size.split(","):
        if(i==item):
            flag = True
            break
    return flag


@register.filter("orderstatus")
def orderstatus(request , num):
    if(num==0):
        return "Cancelled"
    elif(num==1):
        return "NotPacked"
    elif(num==2):
        return "Packed"
    elif(num==3):
        return "Out For Delivery"
    else:
        return "Delivered"

@register.filter("paymentstatus")
def paymentstatus(request , num):
    if(num==1):
        return "Pending"
    elif(num==2):
        return "Done"

@register.filter("paymentstatuscon")
def paymentstatuscon(request , num):
    if(num==1):
        return True
    elif(num==2):
        return False

@register.filter("orderitem")
def orderitem(request , num):
    check = Checkout.objects.get(id=num)
    p = Checkoutproduct.objects.filter(checkout=check)
    return p 

