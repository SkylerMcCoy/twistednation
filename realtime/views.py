# Create your views here.
#from django.http import HttpResponseRedirect
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
#from members.forms import UserCreateForm, ProfileEditForm
from members.models import MemberRelations
#from posts.models import Post
from django.contrib.auth.decorators import login_required
#from posts.forms import PostAddForm
import json
from django.http import HttpResponse
from messages.models import Message

@login_required
def notifications(request):
	return_dict = {}
	try:
		pending_requests = MemberRelations.objects.order_by('-timestamp').filter(
			Q(member_who_was_added = request.user.members) &
			Q(active = False)
		)
	except:
		pending_requests = []
	return_dict['requests_no'] = len(pending_requests)
	try:
		messages = Message.objects.filter(
			Q(member2 = request.user.members) &
			Q(has_read = False)
		)
	except:
		messages = []
	return_dict['messages_no'] = len(messages)
	senders = []
	for message in messages:
		if message.member1 not in senders:
			senders.append(message.member1)
	print senders
	return_dict['senders_no'] = len(senders)




	return HttpResponse(json.dumps(return_dict))


