from django.contrib import admin

from wallets.models import Wallet


@admin.register(Wallet)
class Wallet(admin.ModelAdmin):
    list_display = ["uuid", "balance", "owner"]
    list_filter = ["uuid", "balance", "owner"]
    search_fields = ["uuid", "balance"]
