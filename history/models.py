from django.db import models
from members.models import Member

# Create your models here.


class History(models.Model):
	user=models.ForeignKey(Member)
	item_type=models.CharField(max_length=100)
	timestamp=models.DateTimeField(auto_now=True)
	item_id=models.IntegerField()
