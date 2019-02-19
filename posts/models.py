from django.db import models
from members.models import Member
# Create your models here.

class Post(models.Model):
	member = models.ForeignKey(Member, related_name='posts')
	member_to = models.ForeignKey(Member, related_name='posts_on_wall')
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	comments_number = models.IntegerField(default=0)
	upvotes_number = models.IntegerField(default=0)
	upvoted_by = models.TextField(default="{}")
	downvotes_number = models.IntegerField(default=0)
	downvoted_by = models.TextField(default="{}")


	def __unicode__(self):
		return self.content + ' by ' + self.member.user.first_name+' '+self.member.user.last_name	


