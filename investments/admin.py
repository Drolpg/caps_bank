from django.contrib import admin
from .models import ProductInvestment, Investment, Indexer


admin.site.register(Investment)
admin.site.register(Indexer)
admin.site.register(ProductInvestment)

@admin.register(ProductInvestment)
class ProductInvestmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "tax",
        "indexer",
        "index_multiplier",
        "start_date",
        "final_date",
        "minimum_value",
        "is_premium",
    )
    search_fields = ("name", "minimum_value")
    fieldsets = (
        ("Informações do Produto", {"fields": ["name", "final_date"]}),
        ("Rendimentos do Produto",
            {"fields": ["tax", "indexer", "index_multiplier"]}),
        (None, {"fields": ["minimum_value", "is_premium"]}),
    )
