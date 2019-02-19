from django.db import models
from members.models import Member


# Create your models here.

class Petition(models.Model):
	title=models.CharField(max_length=100)
	content=models.CharField(max_length=200)
	user=models.ForeignKey(Member)
	target=models.CharField(max_length=100)
	target_num=models.IntegerField()
	current_num=models.IntegerField()
	stories=models.CharField(max_length=500)
	timestamp=models.DateTimeField(auto_now=True)
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")
	def __unicode__(self):
		return self.title

class SignPetition(models.Model):
	user=models.ForeignKey(Member)
	signedpet=models.ForeignKey(Petition)
	whysign=models.CharField(max_length=300,blank=True, null=True)

