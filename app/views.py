from django.http import HttpResponse
from .AA_calculations import COUNTRY_RISK_LEVELS, COUNTRY_SURCHARGES
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Paslaugos, Klientai
from datetime import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import ProfileUpdateForm
from .models import Profile

def susi(request):
 return HttpResponse("Labas, pasauli!")


def home(request):
    return render(request, 'home.html')


################ PRICE CALC
def get_all_countries():
    all_countries = []
    for risk_level_countries in COUNTRY_RISK_LEVELS.values():
        all_countries.extend(risk_level_countries)
    return all_countries

def price_calculator(request):
    return render(request, 'price_calculator.html')

def calculate_price(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging line to check received POST data
        country = request.POST.get('country')
        travel_mode = request.POST.get('travel_mode')
        trip_duration = request.POST.get('trip_duration')

        print(f"Country: {country}, Travel Mode: {travel_mode}, Trip Duration: {trip_duration}")  # Debugging line

        if not all([country, travel_mode, trip_duration]):
            print("Missing required fields.")
            return HttpResponseBadRequest("Missing required fields.")

        # Country risk level
        country_risk_level = get_country_risk_level(country)
        print(f"Country Risk Level: {country_risk_level}")  # Debugging line
        if country_risk_level is None:
            return HttpResponseBadRequest("Country risk level not found.")

        # Country surcharge
        country_surcharge = get_country_surcharge(country_risk_level)
        print(f"Country Surcharge: {country_surcharge}")  # Debugging line

        # Base price per day
        base_price_per_day = get_base_price_per_day()
        print(f"Base Price Per Day: {base_price_per_day}")  # Debugging line

        # Calculate total price
        total_price = calculate_total_price(base_price_per_day, int(trip_duration), country_surcharge, travel_mode)
        print(f"Total Price: {total_price}")  # Debugging line

        return render(request, 'price_calculator.html', {'total_price': total_price})

    return render(request, 'price_calculator.html')

def get_country_risk_level(country):
    for risk_level, countries in COUNTRY_RISK_LEVELS.items():
        if country in countries:
            return risk_level
    return None

def get_country_surcharge(risk_level):
    if risk_level == 'high':
        return 0.80
    elif risk_level == 'medium':
        return 0.50
    elif risk_level == 'low':
        return 0.20
    else:
        return 10.0

def get_base_price_per_day():
    try:
        paslauga = Paslaugos.objects.get(pavadinimas="Kelionių draudimas")
        return paslauga.kaina
    except Paslaugos.DoesNotExist:
        return 10.0

def calculate_total_price(base_price_per_day, trip_duration, country_surcharge, travel_mode):
    TRAVEL_MODE_MULTIPLIERS = {
        'plane': 1.5,
        'car': 1.2,
        'motorcycle': 1.3,
        'ship': 1.4,
        'bike': 2.1,
        'foot': 2.0
    }
    travel_mode_multiplier = TRAVEL_MODE_MULTIPLIERS.get(travel_mode, 1.0)
    base_price = base_price_per_day * trip_duration
    total_price = base_price * travel_mode_multiplier + country_surcharge
    return total_price







############### REGISTRATION
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm

def kliento_paskyra(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('Vartotojo vardas')
            password = form.cleaned_data.get('Slaptažodis')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Sveiki atvykę, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Neteisingas vartotojo vardas arba slaptažodis.")
        else:
            messages.error(request, "Neteisingas vartotojo vardas arba slaptažodis.")
    else:
        form = AuthenticationForm()
    return render(request, 'kliento_paskyra.html', {'form': form})

def registracija(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto log userį suvedant
            username = form.cleaned_data.get('Vartotojo vardas')
            messages.success(request, f"Paskyra sukurta: {username}!")
            return redirect('home')
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
    else:
        form = UserCreationForm()
    return render(request, 'registracija.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Jūs sėkmingai atsijungėte.")
    return redirect('home')

def kliento_paskyra(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or any other page after successful login
            else:
                form.add_error(None, "Neteisingas vartotojo vardas arba slaptažodis")
    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

@login_required
def client_policies(request):
    try:
        klientas = Klientai.objects.get(user=request.user)
        policies = klientas.polisai.all()
    except Klientai.DoesNotExist:
        policies = []
    return render(request, 'client_policies.html', {'policies': policies})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})



####################### REGISTER CONTRACT
from .forms import KlientaiForm, PolisaiForm

@login_required
def registruoti_sutarti(request):

    if request.method == 'POST':
        klientai_form = KlientaiForm(request.POST)
        polisai_form = PolisaiForm(request.POST)
        if klientai_form.is_valid() and polisai_form.is_valid():
            klientas = klientai_form.save()
            polisas = polisai_form.save(commit=False)
            polisas.klientai = klientas
            polisas.save()
            messages.success(request, "Sutartis sėkmingai užregistruota!")
            return redirect('success_url')  # Replace with your success URL
    else:
        klientai_form = KlientaiForm()
        polisai_form = PolisaiForm()

    return render(request, 'register_contract.html', {
        'klientai_form': klientai_form,
        'polisai_form': polisai_form,
    })