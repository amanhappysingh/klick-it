
from django.contrib import admin
from .models import *

admin.site.site_header = " Klick iT Admin"
admin.site.site_title = "Klick iT Admin Portal"
admin.site.index_title = "Welcome to Klick iT Portal"

# admin.site.register((Maincategory,Subcategory,Brand,Seller,Product,Buyer,Wishlist,Checkout,Checkoutproduct,Newslatter))

@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name"]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["id","name","email","phone","city"]
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id","name","size","color","baseprice","finalprice"]
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ["id","name","email","phone","city"]
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id","product"]
@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["id","orderstatus","paymentstatus","total"]
@admin.register(Checkoutproduct)
class CheckoutproductAdmin(admin.ModelAdmin):
    list_display = ["id","name","color","size","price","total"]
@admin.register(Newslatter)
class NewslatterAdmin(admin.ModelAdmin):
    list_display = ["id","email"]