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
    def get(self, request):
        return render(request, "allusers/login.html")

    def post(self, request):
        personnel_code = request.POST.get("personnelCode")
        meliCardCode = request.POST.get("meliCardCode")

        user = authenticate(request, username=personnel_code, password=meliCardCode)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            
            try:
                profile = user.ProfileUser
                role = profile.position.group_name if profile.position else None
            except ProfileTB.DoesNotExist:
                role = None

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
    
class AllusersView(LoginRequiredMixin,View):
    def get(self,request, *args, **kwargs):
        users = ProfileTB.objects.all()
        msg = self.request.GET.get('msg')
        context ={
            'users':users,
            'msg':msg,
        }
        return render(request,'allusers/users.html',context)
    
class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        position = self.request.user.ProfileUser.position.group_name
        return position in ["Manager", "CEO"]

    def get(self, request):
        positions = PositionTB.objects.all()
        genders = GenderTB.objects.all()
        return render(request, "allusers/createuser.html", {"positions": positions, "genders": genders})

    def post(self, request):
        personnel_code = request.POST.get("personnelCode")
        meliCardCode = request.POST.get("meliCardCode")
        position_id = request.POST.get("position")
        gender_id = request.POST.get("gender")
        age = request.POST.get("age")
        desc = request.POST.get("desc")

        if User.objects.filter(username=personnel_code).exists():
            messages.error(request, "کاربری با این کدپرسنلی ثبت شده است.")
            return redirect("create_user")

        user = User.objects.create_user(username=personnel_code, password=meliCardCode)
        position = PositionTB.objects.get(id=position_id)
        gender = GenderTB.objects.get(id=gender_id)

        ProfileTB.objects.create(
            user=user,
            position=position,
            meliCardCode =meliCardCode,
            gender=gender,
            age=age,
            desc=desc,
            personnelCode=personnel_code
        )

        messages.success(request, f"کاربر {personnel_code} با موفقیت ثبت نام شد")
        return redirect("")


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
         