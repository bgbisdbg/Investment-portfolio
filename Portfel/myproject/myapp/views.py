import re

from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tradingview_ta import TA_Handler, Interval

from myapp.models import CurrencyPairsModel, ActivesModel, HistoryModel, ActionModel, ScreenerModel, SourceModel
from myapp.serializers import HistorySerializer, ActivesSerializer, CalculationSerializer


class IndexAPIView(APIView):
    def get(self, request):
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

        return Response(context, status=status.HTTP_200_OK)


class HistoryAPIView(ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем текущего пользователя
        current_user = self.request.user
        # Фильтруем историю по текущему пользователю
        return HistoryModel.objects.filter(user_id=current_user)


class ActivesCreateAPIView(CreateAPIView):
    serializer_class = ActivesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        active_name = serializer.validated_data.get('active_name')
        pair_id = serializer.validated_data.get('pair_id')
        source_id = None
        screener_id = None

        if pair_id.pair_mame == 'USDT':
            screener_id = ScreenerModel.objects.get(screener_name='Crypto')
            source_id = SourceModel.objects.get(source_name='BINANCE')

        # Проверяем, существует ли актив с таким именем
        active, created = ActivesModel.objects.get_or_create(
            active_name=active_name,
            defaults={
                'pair_id': pair_id,
                'screener_id': screener_id,
                'source_id': source_id,
            }
        )

        if not created:
            # Если актив уже существует, обновляем его поля, если нужно
            active.pair_id = pair_id
            active.screener_id = screener_id
            active.source_id = source_id
            active.save()

        headers = self.get_success_headers(serializer.data)
        return Response({'active_id': active.active_id}, status=status.HTTP_201_CREATED, headers=headers)


class HistoryCreatedView(APIView):
    serializer_class = HistorySerializer

    def post(self, request, active_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            price = serializer.validated_data.get('price')
            count = serializer.validated_data.get('count')
            action_id = serializer.validated_data.get('action_id')
            user = self.request.user

            active_instance = ActivesModel.objects.get(pk=active_id)

            new_history = HistoryModel.objects.create(
                user_id=user,
                active_id=active_instance,
                price=price,
                count=count,
                action_id=action_id,
            )
            new_history.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalculationsAPIListView(ListAPIView):
    serializer_class = CalculationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        serializer = self.serializer_class(data=request.data)
        user_id = self.kwargs.get('user_id')
        result = HistoryModel.objects.filter(user_id=user_id).values(
            'active_name',
            'active_id__active_name',
            'active_id__now_price'
        ).annotate(
            weighted_average_price=Sum(F('price') * F('count')) / Sum('count'),
            total_count=Sum('count'),
            value=Sum(F('price') * F('count')),
            current_value=F('active_id__now_price') * Sum(F('count')),
            profit=F('current_value') - F('value'),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)