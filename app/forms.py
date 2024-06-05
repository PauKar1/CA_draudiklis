from django.contrib.auth.models import User
from django import forms
from .models import Profile, Polisai, Klientai, Brokeriai, Country, Paslaugos, TravelMode, Cover1, Cover2, Cover3, \
    Iskaita
from .widgets import DeductibleSelect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class KlientasRegistrationForm(forms.ModelForm):
    class Meta:
        model = Klientai  # Nustato, kad ši forma naudoja Klientai modelį
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas',
                  'el_pastas']  # Nurodo, kurie modelio laukai bus naudojami formoje
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'vardas' lauką kaip form-control
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'pavarde' lauką kaip form-control
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'tel_numeris' lauką kaip form-control
            'gimimo_data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Stilizuoja 'gimimo_data' lauką kaip form-control su date tipo
            'adresas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'adresas' lauką kaip form-control
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'el_pastas' lauką kaip form-control
        }

    def save(self, commit=True):
        klientas = super().save(commit=False)  # Išsaugo formos duomenis, bet dar neišsaugo į duomenų bazę
        username = self.cleaned_data['username']  # Gauk išvalytą 'username' vertę
        email = self.cleaned_data['el_pastas']  # Gauk išvalytą 'el_pastas' vertę

        # Patikrina, ar vartotojas su tokiu vardu jau egzistuoja
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with this username already exists.")

        # Patikrina, ar vartotojas su tokiu el. pašto adresu jau egzistuoja
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email already exists.")

        return klientas  # Grąžina neišsaugotą 'klientas' objektą


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Nustato, kad ši forma naudoja Profile modelį
        fields = ['picture']  # Nurodo, kad forma turi tik 'picture' lauką


class KlientasUpdateForm(forms.ModelForm):
    class Meta:
        model = Klientai  # Nustato, kad ši forma naudoja Klientai modelį
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas',
                  'el_pastas']  # Nurodo, kurie modelio laukai bus naudojami formoje
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'vardas' lauką kaip form-control
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'pavarde' lauką kaip form-control
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'tel_numeris' lauką kaip form-control
            'gimimo_data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Stilizuoja 'gimimo_data' lauką kaip form-control su date tipo
            'adresas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'adresas' lauką kaip form-control
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'el_pastas' lauką kaip form-control
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Prideda el. pašto lauką į UserCreationForm

    class Meta:
        model = User  # Nustato, kad ši forma naudoja User modelį
        fields = ['username', 'email', 'password1',
                  'password2']  # Nurodo, kurie modelio laukai bus naudojami formoje
        labels = {
            'username': 'Vartotojo vardas',  # Pakeičia 'username' lauko etiketę
            'password1': 'Slaptažodis',  # Pakeičia 'password1' lauko etiketę
            'password2': 'Slaptažodžio patvirtinimas',  # Pakeičia 'password2' lauko etiketę
        }


class PolisaiForm(forms.ModelForm):
    pradzios_data = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))  # Nustato, kad 'pradzios_data' laukas bus date tipo
    pabaigos_data = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))  # Nustato, kad 'pabaigos_data' laukas bus date tipo
    # price = forms.FloatField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    #                          required=False)  # Nustato, kad 'price' laukas bus tik skaitymui

    class Meta:
        model = Polisai  # Nustato, kad ši forma naudoja Polisai modelį
        fields = ['brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'iskaita', 'country', 'travel_mode',
                  'cover1', 'cover2', 'cover3']  # Nurodo, kurie modelio laukai bus naudojami formoje
        labels = {
            'brokeriai': 'Brokeris',  # Pakeičia 'brokeriai' lauko etiketę
            'paslaugos': 'Paslaugos',  # Pakeičia 'paslaugos' lauko etiketę
            'pradzios_data': 'Pradžios data',  # Pakeičia 'pradzios_data' lauko etiketę
            'pabaigos_data': 'Pabaigos data',  # Pakeičia 'pabaigos_data' lauko etiketę
            'iskaita': 'Išskaita',  # Pakeičia 'iskaita' lauko etiketę
            'country': 'Šalis',  # Pakeičia 'country' lauko etiketę
            'travel_mode': 'Kelionės būdas',  # Pakeičia 'travel_mode' lauko etiketę
            'cover1': 'Nelaimingi atsitikimai',  # Pakeičia 'cover1' lauko etiketę
            'cover2': 'Civilinė atsakomybė',  # Pakeičia 'cover2' lauko etiketę
            'cover3': 'Medicininės išlaidos',  # Pakeičia 'cover3' lauko etiketę
            # 'price': 'Kaina',  # Pakeičia 'price' lauko etiketę
        }


