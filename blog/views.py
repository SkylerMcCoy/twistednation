# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
#from django.db.models import Q
from members.models import Member
from django.contrib.auth.decorators import login_required
from blog.forms import BlogEditForm
from blog.models import BlogPost
from history.models import History

@login_required
def blog_edit(request, blog_id = None):
    if request.user.is_authenticated():
        try:
            existing_member = Member.objects.get(user__exact=request.user)
        except:
            existing_member = None
        try:
			blog = BlogPost.objects.get(pk__exact=blog_id)
			if blog.member != request.user.members:
				return HttpResponseRedirect("/blog/")
        except:
            blog = None
        if request.method == 'POST':
        	print 'Posted'
        	print request.POST
        	form = BlogEditForm(request.POST, instance = blog )
	        if form.is_valid():
	            blog_post = form.save(commit=False)
	            blog_post.member = request.user.members
	            blog_post.save()
	            if blog_id == None:
	            	history = History(user = request.user.members, item_type = 'BLOG', item_id = blog_post.id)
	            	history.save()
	            return HttpResponseRedirect("/blog/"+str(blog_post.id)+"/")
	        else:
	        	print 'not valid'
        form = BlogEditForm(instance = blog )
        template_dict = {
            'error': '',
            'form' : form,
            'member': existing_member,
        }
        return render_to_response(
            'user_pages/blogs/blog_edit.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")

@login_required
def blog_view(request, blog_id = None):
    if request.user.is_authenticated():
        try:
			blog = BlogPost.objects.get(pk__exact=blog_id)
        except:
            blog = None
        template_dict = {
            'error': '',
            'blog' : blog,
        }
        return render_to_response(
            'user_pages/blogs/blog_view.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")

@login_required
def blog_view_all(request):
    if request.user.is_authenticated():
        try:
			blogs = BlogPost.objects.order_by('-timestamp').filter(member = request.user.members)
        except:
            blogs = None
        template_dict = {
            'error': '',
            'blogs' : blogs,
        }
        return render_to_response(
            'user_pages/blogs/blog_view_all.html',
            template_dict, 
            context_instance=RequestContext(request)
        )
    else:
        return HttpResponseRedirect("/login/")        