from django.contrib.auth.models import User
from django import forms
from .models import Profile, Polisai, Klientai, Brokeriai, Country, Paslaugos, TravelMode, Cover1, Cover2, Cover3, Iskaita
from .widgets import DeductibleSelect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class KlientasRegistrationForm(forms.ModelForm):
    class Meta:
        model = Klientai
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas', 'el_pastas']
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            'gimimo_data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adresas': forms.TextInput(attrs={'class': 'form-control'}),
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        klientas = super().save(commit=False)
        username = self.cleaned_data['username']
        email = self.cleaned_data['el_pastas']

        # Patikrinkime, ar vartotojas su tokiu username arba email jau egzistuoja
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")

        # # Sukurkime naują vartotoją
        # user = User(username=username, email=email)
        # user.set_password(self.cleaned_data['password1'])
        # if commit:
        #     try:
        #         user.save()
        #         klientas.user = user
        #         klientas.save()
        #     except IntegrityError:
        #         user.delete()
        #         raise forms.ValidationError("Failed to save client. User already associated with another client.")
        # return klientas



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']




class KlientasUpdateForm(forms.ModelForm):
    class Meta:
        model = Klientai
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas', 'el_pastas']
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            'gimimo_data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adresas': forms.TextInput(attrs={'class': 'form-control'}),
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
        }

###### used after calculating price in site to register client and policy
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Vartotojo vardas',
            'password1': 'Slaptažodis',
            'password2': 'Slaptažodžio patvirtinimas',
        }

class PolisaiForm(forms.ModelForm):
    pradzios_data = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    pabaigos_data = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    price = forms.FloatField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = Polisai
        fields = ['brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'iskaita', 'country', 'travel_mode',
                  'cover1', 'cover2', 'cover3', 'price']
        labels = {
            'brokeriai': 'Brokeris',
            'paslaugos': 'Paslaugos',
            'pradzios_data': 'Pradžios data',
            'pabaigos_data': 'Pabaigos data',
            'iskaita': 'Išskaita',
            'country': 'Šalis',
            'travel_mode': 'Kelionės būdas',
            'cover1': 'Nelaimingi atsitikimai',
            'cover2': 'Civilinė atsakomybė',
            'cover3': 'Medicininės išlaidos',
            'price': 'Kaina'
        }

class KlientaiForm(forms.ModelForm):
    class Meta:
        model = Klientai
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas', 'el_pastas']
        labels = {
            'vardas': 'Vardas',
            'pavarde': 'Pavardė',
            'tel_numeris': 'Tel numeris',
            'gimimo_data': 'Gimimo data',
            'adresas': 'Adresas',
            'el_pastas': 'El. paštas',
        }
        widgets = {
            'adresas': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

###### TEST
class NaujaKlientoRegistracijosForma(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _("Vartotojo vardas"),
            'password1': _("Slaptažodis"),
            'password2': _("Slaptažodžio patvirtinimas"),
        }
        help_texts = {
            'username': _("Privalomas. 150 arba mažiau simbolių. Raidės, skaičiai bei @/./+/-/_ simboliai."),
            'password1': _(
                "<ul>"
                "<li>Jūsų slaptažodį turi sudaryti bent 8 simboliai.</li>"
                "<li>Jūsų slaptažodis neturi būti per daug panašus į kitą jūsų asmeninę informaciją.</li>"
                "<li>Jūsų slaptažodis negali būti dažnai naudojamas slaptažodis.</li>"
                "<li>Jūsų slaptažodis negali būti vien skaičiai.</li>"
                "</ul>"
            ),
            'password2': _("Patikrinimui įveskite tokį patį slaptažodį, kaip anksčiau."),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

##### TEST nenaudojama
class BrokeriaiUpdateForm(forms.ModelForm):
    class Meta:
        model = Brokeriai
        fields = ['vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas', 'tel_numeris']
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),
            'imones_pavadinimas': forms.TextInput(attrs={'class': 'form-control'}),
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
        }

###### Brokerių etapas
class BrokerLoginForm(forms.Form):
    # username = forms.CharField(max_length=100, label='Vartotojo vardas')
    # company = forms.CharField(max_length=100, label='Brokerio įmonė')
    email = forms.EmailField(label='El. paštas')
    password = forms.CharField(widget=forms.PasswordInput, label='Slaptažodis')


class BrokerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Slaptažodis')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Slaptažodžio patvirtinimas')

    class Meta:
        model = Brokeriai
        fields = ['vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas', 'tel_numeris']
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),
            'imones_pavadinimas': forms.TextInput(attrs={'class': 'form-control'}),
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError("Slaptažodžiai nesutampa")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password1 = cleaned_data.get("password1")

        if password and password1 and password != password1:
            self.add_error('password1', "Slaptažodžiai nesutampa")

class BrokerKlientaiUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Slaptažodis')
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Patvirtinkite slaptažodį')

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Slaptažodžiai nesutampa")
        return password_confirmation

class KlientaiUpdateForm(forms.ModelForm):
    class Meta:
        model = Klientai
        fields = ['vardas', 'pavarde', 'adresas', 'tel_numeris', 'el_pastas', 'gimimo_data']
        widgets = {
            'gimimo_data': forms.DateInput(attrs={'type': 'date'}),
        }

###### TEST
class TravelContractForm(forms.Form):
    klientas = forms.ModelChoiceField(queryset=Klientai.objects.all(), label='Klientas', required=False)
    brokeris = forms.ModelChoiceField(queryset=Brokeriai.objects.all(), label='Brokeris', required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label='Šalis')
    travel_start_date = forms.DateField(label='Kelionės pradžios data')
    travel_end_date = forms.DateField(label='Kelionės pabaigos data')
    paslaugos = forms.ModelChoiceField(queryset=Paslaugos.objects.all(), label='Paslaugos')
    cover3 = forms.ModelChoiceField(queryset=Cover1.objects.all(), label='Medicininės išlaidos', required=False)
    cover1 = forms.ModelChoiceField(queryset=Cover2.objects.all(), label='Nelaimingi atsitikimai', required=False)
    cover2 = forms.ModelChoiceField(queryset=Cover3.objects.all(), label='Civilinė atsakomybė', required=False)
    travel_mode = forms.ModelChoiceField(queryset=TravelMode.objects.all(), label='Kelionės būdas')
    iskaita = forms.ModelChoiceField(queryset=Iskaita.objects.all(), label='Išskaita', required=False)
    total_price = forms.FloatField(label='Viso kaina', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))


##### price calc

class InsuranceCostCalculationForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label='Pasirinkite šalį')
    travel_mode = forms.ModelChoiceField(queryset=TravelMode.objects.all(), label='Keliavimo būdas')
    trip_duration = forms.IntegerField(label='Kelionės dienų skaičius')
    cover1 = forms.ModelChoiceField(queryset=Cover1.objects.all(), label='Nelaimingi atsitikimai', required=False)
    cover2 = forms.ModelChoiceField(queryset=Cover2.objects.all(), label='Civilinė atsakomybė', required=False)
    cover3 = forms.ModelChoiceField(queryset=Cover3.objects.all(), label='Medicininės išlaidos', required=True)
    iskaita = forms.ModelChoiceField(queryset=Iskaita.objects.all(), label='Taikoma išskaita')
    paslaugos = forms.ModelChoiceField(queryset=Paslaugos.objects.all(), label='Paslaugos', widget=forms.HiddenInput, required=True)

    class Meta:
        model = Polisai
        fields = ['country', 'travel_mode', 'trip_duration', 'cover1', 'cover2', 'cover3', 'iskaita', 'paslaugos']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'paslaugos' not in kwargs['initial']:
            default_paslaugos = Paslaugos.objects.get(pk=1)  # Assuming the default is Kelionių draudimas
            self.fields['paslaugos'].initial = default_paslaugos.pk
        elif not self.fields['paslaugos'].initial:
            default_paslaugos = Paslaugos.objects.get(pk=1)
            self.fields['paslaugos'].initial = default_paslaugos.pk

    def clean_paslaugos(self):
        paslaugos = self.cleaned_data.get('paslaugos')
        if not paslaugos:
            default_paslaugos = Paslaugos.objects.get(pk=1)  # Assuming the default is Kelionių draudimas
            return default_paslaugos
        return paslaugos

