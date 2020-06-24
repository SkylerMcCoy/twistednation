# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from upload.forms import UploadImageForm
from django.template import RequestContext
from members.models import Member
from upload.models import Album,Photo
from history.models import History
from upload.forms import CreateAlbumForm
from django.contrib.auth.decorators import login_required
import random, string,datetime
from PILLOW import Image
import os,errno
from django.core.files.storage import default_storage
from django.conf import settings

@login_required
def upload_image(request):
	if request.method=='POST':
		userobject=get_object_or_404(Member,user=request.user)
		form=UploadImageForm(request.POST, request.FILES)
		f=request.FILES['file']
		filename=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(100))
		originalfilename=filename+'.jpeg'
		print f.content_type
		if form.is_valid():
			os.mkdir('/python/mysite/'+userobject.directoryname)
			with open(userobject.directoryname+'/'+originalfilename,'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			size =150,150
			infile=userobject.directoryname+'/'+originalfilename
			outfile=os.path.splitext(infile)[0]+"_thumbnail.jpeg"
			if infile!=outfile:
				try:
					im=Image.open(infile)
					im.thumbnail(size,Image.ANTIALIAS)
					im.save(outfile,"JPEG")
				except IOError:
					print "cannot create thumbnail"
			return render_to_response('upload/success.html',context_instance=RequestContext(request))
	else:
		form=UploadImageForm()
	return render_to_response('upload/upload.html',
		{'form':form},context_instance=RequestContext(request))

@login_required
def index(request):
	userobject=get_object_or_404(Member,user=request.user)
	print userobject.id
	user_albums=Album.objects.filter(user=userobject)
	dic=[]
	i=0
	print user_albums
	print "^^look here"
	print "now"
	if user_albums:
		for alb in user_albums:
			print alb
			print "---"
			try:
				pic=Photo.objects.filter(album=alb).latest('timestamp')
				dic.append([{'albumid':alb.id},{'albuma':alb.name},{'photo':pic.filename}])
			except:
				dic.append([{'albumid':alb.id},{'albuma':alb.name}])
			print dic[i]
			i=i+1
	print "look down"
	print dic	
	if request.method=='POST':
		form=CreateAlbumForm(request.POST)
		#uploading image
		form2=UploadImageForm(request.POST, request.FILES)
		f=request.FILES['file']
		filename=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(80))
		originalfilename=str(userobject.id)+"-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"-"+filename+'.jpeg'
		if form.is_valid() and form2.is_valid():
			new_album=form.save(commit=False)
			new_album.user=userobject
			new_album.timestamp=datetime.datetime.now()
			new_album.save()
			#uploding image
			foldername=settings.PHOTO_DIR
			try:
				os.mkdir(foldername)
			except OSError as exc: # Python >2.5
				if exc.errno == errno.EEXIST and os.path.isdir(foldername):
					pass
				else: 
					raise
			with open('ups/albumpics/'+originalfilename,'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			size =150,150
			infile='ups/albumpics/'+originalfilename
			outfile=infile+"_thumbnail.jpeg"
	#		outfile=os.path.splitext(infile)[0]+"_thumbnail.jpeg"
			if infile!=outfile:
				try:
					im=Image.open(infile)
					im.thumbnail(size,Image.ANTIALIAS)
					im.save(outfile,"JPEG")
				except IOError:
					print "cannot create thumbnail"
			savepic=form2.save(commit=False)
			savepic.album_id=new_album.id
			savepic.filename=originalfilename
			savepic.timestamp=datetime.datetime.now()
			savepic.save()

			new_hist=History()
			new_hist.user=userobject
			new_hist.item_type="ALBUM"
			new_hist.timestamp=new_album.timestamp
			new_hist.item_id=new_album.id
			new_hist.save()
			print "saving object with"
			print new_album.user
			print new_album.timestamp
			print new_album.name
		 	return HttpResponseRedirect('/albumlist/'+str(new_album.id)+'/')
	else:
		form=CreateAlbumForm()
		uploadform=UploadImageForm()
	return render_to_response('user_pages/photo/gallery.html',
		{'albumlist':dic,'form':form,'imageform':uploadform},
		context_instance=RequestContext(request))

@login_required
def viewalbum(request,album_id):
	album=get_object_or_404(Album,pk=album_id)
	photos=Photo.objects.filter(album=album)
	if request.method=='POST':
		userobject=get_object_or_404(Member,user=request.user)
		form=UploadImageForm(request.POST, request.FILES)
		f=request.FILES['file']
		filename=''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(80))
		originalfilename=str(userobject.id)+"-"+datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"-"+filename+'.jpeg'
		print f.content_type
		if form.is_valid():
			foldername=settings.PHOTO_DIR
			try:
				os.mkdir(foldername)
			except OSError as exc: # Python >2.5
				if exc.errno == errno.EEXIST and os.path.isdir(foldername):
					pass
				else: 
					raise
			with open('ups/albumpics/'+originalfilename,'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
			size =150,150
			destination.close()
			infile='ups/albumpics/'+originalfilename
			outfile=infile+"_thumbnail.jpeg"
	#		outfile=os.path.splitext(infile)[0]+"_thumbnail.jpeg"
			if infile!=outfile:
				try:
					im=Image.open(infile)
					im.seek(0)
					im.thumbnail(size,Image.ANTIALIAS)
					im.save(outfile,"JPEG")
				except IOError:
					print "cannot create thumbnail"
			savepic=form.save(commit=False)
			savepic.album_id=album_id
			savepic.filename=originalfilename
			savepic.timestamp=datetime.datetime.now()
			savepic.save()
			return HttpResponseRedirect('/albumlist/'+album_id+'/')
		else:
			print 'form invalid'
			form=UploadImageForm()
	else:
		print "there is no post"
		form=UploadImageForm()
	return render_to_response('user_pages/photo/gallery_album.html',
		{'album':album,'pics':photos,'form':form},
		context_instance=RequestContext(request))

@login_required
def viewpic(request,pic_id):
	picture=get_object_or_404(Photo,pk=pic_id)
	allpics=Photo.objects.filter(album=picture.album)
	for key,photo in enumerate(allpics):
		flag=0
		if photo==picture:
			val=key
			flag=1
	if flag==1:   #means last pic
		next=allpics[0].id
		if(len(allpics)>1):
			prev=allpics[val-1].id
		else:
			prev=allpics[0].id
	elif val==0:
		next=allpics[1].id
		prev=allpics[len(allpics)-1].id
	else:
		next=allpics[val+1].id
		prev=allpics[val-1].id
	print next
	print prev

	return render_to_response('user_pages/photo/gallery_album.html',{'picture':picture,'next':next,'prev':prev},context_instance=RequestContext(request))

@login_required
def deletepic(request,pic_id):
	instance=Photo.objects.get(pk=pic_id)
	album=instance.album_id
	albumobject=Album.objects.get(pk=album)
	userobject=get_object_or_404(Member,user=request.user)
	if(albumobject.user==userobject):
		default_storage.delete('ups/albumpics/'+instance.filename)
		default_storage.delete('ups/albumpics/'+instance.filename+'_thumbnail.jpeg')
		instance.delete()
	return HttpResponseRedirect('/albumlist/'+str(album)+'/')

@login_required
def editalbum(request,album_id):
	instance=Album.objects.get(pk=album_id)
	userobject=get_object_or_404(Member,user=request.user)
	if request.method=='POST':
		if(instance.user==userobject):
			albumname=request.POST['albumname']
			instance.name=albumname
			instance.save()
	return HttpResponseRedirect('/albumlist/'+str(album_id)+'/')	