class KlientaiForm(forms.ModelForm):
    class Meta:
        model = Klientai  # Nustato, kad ši forma naudoja Klientai modelį
        fields = ['vardas', 'pavarde', 'tel_numeris', 'gimimo_data', 'adresas',
                  'el_pastas']  # Nurodo, kurie modelio laukai bus naudojami formoje
        labels = {
            'vardas': 'Vardas',  # Pakeičia 'vardas' lauko etiketę
            'pavarde': 'Pavardė',  # Pakeičia 'pavarde' lauko etiketę
            'tel_numeris': 'Tel numeris',  # Pakeičia 'tel_numeris' lauko etiketę
            'gimimo_data': 'Gimimo data',  # Pakeičia 'gimimo_data' lauko etiketę
            'adresas': 'Adresas',  # Pakeičia 'adresas' lauko etiketę
            'el_pastas': 'El. paštas',  # Pakeičia 'el_pastas' lauko etiketę
        }
        widgets = {
            'adresas': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            # Nustato 'adresas' lauką kaip Textarea su tam tikrais dydžio atributais
        }


class NaujaKlientoRegistracijosForma(UserCreationForm):
    class Meta:
        model = User  # Nustato, kad ši forma naudoja User modelį
        fields = ['username', 'password1', 'password2']  # Nurodo, kurie modelio laukai bus naudojami formoje
        labels = {
            'username': _("Vartotojo vardas"),  # Pakeičia 'username' lauko etiketę į lietuvių kalbą
            'password1': _("Slaptažodis"),  # Pakeičia 'password1' lauko etiketę į lietuvių kalbą
            'password2': _("Slaptažodžio patvirtinimas"),  # Pakeičia 'password2' lauko etiketę į lietuvių kalbą
        }
        help_texts = {
            'username': _("Privalomas. 150 arba mažiau simbolių. Raidės, skaičiai bei @/./+/-/_ simboliai."),
            # Pateikia pagalbos tekstą vartotojo vardui
            'password1': _(
                "<ul>"
                "<li>Jūsų slaptažodį turi sudaryti bent 8 simboliai.</li>"
                "<li>Jūsų slaptažodis neturi būti per daug panašus į kitą jūsų asmeninę informaciją.</li>"
                "<li>Jūsų slaptažodis negali būti dažnai naudojamas slaptažodis.</li>"
                "<li>Jūsų slaptažodis negali būti vien skaičiai.</li>"
                "</ul>"
            ),  # Pateikia pagalbos tekstą slaptažodžiui
            'password2': _("Patikrinimui įveskite tokį patį slaptažodį, kaip anksčiau."),
            # Pateikia pagalbos tekstą slaptažodžio patvirtinimui
        }

    def save(self, commit=True):
        user = super().save(commit=False)  # Išsaugo formos duomenis, bet dar neišsaugo į duomenų bazę
        if commit:
            user.save()  # Išsaugo vartotoją į duomenų bazę
        return user  # Grąžina išsaugotą vartotoją


class BrokeriaiUpdateForm(forms.ModelForm):
    class Meta:
        model = Brokeriai  # Nustato, kad ši forma naudoja Brokeriai modelį
        fields = ['vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas',
                  'tel_numeris']  # Nurodo, kurie modelio laukai bus naudojami formoje
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'vardas' lauką kaip form-control
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'pavarde' lauką kaip form-control
            'imones_pavadinimas': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'imones_pavadinimas' lauką kaip form-control
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'el_pastas' lauką kaip form-control
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'tel_numeris' lauką kaip form-control
        }


