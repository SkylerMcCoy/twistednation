from django import forms
from django.shortcuts import get_object_or_404
from petitions.models import Petition,SignPetition
from members.models import Member
import datetime
from django.contrib.auth.models import User

class PetitionForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super(PetitionForm,self).__init__(*args,**kwargs)
	class Meta:
		model=Petition
		exclude=('user','current_num','timestamp','signed_users','upvotes_number','upvoted_by','downvotes_number','downvoted_by')
	title=forms.CharField(max_length=100,label='What change do you want to see')
	target=forms.CharField(max_length=100,label='Who are you petitioning')
	target_num=forms.IntegerField(label='How many signatures do you need')
	content=forms.CharField(label='Why is this important',widget=forms.Textarea(attrs={'rows':'3', 'cols': '30'}))
	stories=forms.CharField(label='What is the story behind this petition',widget=forms.Textarea(attrs={'rows':'3', 'cols': '30'}))
	#def save(self,*args,**kwargs):
	#	commit=kwargs.pop('commit',True)
	#	thisuser=kwargs.pop('user')
	#	userobject=get_object_or_404(Member,user=thisuser)
	#	instance = super(PetitionForm, self).save(*args, commit = False, **kwargs)
	#	instance.user=userobject
	#	instance.current_num=0
		#get user session and include user='his user_id' here
	#	instance.timestamp=datetime.datetime.now()
	#	if commit:
	#		instance.save()
	#	return instance

class PetitionSignForm(forms.ModelForm):
	class Meta:
		model=SignPetition
		exclude=('user','signedpet')