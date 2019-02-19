from django.db import models
from members.models import Member

# Create your models here.
class Comment(models.Model):
	parent = models.TextField()
	parent_type = models.CharField(max_length=20)
	member = models.ForeignKey(Member, related_name='comments')
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)


	def __unicode__(self):
		return self.content
