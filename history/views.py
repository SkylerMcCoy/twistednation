# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from history.models import History
from petitions.models import Petition
from posts.forms import PostAddForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from members.models import Member, MemberRelations
from posts.models import Post
from django.db.models import Q
from pins.models import PostPinned
from upload.models import Album, Photo
from debate.models import Debate
from polls.models import Poll, Choice
import json




@login_required
def histry(request):
	history=History.objects.all().order_by('-timestamp')
	wholelist=[]
	for eachhist in history:
		if eachhist.item_type == "DEBATE":
			print "item is debate"
			debateobj=Debate.objects.get(pk=eachhist.item_id)
			wholelist.append(debateobj)
		elif eachhist.item_type == "PETITION":
			print "item is petition"
			petitionobj=Petition.objects.get(pk=eachhist.item_id)
			wholelist.append(petitionobj)
	return render_to_response('user_pages/history.html',{'history':history,'histobjects':wholelist},context_instance=RequestContext(request))

@login_required
def home(request):
    if request.user.is_authenticated():
		if not request.user.is_active:
			return HttpResponseRedirect("/profile/edit/")
		user = User.objects.get(username__exact=request.user.username)
		print user
		try:
			member = Member.objects.get(user__exact=request.user)
		except:
			member = None
		if request.method == 'POST':
			try:
				post_add_form = PostAddForm(request.POST)
				form = post_add_form.save(commit=False)
				form.member = member
				form.member_to = member
				form.save()
				post_history = History(user = request.user.members, item_type = 'POST', item_id = form.id)
				post_history.save()
			except:
				pass
		try:
			relations = MemberRelations.objects.filter(
				(
					Q(member_who_added = member) |
					Q(member_who_was_added = member)
				) &
				Q(active = True)
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
		friends_list.append(request.user.members)
		print "####Friends List####"
		print friends_list
		try:
			friends_history = History.objects.filter(
				user__in = friends_list
			)
		except:
			friends_history = None
		friends_history = friends_history.reverse()
		print "####Friends History####"
		print friends_history
		home_feed = []
		for each_friend_history in friends_history:
			test = {}
			test['owner_member'] = each_friend_history.user
			test['type'] = each_friend_history.item_type
			test['item_id'] = each_friend_history.item_id
			try:
				pin = PostPinned.objects.get(
					Q(post = test['item_id']) &
					Q(post_type = test['type']) &
					Q(member = request.user.members)
				)
			except:
				pin = None
			if pin is not None:
				test['pin'] = True
			else:
				test['pin'] = False
#Data for populating each activity Template
			if test['type'] == "POST":
				try:
					post = Post.objects.get(
						pk__exact = test['item_id']
					)
					test['parent_activity'] = post
					test['upvotes_number'] = post.upvotes_number
					test['downvotes_number'] = post.downvotes_number
					test['comments_number'] = post.comments_number
				except:
					post = None
			elif test['type'] == "ALBUM":
				try:
					album = Album.objects.get(
						pk__exact=test['item_id']
					)
				except:
					album = None
				try:
					photos = Photo.objects.order_by('-timestamp').filter(album = album)[:3]
					test['parent_activity'] = album
					test['album_photos'] = photos
					test['upvotes_number'] = album.upvotes_number
					test['downvotes_number'] = album.downvotes_number
					test['comments_number'] = album.comments_number
				except:
					photos  = []
			elif test['type'] == "PETITION":
				try:
					petition = Petition.objects.get(
						pk__exact = test['item_id']
					)
					test['parent_activity'] = petition
					test['upvotes_number'] = petition.upvotes_number
					test['downvotes_number'] = petition.downvotes_number
					test['comments_number'] = petition.comments_number
				except:
					petition = None
			elif test['type'] == "FRIEND":
				try:
					relation = MemberRelations.objects.get(
						pk__exact = test['item_id']
					)
					test['parent_activity'] = relation
				except:
					relation = None
			elif test['type'] == "DEBATE":
				try:
					debate = Debate.objects.get(
						pk__exact = test['item_id']
					)
					test['parent_activity'] = debate
				except:
					debate = None
			elif test['type'] == "POLL":
				try:
					poll = Poll.objects.get(
						pk__exact = test['item_id']
					)
					test['parent_activity'] = poll
				except:
					poll = None
				test['upvotes_number'] = poll.upvotes_number
				test['downvotes_number'] = poll.downvotes_number
				test['comments_number'] = poll.comments_number
				choices = []
				try:
					choices = Choice.objects.filter(poll = poll)
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
		print "####Home Feed####"
		print home_feed
		home_feed.reverse()
		print home_feed
		post_add_form = PostAddForm()
		template_dict = {
			'error': '',
			'page_name':'news',
			'user' : request.user,
			'member':member,
			'owner_member':member,
			'post_add_form': post_add_form,
			'home_feed': home_feed
		}
		return render_to_response('user_pages/home/page_news.html', template_dict, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/login/")