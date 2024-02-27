import re

from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from tradingview_ta import TA_Handler, Interval

from myapp.forms import ActiveCreatedForm, HistoryCreatedForm
from myapp.models import CurrencyPairsModel, ActivesModel, HistoryModel, ActionModel, ScreenerModel, SourceModel


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


class HistoryView(ListView):
    model = HistoryModel
    template_name = 'myapp/history.html'


    def get_queryset(self):
        # Получаем текущего пользователя
        current_user = self.request.user
        # Фильтруем историю по текущему пользователю
        return HistoryModel.objects.filter(user_id=current_user)


def actives_create(request):
    if request.method == 'POST':
        active_name = request.POST.get('active_name')
        pair_id = request.POST.get('pair_id')
        screener_id = None
        source_id = None
        if pair_id == '1':
            pair = CurrencyPairsModel.objects.get(pair_mame='USDT')
            screener_id = ScreenerModel.objects.get(screener_name='Crypto')
            source_id = SourceModel.objects.get(source_name='BINANCE')
        else:
            pass

        # Проверяем, существует ли актив с таким именем
        active, created = ActivesModel.objects.get_or_create(
            active_name=active_name,
            defaults={
                'pair_id': pair,
                'screener_id': screener_id,
                'source_id': source_id,
            }
        )

        if not created:
            # Если актив уже существует, обновляем его поля, если нужно
            active.pair_id = pair
            active.screener_id = screener_id
            active.source_id = source_id
            active.save()

        return redirect('myapp:history_created', active_id=active.active_id)
    else:
        form = ActiveCreatedForm()
    return render(request, 'myapp/actives_create.html', {'form': form})


def history_created(request, active_id):
    if request.method == "POST":
        price = request.POST.get('price')
        count = request.POST.get('count')
        action_id = request.POST.get('action_id')
        active = ActivesModel.objects.get(active_id=active_id)

        # Получаем действие по переданному action_id
        action = ActionModel.objects.get(action_id=action_id)

        new_history = HistoryModel.objects.create(
            user_id=request.user,
            active_id=active,
            price=price,
            count=count,
            action_id=action,

        )
        new_history.save()
        return redirect('myapp:index')
    else:
        form = HistoryCreatedForm()
    return render(request, 'myapp/history_created.html', {'form': form, 'active_id': active_id})


class BreafceseListView(ListView):
    model = HistoryModel
    template_name = 'myapp/brefcese.html'

    def get_queryset(self):
        user = self.request.user.id

        result = HistoryModel.objects.filter(user_id_id=user).values(
            'user_id_id',
            'active_id__active_name',
            'active_id__now_price'
        ).annotate(
            weighted_average_price=Sum(F('price') * F('count')) / Sum('count'),
            total_count=Sum('count'),
            value=Sum(F('price') * F('count')),
            current_value=F('active_id__now_price') * Sum(F('count')),
            profit=F('current_value') - F('value'),
        )

        return result

