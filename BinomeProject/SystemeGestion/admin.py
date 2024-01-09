from django.contrib import admin

from .models import*
admin.site.register(MatierePremiere)
admin.site.register(Fournisseur)
admin.site.register(Client)
admin.site.register(Reglement_Fournisseur)
admin.site.register(Achat)
admin.site.register(Centre)
admin.site.register(Transfert)
