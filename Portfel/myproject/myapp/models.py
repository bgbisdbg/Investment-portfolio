from django.db import models

from myproject import settings


class ActionModel(models.Model):
    action_id = models.BigAutoField(primary_key=True)
    action_name = models.CharField(max_length=4)


class CurrencyPairsModel(models.Model):
    pair_id = models.BigAutoField(primary_key=True)
    pair_mame = models.TextField(max_length=100)


class ScreenerModel(models.Model):
    screener_id = models.BigAutoField(primary_key=True)
    screener_name = models.TextField(max_length=100)


class SourceModel(models.Model):
    source_id = models.BigAutoField(primary_key=True)
    source_name = models.TextField(max_length=100)


class ActivesModel(models.Model):
    active_id = models.BigAutoField(primary_key=True)
    active_name = models.TextField(max_length=100)
    pair_id = models.ForeignKey('CurrencyPairsModel', on_delete=models.CASCADE)
    screener_id = models.ForeignKey('ScreenerModel', on_delete=models.CASCADE)
    source_id = models.ForeignKey('SourceModel', on_delete=models.CASCADE)
    now_price = models.DecimalField(max_digits=10, decimal_places=2)


class BriefcaseModel(models.Model):
    user_id =  models.ForeignKey('auth.user', on_delete=models.CASCADE)
    active_id = models.ForeignKey('ActivesModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.DecimalField(max_digits=10000000, decimal_places=2)
    action_id = models.ForeignKey('ActionModel', on_delete=models.CASCADE)
