# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
#from django.http import HttpResponseRedirect
#from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
#from members.forms import UserCreateForm, ProfileEditForm
from members.models import Member, MemberRelations
#from posts.models import Post
from django.contrib.auth.decorators import login_required
#from posts.forms import PostAddForm
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt 
from messages.models import Message
from datetime import datetime
from django.utils.timezone import utc




@login_required
def message_view(request):
	member = Member.objects.get(user=request.user)
	try:
		relations = MemberRelations.objects.filter(
				(Q(member_who_added = member) | Q(member_who_was_added = member) ) & Q(active=True)
		)
	except:
		relations = None
	friends_list = []
	for relation in relations:
		if relation.member_who_added == member:
			friend = relation.member_who_was_added
		else:
			friend = relation.member_who_added
		friends_list.append(friend)
	try:
		messages = Message.objects.filter(
			Q(member2 = request.user.members) &
			Q(has_read = False)
		)
	except:
		messages = []
	senders = []
	for message in messages:
		if message.member1 not in senders:
			senders.append(message.member1)
	unread_conversations = []
	for sender in senders:
		try:
			messages = Message.objects.order_by('-timestamp').filter(
				Q(member1 = sender) &
				Q(has_read = False)
			)[:1]
		except:
			messages = []
		unread_conversations.append(messages[0])
	template_dict = {
		'friends_list': friends_list,
		'unread_conversations': unread_conversations
	}
	return render_to_response("user_pages/messages/message_view.html", template_dict, context_instance=RequestContext(request))

@login_required
def message_individual_view(request, username):
	user = User.objects.get(username__exact = username)
	friend = user.members
	try:
		messages = Message.objects.order_by('-timestamp').filter(
			(
				Q(member1 = request.user.members) &
				Q(member2 = user.members)
			) | 
			(
				Q(member1 = user.members) &
				Q(member2 = request.user.members)
			)
		)[:100]
		for message in messages:
			if message.member2 == request.user.members:
				message.has_read = True
				message.save()
		messages = reversed(messages)
	except:
		messages = None
	template_dict = {
		'friend': friend,
		'messages': messages
	}
	return render_to_response("user_pages/messages/message_individual_view.html", template_dict, context_instance=RequestContext(request))


@csrf_exempt
def message_send(request, username):
	return_dict = {
		'status': 1,
	}
	if request.method == 'POST':
		try:
			friend_user = User.objects.get(username__exact = username)
		except:
			return_dict['status'] = 0
			return HttpResponse(json.dumps(return_dict))
		friend_member = friend_user.members

		message = Message(member1 = request.user.members, member2 = friend_member)
		message.content = request.POST['message']
		message.timestamp = datetime.utcnow().replace(tzinfo=utc)
		message.save()
		template_dict = {
			'message': message,
			'member': request.user.members,
		}
		return render_to_response("user_pages/ajax_delivery/message_after_send.html", template_dict, context_instance=RequestContext(request))

	else:
		return_dict['status'] = 0
	return HttpResponse(json.dumps(return_dict))


def message_check(request, username):
	user = User.objects.get(username__exact = username)
	friend = user.members
	try:
		messages = Message.objects.order_by('timestamp').filter(
			Q(member1 = user.members) &
			Q(member2 = request.user.members) &
			Q(has_read = False)
		)
	except:
		messages = None
	print messages
	print messages
	for message in messages:
		print message
		if message.member2 == request.user.members:
			message.has_read = True
			message.save()
	template_dict = {
		'friend': friend,
		'messages': messages
	}
	return render_to_response("user_pages/ajax_delivery/message_unread_view.html", template_dict, context_instance=RequestContext(request))

