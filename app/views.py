from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import (KlientasRegistrationForm, ProfileUpdateForm, KlientasUpdateForm, KlientaiForm,
                    PolisaiForm, NaujaKlientoRegistracijosForma, BrokeriaiUpdateForm, BrokerLoginForm,
                    BrokerRegisterForm, TravelContractForm, InsuranceCostCalculationForm)
from .models import Profile, Country, Paslaugos, Klientai, Brokeriai, Polisai, BrokerProfile, CountryRisk
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction


def susi(request):
    return HttpResponse("Labas, pasauli!")


def home(request):
    return render(request, 'home.html')





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



####### TEST

def naujas_user_register(request):
    if request.method == 'POST':
        form = NaujaKlientoRegistracijosForma(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Paskyra sukurta: {user.username}!")
            return redirect('profile')  # Nukreipkite į tinkamą puslapį po registracijos
        else:
            messages.error(request, "Nepavyko sukurti paskyros. Patikrinkite formą.")
    else:
        form = NaujaKlientoRegistracijosForma()
    return render(request, 'naujas_user_register.html', {'form': form})


@login_required
def choose_account_type(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        if account_type == 'client':
            return redirect('update_klientas')
        elif account_type == 'broker':
            return redirect('update_brokeris')
    return render(request, 'choose_account_type.html')


@login_required
def update_brokeris(request):
    try:
        brokeris = request.user.brokeriai
    except Brokeriai.DoesNotExist:
        brokeris = Brokeriai(user=request.user)

    if request.method == 'POST':
        form = BrokeriaiUpdateForm(request.POST, instance=brokeris)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brokerio profilis sėkmingai atnaujintas!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = BrokeriaiUpdateForm(instance=brokeris)

    return render(request, 'update_brokeris.html', {'form': form})



##### profilis
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        username = request.POST.get('username')
        if form.is_valid():
            if username:
                request.user.username = username
                request.user.save()
            form.save()
            messages.success(request, 'Profilis sėkmingai atnaujintas!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form, 'profile': profile, 'user_profile_picture': profile.picture.url})

@login_required
def profile(request):
    username = request.user.username
    try:
        klientai = request.user.klientai
        contracts = Polisai.objects.filter(klientai=klientai)
    except Klientai.DoesNotExist:
        klientai = None
        contracts = []

    # Debugging output
    print("Username:", username)
    print("Klientai:", klientai)
    for contract in contracts:
        print("Contract ID:", contract.id, "Klientai ID:", contract.klientai_id)

    return render(request, 'profile.html', {'profile': klientai, 'contracts': contracts})



#####static() fields

def draudimo_produktai(request):
    return render(request, 'draudimo_produktai.html')

def keliones_draudimas(request):
    return render(request, 'keliones_draudimas.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    return render(request, 'contact.html')


###### Brokerių

def broker_login(request):
    if request.method == 'POST':
        form = BrokerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    broker = Brokeriai.objects.get(el_pastas=email)
                    login(request, user)
                    return redirect('broker_profile', broker_id=broker.id)
                except Brokeriai.DoesNotExist:
                    form.add_error(None, 'Brokerio informacija neteisinga.')
            else:
                form.add_error(None, 'Neteisingas vartotojo vardas arba slaptažodis.')
    else:
        form = BrokerLoginForm()
    return render(request, 'broker_login.html', {'form': form})


def broker_register(request):
    if request.method == 'POST':
        form = BrokerRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['el_pastas']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=email, email=email, password=password)
            broker = form.save(commit=False)
            broker.user = user
            broker.save()

            # Create a BrokerProfile
            broker_profile = BrokerProfile.objects.create(user=user, broker=broker)

            login(request, user)
            return redirect('broker_profile', broker_id=broker.id)
    else:
        form = BrokerRegisterForm()
    return render(request, 'broker_register.html', {'form': form})

def broker_profile(request, broker_id):
    profile = get_object_or_404(BrokerProfile, broker__id=broker_id)
    return render(request, 'broker_profile.html', {
        'profile': profile,
        'user_profile_picture': request.user.brokerprofile.profile_picture.url
    })
def broker_logout(request):
    logout(request)
    return render(request, 'broker_logout.html')

################ PRICE CALC

def price_calculator(request):
    if request.method == 'POST':
        form = InsuranceCostCalculationForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            country = form.cleaned_data['country']
            travel_mode = form.cleaned_data['travel_mode']
            trip_duration = form.cleaned_data['trip_duration']
            cover1 = form.cleaned_data.get('cover1')
            cover2 = form.cleaned_data.get('cover2')
            cover3 = form.cleaned_data.get('cover3')
            iskaita = form.cleaned_data['iskaita']
            paslaugos = form.cleaned_data['paslaugos']
            paslaugos_kaina = paslaugos.kaina

            # Perform the cost calculation logic
            base_cost = paslaugos_kaina * trip_duration
            cover1_cost = base_cost * cover1.na_kof if cover1 else 0
            cover2_cost = base_cost * cover2.civ_kof if cover2 else 0
            cover3_cost = base_cost * cover3.med_kof if cover3 else 0
            iskaita_cost = iskaita.sum

            total_cost = base_cost + cover1_cost + cover2_cost + cover3_cost - iskaita_cost

            context = {
                'form': form,
                'total_cost': total_cost,
                'country': country,
                'travel_mode': travel_mode,
                'trip_duration': trip_duration,
                'cover1': cover1,
                'cover2': cover2,
                'cover3': cover3,
                'iskaita': iskaita,
                'paslaugos_kaina': paslaugos_kaina,
            }
            return render(request, 'price_calculator.html', context)
        else:
            print(form.errors)
    else:
        form = InsuranceCostCalculationForm()
        form.initial['country'] = form.fields['country'].queryset.first().pk

    return render(request, 'price_calculator.html', {'form': form})



@login_required
def register_contract(request):
    if request.method == 'POST':
        klientai_form = KlientaiForm(request.POST)
        polisai_form = TravelContractForm(request.POST)
        if klientai_form.is_valid() and polisai_form.is_valid():
            klientai = klientai_form.save(commit=False)
            klientai.user = request.user  # Associate with authenticated user
            klientai.save()

            polisai = polisai_form.save(commit=False)
            polisai.klientai = klientai

            # Check if the klientai belongs to the broker
            if klientai.broker == request.user.brokerprofile.broker:
                polisai.save()
                # Redirect to a success page or appropriate URL
                return redirect('broker_profile')
            else:
                # Broker does not have permission to register contract for this client
                # You can add error handling or redirect to an error page
                pass

    else:
        klientai_form = KlientaiForm()
        polisai_form = TravelContractForm()

    return render(request, 'register_contract.html', {'klientai_form': klientai_form, 'polisai_form': polisai_form})


#############
###### for pricing part

def register_client(request):

    if request.method == 'POST':
        form = KlientaiForm(request.POST)
        if form.is_valid():
            client = form.save()
            request.session['client_id'] = client.id
            messages.success(request, 'Client registered successfully. Now proceed to register the policy.')
            return redirect('broker_profile')
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

###### for pricing part END