###### Brokerių etapas
class BrokerLoginForm(forms.Form):
    email = forms.EmailField(label='El. paštas')  # El. pašto laukas su lietuviška etikete
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Slaptažodis')  # Slaptažodžio laukas su PasswordInput widget ir lietuviška etikete


class BrokerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Slaptažodis')  # Slaptažodžio laukas su PasswordInput widget ir lietuviška etikete
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label='Slaptažodžio patvirtinimas')  # Slaptažodžio patvirtinimo laukas su PasswordInput widget ir lietuviška etikete

    class Meta:
        model = Brokeriai  # Nustato, kad ši forma naudoja Brokeriai modelį
        fields = ['vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas',
                  'tel_numeris']  # Nurodo, kurie modelio laukai bus naudojami formoje
        widgets = {
            'vardas': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'vardas' lauką kaip form-control
            'pavarde': forms.TextInput(attrs={'class': 'form-control'}),  # Stilizuoja 'pavarde' lauką kaip form-control
            'imones_pavadinimas': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'imones_pavadinimas' lauką kaip form-control
            'el_pastas': forms.EmailInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'el_pastas' lauką kaip form-control
            'tel_numeris': forms.TextInput(attrs={'class': 'form-control'}),
            # Stilizuoja 'tel_numeris' lauką kaip form-control
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password')  # Gauk išvalytą 'password' vertę
        password1 = self.cleaned_data.get('password1')  # Gauk išvalytą 'password1' vertę
        if password and password1 and password != password1:  # Patikrina, ar slaptažodžiai sutampa
            raise forms.ValidationError("Slaptažodžiai nesutampa")
        return password1  # Grąžina 'password1' vertę

    def clean(self):
        cleaned_data = super().clean()  # Gauk išvalytus duomenis
        password = cleaned_data.get("password")  # Gauk 'password' vertę
        password1 = cleaned_data.get("password1")  # Gauk 'password1' vertę

        if password and password1 and password != password1:  # Patikrina, ar slaptažodžiai sutampa
            self.add_error('password1', "Slaptažodžiai nesutampa")  # Prideda klaidą prie 'password1' lauko


class BrokerKlientaiUserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Slaptažodis')  # Slaptažodžio laukas su PasswordInput widget ir lietuviška etikete
    password_confirmation = forms.CharField(widget=forms.PasswordInput,
                                            label='Patvirtinkite slaptažodį')  # Slaptažodžio patvirtinimo laukas su PasswordInput widget ir lietuviška etikete

    class Meta:
        model = User  # Nustato, kad ši forma naudoja User modelį
        fields = ['username', 'password']  # Nurodo, kurie modelio laukai bus naudojami formoje

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')  # Gauk išvalytą 'password' vertę
        password_confirmation = self.cleaned_data.get(
            'password_confirmation')  # Gauk išvalytą 'password_confirmation' vertę
        if password and password_confirmation and password != password_confirmation:  # Patikrina, ar slaptažodžiai sutampa
            raise forms.ValidationError("Slaptažodžiai nesutampa")  # Išmeta klaidą, jei slaptažodžiai nesutampa
        return password_confirmation  # Grąžina 'password_confirmation' vertę


class KlientaiUpdateForm(forms.ModelForm):
    class Meta:
        model = Klientai  # Nustato, kad ši forma naudoja Klientai modelį
        fields = ['vardas', 'pavarde', 'adresas', 'tel_numeris', 'el_pastas',
                  'gimimo_data']  # Nurodo, kurie modelio laukai bus naudojami formoje
        widgets = {
            'gimimo_data': forms.DateInput(attrs={'type': 'date'}),  # Nustato 'gimimo_data' lauką kaip date tipo
        }


###### Pricing
class TravelContractForm(forms.Form):
    klientas = forms.ModelChoiceField(queryset=Klientai.objects.all(), label='Klientas',
                                      required=False)  # Laukas pasirinkti klientą
    brokeris = forms.ModelChoiceField(queryset=Brokeriai.objects.all(), label='Brokeris',
                                      required=False)  # Laukas pasirinkti brokerį
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label='Šalis')  # Laukas pasirinkti šalį
    travel_start_date = forms.DateField(label='Kelionės pradžios data')  # Laukas įvesti kelionės pradžios datą
    travel_end_date = forms.DateField(label='Kelionės pabaigos data')  # Laukas įvesti kelionės pabaigos datą
    paslaugos = forms.ModelChoiceField(queryset=Paslaugos.objects.all(),
                                       label='Paslaugos')  # Laukas pasirinkti paslaugas
    cover3 = forms.ModelChoiceField(queryset=Cover1.objects.all(), label='Medicininės išlaidos',
                                    required=False)  # Laukas pasirinkti medicinines išlaidas
    cover1 = forms.ModelChoiceField(queryset=Cover2.objects.all(), label='Nelaimingi atsitikimai',
                                    required=False)  # Laukas pasirinkti nelaimingus atsitikimus
    cover2 = forms.ModelChoiceField(queryset=Cover3.objects.all(), label='Civilinė atsakomybė',
                                    required=False)  # Laukas pasirinkti civilinę atsakomybę
    travel_mode = forms.ModelChoiceField(queryset=TravelMode.objects.all(),
                                         label='Kelionės būdas')  # Laukas pasirinkti kelionės būdą
    iskaita = forms.ModelChoiceField(queryset=Iskaita.objects.all(), label='Išskaita',
                                     required=False)  # Laukas pasirinkti išskaitą
    total_price = forms.FloatField(label='Viso kaina', required=False,
                                   widget=forms.TextInput(attrs={'readonly': 'readonly'}))  # Viso kaina, tik skaitymui


