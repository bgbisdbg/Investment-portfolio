from django.contrib import admin

from myapp.models import *

admin.site.register(ActionModel)
admin.site.register(CurrencyPairsModel)
admin.site.register(ScreenerModel)
admin.site.register(SourceModel)



@admin.register(HistoryModel)
class History(admin.ModelAdmin):
    list_display = ('user_id', 'active_id')


@admin.register(ActivesModel)
class Actives(admin.ModelAdmin):
    list_display = ('active_name', 'active_id')
