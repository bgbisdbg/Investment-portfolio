from django.db import models
from tradingview_ta import TA_Handler, Interval



class ActionModel(models.Model):
    action_id = models.BigAutoField(primary_key=True)
    action_name = models.CharField(max_length=4)

    def __str__(self):
        return self.action_name


class CurrencyPairsModel(models.Model):
    pair_id = models.BigAutoField(primary_key=True)
    pair_mame = models.TextField(max_length=100)

    def __str__(self):
        return self.pair_mame


class ScreenerModel(models.Model):
    screener_id = models.BigAutoField(primary_key=True)
    screener_name = models.TextField(max_length=100)

    def __str__(self):
        return self.screener_name


class SourceModel(models.Model):
    source_id = models.BigAutoField(primary_key=True)
    source_name = models.TextField(max_length=100)

    def __str__(self):
        return self.source_name


class ActivesModel(models.Model):
    active_id = models.BigAutoField(primary_key=True)
    active_name = models.TextField(max_length=100)
    pair_id = models.ForeignKey('CurrencyPairsModel', on_delete=models.CASCADE)
    screener_id = models.ForeignKey('ScreenerModel', on_delete=models.CASCADE)
    source_id = models.ForeignKey('SourceModel', on_delete=models.CASCADE)
    now_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.active_name

    def save(self, *args, **kwargs):
        # Используйте tradingview_ta для получения актуальной цены
        symbol = self.active_name + self.pair_id.pair_mame
        exchange = self.source_id.source_name
        screener = self.screener_id.screener_name
        interval = Interval.INTERVAL_1_MINUTE
        ta = TA_Handler(symbol=symbol, exchange=exchange, screener=screener, interval=interval)
        analysis = ta.get_analysis()
        self.now_price = analysis.indicators['close']
        super().save(*args, **kwargs)


class HistoryModel(models.Model):
    user_id = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    active_id = models.ForeignKey('ActivesModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.DecimalField(max_digits=10000000, decimal_places=2)
    action_id = models.ForeignKey('ActionModel', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.active_id.active_name

