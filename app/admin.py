from django.contrib import admin
from .models import Klientai, Polisai, Brokeriai, Paslaugos, Cover1, Cover2, Cover3, TravelMode, Iskaita, CountryRisk, \
    Country


class PolisaiInline(admin.TabularInline):
    model = Polisai
    extra = 0


class KlientaiAdmin(admin.ModelAdmin):
    inlines = [PolisaiInline]
    list_display = ('user', 'vardas', 'pavarde', 'tel_numeris', 'el_pastas', 'get_total_policies')
    search_fields = ('vardas', 'pavarde', 'el_pastas')
    list_filter = ('vardas', 'pavarde')

    def get_total_policies(self, obj):
        return obj.polisai.count()

    get_total_policies.short_description = 'Total Policies'


class PolisaiAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_klientai_name', 'brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'iskaita',
        'cover1', 'cover2', 'cover3', 'country', 'travel_mode', 'price'
    )
    search_fields = (
        'klientai__vardas', 'klientai__pavarde', 'brokeriai__vardas', 'brokeriai__pavarde',
        'paslaugos__pavadinimas', 'cover1__na_sum', 'cover2__civ_sum', 'cover3__med_sum',
    )
    list_filter = ('pradzios_data', 'pabaigos_data', 'iskaita', 'cover1', 'cover2', 'cover3')
    readonly_fields = ('get_klientai_name',)
    fieldsets = (
        (None, {
            'fields': (
                'klientai', 'brokeriai', 'paslaugos', 'pradzios_data', 'pabaigos_data', 'iskaita',
                'cover1', 'cover2', 'cover3', 'country', 'travel_mode', 'price'
            )
        }),
    )
    actions = ['approve_policies', 'reject_policies']

    def get_klientai_name(self, obj):
        return f"{obj.klientai.vardas} {obj.klientai.pavarde}"

    get_klientai_name.short_description = 'Klientas'
    get_klientai_name.admin_order_field = 'klientai__vardas'

    def approve_policies(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"Successfully approved {queryset.count()} policies.")

    approve_policies.short_description = "Approve selected policies"

    def reject_policies(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"Successfully rejected {queryset.count()} policies.")

    reject_policies.short_description = "Reject selected policies"


class BrokeriaiAdmin(admin.ModelAdmin):
    list_display = ('vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas', 'tel_numeris', 'get_total_policies')
    search_fields = ('vardas', 'pavarde', 'imones_pavadinimas', 'el_pastas')
    list_filter = ('imones_pavadinimas',)
    inlines = [PolisaiInline]

    def get_total_policies(self, obj):
        return obj.polisai.count()

    get_total_policies.short_description = 'Total Policies'


class PaslaugosAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina', 'get_total_policies')
    search_fields = ('pavadinimas',)
    list_filter = ('pavadinimas',)

    def get_total_policies(self, obj):
        return Polisai.objects.filter(paslaugos=obj).count()

    get_total_policies.short_description = 'Total Policies'


admin.site.register(Polisai, PolisaiAdmin)
admin.site.register(Klientai, KlientaiAdmin)
admin.site.register(Brokeriai, BrokeriaiAdmin)
admin.site.register(Paslaugos, PaslaugosAdmin)
admin.site.register(Cover1)
admin.site.register(Cover2)
admin.site.register(Cover3)
admin.site.register(TravelMode)
admin.site.register(Iskaita)
admin.site.register(CountryRisk)
admin.site.register(Country)
