from django import forms
from models import Album, Photo
from django.shortcuts import get_object_or_404
from members.models import Member
import datetime

class UploadImageForm(forms.ModelForm):
	class Meta:
		model=Photo
		exclude=('album','filename','timestamp','upvotes_number','downvotes_number','comments_number','upvoted_by','downvoted_by',)
	file=forms.ImageField()
	fields=('file','desc')


class CreateAlbumForm(forms.ModelForm):
	class Meta:
		model=Album
		exclude=('user','timestamp','upvotes_number','downvotes_number','comments_number','upvoted_by','downvoted_by',)
	