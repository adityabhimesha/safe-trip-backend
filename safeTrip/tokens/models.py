from django.db import models
from requests.api import request

# Create your models here.
class Tokens(models.Model):
    pair_address = models.CharField(max_length=255, null=False, primary_key=True)
    pair_base_name = models.CharField(max_length=255,null=False,)
    pair_quote_name = models.CharField(max_length=255,null=False,default="")
    pair_base_address = models.CharField(max_length=255, null=False,default="")
    pair_quote_address = models.CharField(max_length=255, null=False,default="")

    cmc_link = models.CharField(max_length=255,default="",blank=True)
    coin_gecko_link = models.CharField(max_length=255,default="",blank=True)
    telegram = models.CharField(max_length=255,default="",blank=True)
    website = models.CharField(max_length=255,default="",blank=True)
    twitter = models.CharField(max_length=255,default="",blank=True)

    is_trending = models.BooleanField(default=False,blank=True)
    is_sponsored = models.BooleanField(default=False,blank=True)
    sponsored_details = models.CharField(max_length=500, default="",blank=True)
    views = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return self.pair_base_name + '/' + self.pair_quote_name