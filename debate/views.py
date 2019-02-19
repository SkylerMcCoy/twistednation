# Create your views here.
from django.contrib.auth.decorators import login_required
from debate.models import Debate,Invited,Participants,Questions
from debate.forms import CreateDebateForm,InviteDebateForm,ParticipantDebateForm,QuestionsDebateForm
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import Http404,HttpResponseRedirect
from django.forms.formsets import formset_factory
from members.models import Member
import datetime
from history.models import History

@login_required
def index(request):
	userobject=Member.objects.get(user=request.user)
	inv_list=Invited.objects.filter(invited_user=userobject).values_list('debateinvite_id',flat=True)
	debate_list=Debate.objects.filter(id__in=inv_list)
	part_list=Participants.objects.filter(participant=userobject).values_list('debateparticipate_id',flat=True)
	part_deb_list=Debate.objects.filter(id__in=part_list)
	if request.method=='POST':
		#form1=InviteDebateForm()
		form2=ParticipantDebateForm()
		form=CreateDebateForm(request.POST)
		print 'request method is post(index)'
		if form.is_valid():
			print 'form is valid(index)'
			new_debate=	form.save(commit=False)
			new_debate.created_by=userobject
			new_debate.privacy="none"
			new_debate.timestamp=datetime.datetime.now()
			new_debate.save()
			#
			#	HISTORY TABLE UPDATION>>>
			#
			new_hist=History()
			new_hist.user=userobject
			new_hist.item_type="DEBATE"
			new_hist.timestamp=new_debate.timestamp
			new_hist.item_id=new_debate.id
			new_hist.save()
			#p=get_object_or_404(Debate,pk=pet_id)
			print new_debate.num_part
			formset1=formset_factory(InviteDebateForm,extra=new_debate.num_part)
			form1=formset1()
			return render_to_response('user_pages/home/base_home_debate.html',
		 		{'dform1':form1,'dform2':form2,
		 		'new_debate':new_debate,'cur_user':request.user},
		 		context_instance=RequestContext(request))
		else:
			form=CreateDebateForm()
			return render_to_response('user_pages/home/base_home_debate.html',
			{'debate_list':debate_list,'part_deb_list':part_deb_list,
			'dform':form,},context_instance=RequestContext(request))
	else:
		form=CreateDebateForm()
		return render_to_response('user_pages/home/base_home_debate.html',
		{'debate_list':debate_list,'part_deb_list':part_deb_list,
		'dform':form,},context_instance=RequestContext(request))

@login_required
def steptwo(request):
	if request.method=='POST':
		debateobj=get_object_or_404(Debate,pk=request.POST.get('debate',False))
		formset1=formset_factory(InviteDebateForm,extra=debateobj.num_part)
		print debateobj.num_part
		print "^^^"
		form1=formset1(request.POST)
		form2=ParticipantDebateForm(request.POST)
		print 'request method is post(steptwo)'
		print debateobj.topic
		if form1.is_valid() and form2.is_valid():
			print 'both forms are valid(steptwo)'
			for inviteform in form1:
				invite=inviteform.save(commit=False)
				invite.debateinvite=debateobj
				invite.save()
			participate=form2.save(commit=False)
			participate.debateparticipate=debateobj
			print 'i\'m here'
			userobject=get_object_or_404(Member,user=request.user)
			participate.participant=userobject
			participate.save()
			return HttpResponseRedirect('/debate/'+str(debateobj.id)+'/')
		else:
			print 'step two form is invalid'
			userobject=get_object_or_404(Member,user=request.user)
			inv_list=Invited.objects.filter(invited_user=userobject).values_list('debateinvite_id',flat=True)
			print list
			debate_list=Debate.objects.filter(id__in=inv_list)
			part_list=Participants.objects.filter(participant=userobject).values_list('debateparticipate_id',flat=True)
			part_deb_list=Debate.objects.filter(id__in=part_list)
			form=CreateDebateForm()
			return render_to_response('user_pages/home/base_home_debate.html',
			{'debate_list':debate_list,'part_deb_list':part_deb_list,
			'dform':form,},context_instance=RequestContext(request))	
	else:
		formset1=formset_factory(InviteDebateForm,extra=debateobj.num_part)
		form1=formset1(request.POST)
		form2=CreateDebateForm()
		print form2
		return render_to_response('user_pages/home/base_home_debate.html',
		{'dform1':form1,'dform2':form2,
		},context_instance=RequestContext(request))

@login_required
def stepthree(request):
	userobject=get_object_or_404(Member,user=request.user)
	print "user id"
	print userobject.id
	inv_list=Invited.objects.filter(invited_user=userobject).values_list('debateinvite_id',flat=True)
	debate_list=Debate.objects.filter(id__in=inv_list)
	for test in debate_list:
		print test
		print "^^^look here^^^"
	part_list=Participants.objects.filter(participant=userobject).values_list('debateparticipate_id',flat=True)
	part_deb_list=Debate.objects.filter(id__in=part_list)
	for test in part_deb_list:
		print test
		print "^^^look here^^^"
	
	return render_to_response('user_pages/home/base_home_debate.html',
			{'debate_list':debate_list,'part_deb_list':part_deb_list,'cur_user':request.user},
			context_instance=RequestContext(request))		
	#return render_to_response('debate/index.html',
	#		{'debate_list':debate_list,'part_deb_list':part_deb_list,'cur_user':request.user},
	#		context_instance=RequestContext(request))		

