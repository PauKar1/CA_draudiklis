from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import KlientasRegistrationForm, ProfileUpdateForm, KlientasUpdateForm, KlientaiForm, PolisaiForm, NaujaKlientoRegistracijosForma
from .models import Profile, Country, Paslaugos, Klientai
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Klientai, Profile
from django.db import IntegrityError, transaction


def susi(request):
    return HttpResponse("Labas, pasauli!")


def home(request):
    return render(request, 'home.html')


################ PRICE CALC


def price_calculator(request):
    countries = Country.objects.all()
    selected_country = request.GET.get('country', '')

    return render(request, 'price_calculator.html', {
        'countries': countries,
        'selected_country': selected_country,
    })


def get_country_risk_level(country):
    country_obj = Country.objects.filter(name=country).first()
    return country_obj.risk_level if country_obj else None


def get_country_surcharge(risk_level):
    # Dummy function for example purposes
    surcharge_mapping = {
        'low': 0.4,
        'medium': 0.6,
        'high': 1.5,
        'very high': 3.0
    }
    return surcharge_mapping.get(risk_level, 1.0)


def get_base_price_per_day():
    try:
        paslauga = Paslaugos.objects.get(pavadinimas="Kelionių draudimas")
        return paslauga.kaina
    except Paslaugos.DoesNotExist:
        return 10.0


def calculate_total_price(base_price, duration, surcharge, travel_mode, draudimo_suma, iskaita, apsauga):
    # Example calculation logic, adjust as needed
    travel_mode_factor = {
        'plane': 0.5,
        'car': 0.8,
        'motorcycle': 1.0,
        'ship': 0.6,
        'bike': 1.5,
        'foot': 1.7
    }
    mode_factor = travel_mode_factor.get(travel_mode, 1.0)
    apsauga_factor = {
        'medicinines_islados': 0.2,
        'nelaimingi_atsitikimai': 4.0,
        'civiline_atsakomybe': 2.0
    }
    draudimo_suma_factor = {
        '100,000': 0.0,
        '300,000': 0.5,
        '500,000': 0.7,
    }
    iskaita_factor = {
        '0': 1.0,
        '50': 0.8,
        '80': 0.6,
        '100': 0.5,
        '120': 0.4,
    }
    apsauga_factor_value = apsauga_factor.get(apsauga, 1.0)
    draudimo_suma_factor_value = draudimo_suma_factor.get(apsauga, 1.0)
    iskaita_factor_value = iskaita_factor.get(apsauga, 1.0)
    total_price = ((base_price + apsauga_factor_value) * (
                surcharge * mode_factor * apsauga_factor_value * draudimo_suma_factor_value * iskaita_factor_value) * duration)
    return total_price


def calculate_price(request):
    countries = Country.objects.all()
    if request.method == 'POST':
        print(request.POST)  # Debugging line to check received POST data
        country = request.POST.get('country')
        travel_mode = request.POST.get('travel_mode')
        trip_duration = request.POST.get('trip_duration')
        draudimo_suma = request.POST.get('draudimo_suma')
        iskaita = request.POST.get('iskaita')
        apsauga = request.POST.get('apsauga')

        print(
            f"Country: {country}, Travel Mode: {travel_mode}, Trip Duration: {trip_duration}, Draudimo Suma: {draudimo_suma}, Iskaita: {iskaita}, Apsauga: {apsauga}")  # Debugging line

        if not all([country, travel_mode, trip_duration, draudimo_suma, iskaita, apsauga]):
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
        total_price = calculate_total_price(
            base_price_per_day,
            int(trip_duration),
            country_surcharge,
            travel_mode,
            int(draudimo_suma),
            int(iskaita),
            apsauga
        )
        print(f"Total Price: {total_price}")  # Debugging line

        return render(request, 'price_calculator.html', {'total_price': total_price, 'countries': countries})

    return render(request, 'price_calculator.html', {'countries': countries})

################### MAP

def map_view(request):
    return render(request, 'country_map.html')

############### REGISTRATION


