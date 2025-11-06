from django.db import models
from django.contrib.auth.models import User

class CenterTB(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=250, null=True,blank=True)
    manager = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True,related_name='CenterManager')
    employees = models.ManyToManyField(User, related_name='CenterEmployees')
    
    def __str__(self):
        return self.name