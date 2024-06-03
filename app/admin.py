from django.contrib import admin
from .models import Klientai, Polisai, Brokeriai, Paslaugos


class PolisaiInline(admin.TabularInline):
    model = Polisai
    extra = 0


class KlientaiAdmin(admin.ModelAdmin):
    inlines = [PolisaiInline]
    list_display = ('user', 'vardas', 'pavarde', 'tel_numeris', 'el_pastas')
    search_fields = ('vardas', 'pavarde', 'el_pastas')


class PolisaiAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'get_klientai_name', 'brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'draudimo_suma', 'iskaita',
    'apsauga')
    search_fields = (
    'klientai__vardas', 'klientai__pavarde', 'brokeriai__vardas', 'brokeriai__pavarde', 'paslaugos__pavadinimas')
    list_filter = ('pradzios_data', 'pabaigos_data', 'draudimo_suma', 'iskaita', 'apsauga')
    readonly_fields = ('get_klientai_name',)
    fieldsets = (
        (None, {
            'fields': (
            'get_klientai_name', 'brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'draudimo_suma', 'iskaita',
            'apsauga')
        }),
    )
    actions = ['approve_policies', 'reject_policies']

    def get_klientai_name(self, obj):
        return f"{obj.klientai.vardas} {obj.klientai.pavarde}"

    get_klientai_name.short_description = 'Klientas'
    get_klientai_name.admin_order_field = 'klientai__vardas'

    def approve_policies(self, request, queryset):
        queryset.update(status='approved')

    approve_policies.short_description = "Approve selected policies"

    def reject_policies(self, request, queryset):
        queryset.update(status='rejected')

    reject_policies.short_description = "Reject selected policies"


class BrokeriaiAdmin(admin.ModelAdmin):
    list_display = ('vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas', 'tel_numeris')
    search_fields = ('vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas')
    list_filter = ('imones_pavadinimas',)
    inlines = [PolisaiInline]


class PaslaugosAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')
    search_fields = ('pavadinimas',)
    list_filter = ('pavadinimas',)


admin.site.register(Polisai, PolisaiAdmin)
admin.site.register(Klientai, KlientaiAdmin)
admin.site.register(Brokeriai, BrokeriaiAdmin)
admin.site.register(Paslaugos, PaslaugosAdmin)
