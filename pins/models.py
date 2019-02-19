from django.db import models
from members.models import Member

# Create your models here.
class PostPinned(models.Model):
	post = models.TextField()
	post_type = models.CharField(max_length=20)
	member = models.ForeignKey(Member, related_name='pinned_posts')
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.post