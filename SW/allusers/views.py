from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import *
from centers.models import *


class LoginView(View):
    template_name= "allusers/login.html"
    def get(self, request):
        return render(request,self.template_name)

    def post(self, request):
        personnel_code = request.POST.get("personnelCode")
        meliCardCode = request.POST.get("meliCardCode")

        user = authenticate(request, username=personnel_code, password=meliCardCode)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            try:
                profile = ProfileTB.objects.get(user=user)
            except ProfileTB.DoesNotExist:
                messages.error(request, "پروفایلی برای این کاربر ثبت نشده است")
                return redirect("login")
            
            role = profile.position.group_name if profile.position else None
            if role == "Manager":
                return redirect("manager_dashboard")
            elif role == "Employee":
                return redirect("employee_dashboard")
            else:
                messages.warning(request, "نقش شما مشخص نیست")
                return redirect("login") 
        else:
            messages.error(request, "کاربر شناسایی نشد")
            return render(request, "allusers/login.html")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "با موفقیت خارج شدید")
        return redirect("login")
    
class UserEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        target_user = get_object_or_404(User, id=self.kwargs["user_id"])
        requester = self.request.user
        requester_role = requester.ProfileUser.position.group_name
        return requester == target_user or requester_role in ["Manager", "CEO"]

    def get(self, request, pk,*args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            centers = CenterTB.objects.all()
            context ={'user':user,
                      'centers':centers,}
            return render(request,"allusers/'edituser.html",context)
        except User.DoesNotExist:
            return redirect(f'/allusers/{pk}/?msg= کاربری با این ایدی یافت نشد.')
    
    def post(self,request,pk,*args, **kwargs):
        try:
            user = User.objects.get(id=pk)
        except:
            return redirect(f"/allusers/{pk}/?msg= کاربر یافت نشد")
        first_name = self.request.POST['first_name']
        if first_name is not None and first_name !='':
            user.first_name = first_name 
        last_name = self.request.POST['last_name']
        if last_name is not None and last_name !='':
            user.last_name = last_name 
        personnelCode = self.request.POST['personnelCode']
        if personnelCode is not None and personnelCode !='':
            user.username = personnelCode
        phone = self.request.POST['phone']
        if phone is not None and phone !='':
            user.password = phone
        user.save()
        userProfile = ProfileTB.objects.get(user=user)
        phone = self.request.POST['phone']
        if phone is not None and phone !='':
            userProfile.phone = phone
        position = self.request.POST['position']
        if position is not None and position !='--':
            userProfile.position = position
        gender = self.request.POST['gender']
        if gender is not None and gender !='--':
            userProfile.gender = gender
        age = self.request.POST['age']
        if age is not None and age !='':
            userProfile.age = age
        desc = self.request.POST['desc']
        if desc is not None and desc !='':
            userProfile.desc = desc
        meliCardCode = self.request.POST['meliCardCode']
        if meliCardCode is not None and meliCardCode !='':
            userProfile.meliCardCode = meliCardCode
        personnelCode = self.request.POST['personnelCode']
        if personnelCode is not None and personnelCode !='':
            userProfile.personnelCode = personnelCode
        center = self.request.POST['center']
        if center is not None and center !='--':
            userProfile.center = center
        userProfile.save()

        return redirect(f'/allusers/edituser/{pk}/?msg= تغییرات کاربر با موفقیت ثبت شد.')
        
        
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        position = self.request.user.ProfileUser.position.group_name
        return position in ["Manager", "CEO"]
    def post(self,request,*args, **kwargs):
        try:
            userId =self.request.POST['userId']
            if userId is not None or userId !='':
                user = User.objects.get(id=userId)
                user.delete()
                return redirect('/allusers/?msg=کاربر با موفقیت حذف شد.')
        except:
            return redirect('/allusers/?msg=دیتای ارسالی دارای مشکل است.')
         