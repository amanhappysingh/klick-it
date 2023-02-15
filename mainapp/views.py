

from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from klickit.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from .models import *
from django.db.models import Q
import os
import razorpay
from smtpd import *
from random import randint
from django.conf import settings


def homepage(request):
    products = Product.objects.all()
    products = products[::-1]
    if (request.method == "POST"):
        try:
            email = request.POST.get("email")
            n = Newslatter()
            n.email = email
            n.save()

        except:
            pass
        return HttpResponseRedirect("/")
    return render(request, "home.html", {"products": products})


def shoppage(request, mc, sc, br):
    products = Product.objects.all()
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if (request.method == "POST"):
        search = request.POST.get('search')
        products = Product.objects.filter(Q(name__icontains=search))
    else:
        if (mc == "All" and sc == "All" and br == "All"):
            products = Product.objects.all()
        elif (mc != "All" and sc == "All" and br == "All"):
            products = Product.objects.filter(
                maincategory=Maincategory.objects.get(name=mc))
        elif (mc == "All" and sc != "All" and br == "All"):
            products = Product.objects.filter(
                subcategory=Subcategory.objects.get(name=sc))
        elif (mc == "All" and sc == "All" and br != "All"):
            products = Product.objects.filter(brand=Brand.objects.get(name=br))
        elif (mc != "All" and sc != "All" and br == "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), subcategory=Subcategory.objects.get(name=sc))
        elif (mc != "All" and sc == "All" and br != "All"):
            products = Product.objects.filter(maincategory=Maincategory.objects.get(
                name=mc), brand=Brand.objects.get(name=br))
        elif (mc == "All" and sc != "All" and br != "All"):
            products = Product.objects.filter(subcategory=Subcategory.objects.get(
                name=sc), brand=Brand.objects.get(name=br))
        else:
            products = Product.objects.filter(subcategory=Subcategory.objects.get(
                name=sc), brand=Brand.objects.get(name=br), maincategory=Maincategory.objects.get(name=mc))
    brand = Brand.objects.all()
    products = products[::-1]
    return render(request, "shop.html", {"products": products,
                                        "maincategory": maincategory,
                                        "subcategory": subcategory,
                                        "brand": brand,
                                        "mc": mc,
                                        "sc": sc,
                                        "br": br})


def loginpage(request):
    if (request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if (user is not None):
            auth.login(request, user)
            if (user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            messages.error(request, "Invalid Username and Password")

    return render(request, "login.html")


def signup(request):
    if (request.method == "POST"):
        actype = request.POST.get('actype')
        if (actype == "seller"):
            u = Seller()
        else:
            u = Buyer()
        u.name = request.POST.get("name")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        u.phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if (password == cpassword):
            try:
                user = User.objects.create_user(
                    username=u.username, password=password, email=u.email)
                user.save()
                u.save()
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request, " Username already exists! try new")
                return render(request, "signup.html")
        else:
            messages.error(request, " password didn't  matched")

    return render(request, "signup.html")


@login_required(login_url="/login/")
def profilepage(request):
    user = User.objects.get(username=request.user)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            seller = Seller.objects.get(username=request.user)
            products = Product.objects.all()
            products = products[::-1]
            return render(request, "sellerprofile.html", {"User": seller, "product": products})
        except:
            buyer = Buyer.objects.get(username=request.user)
            wishlist = Wishlist.objects.filter(buyer=buyer)
            checkouts = Checkout.objects.filter(buyer=buyer)
            checkouts = checkouts[::-1]
            return render(request, "buyerprofile.html", {"User": buyer, "wishlist": wishlist, "order": checkouts})


@login_required(login_url="/login/")
def updateprofile(request):
    user = User.objects.get(username=request.user)
    if (user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        try:
            user = Seller.objects.get(username=request.user)
        except:
            user = Buyer.objects.get(username=request.user)

        if (request.method == "POST"):
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.phone = request.POST.get("phone")
            user.address1 = request.POST.get("address1")
            user.address2 = request.POST.get("address2")
            user.address3 = request.POST.get("address3")
            user.pin = request.POST.get("pin")
            user.city = request.POST.get("city")
            user.state = request.POST.get("state")
            if (request.FILES.get("pic")):
                if (user.pic):
                    os.remove("media/"+str(user.pic))
                user.pic = request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
        return render(request, "updateprofile.html", {"User": user})


def productdetail(request):
    maincategory = Maincategory.objects.all()
    subcategory = Subcategory.objects.all()
    brand = Brand.objects.all()
    if (request.method == "POST"):
        p = Product()
        p.name = request.POST.get("name")
        p.maincategory = Maincategory.objects.get(
            name=request.POST.get('maincategory'))
        p.subcategory = Subcategory.objects.get(
            name=request.POST.get('subcategory'))
        p.brand = Brand.objects.get(name=request.POST.get("brand"))
        p.stock = request.POST.get("stock")
        p.baseprice = int(request.POST.get("baseprice"))
        p.discount = int(request.POST.get("discount"))
        p.finalprice = p.baseprice-p.baseprice*p.discount/100
        color = ""
        if (request.POST.get("red")):
            color = color+"red,"
        if (request.POST.get("orange")):
            color = color+"orange,"
        if (request.POST.get("blue")):
            color = color+"blue,"
        if (request.POST.get("pink")):
            color = color+"pink,"
        if (request.POST.get("skyblue")):
            color = color+"skyblue,"
        if (request.POST.get("green")):
            color = color+"green,"
        if (request.POST.get("white")):
            color = color+"white,"
        if (request.POST.get("black")):
            color = color+"black,"
        if (request.POST.get("yellow")):
            color = color+"yellow,"
        if (request.POST.get("navyblue")):
            color = color+"navyblue,"
        if (request.POST.get("gray")):
            color = color+"gray,"
        if (request.POST.get("brown")):
            color = color+"brown,"
        size = ""
        if (request.POST.get("S")):
            size = size+"S,"
        if (request.POST.get("XS")):
            size = size+"XS,"
        if (request.POST.get("M")):
            size = size+"M,"
        if (request.POST.get("L")):
            size = size+"L,"
        if (request.POST.get("XL")):
            size = size+"XL,"
        if (request.POST.get("XXL")):
            size = size+"XXL,"
        if (request.POST.get("XXXL")):
            size = size+"XXXL,"
        p.color = color
        p.size = size
        p.description = request.POST.get("description")
        p.pic1 = request.FILES.get("pic1")
        p.pic2 = request.FILES.get("pic2")
        p.pic3 = request.FILES.get("pic3")
        p.pic4 = request.FILES.get("pic4")
        try:
            p.seller = Seller.objects.get(username=request.user)
        except:
            return HttpResponseRedirect("/profile/")
        p.save()
        return HttpResponseRedirect("/profile/")
    return render(request, "addproduct.html", {"Maincategory": maincategory, "Subcategory": subcategory, "Brand": brand})


@login_required(login_url="/login/")
def deleteproduct(request, num):
    try:
        p = Product()
        q = Product.objects.get(id=num)
        p.seller = Seller.objects.get(username=request.user)
        seller = Seller.objects.get(username=request.user)
        if (p.seller == seller):
            q.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def editproduct(request, num):
    try:
        q = Product()
        q.seller = Seller.objects.get(username=request.user)
        p = Product.objects.get(id=num)
        sell = Seller.objects.get(username=request.user)
        if (q.seller == sell):
            maincategory = Maincategory.objects.exclude(name=p.maincategory)
            subcategory = Subcategory.objects.exclude(name=p.subcategory)
            brand = Brand.objects.exclude(name=p.brand)
            if (request.method == "POST"):
                p.name = request.POST.get("name")
                p.maincategory = Maincategory.objects.get(
                    name=request.POST.get('maincategory'))
                p.subcategory = Subcategory.objects.get(
                    name=request.POST.get('subcategory'))
                p.brand = Brand.objects.get(name=request.POST.get("brand"))
                p.stock = request.POST.get("stock")
                p.baseprice = int(request.POST.get("baseprice"))
                p.discount = int(request.POST.get("discount"))
                p.finalprice = p.baseprice-p.baseprice*p.discount/100
                color = ""
                if (request.POST.get("red")):
                    color = color+"red,"
                if (request.POST.get("orange")):
                    color = color+"orange,"
                if (request.POST.get("blue")):
                    color = color+"blue,"
                if (request.POST.get("pink")):
                    color = color+"pink,"
                if (request.POST.get("skyblue")):
                    color = color+"skyblue,"
                if (request.POST.get("green")):
                    color = color+"green,"
                if (request.POST.get("white")):
                    color = color+"white,"
                if (request.POST.get("black")):
                    color = color+"black,"
                if (request.POST.get("yellow")):
                    color = color+"yellow,"
                if (request.POST.get("navyblue")):
                    color = color+"navyblue,"
                if (request.POST.get("gray")):
                    color = color+"gray,"
                if (request.POST.get("brown")):
                    color = color+"brown,"
                size = ""
                if (request.POST.get("S")):
                    size = size+"S,"
                if (request.POST.get("XS")):
                    size = size+"XS,"
                if (request.POST.get("M")):
                    size = size+"M,"
                if (request.POST.get("L")):
                    size = size+"L,"
                if (request.POST.get("XL")):
                    size = size+"XL,"
                if (request.POST.get("XXL")):
                    size = size+"XXL,"
                if (request.POST.get("XXXL")):
                    size = size+"XXXL,"
                p.color = color
                p.size = size
                p.description = request.POST.get("description")
                if (request.FILES.get('pic1')):
                    if (p.pic1):
                        os.remove("media/"+str(p.pic))
                    p.pic1 = request.FILES.get("pic1")
                if (request.FILES.get('pic2')):
                    if (p.pic2):
                        os.remove("media/"+str(p.pic2))
                    p.pic2 = request.FILES.get("pic2")
                if (request.FILES.get('pic3')):
                    if (p.pic3):
                        os.remove("media/"+str(p.pic3))
                    p.pic3 = request.FILES.get("pic3")
                if (request.FILES.get('pic4')):
                    if (p.pic4):
                        os.remove("media/"+str(p.pic4))
                    p.pic4 = request.FILES.get("pic4")

                p.save()
                return HttpResponseRedirect("/profile/")
            return render(request, "editproduct.html", {"product": p, "Maincategory": maincategory,        "Subcategory": subcategory, "Brand": brand})

        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")


def singleproductpage(request, num):
    product = Product.objects.get(id=num)
    color = product.color.split(",")
    color = color[:-1]
    size = product.size.split(",")
    size = size[:-1]
    return render(request, "singleproductpage.html", {"product": product, "color": color, "size": size})


def wishlist(request, num):
    try:
        buyer = Buyer.objects.get(username=request.user)
        wishlist = Wishlist.objects.filter(buyer=buyer)
        product = Product.objects.get(id=num)
        flag = False
        for i in wishlist:
            if (i.product == product):
                flag = True
                break
        if (flag == False):
            w = Wishlist()
            w.buyer = buyer
            w.product = product
            w.save()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def deletewishlist(request, num):
    try:
        p = Wishlist()
        q = Wishlist.objects.get(id=num)
        p.buyer = Buyer.objects.get(username=request.user)
        buyer = Buyer.objects.get(username=request.user)
        if (p.buyer == buyer):
            q.delete()
        return HttpResponseRedirect("/profile/")
    except:
        return HttpResponseRedirect("/profile/")


def addtocart(request):
    pid = request.POST.get('pid')
    color = request.POST.get('color')
    size = request.POST.get('size')
    cart = request.session.get('cart', None)
    if (cart):
        if (pid in cart.keys() and color == cart[pid][0] and size == cart[pid][2]):
            pass
        else:
            count = len(cart.keys())
            count = count+1
            cart.setdefault(str(count), [pid, 1, color, size])

    else:
        cart = {"1": [pid, 1, color, size]}
    request.session['cart'] = cart
    return HttpResponseRedirect("/cart/")


def cartpage(request):
    cart = request.session.get('cart', None)
    total = 0
    shipping = 0
    final = 0
    if (cart):
        for value in cart.values():
            p = Product.objects.get(id=int(value[0]))
            total = total+p.finalprice*value[1]
        if (total < 1000):
            shipping = 150
        final = total+shipping

    return render(request, 'cart.html', {"cart": cart, "total": total, "shipping": shipping, "final": final})


def updatecart(request, id, num):
    cart = request.session.get("cart", None)
    if (cart):
        if (num == "-1"):
            if (cart[id][1] > 1):
                q = cart[id][1]
                q = q-1
                cart[id][1] = q
        else:
            q = cart[id][1]
            q = q+1
            cart[id][1] = q

        request.session["cart"] = cart
    return HttpResponseRedirect("/cart/")


def deletecart(request, id):
    cart = request.session.get("cart", None)
    if (cart):
        cart.pop(id)
        request.session["cart"] = cart

    return HttpResponseRedirect("/cart/")


client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


@login_required(login_url="/login/")
def checkout(request):
    cart = request.session.get("cart", None)
    total = 0
    shipping = 0
    final = 0
    if (cart):
        for value in cart.values():
            p = Product.objects.get(id=int(value[0]))
            total = total+p.finalprice*value[1]
        if (total < 1000):
            shipping = 150
        final = total+shipping

    try:
        buyer = Buyer.objects.get(username=request.user)
        if (request.method == "POST"):
            mode = request.POST.get("mode")
            check = Checkout()
            check.buyer = buyer
            check.total = total
            check.shipping = shipping
            check.final = final
            check.save()
            for value in cart.values():
                cp = Checkoutproduct()
                p = Product.objects.get(id=int(value[0]))
                cp.name = p.name
                cp.pic = p.pic1
                cp.size = value[3]
                cp.color = value[2]
                cp.price = p.finalprice
                cp.qty = value[1]
                cp.total = p.finalprice*value[1]
                cp.checkout = check
                cp.save()
            request.session["cart"] = {}
            if (mode == "COD"):
                return HttpResponseRedirect("/confirmation/")
            else:
                orderAmount = check.final*100
                orderCurrency = 'INR'
                paymentOrder = client.order.create(
                    dict(amount=orderAmount, currency=orderCurrency, payment_capture=1))
                paymentId = paymentOrder['id']
                check.mode = "Net Banking"
                check.save()
                return render(request, "pay.html", {
                    "amount": orderAmount,
                    "api_key": RAZORPAY_API_KEY,
                    "order_id": paymentId,
                    "User": buyer

                })
        return render(request, 'checkout.html', {"cart": cart, "total": total, "shipping": shipping, "final": final, "User": buyer})
    except:
        return HttpResponseRedirect('/profile/')


@login_required(login_url="/login/")
def confirmationpage(request):
    return render(request, "confirmation.html")


@login_required(login_url="/login/")
def paymrntsuccess(request, rppid, rpoid, rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(buyer=buyer)
    check = check[::-1]
    check.rppid = rppid
    check.rpoid = rpoid
    check.rpsid = rpsid
    check.paymentstatus = 2
    check.save()
    return HttpResponseRedirect("confirmation")


@login_required(login_url="/login/")
def paynow(request, num):
    try:
        buyer = Buyer.objects.get(username=request.user)
    except:
        return HttpResponseRedirect("profile")

    check = Checkout.objects.get(id=num)
    orderAmount = check.final*100
    ordercurrency = "INR"
    paymentOrder = client.order.create(
        dict(amount=orderAmount, currency=ordercurrency))
    paymentId = paymentOrder["id"]
    check.save()
    return render(request, "pay.html", {
        "amount": orderAmount,
        "api_key": RAZORPAY_API_KEY,
        "order_id": paymentId,
        "user": buyer
    })


def contact(request):
    return render(request, "contact.html")


def forgetemail(request):
    if (request.method == 'POST'):
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
            if (user.is_superuser):
                return HttpResponseRedirect("/admin/")
            num = randint(100000, 999999)
            request.session['num'] = num
            request.session['resetuser'] = username
            try:
                user = Buyer.objects.get(username=username)
            except:
                user = Seller.objects.get(username=username)
            subject = "OTP For Password Reset"
            message = """
                        OTP to reset password is %d
                        visit for latest products and offers
                        http://localhost:8000/
                        Team : Klickit

                    """%num
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return HttpResponseRedirect("/forget-otp/")
        except:
             messages.error(
                 request, "User Name Dose Not Match With Our DataBase")

    return render(request, "forget-email.html")


def forgetotp(request):
    if (request.method == 'POST'):
        otp = request.POST.get("otp")
        sessionOTP = int(request.session.get('num'))
        if(otp!=sessionOTP):
            return HttpResponseRedirect('/forget-password/')
        # else:
            # messages.error(request,"Invalid Otp")
    return render(request, "forget-otp.html")

def resetpassword(request):
    if (request.method == 'POST'):
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(cpassword==password):
            user = User.objects.get(username=request.session.get('resetuser'))
            user.set_password(password)
            user.save()

            return HttpResponseRedirect('/login/')
        else:
            messages.error(request,"Password and Confirm Password Does not Match")
    return render(request, "forget-otp.html")
