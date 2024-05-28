from django.contrib import admin
from .models import Klientai, Brokeriai, Paslaugos, Polisai

admin.site.register(Klientai)
admin.site.register(Brokeriai)
admin.site.register(Paslaugos)
admin.site.register(Polisai)