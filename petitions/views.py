# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render_to_response,get_object_or_404
from petitions.models import Petition,SignPetition
import datetime
from django.template import RequestContext
from django.core.context_processors import csrf
from petitions.forms import PetitionForm,PetitionSignForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from members.models import Member
from history.models import History
import json


@login_required
def index(request):
	userobject = Member.objects.get(user=request.user)
	print userobject
	if request.method=='POST':
		form=PetitionForm(request.POST)
		if form.is_valid():
			newpetobj=form.save(commit=False)
			newpetobj.user=userobject
			newpetobj.current_num=0
			newpetobj.timestamp=datetime.datetime.now()
			newpetobj.save()
			new_hist=History()
			new_hist.user=userobject
			new_hist.item_type="PETITION"
			new_hist.timestamp=newpetobj.timestamp
			new_hist.item_id=newpetobj.id
			new_hist.save()
		 	return HttpResponseRedirect('/petitions/')
	else:
		form=PetitionForm()

	return render_to_response('user_pages/home/base_home_petitions.html',
		{'form':form,},context_instance=RequestContext(request))

@login_required
def listall(request):
	petition_list=Petition.objects.all().order_by('-upvotes_number')
	return render_to_response('user_pages/home/base_home_petitions.html',
		{'petition_list':petition_list},context_instance=RequestContext(request))


@login_required
def viewpet(request,pet_id):
	p=get_object_or_404(Petition,pk=pet_id)
	signedusers=SignPetition.objects.filter(signedpet=p)
	signform=PetitionSignForm()
	return render_to_response('user_pages/home/base_home_petitions_view.html',{'pet':p,'signedusers':signedusers,'signform':signform},context_instance=RequestContext(request))

@login_required
def delpet(request,pet_id):
	p=Petition.objects.get(pk=pet_id)
	if(p.user==request.user.members):
		p.delete()
		print 'deleted'
	else:
		print p.user
		print "-+_"
		print request.user.members
		print 'unable to delete'
	return HttpResponseRedirect('/petitions/')

@login_required
def signed(request,pet_id):
	p=get_object_or_404(Petition,pk=pet_id)
	userobject=get_object_or_404(Member,user=request.user)
	print userobject
	print "^^userobject^^"
	already_signed=SignPetition.objects.filter(user=userobject).filter(signedpet_id=pet_id)
	print already_signed
	if request.method=='POST':
		signform=PetitionSignForm(request.POST)
		if already_signed:
			print "user already signed this petition!!!"
		elif signform.is_valid():
			print 'user not signed yet. going to update database'
			instance=signform.save(commit=False)
			instance.user=userobject
			instance.signedpet=p
			instance.save()
			p.current_num=p.current_num+1
			p.save()
			new_hist=History()
			new_hist.user=userobject
			new_hist.item_type="SIGN"
			new_hist.timestamp=datetime.datetime.now()
			new_hist.item_id=instance.id
			new_hist.save()
	return HttpResponseRedirect('/petitions/'+pet_id+'/')

