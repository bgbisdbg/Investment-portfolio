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


class CalculationSerializer(serializers.Serializer):
    active_name = serializers.CharField()
    now_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    weighted_average_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_count = serializers.DecimalField(max_digits=10000000, decimal_places=2)
    value = serializers.DecimalField(max_digits=10000000, decimal_places=2)
    current_value = serializers.DecimalField(max_digits=10000000, decimal_places=2)
    profit = serializers.DecimalField(max_digits=10000000, decimal_places=2)
