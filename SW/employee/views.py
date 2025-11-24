from allusers.models import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
# Create your views here.

class BaseEmployeerView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url="/login/"

    def test_func(self):
        return self.request.user.groups.filter(name='Employee').exists()

    def handle_no_permission(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return redirect('/manager/')
        else:
            return redirect('/login/')

class IndexView(BaseEmployeerView):
    template_name = 'employee/index.html'

    def get(self, request, *args ,**kwargs ):

        return render(request,self.template_name)
# Create your views here.
