from django.db import models
from members.models import Member
from tinymce.models import HTMLField

# Create your models here.
class NewPetition(models.Model):
    user = models.ForeignKey(Member)
    title = models.CharField(max_length=100)
    slug = models.TextField()
    body = HTMLField()
    deadline = models.DateField()
    target_no_signs = models.IntegerField()
    petition_type = models.CharField(max_length = 20)
    tts = models.TextField(verbose_name = "Text which should be sent to the decision maker over phone")
    current_num=models.IntegerField(default = 0)
    timestamp=models.DateTimeField(auto_now=True)
    comments_number = models.IntegerField(default=0)
    upvotes_number = models.IntegerField(default=0)
    upvoted_by = models.TextField(default="{}")
    downvotes_number = models.IntegerField(default=0)
    downvoted_by = models.TextField(default="{}")

    def __unicode__(self):
        return self.title


class SignNewPetition(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    zipcode = models.IntegerField(blank = True, null = True, verbose_name = "Your zipcode")
    signedpet = models.ForeignKey(NewPetition)
    is_confirmed = models.BooleanField(default = True)
    whysign = HTMLField(verbose_name = "Why do you support this petition?")
    
    def __unicode__(self):
        return self.name + ', ' + self.email

class DecisionMaker(models.Model):
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    phone = models.CharField(max_length = 30)
    fax = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return self.name + ' ' +  self.email

class DM2(models.Model):
    petition = models.ForeignKey(NewPetition)
    name = models.CharField(max_length = 200)
    email = models.EmailField()
    phone = models.CharField(max_length = 30, verbose_name = "Phonenumber with the countrycode"  )
    fax = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return self.name + ' ' +  self.email


class PetitionType(models.Model):
    title = models.CharField(max_length = 100)