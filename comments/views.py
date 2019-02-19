# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
#import json
#from posts.forms import PostAddForm
#from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
#from members.models import Member, MemberRelations
from posts.models import Post
#from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#from history.models import History
from comments.models import Comment
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from upload.models import Album
from polls.models import Poll
from petitions.models import Petition

COMMENTS_MAP = {
	'POST' : Post,
    'DEBATE': None,
    'PETITION': Petition,
    'ALBUM': Album,
    'PHOTO': None,
    'POLL': Poll,
    'BLOG': None,
    'VOTE': None,
    'COMMENT': None,
    'FRIEND': None,
}

@csrf_exempt
@login_required
def comment_add(request, type, id):
	if request.method == 'POST' :
		if 'content' in request.POST:
			comment = Comment(parent = id, parent_type = type, member = request.user.members)
			comment.content = request.POST['content']
			comment.save()
			instance = COMMENTS_MAP[type].objects.get(pk__exact = id)
			instance.comments_number = instance.comments_number + 1
			instance.save()
			template_dict = {
				'member': request.user.members,
				'comment': comment,
				'instance': instance,
			}
			return render_to_response('user_pages/ajax_delivery/comment_single.html', template_dict, context_instance=RequestContext(request))
	return HttpResponse(0)

@login_required
def comment_view(request, type, id):
	comments = Comment.objects.filter(parent=id, parent_type=type)
	template_dict = {
		'comments': comments
	}
	return render_to_response('user_pages/ajax_delivery/comment_view_all.html', template_dict, context_instance=RequestContext(request))