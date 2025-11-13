from .views import *
from allusers.views import *
from django.urls import path

urlpatterns = [
    path('',AllusersView.as_view(),name='manager_dashboard')
]