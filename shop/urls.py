from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.store, name="store"),
    path("view/<str:pk>/", views.view, name="view"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),

    path("update_item", views.updateitem, name="updateitem"),
    path("proccess_order", views.proccessOrder, name="processorder"),

    path("login", views.loginPage, name='login'),
    path("register", views.register, name="register"),
    path("logout", views.logoutPage, name='logout'),

    path("reset_password", 
         auth_views.PasswordResetView.as_view(template_name="shop/password_reset.html"), 
         name="password_reset"),

    path("password_reset_done", 
         auth_views.PasswordResetDoneView.as_view(template_name="shop/password_reset_done.html"), 
         name="password_reset_done"),
    
    path("confirm/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="shop/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    
    path("reset_password_complete", 
         auth_views.PasswordResetCompleteView.as_view(template_name="shop/password_reset_complete.html"), 
         name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)