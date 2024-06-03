# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('price-calculator/', views.price_calculator, name='price_calculator'),
    path('calculate-price/', views.calculate_price, name='calculate_price'),
    path('app/kliento_paskyra/', views.kliento_paskyra, name='kliento_paskyra'),
    path('registracija/', views.registracija, name='registracija'),
    path('app/atsijungti/', views.logout_view, name='logout'),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('client_policies/', views.client_policies, name='client_policies'),
    path('register_client/', views.register_client, name='register_client'),
    path('register_policy/', views.register_policy, name='register_policy'),
    path('register_contract/', views.register_contract, name='register_contract'),
    path('map/', views.map_view, name='map_view'),
    path('update_klientas/', views.update_klientas, name='update_klientas'),

    path('naujas_user_register/', views.naujas_user_register, name='naujas_user_register'),
    path('choose_account_type/', views.choose_account_type, name='choose_account_type'),
    path('update_klientas/', views.update_klientas, name='update_klientas'),
    path('update_brokeris/', views.update_brokeris, name='update_brokeris'),

    path('profile/edit/', views.profile_view, name='profile_view'),
    path('profile/', views.profile, name='profile'),

    path('draudimo-produktai/', views.draudimo_produktai, name='draudimo_produktai'),
    path('draudimo-produktai/keliones-draudimas/', views.keliones_draudimas, name='keliones_draudimas'),

    path('partneriams/', views.broker_login, name='broker_login'),
    path('partneriams/register/', views.broker_register, name='broker_register'),
    path('partneriams/profile/<int:broker_id>/', views.broker_profile, name='broker_profile'),
    path('partneriams/logout/', auth_view.LogoutView.as_view(next_page='home'), name='broker_logout'),
    path('logout/', auth_view.LogoutView.as_view(next_page='home'), name='logout'),

]
