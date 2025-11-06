from django.db import models
from centers.models import *
from allusers.models import *
from jalali_date import date2jalali

# Create your models here.
class NewPostTB(models.Model):
    title = models.CharField(max_length=25, null=True,blank=True)
    post = models.TextField(blank=True,max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='PostAuthor')
    date = models.DateField( auto_now=True, auto_now_add=True)

    def __str__(self):
        return self.title