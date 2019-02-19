from django.forms import ModelForm, Textarea
from blog.models import BlogPost

class BlogEditForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('member', 'timestamp', 'comments_number', 'upvotes_number', 'upvoted_by', 'downvotes_number', 'downvoted_by',)
        widgets = {
        	'content': Textarea(attrs={'id': ''}),
		}

    