@login_required
def viewdeb(request,deb_id):
	p=get_object_or_404(Debate,pk=deb_id)
	flag=0
	userobject=get_object_or_404(Member,user=request.user)
	if Invited.objects.filter(debateinvite=p,invited_user=userobject):
		flag=1
	if Participants.objects.filter(debateparticipate=p,participant=userobject):
		print "participant"
		print Participants.objects.filter(debateparticipate=p,participant=userobject)
		if flag==1:
			print "invited"
			print Invited.objects.filter(debateinvite=p,invited_user=userobject)
			Invited.objects.filter(debateinvite=p,invited_user=userobject).delete()
		flag=2
	Participants.objects.filter(participant=userobject).values_list('debateparticipate_id',flat=True)
	return render_to_response('user_pages/home/base_home_debate_view.html',
		{'deb':p,'flag':flag},context_instance=RequestContext(request))

@login_required
def participate(request,deb_id):
	if request.method=='POST':
		PForm=ParticipantDebateForm(request.POST)
		if PForm.is_valid():
			debateobj=get_object_or_404(Debate,pk=deb_id)
			participate=PForm.save(commit=False)
			participate.debateparticipate=debateobj
			userobject=get_object_or_404(Member,user=request.user)
			participate.participant=userobject
			participate.save()
			Invited.objects.filter(debateinvite=debateobj,invited_user=userobject).delete()
			return HttpResponseRedirect('/debate/participate/'+deb_id+'/')
		else:
			PForm=ParticipantDebateForm()
			return render_to_response('debate/participate.html',
			{'form':PForm,'deb':deb_id},
			context_instance=RequestContext(request))
	else:
		PForm=ParticipantDebateForm()
		return render_to_response('debate/participate.html',
			{'form':PForm,'deb':deb_id},
			context_instance=RequestContext(request))

@login_required
def invite(request,deb_id):
	userobject=get_object_or_404(Member,user=request.user)
	debateobj=get_object_or_404(Debate,pk=deb_id)
	if debateobj.created_by!=userobject:
		print "You are not allowed to invite users. You are not the creator of this debate"
		raise Http404("You are not allowed to invite users. You are not the creator of this debate")
	else:
		if request.method=='POST':
			IForm=InviteDebateForm(request.POST)
			if IForm.is_valid():
				debateobj=get_object_or_404(Debate,pk=deb_id)
				invitedebate=IForm.save(commit=False)
				invitedebate.debateinvite=debateobj
				invitedebate.save()
				return HttpResponseRedirect('/debate/invite/'+deb_id+'/')
			else:
				IForm=InviteDebateForm()
				return render_to_response('debate/invite.html',
				{'form':IForm,'deb':deb_id},
				context_instance=RequestContext(request))
		else:
			IForm=InviteDebateForm()
			return render_to_response('debate/invite.html',
				{'form':IForm,'deb':deb_id},
				context_instance=RequestContext(request))

@login_required
def start(request,deb_id):
	userobject=get_object_or_404(Member,user=request.user)
	debateobj=get_object_or_404(Debate,pk=deb_id)
	if debateobj.date  >= datetime.date.today():
		participantsfor=Participants.objects.filter(debateparticipate=debateobj,stand=True).values_list('participant_id',flat=True)
		usersfor=Member.objects.filter(id__in=participantsfor)
		participantsagainst=Participants.objects.filter(debateparticipate=debateobj,stand=False).values_list('participant_id',flat=True)
		usersagainst=Member.objects.filter(id__in=participantsagainst)

		debatequestionsfor=Questions.objects.filter(debatequestion=debateobj,user_questioning_id__in=participantsfor)
		debatequestionsagainst=Questions.objects.filter(debatequestion=debateobj,user_questioning_id__in=participantsagainst)
		
		flag=0
		if Participants.objects.filter(participant=userobject,debateparticipate=debateobj):
			flag=1
		if flag==0:
			print "You are not allowed to participate in this debate. Get an invitation from the creator of this debate"
			raise Http404("You are not allowed to participate in this debate. Get an invitation from the creator of this debate")
		else:
			if request.method=='POST':
				QForm=QuestionsDebateForm(request.POST)
				if QForm.is_valid():
					formsave=QForm.save(commit=False)
					formsave.debatequestion=debateobj
					formsave.user_questioning=userobject
					formsave.timestamp=datetime.datetime.now()
					formsave.save()
					return HttpResponseRedirect('/debate/'+deb_id+'/start/')
				else:
					QForm=QuestionsDebateForm()
					return render_to_response('user_pages/home/base_home_debate.html',
						{'debate':debateobj,'form':QForm,'deb':deb_id,
						'usersfor':usersfor,'usersagainst':usersagainst,
						'argfor':debatequestionsfor,'argagainst':debatequestionsagainst,},
						context_instance=RequestContext(request))
			else:
				QForm=QuestionsDebateForm()
				return render_to_response('user_pages/home/base_home_debate.html',
					{'debate':debateobj,'form':QForm,'deb':deb_id,
					'usersfor':usersfor,'usersagainst':usersagainst,
					'argfor':debatequestionsfor,'argagainst':debatequestionsagainst,},
					context_instance=RequestContext(request))
	else:
		return render_to_response('user_pages/home/base_home_debate_view.html',context_instance=RequestContext(request))