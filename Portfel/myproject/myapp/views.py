from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics
from tradingview_ta import TA_Handler, Interval

from myapp import serializers
from myapp.models import CurrencyPairsModel, ActivesModel
from myapp.serializers import ActivesModelSerializer


class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get(self, request, *args, **kwargs):
        btc_usdt = TA_Handler(
            symbol="BTCUSDT",
            exchange='BINANCE',
            screener="Crypto",
            interval=Interval.INTERVAL_1_MINUTE,
        )

        analysis = btc_usdt.get_analysis()
        price = analysis.indicators["close"]
        low = analysis.indicators["low"]
        high = analysis.indicators["high"]

        context = {
            'close_price': price,
            'low_price': low,
            'high_price': high,
        }

        return render(request, self.template_name, context)


class BrifcaseView(TemplateView):
    template_name = 'myapp/briefcase.html'


# class App(TemplateView):
#     template_name = 'myapp/actives_create.html'

def actives_create(request):
    currency_pairs = CurrencyPairsModel.objects.all()
    return render(request, 'myapp/actives_create.html', {'currency_pairs': currency_pairs})


class ActivesCreateAPIView(generics.CreateAPIView):
    queryset = ActivesModel.objects.all()
    serializer_class = ActivesModelSerializer
