# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from posts.forms import PostAddForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from members.models import Member, MemberRelations
from posts.models import Post
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from history.models import History

def test_view(request):
	template_dict = {
	}
	json_text =  json.dumps(template_dict)
	pyth = json.loads(json_text)
	print pyth
	form = PostAddForm()
	template_dict = {
		'form': form
	}
	return render_to_response('1base.html', template_dict, context_instance=RequestContext(request))




@login_required
def post_vote(request, post_id):
	return_dict = {
		"status": 1,
	}

	try:
		post = Post.objects.get(pk=post_id)
	except:
		post = None
		return_dict['status'] = 0
		return HttpResponse(json.dumps(return_dict))
	if 'action' in request.GET:
		if request.GET['action'] == 'upvote':
			return_dict['action'] = 'upvote'
			upvoted_by_dict = json.loads(post.upvoted_by)
			downvoted_by_dict = json.loads(post.downvoted_by)
			if request.user.username in downvoted_by_dict.values():
				print 'user exists in downvotes'
				del downvoted_by_dict[request.user.username]
				post.downvoted_by = json.dumps(downvoted_by_dict)
				post.downvotes_number = post.downvotes_number - 1
				post.save()
			if request.user.username in upvoted_by_dict.values():
				print 'user exists in upvotes'
				return_dict['already_voted'] = 1
				return_dict['already_upvoted'] = 'already_upvoted'
				return_dict['upvotes_number'] = post.upvotes_number
				return_dict['downvotes_number'] = post.downvotes_number
				return_dict['comments_number'] = post.comments_number
				return HttpResponse(json.dumps(return_dict))
			else:
				return_dict['already_voted'] = 0
				upvoted_by_dict[request.user.username]= request.user.username
				post.upvoted_by = json.dumps(upvoted_by_dict)
				post.upvotes_number = post.upvotes_number +1
			post.save()
		if request.GET['action'] == 'downvote':
			return_dict['action'] = 'downvote'
			downvoted_by_dict = json.loads(post.downvoted_by)
			upvoted_by_dict = json.loads(post.upvoted_by)
			if request.user.username in upvoted_by_dict.values():
				print 'user exists in upvotes'
				del upvoted_by_dict[request.user.username]
				post.upvoted_by = json.dumps(upvoted_by_dict)
				post.upvotes_number = post.upvotes_number - 1
				post.save()
			if request.user.username in downvoted_by_dict.values():
				print 'user exists in downvotes'
				return_dict['already_voted'] = 1
				return_dict['already_downvoted'] = 'already_downvoted'
				return_dict['upvotes_number'] = post.upvotes_number
				return_dict['downvotes_number'] = post.downvotes_number
				return_dict['comments_number'] = post.comments_number
				return HttpResponse(json.dumps(return_dict))
			else:
				return_dict['already_voted'] = 0
				downvoted_by_dict[request.user.username]= request.user.username
				post.downvoted_by = json.dumps(downvoted_by_dict)
				post.downvotes_number = post.downvotes_number +1
			post.save()


	return_dict['upvotes_number'] = post.upvotes_number
	return_dict['downvotes_number'] = post.downvotes_number
	return_dict['comments_number'] = post.comments_number


	return HttpResponse(json.dumps(return_dict))


	


@login_required
def templates(request):
	template_dict = {
	}
	return render_to_response('user_pages/common_elements/activities_templates/templates.html', template_dict, context_instance=RequestContext(request))	


