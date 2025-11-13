from .views import *
from django.urls import path
from allusers.views import *
urlpatterns = [
    path('',AllusersView.as_view(),name='employee_dashboard')
]