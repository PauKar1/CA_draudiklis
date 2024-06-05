from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from datetime import date


class Klientai(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vardas = models.CharField(max_length=100)
    pavarde = models.CharField(max_length=100)
    tel_numeris = models.CharField(max_length=15)
    gimimo_data = models.DateField(null=True)
    adresas = models.TextField()
    el_pastas = models.EmailField()

    def __str__(self):
        return f"{self.vardas} {self.pavarde}"


class Brokeriai(models.Model):
    vardas = models.CharField(max_length=100)
    pavarde = models.CharField(max_length=100)
    imones_pavadinimas = models.CharField(max_length=100)
    el_pastas = models.EmailField(null=True)
    tel_numeris = models.CharField(max_length=15, null=True)  # Changed to CharField

    def __str__(self):
        return f"{self.vardas} {self.pavarde} - {self.imones_pavadinimas}"


class Paslaugos(models.Model):
    pavadinimas = models.CharField(max_length=100, default='Kelionių draudimas')
    aprasymas = models.TextField()
    kaina = models.FloatField()

    def __str__(self):
        return self.pavadinimas

################################
class Cover1(models.Model):
    na_sum = models.FloatField()
    na_kof = models.FloatField()

    def __str__(self):
        return f"Nelaimingi atsitikimai (Suma: {self.na_sum})"
class Cover2(models.Model):
    civ_sum = models.FloatField()
    civ_kof = models.FloatField()
    def __str__(self):
        return f"Civilinė atsakomybė (Suma: {self.civ_sum})"
class Cover3(models.Model):
    med_sum = models.FloatField()
    med_kof = models.FloatField()
    def __str__(self):
        return f"Medicininės išlaidos (Suma: {self.med_sum})"
class TravelMode(models.Model):
    type = models.CharField(max_length=100)  # Changed to CharField
    kof = models.FloatField()
    def __str__(self):
        return f"Keliausite su {self.type}"

class Iskaita(models.Model):
    sum = models.FloatField()
    kof = models.FloatField()
    def __str__(self):
        return f"Išskaitos dydis {self.sum}"

class CountryRisk(models.Model):
    risk_level = models.CharField(max_length=100)  # Changed to CharField
    kof = models.FloatField()

class Country(models.Model):
    map_risk = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    link = models.TextField()

    def __str__(self):
        return f"kelionės šalis {self.name}"
####################################
class Polisai(models.Model):
    klientai = models.ForeignKey(Klientai, on_delete=models.CASCADE, related_name='polisai')
    brokeriai = models.ForeignKey(Brokeriai, on_delete=models.SET_NULL, null=True, blank=True, related_name='polisai')
    paslaugos = models.ForeignKey(Paslaugos, on_delete=models.CASCADE, related_name='polisai', default=1)
    poliso_tipas = models.CharField(max_length=100, blank=True)
    pradzios_data = models.DateField()
    pabaigos_data = models.DateField()
    iskaita = models.ForeignKey(Iskaita, on_delete=models.CASCADE)
    cover1 = models.ForeignKey(Cover1, on_delete=models.CASCADE)
    cover2 = models.ForeignKey(Cover2, on_delete=models.CASCADE)
    cover3 = models.ForeignKey(Cover3, on_delete=models.CASCADE)
    travel_mode = models.ForeignKey(TravelMode, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"Polisas {self.pk} for {self.klientai}"

    @property
    def trip_duration(self) -> int:
        """Calculate the trip duration in days."""
        if isinstance(self.pradzios_data, date) and isinstance(self.pabaigos_data, date):
            return (self.pabaigos_data - self.pradzios_data).days
        return 0


class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', default='default-user.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} profilis'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            thumb_size = (200, 200)
            img.thumbnail(thumb_size)
            img.save(self.picture.path)
        except Exception as e:
            pass  # Handle exceptions

class BrokerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    broker = models.OneToOneField(Brokeriai, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='broker_pics', default='default-broker.png')

    def __str__(self):
        return f'{self.broker.vardas} {self.broker.pavarde} Profile'
