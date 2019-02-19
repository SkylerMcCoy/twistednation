from django.db import models
from members.models import Member

# Create your models here.

class Video(models.Model):
	name=models.CharField(max_length=100)
	user=models.ForeignKey(Member)
	filename=models.CharField(max_length=500)
	desc=models.CharField(max_length=100,null=True,blank=True,verbose_name="Description")
	timestamp=models.DateTimeField()