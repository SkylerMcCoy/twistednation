from django.forms import ModelForm
from posts.models import Post

class PostAddForm(ModelForm):
    class Meta:
        model = Post
        fields = ('content',)
    