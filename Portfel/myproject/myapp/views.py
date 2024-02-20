from django.shortcuts import render
from django.views.generic import TemplateView
from binance import Client
from tradingview_ta import TA_Handler, Interval, Exchange

from myproject.settings import api_key, secret_key


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


class RegisterView(TemplateView):
    template_name = 'myapp/register.html'
