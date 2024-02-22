from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ActivesModel, CurrencyPairsModel, ScreenerModel, SourceModel


class ActivesModelSerializer(serializers.ModelSerializer):
    pair_id = serializers.PrimaryKeyRelatedField(queryset=CurrencyPairsModel.objects.all())
    screener_id = serializers.PrimaryKeyRelatedField(queryset=ScreenerModel.objects.all())
    source_id = serializers.PrimaryKeyRelatedField(queryset=SourceModel.objects.all())

    class Meta:
        model = ActivesModel
        fields = ['active_id', 'active_name', 'pair_id', 'screener_id', 'source_id']