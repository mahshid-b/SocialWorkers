from .views import *
from allusers.views import *
from django.urls import path

urlpatterns = [
    path('',AllusersView.as_view(),name='manager_dashboard'),
    path('delete-employee/',DeleteEmployeeView.as_view(),name='delete_employee'),
    path('employee/<int:pk>/',UserView.as_view(),name='edit_employee'),
]