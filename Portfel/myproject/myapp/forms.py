from django import forms

from myapp.models import ActivesModel, CurrencyPairsModel, SourceModel, ScreenerModel, HistoryModel, ActionModel


class ActiveCreatedForm(forms.ModelForm):
    active_name = forms.CharField(max_length=100)
    pair_id = forms.ModelChoiceField(queryset=CurrencyPairsModel.objects.all(), empty_label="Выберите пару")

    class Meta:
        model = ActivesModel
        fields = ['active_name', 'pair_id']


class HistoryCreatedForm(forms.ModelForm):
    price = forms.DecimalField()
    count = forms.DecimalField()
    action_id = forms.ModelChoiceField(queryset=ActionModel.objects.all(), empty_label="Купил или продал")

    class Meta:
        model = HistoryModel
        fields = ['price', 'count', 'action_id']
