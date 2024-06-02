from django.contrib.auth.models import User
from django import forms
from .models import Profile, Polisai, Klientai
from .widgets import DeductibleSelect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm


class KlientasRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

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

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        klientas = super().save(commit=False)
        username = self.cleaned_data['username']
        email = self.cleaned_data['el_pastas']

        # Patikrinkime, ar vartotojas su tokiu username arba email jau egzistuoja
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")

        # Sukurkime naują vartotoją
        user = User(username=username, email=email)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            try:
                user.save()
                klientas.user = user
                klientas.save()
            except IntegrityError:
                user.delete()
                raise forms.ValidationError("Failed to save client. User already associated with another client.")
        return klientas



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
    iskaita = forms.ChoiceField(
        choices=Polisai.ISKAITA_CHOICES,
        widget=DeductibleSelect  # not used
    )

    class Meta:
        model = Polisai
        fields = ['klientai', 'brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'draudimo_suma', 'iskaita', 'apsauga']


class PriceCalculatorForm(forms.ModelForm):
    class Meta:
        model = Polisai
        fields = ['draudimo_suma', 'iskaita', 'apsauga']



###### TEST
class NaujaKlientoRegistracijosForma(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user