
from ctypes.wintypes import PSHORT
from pathlib import Path
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage),
    path('login/',views.loginpage),
    path('signup/', views.signup),
    path('profile/',views.profilepage),
    path('updateprofile/',views.updateprofile),
    path('add-product/',views.productdetail),
    path('delete-product/<int:num>/',views.deleteproduct),
    path('delete-wishlist/<int:num>/',views.deletewishlist),
    path('edit-product/<int:num>/',views.editproduct),
    path('logout/',views.logout),
    path('shop/<str:mc>/<str:sc>/<str:br>/', views.shoppage),
    path('single-product-page/<int:num>/', views.singleproductpage),
    path('add-to-wishlist/<int:num>/',views.wishlist),
    path('add-to-cart/',views.addtocart),
    path('cart/',views.cartpage),
    path('update-cart/<str:id>/<str:num>/',views.updatecart),
    path('delete-cart/<str:id>/',views.deletecart),
    path('checkout/',views.checkout),
    path('confirmation/',views.confirmationpage),
    path("paymentsuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/",views.paymrntsuccess),
    path('paynow/<int:num>/',views.paynow),
    path('contact/',views.contact),
    path('forget-email/',views.forgetemail),
    path('forget-password/',views.resetpassword),
    path('forget-otp/',views.forgetotp),
]+static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
