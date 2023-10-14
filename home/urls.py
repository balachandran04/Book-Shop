# # from django.contrib import admin
# # from django.urls import path,include
# # from . import views
# # from  django.contrib.auth import views as auth_view
# # from .form import LoginForm
# #
# # urlpatterns = [
# #     path('', views.home, name='home'),
# #     path('about', views.about, name='about'),
# #     path('contact', views.contact, name='contact'),
# #     path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
# #     path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title    '),
# #     path('product_details/<int:pk>', views.ProductDetails.as_view(), name='productdeatils'),
# #     path('registration/', views.CustomerRegister.as_view(), name='customerregistration'),
# #     path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm)),name='login')
# #
# # ]
# from django.contrib import admin
# from django.urls import path, include
# from . import views
# from django.contrib.auth import views as auth_view
# from .form import LoginForm, MyPasswordResetForm, MyPasswordChangeForm
#
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('about', views.about, name='about'),
#     path('contact', views.contact, name='contact'),
#     path('profile',views.ProfileView.as_view(),name='profile'),
#     path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
#     path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),
#     path('product_details/<int:pk>', views.ProductDetails.as_view(), name='productdeatils'),
#     path('registration/', views.CustomerRegister.as_view(), name='customerregistration'),
#     path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
#     path('password-reset/',
#          auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm),
#          name='password_reset'),
#     path('password-change/',
#          auth_view.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm,
#                                               success_url='/passwordchangedone/'), name='password_change'),
#     path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),
#          name='passwordchangedone'),
#     path('logout/',auth_view.LogoutView.as_view(next_page='login'), name='logout'),
#
#
# ]
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
from .form import LoginForm, MyPasswordResetForm, MyPasswordChangeForm,MySetPasswordForm




urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('category-title/<val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product_details/<int:pk>/', views.ProductDetails.as_view(), name='productdeatils'),
    path('registration/', views.CustomerRegister.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='password_change'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm) , name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.show_card, name='show_cart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minuscart),
    path('removecart',views.removecart),
    path('paymentdone/', views.paymentdone, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),



]
