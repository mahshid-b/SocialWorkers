from django.db import models
from django.contrib.auth.models import User

class GenderTB(models.Model):
    name = models.CharField(null = True, blank = True, max_length = 31)

    def __str__(self):
        return self.name
    
class PositionTB(models.Model):
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('CEO', 'CEO'),
    ]
    group_name = models.CharField(choices=ROLE_CHOICES, max_length=155, null=True, blank=True)

    def __str__(self):
        return self.group_name

class ProfileTB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True , blank=True ,  related_name="ProfileUser")
    phone = models.IntegerField(null=True,blank=True)
    profilePic = models.ImageField(null = True, blank = True, upload_to='profile_picture/')
    position = models.ForeignKey(PositionTB, null = True, blank = True, on_delete = models.CASCADE ,related_name = 'ProfilePosition')
    gender = models.ForeignKey(GenderTB, null = True, blank = True, on_delete = models.CASCADE ,related_name = 'ProfileGender')
    age = models.IntegerField(null = True , blank = True )
    desc = models.TextField(null = True , blank = True)
    meliCardCode = models.IntegerField(null=True,blank=True)
    personnelCode = models.IntegerField( null=True,blank=True)
    otp_code = models.CharField(max_length=15, blank=True, null=True)
    center = models.ForeignKey('centers.CenterTB', on_delete=models.CASCADE, null=True, blank=True,related_name='profileCenter')
    
    def is_otp_valid(self, otp):
        return self.otp_code == otp
    def __str__(self):
        return self.user.username 