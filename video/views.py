# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from video.forms import UploadVideoForm
from members.models import Member
from video.models import Video
import os
import datetime
import string
import random

@login_required
def upload(request):
	userobject=get_object_or_404(Member,user=request.user)
	videos=Video.objects.filter(user=userobject)
	if request.method == 'POST':
		form = UploadVideoForm(request.POST, request.FILES)
		f=request.FILES['file']
		fileext=os.path.splitext(f.name)[1]
		print f.name+"<<filename with extension"
		print f.content_type+"<<content type"
		print os.path.splitext(f.name)[0]+"<<filename alone"
		print os.path.splitext(f.name)[1]+"<<file extension alone"
		filename=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(80))
		originalfilename=str(userobject.id)+"-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"-"+filename+fileext
		if form.is_valid() and (fileext==".mp4" or fileext==".flv"):
			with open('ups/videos/'+originalfilename, 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			instance=form.save(commit=False)
			instance.user=userobject
			instance.filename=originalfilename
			instance.timestamp=datetime.datetime.now()
			instance.save()
			return HttpResponseRedirect('/video/')
		else:
			return HttpResponse("Invalid file dude")
	else:
		form = UploadVideoForm()
	return render_to_response('user_pages/video/allvideos.html', {'form': form,'videos':videos},context_instance=RequestContext(request))

@login_required
def viewvid(request,vid_id):
	video=Video.objects.get(pk=vid_id)
	return render_to_response('user_pages/video/video.html', {'video':video},context_instance=RequestContext(request))
