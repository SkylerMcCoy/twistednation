from django.db import models
from members.models import Member

# Create your models here.
class Message(models.Model):
	member1 = models.ForeignKey(Member, related_name='sent_messages')
	member2 = models.ForeignKey(Member, related_name='received_messages')
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=False)
	has_read = models.BooleanField(default=False)

