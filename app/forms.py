from django.contrib.auth.models import User
from django import forms
from .models import Profile, Polisai

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Vartotojas'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Slaptažodis'})
    )

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture']

class PolisaiForm(forms.ModelForm):
    class Meta:
        model = Polisai
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        paslaugos = cleaned_data.get("paslaugos")
        if paslaugos:
            cleaned_data['apsauga'] = paslaugos.aprasymas
        return cleaned_data