##### price calc
class InsuranceCostCalculationForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), label='Pasirinkite šalį')  # Laukas pasirinkti šalį
    travel_mode = forms.ModelChoiceField(queryset=TravelMode.objects.all(),
                                         label='Keliavimo būdas')  # Laukas pasirinkti keliavimo būdą
    trip_duration = forms.IntegerField(label='Kelionės dienų skaičius')  # Laukas įvesti kelionės dienų skaičių
    cover1 = forms.ModelChoiceField(queryset=Cover1.objects.all(), label='Nelaimingi atsitikimai',
                                    required=False)  # Laukas pasirinkti nelaimingus atsitikimus
    cover2 = forms.ModelChoiceField(queryset=Cover2.objects.all(), label='Civilinė atsakomybė',
                                    required=False)  # Laukas pasirinkti civilinę atsakomybę
    cover3 = forms.ModelChoiceField(queryset=Cover3.objects.all(), label='Medicininės išlaidos',
                                    required=True)  # Laukas pasirinkti medicinines išlaidas
    iskaita = forms.ModelChoiceField(queryset=Iskaita.objects.all(),
                                     label='Taikoma išskaita')  # Laukas pasirinkti taikomą išskaitą
    paslaugos = forms.ModelChoiceField(queryset=Paslaugos.objects.all(), label='Paslaugos', widget=forms.HiddenInput,
                                       required=True)  # Laukas pasirinkti paslaugas, paslėptas

    class Meta:
        model = Polisai  # Nustato, kad ši forma naudoja Polisai modelį
        fields = ['country', 'travel_mode', 'trip_duration', 'cover1', 'cover2', 'cover3', 'iskaita',
                  'paslaugos']  # Nurodo, kurie modelio laukai bus naudojami formoje

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs and 'paslaugos' not in kwargs['initial']:
            default_paslaugos = Paslaugos.objects.get(pk=1)  # Nustato numatytąją paslaugą, jei nėra nurodyta
            self.fields['paslaugos'].initial = default_paslaugos.pk
        elif not self.fields['paslaugos'].initial:
            default_paslaugos = Paslaugos.objects.get(pk=1)
            self.fields['paslaugos'].initial = default_paslaugos.pk

    def clean_paslaugos(self):
        paslaugos = self.cleaned_data.get('paslaugos')
        if not paslaugos:
            default_paslaugos = Paslaugos.objects.get(pk=1)  # Grąžina numatytąją paslaugą, jei nėra pasirinkta
            return default_paslaugos
        return paslaugos  # Grąžina pasirinktas paslaugas
