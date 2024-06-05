from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from datetime import date
from PIL import UnidentifiedImageError
import logging

logger = logging.getLogger(__name__)


# Modelis, skirtas klientų informacijai saugoti
class Klientai(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Susiejimas su vartotojo modeliu
    vardas = models.CharField(max_length=100)  # Kliento vardas
    pavarde = models.CharField(max_length=100)  # Kliento pavardė
    tel_numeris = models.CharField(max_length=15)  # Kliento telefono numeris
    gimimo_data = models.DateField(null=True)  # Kliento gimimo data
    adresas = models.TextField()  # Kliento adresas
    el_pastas = models.EmailField()  # Kliento el. paštas

    def __str__(self):
        return f"{self.vardas} {self.pavarde}"


# Modelis, skirtas brokerių informacijai saugoti
class Brokeriai(models.Model):
    vardas = models.CharField(max_length=100)  # Brokerio vardas
    pavarde = models.CharField(max_length=100)  # Brokerio pavardė
    imones_pavadinimas = models.CharField(max_length=100)  # Įmonės pavadinimas, kuriai brokeris dirba
    el_pastas = models.EmailField(null=True)  # Brokerio el. paštas
    tel_numeris = models.CharField(max_length=15, null=True)  # Brokerio telefono numeris

    def __str__(self):
        return f"{self.vardas} {self.pavarde} - {self.imones_pavadinimas}"


# Modelis, skirtas paslaugų informacijai saugoti
class Paslaugos(models.Model):
    pavadinimas = models.CharField(max_length=100, default='Kelionių draudimas')  # Paslaugos pavadinimas
    aprasymas = models.TextField()  # Paslaugos aprašymas
    kaina = models.FloatField()  # Paslaugos kaina

    def __str__(self):
        return self.pavadinimas


# Modelis, skirtas nelaimingų atsitikimų draudimo sumai ir koeficientui saugoti
class Cover1(models.Model):
    na_sum = models.FloatField()  # Nelaimingų atsitikimų draudimo suma
    na_kof = models.FloatField()  # Nelaimingų atsitikimų draudimo koeficientas

    def __str__(self):
        return f"Nelaimingi atsitikimai (Suma: {self.na_sum})"


# Modelis, skirtas civilinės atsakomybės draudimo sumai ir koeficientui saugoti
class Cover2(models.Model):
    civ_sum = models.FloatField()  # Civilinės atsakomybės draudimo suma
    civ_kof = models.FloatField()  # Civilinės atsakomybės draudimo koeficientas

    def __str__(self):
        return f"Civilinė atsakomybė (Suma: {self.civ_sum})"


# Modelis, skirtas medicininių išlaidų draudimo sumai ir koeficientui saugoti
class Cover3(models.Model):
    med_sum = models.FloatField()  # Medicininių išlaidų draudimo suma
    med_kof = models.FloatField()  # Medicininių išlaidų draudimo koeficientas

    def __str__(self):
        return f"Medicininės išlaidos (Suma: {self.med_sum})"


# Modelis, skirtas kelionės būdo tipui ir koeficientui saugoti
class TravelMode(models.Model):
    type = models.CharField(max_length=100)  # Kelionės būdas
    kof = models.FloatField()  # Kelionės būdo koeficientas

    def __str__(self):
        return f"Keliausite su {self.type}"


# Modelis, skirtas išskaitos dydžiui ir koeficientui saugoti
class Iskaita(models.Model):
    sum = models.FloatField()  # Išskaitos dydis
    kof = models.FloatField()  # Išskaitos koeficientas

    def __str__(self):
        return f"Išskaitos dydis {self.sum}"


# Modelis, skirtas šalies rizikos lygiui ir koeficientui saugoti
class CountryRisk(models.Model):
    risk_level = models.CharField(max_length=100)  # Šalies rizikos lygis
    kof = models.FloatField()  # Šalies rizikos koeficientas


# Modelis, skirtas šalies informacijai saugoti
class Country(models.Model):
    map_risk = models.CharField(max_length=20)  # Šalies žemėlapio rizikos lygis
    name = models.CharField(max_length=100)  # Šalies pavadinimas
    latitude = models.FloatField()  # Šalies platuma
    longitude = models.FloatField()  # Šalies ilguma
    link = models.TextField()  # Šalies nuoroda

    def __str__(self):
        return f"kelionės šalis {self.name}"


# Modelis, skirtas polisų informacijai saugoti
class Polisai(models.Model):
    klientai = models.ForeignKey(Klientai, on_delete=models.CASCADE, related_name='polisai')  # Susiejimas su klientu
    brokeriai = models.ForeignKey(Brokeriai, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='polisai')  # Susiejimas su brokeriu
    paslaugos = models.ForeignKey(Paslaugos, on_delete=models.CASCADE, related_name='polisai',
                                  default=1)  # Susiejimas su paslauga
    poliso_tipas = models.CharField(max_length=100, blank=True)  # Poliso tipas
    pradzios_data = models.DateField()  # Poliso pradžios data
    pabaigos_data = models.DateField()  # Poliso pabaigos data
    iskaita = models.ForeignKey(Iskaita, on_delete=models.CASCADE)  # Susiejimas su išskaita
    cover1 = models.ForeignKey(Cover1, on_delete=models.CASCADE)  # Susiejimas su nelaimingų atsitikimų draudimu
    cover2 = models.ForeignKey(Cover2, on_delete=models.CASCADE)  # Susiejimas su civilinės atsakomybės draudimu
    cover3 = models.ForeignKey(Cover3, on_delete=models.CASCADE)  # Susiejimas su medicininių išlaidų draudimu
    travel_mode = models.ForeignKey(TravelMode, on_delete=models.CASCADE)  # Susiejimas su kelionės būdu
    country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Susiejimas su šalimi
    price = models.FloatField(default=0.0)  # Poliso kaina

    def __str__(self):
        return f"Polisas {self.pk} for {self.klientai}"

    @property
    def trip_duration(self) -> int:
        """Apskaičiuoja kelionės trukmę dienomis."""
        if isinstance(self.pradzios_data, date) and isinstance(self.pabaigos_data, date):
            return (self.pabaigos_data - self.pradzios_data).days
        return 0


# Modelis, skirtas vartotojo profiliui saugoti
class Profile(models.Model):
    picture = models.ImageField(upload_to='profile_pics', default='default-user.png')  # Profilio nuotrauka
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Susiejimas su vartotoju

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            thumb_size = (200, 200)
            img.thumbnail(thumb_size)
            img.save(self.picture.path)
        except FileNotFoundError:
            logger.error(f"File not found: {self.picture.path}")
        except UnidentifiedImageError:
            logger.error(f"Cannot identify image file: {self.picture.path}")
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")


# Modelis, skirtas brokerio profiliui saugoti
class BrokerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Susiejimas su vartotoju
    broker = models.OneToOneField(Brokeriai, on_delete=models.CASCADE)  # Susiejimas su brokeriu
    profile_picture = models.ImageField(upload_to='broker_pics', default='default-broker.png')  # Profilio nuotrauka

    def __str__(self):
        return str(self.broker)
