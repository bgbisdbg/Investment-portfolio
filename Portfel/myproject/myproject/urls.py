"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include



from myapp.views import IndexAPIView, HistoryAPIView, ActivesCreateAPIView, HistoryCreatedView, CalculationsAPIListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include('users.urls', namespace='users')),
    path('api/index/', IndexAPIView.as_view(), name='index-api'),
    path('api/history/', HistoryAPIView.as_view(), name='history-api'),
    path('api/actives/create/', ActivesCreateAPIView.as_view(), name='actives-create'),
    path('history/created/<int:active_id>/', HistoryCreatedView.as_view(), name='history-created'),
    path('calculations/<int:user_id>/', CalculationsAPIListView.as_view(), name='calculations-list'),
    path('calculations/', CalculationsAPIListView.as_view(), name='calculations-list'),
]