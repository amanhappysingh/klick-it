from django import template
from mainapp.models import Product
register = template.Library()

@register.filter("cartcolor")
def cartcolor(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][2]
    else:
        return ""
@register.filter("cartsize")
def cartsize(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][3] 
    else:
        return ""

@register.filter("cartqty")
def cartqty(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        return cart[num][1]
    else:
        return ""
@register.filter("carttotal")
def carttotal(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return cart[num][1]*p.finalprice
    else:
        return ""

@register.filter("cartproductname")
def cartproductname(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.name
    else:
        return ""

@register.filter("cartproductimage")
def cartproductimage(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.pic1.url
    else:
        return ""
@register.filter("cartproductprice")
def cartproductprice(request , num):
    cart = request.session.get("cart",None)
    if(cart):
        p = Product.objects.get(id=int(cart[num][0]))
        return p.finalprice
    else:
        return ""

    

