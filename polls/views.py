from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from history.models import History
#import datetime
#from polls.models import Poll
#from members.models import Member
from polls.forms import PollCreateForm, PollChoicesCreateForm
from polls.models import Poll, Choice
import json

# Create your views here.
@login_required
def poll_create(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            poll_form = PollCreateForm(request.POST, prefix="poll")
            if poll_form.is_valid():
                print 'Valid Form'
                unsaved_poll = poll_form.save(commit=False)
                unsaved_poll.member = request.user.members
                unsaved_poll.save()
                history = History(user = request.user.members, item_type = 'POLL', item_id = unsaved_poll.id)
                history.save()
                return HttpResponseRedirect("/polls/"+str(unsaved_poll.id))

        poll_form = PollCreateForm(prefix="poll")
        try:
            polls = Poll.objects.filter(member = request.user.members)
        except:
            polls = []
        template_dict = {
            'error': '',
            'poll_form' : poll_form,
            'polls': polls
        }
        return render_to_response(
            'user_pages/polls/poll_create.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")


@login_required        
def poll_view(request, poll_id):
    if request.user.is_authenticated():
        try:
            poll = Poll.objects.get(pk__exact = poll_id)
        except:
            poll = None
            return HttpResponseRedirect("/polls/")
        if request.method == 'POST':
            choice_form = PollChoicesCreateForm(request.POST)
            if choice_form.is_valid():
                print 'Valid Form'
                unsaved_choice = choice_form.save(commit=False)
                unsaved_choice.member = request.user.members
                unsaved_choice.poll = poll
                unsaved_choice.save()
        choice_form = PollChoicesCreateForm()
        try:
            choices = Choice.objects.filter(poll__exact = poll)
        except:
            choices = []
        print ('Choices', choices)
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
        template_dict = {
            'error': '',
            'poll' : poll,
            'choices_list': choices_list,
            'choice_form': choice_form,
        }
        if request.is_ajax():
            return render_to_response(
                'user_pages/polls/bar_graph.html',
                template_dict, 
                context_instance=RequestContext(request)
            )
        else:
            return render_to_response(
                'user_pages/polls/poll_view.html',
                template_dict, 
                context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect("/login/")

@login_required
def choice_select(request, poll_id, choice_id):
    if request.user.is_authenticated():
        try:
            poll = Poll.objects.get(pk__exact = poll_id)
        except:
            poll = None
        try:
            choice = Choice.objects.get(pk__exact = choice_id)
        except:
            choice = None
        if choice.poll != poll:
            print 'Choice and Poll not related'
            return HttpResponseRedirect("/polls/"+poll_id)
        try:
            poll_choices = Choice.objects.filter(poll = poll)
        except:
            poll_choices = []
        print ('---------------------', poll_choices)
        for each_choice in poll_choices:
            choice_voted_users = json.loads(each_choice.voted_by)
            print('+++++choice_voted_users', choice_voted_users)
            if request.user.username in choice_voted_users:
                print 'User already voted for some choice '+each_choice.choice_name
                print 'choice_voted_users before deletion ', choice_voted_users
                del choice_voted_users[request.user.username]
                print 'choice_voted_users after deletion ', choice_voted_users
                each_choice.voted_by = json.dumps(choice_voted_users)
                print 'each_choice_votes before saving', each_choice.votes_number
                each_choice.votes_number = each_choice.votes_number - 1
                poll.choice_votes_no = poll.choice_votes_no - 1
                each_choice.save()
                print 'each_choice_votes after saving', each_choice.votes_number
        try:
            choice = Choice.objects.get(pk__exact = choice_id)
        except:
            choice = None
        choice_users = json.loads(choice.voted_by)        
        print ('choice_users', choice_users)
        choice_users[str(request.user.username)]= request.user.username
        print ('choice_users', choice_users)
        choice.voted_by = json.dumps(choice_users)
        choice.votes_number = choice.votes_number + 1
        poll.choice_votes_no = poll.choice_votes_no + 1
        poll.save()
        choice.save()
        print 'votes_number after incrementing', choice.votes_number
        print 'voted_by after incrementing', choice.voted_by
        #if poll_id is not None and choice_id is not None:
        return HttpResponseRedirect("/polls/"+poll_id)
    else:
        return HttpResponseRedirect("/login/")

@login_required
def poll_search(request):
    if request.user.is_authenticated():
        template_dict = {
            'error': '',
        }
        if request.method == 'POST':
            search_string = request.POST['search_string']
            try:
                polls = Poll.objects.filter(
                    Q(title__contains=search_string)
                )
            except:
                polls = []
            template_dict = {
                'searched': True,
                'polls': polls,
            }
        return render_to_response(
            'user_pages/polls/poll_search.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")

@login_required
def poll_trending(request):
    if request.user.is_authenticated():
        template_dict = {
            'error': '',
        }
        try:
            polls = Poll.objects.order_by('-choice_votes_no').all()[:10]
        except:
            polls = []
        print 'polls', polls
        template_dict = {
            'polls': polls,
        }
        return render_to_response(
            'user_pages/polls/poll_trending.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")