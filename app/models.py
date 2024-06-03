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
    tel_numeris = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.vardas} {self.pavarde} - {self.imones_pavadinimas}"


class Paslaugos(models.Model):
    pavadinimas = models.CharField(max_length=100)
    aprasymas = models.TextField()
    kaina = models.FloatField()

    def __str__(self):
        return self.pavadinimas


class Polisai(models.Model):
    DRAUDIMO_SUMA_CHOICES = [
        (100000, '100,000'),
        (300000, '300,000'),
        (500000, '500,000'),
    ]

    ISKAITA_CHOICES = [
        (0, '0'),
        (50, '50'),
        (80, '80'),
        (100, '100'),
        (120, '120'),
    ]

    APSAUGA_CHOICES = [
        ('medicinines_islados', 'Medicininės išlaidos'),
        ('nelaimingi_atsitikimai', 'Nelaimingi atsitikimai'),
        ('civiline_atsakomybe', 'Civilinė atsakomybė'),
    ]

    klientai = models.ForeignKey(Klientai, on_delete=models.CASCADE, related_name='polisai')
    brokeriai = models.ForeignKey(Brokeriai, on_delete=models.SET_NULL, null=True, blank=True, related_name='polisai')
    paslaugos = models.ForeignKey(Paslaugos, on_delete=models.CASCADE, related_name='polisai', default="Kelionių draudimas")
    poliso_tipas = models.CharField(max_length=100, blank=True)
    pradzios_data = models.DateField()
    pabaigos_data = models.DateField()
    draudimo_suma = models.IntegerField(choices=DRAUDIMO_SUMA_CHOICES, default=100000)
    iskaita = models.IntegerField(choices=ISKAITA_CHOICES, default=0)
    apsauga = models.CharField(max_length=50, choices=APSAUGA_CHOICES)

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
        super().save(*args, **kwargs)  # numatytieji Model klasės veiksmai suvykdomi
        img = Image.open(self.picture.path)
        thumb_size = (200, 200)
        img.thumbnail(thumb_size)
        img.save(self.picture.path)


class Country(models.Model):
    name = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
