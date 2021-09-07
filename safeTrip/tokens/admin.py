from django.contrib import admin
from .models import Tokens

# Register your models here.


class TokenModel(admin.ModelAdmin):
    list_filter = ['pair_base_name', 'pair_quote_name',
                   'is_sponsored', 'is_trending']
    ordering = ['pair_base_name', 'pair_quote_name', 'pair_address']
    search_fields = ['pair_base_name', 'pair_quote_name', 'pair_address']


admin.site.register(Tokens, TokenModel)
