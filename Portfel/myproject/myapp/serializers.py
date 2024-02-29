from django.db.models import Sum, F
from rest_framework import serializers
from .models import ActionModel, CurrencyPairsModel, ScreenerModel, SourceModel, ActivesModel, HistoryModel


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionModel
        fields = '__all__'


class CurrencyPairsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPairsModel
        fields = '__all__'


class ScreenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenerModel
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceModel
        fields = '__all__'


class ActivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivesModel
        fields = ['active_name', 'pair_id_id', 'active_id']


class HistorySerializer(serializers.ModelSerializer):
    active_id = ActivesSerializer()
    active_name = ActivesSerializer()
    now_price = ActivesSerializer()

    class Meta:
        model = HistoryModel
        fields = ['price', 'count', 'active_id', 'active_name', 'now_price']


class CalculationSerializer(serializers.ModelSerializer):
    weighted_average_price = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()
    active_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivesModel
        fields = (
            'active_name',
            'weighted_average_price',
            'total_count',
            'value',
            'current_value',
            'profit',
        )

    def get_active_name(self, obj):
        # Возвращаем значение поля active_name из объекта ActivesModel
        return obj.active_name

    def get_weighted_average_price(self, obj):
        return HistoryModel.objects.filter(active_id=obj).aggregate(
            weighted_average_price=Sum(F('price') * F('count')) / Sum('count')
        )['weighted_average_price']

    def get_total_count(self, obj):
        return HistoryModel.objects.filter(active_id=obj).aggregate(
            total_count=Sum('count')
        )['total_count']

    def get_value(self, obj):
        return HistoryModel.objects.filter(active_id=obj).aggregate(
            value=Sum(F('price') * F('count'))
        )['value']

    def get_current_value(self, obj):
        return obj.now_price * self.get_total_count(obj)

    def get_profit(self, obj):
        return self.get_current_value(obj) - self.get_value(obj)
