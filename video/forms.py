from django import forms
from video.models import Video

class UploadVideoForm(forms.ModelForm):
	class Meta:
		model=Video
		exclude=('user','filename','timestamp',)
	file=forms.FileField()