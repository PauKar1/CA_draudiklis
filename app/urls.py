# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),  # Pagrindinis puslapis
    path('price-calculator/', views.price_calculator, name='price_calculator'),  # Draudimo kainos skaičiuoklė

    # path('calculate-price/', views.calculate_price, name='calculate_price'),
    path('app/kliento_paskyra/', views.kliento_paskyra, name='kliento_paskyra'),  # Kliento paskyros peržiūra
    path('registracija/', views.registracija, name='registracija'),  # Naujo vartotojo registracija
    path('app/atsijungti/', views.logout_view, name='logout'),  # Vartotojo atsijungimas

    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),  # Slaptažodžio atstatymo užklausos forma
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Slaptažodžio atstatymo užklausos išsiuntimas
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Slaptažodžio atstatymo patvirtinimas
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Slaptažodžio atstatymo pabaiga
    path('client_policies/', views.client_policies, name='client_policies'),  # Kliento poliso peržiūra

    path('register/', views.register, name='register'),  # Vartotojo registracija
    path('register_client/', views.register_client, name='register_client'),  # Kliento registracija
    path('register_policy/', views.register_policy, name='register_policy'),  # Poliso registracija
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),  # Vartotojo prisijungimas
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),  # Vartotojo atsijungimas
    path('policy_success/', views.policy_success, name='policy_success'),  # Sėkmingai sukurtas polisas

    path('register_contract/', views.register_contract, name='register_contract'),  # Kontrakto registracija
    path('map/', views.map_view, name='map_view'),  # Žemėlapio peržiūra
    path('update_klientas/', views.update_klientas, name='update_klientas'),  # Kliento informacijos atnaujinimas

    path('naujas_user_register/', views.naujas_user_register, name='naujas_user_register'),  # Naujo vartotojo registracija
    path('choose_account_type/', views.choose_account_type, name='choose_account_type'),  # Pasirinkti paskyros tipą
    path('update_klientas/', views.update_klientas, name='update_klientas'),  # Kliento informacijos atnaujinimas
    path('update_brokeris/', views.update_brokeris, name='update_brokeris'),  # Brokerio informacijos atnaujinimas

    path('profile/edit/', views.profile_view, name='profile_view'),  # Profilio redagavimas
    path('profile/', views.profile, name='profile'),  # Profilio peržiūra

    path('draudimo-produktai/', views.draudimo_produktai, name='draudimo_produktai'),  # Draudimo produktų peržiūra
    path('draudimo-produktai/keliones-draudimas/', views.keliones_draudimas, name='keliones_draudimas'),  # Kelionių draudimo peržiūra
    path('faq/', views.faq, name='faq'),  # Dažniausiai užduodami klausimai
    path('contact/', views.contact, name='contact'),  # Kontaktų forma

    path('partneriams/login/', views.broker_login, name='broker_login'),  # Brokerio prisijungimas
    path('partneriams/register/', views.broker_register, name='broker_register'),  # Brokerio registracija
    path('partneriams/profile/<int:broker_id>/', views.broker_profile, name='broker_profile'),  # Brokerio profilis
    path('partneriams/logout/', views.broker_logout, name='broker_logout'),  # Brokerio atsijungimas

    path('broker/register-client-user/', views.broker_klientai_user_create, name='broker_klientai_user_create'),  # Brokeris registruoja kliento vartotoją
    path('broker/update-klientas/<int:client_id>/', views.broker_update_klientas, name='broker_update_klientas'),  # Brokeris atnaujina kliento informaciją
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Medijų failų aptarnavimas debug režime
