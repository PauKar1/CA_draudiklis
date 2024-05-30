from django.contrib import admin
from .models import Klientai, Brokeriai, Paslaugos, Polisai
from .forms import PolisaiForm

admin.site.register(Klientai)
admin.site.register(Brokeriai)
admin.site.register(Paslaugos)



class PolisaiAdmin(admin.ModelAdmin):
    form = PolisaiForm
    list_display = ('brokeriai', 'paslaugos', 'apsauga', 'poliso_tipas')
    search_fields = ('brokeriai__vardas', 'brokeriai__pavarde', 'paslaugos__pavadinimas', 'poliso_tipas')

admin.site.register(Polisai, PolisaiAdmin)