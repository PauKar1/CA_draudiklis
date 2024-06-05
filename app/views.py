from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import (KlientasRegistrationForm, ProfileUpdateForm, KlientasUpdateForm, KlientaiForm,
                    PolisaiForm, NaujaKlientoRegistracijosForma, BrokeriaiUpdateForm, BrokerLoginForm,
                    BrokerRegisterForm, TravelContractForm, InsuranceCostCalculationForm, UserRegisterForm,
                    BrokerKlientaiUserCreateForm, KlientaiUpdateForm)
from .models import (Profile, Country, Paslaugos, Klientai, Brokeriai, Polisai, BrokerProfile,
                     CountryRisk, Cover1, Cover2, Cover3, TravelMode, Iskaita)
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

    profile_picture_url = profile.picture.url if profile.picture else None
    return render(request, 'profile_edit.html', {'form': form, 'profile': profile, 'user_profile_picture': profile_picture_url})


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

    return render(request, 'profile.html', {'profile': klientai, 'contracts': contracts, })



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

            # Check if the email already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('broker_register')

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


@login_required
def broker_profile(request, broker_id):
    profile = get_object_or_404(BrokerProfile, broker__id=broker_id)
    clients = Klientai.objects.filter(polisai__brokeriai=profile.broker).distinct()
    contracts = Polisai.objects.filter(brokeriai=profile.broker)

    if request.method == 'POST':
        form = BrokeriaiUpdateForm(request.POST, instance=profile.broker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('broker_profile', broker_id=broker_id)
    else:
        form = BrokeriaiUpdateForm(instance=profile.broker)

    return render(request, 'broker_profile.html', {
        'profile': profile,
        'form': form,
        'clients': clients,
        'contracts': contracts,
        'user_profile_picture': profile.profile_picture.url if profile.profile_picture else None
    })


def broker_klientai_user_create(request):
    profile = BrokerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = BrokerKlientaiUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create a Klientai instance and associate it with the newly created user
            client = Klientai(user=user)
            client.save()

            messages.success(request, f'Klientas sėkmingai užregistruotas! Vartotojo vardas: {user.username}')
            return redirect('broker_update_klientas', client_id=client.id)
    else:
        form = BrokerKlientaiUserCreateForm()

    return render(request, 'broker_update_klientas.html', {'form': form})


def broker_update_klientas(request, client_id):
    klientas = get_object_or_404(Klientai, id=client_id, user=request.user)

    if request.method == 'POST':
        form = KlientaiUpdateForm(request.POST, instance=klientas)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('broker_profile', client_id=klientas.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = KlientaiUpdateForm(instance=klientas)

    return render(request, 'broker_update_klientas.html', {'form': form})

def broker_logout(request):
    logout(request)
    return render(request, 'broker_logout.html')

################ PRICE CALC

def price_calculator(request):
    if request.method == 'POST':
        form = InsuranceCostCalculationForm(request.POST)
        if form.is_valid():
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

            # Save the form data in the session
            request.session['policy_data'] = {
                'country': country.id,
                'travel_mode': travel_mode.id,
                'trip_duration': trip_duration,
                'cover1': cover1.id if cover1 else None,
                'cover2': cover2.id if cover2 else None,
                'cover3': cover3.id if cover3 else None,
                'iskaita': iskaita.id,
                'paslaugos': paslaugos.id,
            }

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
                'register_contract_url': reverse('register_policy'),  # Updated to 'register_policy'
            }
            return render(request, 'price_calculator.html', context)
        else:
            print(form.errors)
    else:
        form = InsuranceCostCalculationForm()

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
###### calculate and register client
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Sukurtas vartotojo profilis {username}!')
            login(request, user)
            return redirect('register_client')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def register_client(request):
    try:
        klientai = Klientai.objects.get(user=request.user)
        request.session['client_id'] = klientai.id
        messages.info(request, 'Jūs jau esate registruotas klientas.')
        return redirect('register_policy')
    except Klientai.DoesNotExist:
        pass

    if request.method == 'POST':
        form = KlientaiForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            request.session['client_id'] = client.id
            messages.success(request, 'Klientas sėkmingai užregistruotas. Dabar galite registruoti politiką.')
            return redirect('register_policy')
    else:
        form = KlientaiForm()
    return render(request, 'register_client.html', {'form': form})


@login_required
def register_policy(request):
    klientai = get_object_or_404(Klientai, user=request.user)

    if request.method == 'POST':
        klientai_form = KlientaiForm(request.POST, instance=klientai)
        polisai_form = PolisaiForm(request.POST)

        if klientai_form.is_valid():
            klientai_form.save()
            policy = polisai_form.save(commit=False)
            policy.klientai = klientai

            # Calculate the price
            country = policy.country
            travel_mode = policy.travel_mode
            trip_duration = (policy.pabaigos_data - policy.pradzios_data).days
            paslaugos_kaina = policy.paslaugos.kaina

            base_cost = paslaugos_kaina * trip_duration
            cover1_cost = base_cost * policy.cover1.na_kof if policy.cover1 else 0
            cover2_cost = base_cost * policy.cover2.civ_kof if policy.cover2 else 0
            cover3_cost = base_cost * policy.cover3.med_kof if policy.cover3 else 0
            iskaita_cost = policy.iskaita.sum

            total_cost = base_cost + cover1_cost + cover2_cost + cover3_cost - iskaita_cost
            policy.price = total_cost

            # Set the price in the form's cleaned data
            polisai_form.data = polisai_form.data.copy()
            polisai_form.data['price'] = total_cost

            if polisai_form.is_valid():
                policy.save()
                messages.success(request, 'Policy registered successfully.')
                return redirect('policy_success')
            else:
                print("Polisai Form errors:", polisai_form.errors)
        else:
            print("Klientai Form errors:", klientai_form.errors)
    else:
        klientai_form = KlientaiForm(instance=klientai)
        policy_data = request.session.get('policy_data', {})
        if policy_data:
            polisai_form = PolisaiForm(initial=policy_data)
        else:
            polisai_form = PolisaiForm()

        # Calculate price if data is available in session
        if 'country' in policy_data and 'paslaugos' in policy_data:
            country = Country.objects.get(id=policy_data['country'])
            travel_mode = TravelMode.objects.get(id=policy_data['travel_mode'])
            paslaugos = Paslaugos.objects.get(id=policy_data['paslaugos'])
            trip_duration = policy_data['trip_duration']
            cover1 = Cover1.objects.get(id=policy_data['cover1']) if policy_data['cover1'] else None
            cover2 = Cover2.objects.get(id=policy_data['cover2']) if policy_data['cover2'] else None
            cover3 = Cover3.objects.get(id=policy_data['cover3']) if policy_data['cover3'] else None
            iskaita = Iskaita.objects.get(id=policy_data['iskaita'])

            base_cost = paslaugos.kaina * trip_duration
            cover1_cost = base_cost * cover1.na_kof if cover1 else 0
            cover2_cost = base_cost * cover2.civ_kof if cover2 else 0
            cover3_cost = base_cost * cover3.med_kof if cover3 else 0
            iskaita_cost = iskaita.sum

            total_cost = base_cost + cover1_cost + cover2_cost + cover3_cost - iskaita_cost
            polisai_form.initial['price'] = total_cost

    return render(request, 'register_policy.html', {'klientai_form': klientai_form, 'polisai_form': polisai_form})

def policy_success(request):
    return render(request, 'policy_success.html')






###### for pricing part END