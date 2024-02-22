from django.urls import path
from myapp.views import *


app_name = "myapp"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('briefcase/', BrifcaseView.as_view(), name='briefcase'),
    path('actives/create/', actives_create, name='actives-create'),
    path('api/actives/create/', ActivesCreateAPIView.as_view(), name='actives-create-api'),
]