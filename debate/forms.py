from django import forms
from django.db import models
from django.shortcuts import get_object_or_404
from debate.models import Debate,Invited,Participants,Questions
from members.models import Member
import datetime

class CreateDebateForm(forms.ModelForm):
	class Meta:
		model=Debate
		exclude=('created_by','roundquestions','timestamp','privacy',)
		fields=('topic','roundquestion1','roundquestion2','roundquestion3','date','num_part')
	#date=forms.CharField(max_length=100)
	

class InviteDebateForm(forms.ModelForm):
	class Meta:
		model=Invited
		exclude=('debateinvite')
	
class ParticipantDebateForm(forms.ModelForm):
	stand=forms.TypedChoiceField(
		coerce=lambda x: True if x == 'True' else False,
        choices=((False, 'Against'), (True, 'For')),
        widget=forms.RadioSelect
        )
	class Meta:
		model=Participants
		exclude=('participant','debateparticipate')

class QuestionsDebateForm(forms.ModelForm):
	class Meta:
		model=Questions
		question=forms.CharField(max_length=500)
		exclude=('debatequestion','user_questioning','timestamp')
