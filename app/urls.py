from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
 path('', views.home, name='home'),
 path('price-calculator/', views.price_calculator, name='price_calculator'),
 path('calculate-price/', views.calculate_price, name='calculate_price'),
 path('app/kliento_paskyra/', views.kliento_paskyra, name='kliento_paskyra'),
 path('app/registracija/', views.registracija, name='registracija'),
 path('app/atsijungti/', views.logout_view, name='logout'),
 path('login/', auth_view.LoginView.as_view(), name='login'),
 path('logout/', auth_view.LogoutView.as_view(), name='logout'),
 path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
 path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
 path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
 path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
 path('profile/', views.profile_view, name='profile'),
 path('client_policies/', views.client_policies, name='client_policies'),
 path('register_client/', views.register_client, name='register_client'),
 path('register_policy/', views.register_policy, name='register_policy'),
    path('register_contract/', views.register_contract, name='register_contract'),
 path('map/', views.map_view, name='map_view'),
]
