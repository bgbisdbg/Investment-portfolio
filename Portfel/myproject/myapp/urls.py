from django.urls import path
from myapp.views import *


app_name = "myapp"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('history/', HistoryView.as_view(), name='history'),
    path('actives_create/', actives_create, name='actives_create'),
    path('history/create/<int:active_id>/', history_created, name='history_created')

]
