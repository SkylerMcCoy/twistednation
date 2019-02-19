# Create your views here.
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
#from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
#from posts.models import Post, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from members.models import Member, MemberRelations
from posts.models import Post
from pins.models import PostPinned
from upload.models import Album, Photo
from debate.models import Debate
from petitions.models import Petition
from polls.models import Poll, Choice

@login_required
def post_pin(request, post_id):
	return_dict = {
		'status': 0
	}
	if 'type' in request.GET:
		try:
			post_pinned = PostPinned.objects.get(post=post_id, post_type=request.GET['type'])
		except:
			post_pinned = None
		print post_pinned
		if post_pinned is None:
			pinned_post = PostPinned(post=post_id, post_type=request.GET['type'])
			pinned_post.member = request.user.members
			pinned_post.save()
			return_dict['status'] = 1
			return_dict['pinned'] = 1
			return_dict['pinned_post'] = pinned_post.post
		else:
			pinned_post = PostPinned.objects.get(
				Q(post=post_id) &
				Q(post_type=request.GET['type'])
			)
			pinned_post.delete()
			return_dict['status'] = 1
			return_dict['pinned'] = 0
	return HttpResponse(json.dumps(return_dict))


@login_required
def post_pins_view(request):
	try:
		pins = PostPinned.objects.order_by('-timestamp').filter(member = request.user.members)
	except:
		pins = []
		template_dict = {
			'error': '',
			'page_name':'pinned-posts',
			'user' : request.user,
		}
		return render_to_response('user_pages/home/page_pinned_posts.html', template_dict, context_instance=RequestContext(request))
	home_feed = []
	for pin in pins:
		test = {}
		test['pin'] = True
		test['type'] = pin.post_type
		test['post_type'] = pin.post_type
		test['item_id'] = pin.post
		if test['type'] == "POST":
			try:
				obj = Post.objects.get(
					pk__exact = test['item_id']
				)
			except:
				obj = None
			test['owner_member'] = obj.member
			test['parent_activity'] = obj
			test['upvotes_number'] = obj.upvotes_number
			test['downvotes_number'] = obj.downvotes_number
			test['comments_number'] = obj.comments_number
		elif test['type'] == "ALBUM":
			try:
				obj = Album.objects.get(
					pk__exact = test['item_id']
				)
			except:
				obj = None
			try:
				photos = Photo.objects.order_by('-timestamp').filter(album = obj)[:3]
			except:
				photos  = []
			test['album_photos'] = photos
			test['owner_member'] = obj.user
			test['parent_activity'] = obj
			test['upvotes_number'] = obj.upvotes_number
			test['downvotes_number'] = obj.downvotes_number
			test['comments_number'] = obj.comments_number
		if test['type'] == "POLL":
			try:
				obj = Poll.objects.get(
					pk__exact = test['item_id']
				)
			except:
				obj = None
			test['owner_member'] = obj.member
			test['parent_activity'] = obj
			test['upvotes_number'] = obj.upvotes_number
			test['downvotes_number'] = obj.downvotes_number
			test['comments_number'] = obj.comments_number
			choices = []
			try:
				choices = Choice.objects.filter(poll = obj)
			except:
				choices = []
			print choices
			choices_list = []
			total_votes_number = 0
			for choice in choices:
			    each_choice = {}
			    voted_by = json.dumps(choice.voted_by)
			    if request.user.username in voted_by:
			        print '++++++++++++++++++++++++++++++++++++ present in voted_by', voted_by
			        each_choice['voted'] = True
			    each_choice['percentage'] = choice.votes_number
			    each_choice['choice'] = choice
			    choices_list.append(each_choice)
			    total_votes_number += choice.votes_number
			#print ('choices_list ',choices_list)
			if total_votes_number != 0:
				for each_choice in choices_list:
					print('each_choice', each_choice)
					each_choice['percentage'] = each_choice['percentage'] * 100 / total_votes_number
					print ('each choice percentage', each_choice['percentage'])
			print ('Total no of votes', total_votes_number)
			test['choices_list'] = choices_list
		home_feed.append(test)
	print 'home_feed before reversal', home_feed
	home_feed.reverse()
	print 'home_feed after reversal', home_feed
	template_dict = {
		'error': '',
		'page_name':'pinned-posts',
		'user' : request.user,
		'home_feed': home_feed
	}
	return render_to_response('user_pages/home/page_pinned_posts.html', template_dict, context_instance=RequestContext(request))