from allusers.models import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from centers.models import *
# Create your views here.

class BaseManagerView(LoginRequiredMixin,UserPassesTestMixin,View):
    login_url="/login/"

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def handle_no_permission(self):
        if self.request.user.groups.filter(name='Employee').exists():
            return redirect('/employee/')
        else:
            return redirect('/login/')

class IndexView(BaseManagerView):
    template_name = 'manager/index.html'
    def get(self, request, *args ,**kwargs ):
        users = ProfileTB.objects.all()
        return render(request,self.template_name,{'users':users})

class AllusersView(BaseManagerView):
    template_name = 'manager/users.html'
    def get(self,request, *args, **kwargs):
        users = ProfileTB.objects.all()
        genders = GenderTB.objects.all()
        positions = PositionTB.objects.all()
        msg = self.request.GET.get('msg')
        context ={
            'users':users,
            'msg':msg,
            'genders':genders,
            'positions':positions,
        }
        return render(request,self.template_name,context)
    def post(self,request,*args, **kwargs):
        first_name = self.request.POST['first_name']
        if first_name is None or first_name =='':
            return redirect('/manager/employee/?msg= نام مشتری باید وارد شود.')
        last_name = self.request.POST['last_name']
        if last_name is None or last_name =='':
            return redirect('/manager/employee/?msg= نام خانوادگی مشتری باید وارد شود.')
        personnelCode = self.request.POST['personnelCode']
        if personnelCode is None or personnelCode =='':
            return redirect('/manager/employee/?msg= کدپرسنلی را وارد کنید')
        meliCardCode = self.request.POST['meliCardCode']
        if meliCardCode is None or meliCardCode =='':
            return redirect('/manager/employee/?msg= کدملی تان را وارد کنید(برابر با رمز عبور)')
        newUser = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=personnelCode,
            password=meliCardCode
        )
        phone = self.request.POST['phone']
        if phone is None or phone =='':
            return redirect('/manager/employee/?msg= شماره موبایل کاربر را وارد کنید.')
        position_id = self.request.POST['position']
        if position_id is None or position_id =='--':
            return redirect('/manager/employee/?msg= موقعیت شغلی کاربر را انتخاب کنید.')
        position = PositionTB.objects.get(id=position_id)
        gender_id = self.request.POST['gender']
        if gender_id is None or gender_id =='--':
            return render('/manager/employee/?msg= جنسیت کاربر را انتخاب کنید.')
        gender = GenderTB.objects.get(id=gender_id)
        age = self.request.POST['age']
        if age is None or age =='':
            return redirect('/manager/employee/?msg= سن کاربر را وارد کنید.')
        desc = self.request.POST['desc']
        center = self.request.POST['center']
        if center is None or center =='':
            return redirect('/manager/employee/?msg= مرکز را انتخاب کنید.')
        newProfile = ProfileTB.objects.create(
            user = newUser,
            phone = phone ,
            position=position,
            gender=gender,
            age=age,
            desc=desc,
            meliCardCode=meliCardCode,
            personnelCode=personnelCode,
            center=center
        )
        return redirect('/manager/employee/?msg=کاربر جدید با موفقیت ثبت شد.')
    


@method_decorator(csrf_protect, name='dispatch')
class DeleteEmployeeView(BaseManagerView):
    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get('employee_id')

        if not employee_id:
            return redirect('/manager/employee/?msg=کاربر یافت نشد.')

        try:
            user = User.objects.get(id=employee_id)
            user.delete()
            return redirect('/manager/employee/?msg=کاربر با موفقیت حذف شد.')
        except User.DoesNotExist:
            return redirect('/manager/employee/?msg=کاربری با این مشخصات وجود ندارد.')
        
class UserView(BaseManagerView):
    template_name = 'manager/employee.html'
    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id= pk)
            userProfile = ProfileTB.objects.get(user=user)
            genders = GenderTB.objects.all()
            positions = PositionTB.objects.all()
            msg = self.request.GET.get('msg')
            centers = CenterTB.objects.all()
            context ={
                'user':user,
                'userProfile':userProfile,
                'positions':positions,
                'genders':genders,
                'msg':msg,
                'centers':centers,
            }
            return render(request,self.template_name,context)
        except User.DoesNotExist:
            return redirect(f'/manager/employee/{pk}/?msg= کاربر یافت نشد.')
        except ProfileTB.DoesNotExist:
            return redirect(f'/manager/employee/{pk}/?msg= پروفایل کاربر یافت نشد.')
        
    def post(self,request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id = pk)
        except:
            return redirect(f'/manager/client/{pk}/?msg= کاربر یافت نشد.')
        first_name = self.request.POST['first_name']
        if first_name is not None and first_name != '':
            user.first_name = first_name
        last_name = self.request.POST['last_name']
        if last_name is not None and last_name != '':
            user.last_name = last_name
        personnelCode = self.request.POST['personnelCode']
        if personnelCode is not None and personnelCode !='':
            user.username=personnelCode
        meliCardCode = self.request.POST['meliCardCode']
        if meliCardCode is not None or meliCardCode !='':
            user.password=meliCardCode
        user.save()
        userProfile = ProfileTB.objects.get(user=user)
        phone = self.request.POST['phone']
        if phone is not None or phone !='':
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
        userProfile.meliCardCode = meliCardCode
        userProfile.personnelCode = personnelCode
        center = self.request.POST['center']
        if center is not None and center !='--':
            userProfile.center=center
        userProfile.save()
        return redirect(f'/manager/employee/{pk}/?msg= تغییرات با موفقیت ثبت شد.')
    

        

        
