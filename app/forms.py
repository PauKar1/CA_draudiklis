from django.contrib.auth.models import User
from django import forms
from .models import Profile, Polisai, Klientai, Brokeriai
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

class KlientaiForm(forms.ModelForm):
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


class PolisaiForm(forms.ModelForm):
    pradzios_data = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    pabaigos_data = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))


    class Meta:
        model = Polisai
        fields = ['brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'draudimo_suma', 'iskaita', 'apsauga']


class PriceCalculatorForm(forms.ModelForm):
    class Meta:
        model = Polisai
        fields = ['draudimo_suma', 'iskaita', 'apsauga']



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