def registracija(request):
    if request.method == 'POST':
        form = KlientasRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    klientas = form.save(commit=False)
                    password = form.cleaned_data['password1']
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['el_pastas']

                    # Ensure the username is unique
                    if User.objects.filter(username=username).exists():
                        unique_suffix = 1
                        while User.objects.filter(username=f"{username}{unique_suffix}").exists():
                            unique_suffix += 1
                        username = f"{username}{unique_suffix}"

                    # Check if a user with this email already exists
                    user, created = User.objects.get_or_create(email=email, defaults={'username': username})
                    if not created:
                        if Klientai.objects.filter(user=user).exists():
                            messages.error(request, "Nepavyko sukurti paskyros. Vartotojas jau susietas su kitu klientu.")
                            return render(request, 'registracija.html', {'form': form})
                        else:
                            # Update the username if it was modified to ensure uniqueness
                            user.username = username
                            user.set_password(password)
                            user.save()
                    else:
                        user.set_password(password)
                        user.save()

                    # Assign user to 'Klientai' group
                    group, group_created = Group.objects.get_or_create(name='Klientai')
                    user.groups.add(group)

                    # Attach user to klientas and save
                    klientas.user = user
                    klientas.save()

                    # Create or get profile
                    try:
                        profile = user.profile
                    except Profile.DoesNotExist:
                        profile = Profile(user=user)
                    profile.save()

                    # Authenticate and login the user
                    authenticated_user = authenticate(username=username, password=password)
                    if authenticated_user is not None:
                        login(request, authenticated_user)
                        messages.success(request, f"Paskyra sukurta: {username}!")
                        return redirect('registracija_success')
            except IntegrityError as e:
                messages.error(request, "Nepavyko sukurti paskyros dėl vidinės klaidos.")
                print(f"IntegrityError: {e}")  # Debugging output
            except Exception as e:
                messages.error(request, "Nepavyko sukurti paskyros dėl vidinės klaidos.")
                print(f"Exception: {e}")  # Debugging output
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
            print(form.errors)  # Debugging output to check form errors
    else:
        form = KlientasRegistrationForm()
    return render(request, 'registracija.html', {'form': form})

@login_required
def registracija_success(request):
    return render(request, 'registracija_success.html', {'user': request.user})

def logout_view(request):
    logout(request)
    messages.info(request, "Jūs sėkmingai atsijungėte.")
    return redirect('home')

def kliento_paskyra(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
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

@login_required
def update_klientas(request):
    try:
        klientas = request.user.klientai
    except Klientai.DoesNotExist:
        klientas = Klientai(user=request.user)

    if request.method == 'POST':
        form = KlientasUpdateForm(request.POST, instance=klientas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = KlientasUpdateForm(instance=klientas)

    return render(request, 'update_klientas.html', {'form': form})

def register_contract(request):
    klientai_form = KlientaiForm()
    polisai_form = PolisaiForm()

    if request.method == 'POST':
        if 'register_client' in request.POST:
            klientai_form = KlientaiForm(request.POST)
            if klientai_form.is_valid():
                klientai_form.save()
                messages.success(request, 'Client registered successfully.')
                return redirect('register_contract')
            else:
                messages.error(request, 'Error registering client.')
                print(klientai_form.errors)  # Debugging: Print form errors to the console
        elif 'register_policy' in request.POST:
            polisai_form = PolisaiForm(request.POST)
            if polisai_form.is_valid():
                polisai_form.save()
                messages.success(request, 'Policy registered successfully.')
                return redirect('policy_success')  # Redirect to a success page or appropriate URL
            else:
                messages.error(request, 'Error registering policy.')
                print(polisai_form.errors)  # Debugging: Print form errors to the console

    klientai_list = Klientai.objects.all()  # List of all registered clients

    return render(request, 'register_contract.html', {
        'klientai_form': klientai_form,
        'polisai_form': polisai_form,
        'klientai_list': klientai_list,
    })

def register_client(request):
    if request.method == 'POST':
        form = KlientaiForm(request.POST)
        if form.is_valid():
            client = form.save()
            # Store the client ID in the session
            request.session['client_id'] = client.id
            messages.success(request, 'Client registered successfully. Now proceed to register the policy.')
            return redirect('register_policy')
    else:
        form = KlientaiForm()
    return render(request, 'register_client.html', {'form': form})

def register_policy(request):
    client_id = request.session.get('client_id')
    if not client_id:
        messages.error(request, 'You need to register a client first.')
        return redirect('register_client')

    klientai = get_object_or_404(Klientai, id=client_id)

    if request.method == 'POST':
        form = PolisaiForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.klientai = klientai
            policy.save()
            messages.success(request, 'Policy registered successfully.')
            return redirect('policy_success')  # Redirect to a success page or appropriate URL
    else:
        form = PolisaiForm()

    return render(request, 'register_policy.html', {'form': form, 'klientai': klientai})


####### TEST

def naujas_user_register(request):
    if request.method == 'POST':
        form = NaujaKlientoRegistracijosForma(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Paskyra sukurta: {user.username}!")
            return redirect('update_klientas')  # Nukreipkite į tinkamą puslapį po registracijos
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
    else:
        form = NaujaKlientoRegistracijosForma()
    return render(request, 'update_klientas.html', {'form': form})