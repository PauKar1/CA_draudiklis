# app/models.py

from django.db import models

class Klientai(models.Model):
    vardas = models.CharField(max_length=100)
    pavarde = models.CharField(max_length=100)
    tel_numeris = models.IntegerField()
    gimimo_data = models.DateField()
    adresas = models.TextField()
    el_pastas = models.EmailField()

    def __str__(self):
        return f"{self.vardas} {self.pavarde}"

class Brokeriai(models.Model):
    vardas = models.CharField(max_length=100)
    pavarde = models.CharField(max_length=100)
    imones_pavadinimas = models.CharField(max_length=100)
    el_pastas = models.EmailField()
    tel_numeris = models.IntegerField()

    def __str__(self):
        return f"{self.vardas} {self.pavarde} - {self.imones_pavadinimas}"

class Paslaugos(models.Model):
    pavadinimas = models.CharField(max_length=100)
    aprasymas = models.TextField()
    kaina = models.FloatField()

    def __str__(self):
        return self.pavadinimas

class Polisai(models.Model):
    klientai = models.ForeignKey(Klientai, on_delete=models.CASCADE, related_name='polisai')
    brokeriai = models.ForeignKey(Brokeriai, on_delete=models.CASCADE, related_name='polisai')
    paslaugos = models.ForeignKey(Paslaugos, on_delete=models.CASCADE, related_name='polisai')
    poliso_tipas = models.CharField(max_length=100)
    pradzios_data = models.DateField()
    pabaigos_data = models.DateField()
    draudimo_suma = models.FloatField()
    iskaita = models.FloatField()
    apsauga = models.TextField()

    def __str__(self):
        return f"Polisas {self.id} for {self.klientai}"
