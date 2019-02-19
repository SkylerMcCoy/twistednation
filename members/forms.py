from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from members.models import Member
 
class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",)

class ProfileEditForm(ModelForm):
    class Meta:
        model = Member
        exclude = ('user',)
    