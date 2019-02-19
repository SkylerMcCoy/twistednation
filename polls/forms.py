from django.forms import ModelForm
from polls.models import Poll, Choice

class PollCreateForm(ModelForm):
    class Meta:
        model = Poll
        exclude = ('member', 'timestamp', 'comments_number', 'upvotes_number', 'upvoted_by', 'downvotes_number', 'downvoted_by', 'choice_votes_no',)

class PollChoicesCreateForm(ModelForm):
    class Meta:
        model = Choice
        exclude = ('poll', 'member', 'votes_number', 'voted_by',)

    