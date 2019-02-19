from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from members.forms import UserCreateForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from posts.forms import PostAddForm
from history.models import History
import datetime


from members.models import Member, MemberRelations
from posts.models import Post
from pins.models import PostPinned
from upload.models import Album, Photo
from debate.models import Debate
from petitions.models import Petition

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            return HttpResponseRedirect("/login/")
    template_dict = {
        'register_form': UserCreateForm(),
    }
    return render_to_response("public_pages/register.html", template_dict, context_instance=RequestContext(request))

def login_member(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")
    if request.method == 'POST':
        print('Posted');
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            login(request, user)
            if user.is_active:
                # Redirect to a success page
                return HttpResponseRedirect("/home/")
            else:
                return HttpResponseRedirect("/profile/edit/")

    template_dict = {
        'login_form':AuthenticationForm(),
        'register_form': UserCreateForm(),
    }
    return render_to_response('public_pages/login.html',template_dict, context_instance=RequestContext(request) )
def logout_member(request):
    logout(request)
    return HttpResponseRedirect("/home/")




@login_required
def profile_edit(request):
    if request.user.is_authenticated():
        try:
            existing_member = Member.objects.get(user__exact=request.user)
        except:
            existing_member = None
        if request.method == 'POST':
            form = ProfileEditForm(request.POST,request.FILES,  instance = existing_member)
            if form.is_valid():
                member = form.save(commit=False)
                member.user = request.user
                request.user.is_active = True
                request.user.save()
                member.save()
                return HttpResponseRedirect("/home/")
        form = ProfileEditForm(instance = existing_member)
        template_dict = {
            'error': '',
            'form' : form,
            'member': existing_member,
        }
        return render_to_response(
            'user_pages/profile/profile_edit.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")

@login_required
def profile_view(request, profile_id):
    if ((profile_id is None) or profile_id == ''):
        profile_id = request.user.username
    print profile_id
    try:
        user = User.objects.get(username__exact=profile_id)
    except:
        return HttpResponseRedirect("/profile/")
    try:
        member = Member.objects.get(user__exact=user)
    except:
        return HttpResponseRedirect("/profile/")
    try:
        owner_member = Member.objects.get(user__exact=request.user)
    except:
        owner_member = None
    if request.method == 'POST':
        print "++++++++++++++++++++++++method post before try"
        try:
            print "++++++++++++++++++++++++method post after try"
            post_add_form = PostAddForm(request.POST)
            form = post_add_form.save(commit=False)
            form.member = request.user.members
            form.member_to = member
            form.save()
            print "+++++++++++++++loop starts"
            print "+++++++++++++++loop ends"
            post_history = History(user = request.user.members, item_type = 'POST', item_id = form.id)
            post_history.save()
        except:
            pass
    
    posts = Post.objects.order_by('-timestamp').filter(member_to=member)
    home_feed = []
    for post in posts:
        print 'post: ', post
        test = {}
        test['owner_member'] = post.member
        test['type'] = "POST"
        test['item_id'] = post.id
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
        test['parent_activity'] = post
        test['upvotes_number'] = post.upvotes_number
        test['downvotes_number'] = post.downvotes_number
        test['comments_number'] = post.comments_number
        print 'home_feed inside loop: ', home_feed
        home_feed.append(test)
    print 'home_feed: ', home_feed
    post_add_form = PostAddForm()
    template_dict = {
            'error': '',
            'member': member,
            'owner_member': owner_member,
            'profile_user': user,
            'posts': posts,
            'post_add_form': post_add_form,
            'home_feed': home_feed,
    }
    return render_to_response('user_pages/profile/profile_view.html',
        template_dict, context_instance=RequestContext(request))


@login_required
def search_members(request):
    if request.GET and request.GET['q']:
        search_string = request.GET['q']
    else:
        pass
    try:
        matching_users = User.objects.filter(
            Q(first_name__contains=search_string) |
            Q(last_name__contains=search_string) |
            Q(username__contains=search_string)
            
        ).exclude(is_superuser=True)
    except:
        return HttpResponseRedirect("/login/")

    member = Member.objects.get(user__exact=request.user)
    template_dict = {
            'error': '',
            'member': member,
            'matching_users': matching_users,
    }

    return render_to_response('user_pages/search/search_members.html',
        template_dict, context_instance=RequestContext(request))



@login_required
def friend_add(request):
    if request.GET['username']:
        friend_username = request.GET['username']
        try:
            friend = User.objects.get(
                username__exact = friend_username
            )
        except:
            friend = None
            return HttpResponseRedirect("/profile/")
        print "friend"
        print friend
        if friend is not None:
            try:
                existing_relation = MemberRelations.objects.get(
                    (
                        Q(member_who_added = request.user.members) &
                        Q(member_who_was_added = friend.members)
                    )|
                    (
                        Q(member_who_added = friend.members) &
                        Q(member_who_was_added = request.user.members)
                    ) 
                )
            except:
                existing_relation = None
            print "existin_relation"
            print existing_relation
            if existing_relation is None:
                member_relation = MemberRelations(
                    member_who_added = request.user.members,
                    member_who_was_added = friend.members
                )
                member_relation.save()
            else:
                print existing_relation
            return HttpResponseRedirect("/profile/"+friend_username)
    return HttpResponseRedirect("/profile/")


@login_required
def friend_accept(request):
    if request.GET['username']:
        friend_username = request.GET['username']
        try:
            friend = User.objects.get(username__exact=friend_username)
        except:
            friend = None
        try:
            friend_relation = MemberRelations.objects.get(
                Q(member_who_added__exact = friend.members) &
                Q(member_who_was_added__exact = request.user.members)

            )
        except:
            return HttpResponseRedirect("/profile/")
        friend_relation.active = True
        friend_relation.save()
        new_hist=History()
        new_hist.user=request.user.members
        new_hist.item_type="FRIEND"
        new_hist.timestamp=datetime.datetime.now()
        new_hist.item_id=friend_relation.id
        new_hist.save()
        next_hist=History()
        next_hist.user=friend.members
        next_hist.item_type="FRIEND"
        next_hist.timestamp=datetime.datetime.now()
        next_hist.item_id=friend_relation.id
        next_hist.save()
        return HttpResponseRedirect("/notifications/")
    return HttpResponseRedirect("/profile/")


@login_required
def friend_delete(request):
    if request.GET['username']:
        friend_username = request.GET['username']
        try:
            friend = User.objects.get(username__exact=friend_username)
            print friend
        except:
            friend = None
        try:
            friend_relation = MemberRelations.objects.get(
                (
                    Q(member_who_added = request.user.members) &
                    Q(member_who_was_added = friend.members)
                )|
                (
                    Q(member_who_added = friend.members) &
                    Q(member_who_was_added = request.user.members)
                )
            )
        except:
            return HttpResponseRedirect("/profile/")
        friend_relation.delete()
        if 'page' in request.GET:
            if request.GET['page'] == 'notifications':
                return HttpResponseRedirect("/notifications/")
            if request.GET['page'] == 'friends':
                return HttpResponseRedirect("/friends/")

        return HttpResponseRedirect("/profile/"+friend_username)
    return HttpResponseRedirect("/profile/")


@login_required
def notifications(request):

    member = Member.objects.get(user__exact=request.user)
    member_relations = MemberRelations.objects.filter(
        Q(member_who_was_added=member) &
        Q(active=False)
    )

    template_dict = {
            'error': '',
            'member': member,
            'pending_requests': member_relations

    }
    return render_to_response('user_pages/notifications/notifications.html',
        template_dict, context_instance=RequestContext(request))

@login_required
def friends(request):

    member = Member.objects.get(user__exact=request.user)
    member_relations = MemberRelations.objects.filter(
        ( 
            Q(member_who_added = request.user.members) |
            Q(member_who_was_added = request.user.members) 
        ) &
        Q(active = True)
    )
    friends_list = []
    for relation in member_relations:
        if relation.member_who_added == member:
            friend = relation.member_who_was_added
        else:
            friend = relation.member_who_added
        friends_list.append(friend)



    template_dict = {
            'error': '',
            'friends': friends_list,
            'member': member

    }
    return render_to_response('user_pages/notifications/friends.html',
        template_dict, context_instance=RequestContext(request))

