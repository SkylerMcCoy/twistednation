from django.db import models
from members.models import Member
# Create your models here.

class Album(models.Model):
	name=models.CharField(max_length=100,verbose_name="Album name")
	user=models.ForeignKey(Member)
	timestamp = models.DateTimeField(auto_now=True)
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")

class Photo(models.Model):
	album=models.ForeignKey(Album, related_name='photos')
	filename=models.CharField(max_length=500)
	desc=models.TextField(null=True,blank=True,verbose_name="Photo description")
	timestamp = models.DateTimeField(auto_now=True)
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")