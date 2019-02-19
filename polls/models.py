from django.db import models
from members.models import Member

# Create your models here.
class Poll(models.Model):
	member=models.ForeignKey(Member)
	title=models.CharField(max_length=200)
	description=models.TextField()
	choice_votes_no = models.BigIntegerField(default=0)
	timestamp=models.DateTimeField(auto_now=True)
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")
	def __unicode__(self):
		return self.title

class Choice(models.Model):
	poll = models.ForeignKey(Poll, related_name='choices' )
	member = models.ForeignKey(Member)
	choice_name = models.CharField(max_length=200)
	votes_number = models.IntegerField(default=0)
	voted_by = models.TextField(default="{}")
