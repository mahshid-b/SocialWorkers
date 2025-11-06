from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import *


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        personnel_code = request.POST.get("personnelCode")
        meliCardCode = request.POST.get("meliCardCode")

        user = authenticate(request, username=personnel_code, password=meliCardCode)
        if user is not None:
            login(request, user)
            messages.success(request, "با موفقیت وارد شدید")
            return redirect("")
        else:
            messages.error(request, "کاربر شناسایی نشد")
            return render(request, "users/login.html")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "با موفقیت خارج شدید")
        return redirect("login")
    
class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        position = self.request.user.ProfileUser.position.group_name
        return position in ["Manager", "CEO"]

    def get(self, request):
        positions = PositionTB.objects.all()
        genders = GenderTB.objects.all()
        return render(request, "users/create_user.html", {"positions": positions, "genders": genders})

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

    def get(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)
        positions = PositionTB.objects.all()
        genders = GenderTB.objects.all()
        return render(request, "users/edit_user.html", {
            "user_obj": user_obj,
            "positions": positions,
            "genders": genders
        })

    def post(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)
        profile = user_obj.ProfileUser

        profile.age = request.POST.get("age")
        profile.desc = request.POST.get("desc")
        profile.gender_id = request.POST.get("gender")
        profile.save()

        messages.success(request, "User updated successfully.")
        return redirect("user_list")


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        position = self.request.user.ProfileUser.position.group_name
        return position in ["Manager", "CEO"]

    def get(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)
        return render(request, "users/confirm_delete.html", {"user_obj": user_obj})

    def post(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)
        user_obj.delete()
        messages.success(request, "User deleted successfully.")
        return redirect("user_list")