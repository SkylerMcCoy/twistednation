from django.db import models
from members.models import Member
# Create your models here.

class Debate(models.Model):
	created_by=models.ForeignKey(Member)
	topic=models.CharField(max_length=100)
	roundquestion1=models.CharField(max_length=500)
	roundquestion2=models.CharField(max_length=500)
	roundquestion3=models.CharField(max_length=500)
	date=models.DateField()
	privacy=models.CharField(max_length=100)
	timestamp=models.DateTimeField()
	num_part=models.IntegerField()
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")
	
class Invited(models.Model):
	invited_user=models.ForeignKey(Member,verbose_name='Please invite debaters',blank=True,null=True)
	debateinvite=models.ForeignKey(Debate)

class Participants(models.Model):
	participant=models.ForeignKey(Member,verbose_name='Who can participate in this debate?')
	debateparticipate=models.ForeignKey(Debate)
	stand=models.BooleanField()
	
class Questions(models.Model):
	debatequestion=models.ForeignKey(Debate)
	user_questioning=models.ForeignKey(Member)
	question=models.CharField(max_length=500,verbose_name='Your argument')
	timestamp=models.DateTimeField()