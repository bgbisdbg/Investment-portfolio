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
        fields = ['active_name', 'pair_id',]


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = ['price', 'count', 'action_id']
