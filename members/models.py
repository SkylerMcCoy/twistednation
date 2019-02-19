from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Member(models.Model):
	SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

	user = models.OneToOneField(User, related_name='members')
	about = models.TextField()
	sex = models.CharField(max_length=10, choices=SEX, default='Male')
	born_on = models.DateField(default=date.today)
	town = models.CharField(max_length=100)
	institution = models.CharField(max_length=100, null=True, blank=True)
	facebook_handle = models.CharField(max_length=100, null=True, blank=True)
	twitter_handle = models.CharField(max_length=100, null=True, blank=True)
	country = models.CharField(max_length=100, null=True, blank=True)
	photo  = models.ImageField(upload_to = 'ups/profile_pictures/%m%S%Y%d/')
	
	def __unicode__(self):
		return self.user.first_name+' '+self.user.last_name


class MemberRelations(models.Model):
	member_who_added = models.ForeignKey(Member, related_name='member_who_added')
	member_who_was_added  = models.ForeignKey(Member, related_name='member_who_was_added')
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.member_who_added.user.get_full_name() + " added " + self.member_who_was_added.user.get_full_name() + " as friend."


