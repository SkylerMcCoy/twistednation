from django import forms
from models import NewPetition, DecisionMaker, PetitionType, DM2, SignNewPetition

class NewPetitionForm(forms.ModelForm):
    deadline = forms.DateField(
        widget = forms.DateInput(
            attrs = {'class':'datepicker'},
            format = "%m/%d/%Y"
        )
    )
    target_entity = forms.ChoiceField(
    )
    petition_type = forms.ChoiceField(
    )
    
    def __init__(self, *args, **kwargs):
        super(NewPetitionForm, self).__init__(*args, **kwargs)
        self.fields['target_entity'] = forms.ChoiceField(
            choices = [ (o.id, o.name) for o in DecisionMaker.objects.all()]
        )
        self.fields['petition_type'] = forms.ChoiceField(
            choices = [ (o.id, o.title) for o in PetitionType.objects.all()]
        )
    
    class Meta:
        model = NewPetition
        fields = ('title', 'body', 'deadline', 'target_no_signs', 'petition_type', 'target_entity', 'tts', )
        
class DM2Form(forms.ModelForm):
    
    class Meta:
        model = DM2
        exclude = ('petition',)


class SignByRegisteredUser(forms.ModelForm):
    
    class Meta:
        model = SignNewPetition
        exclude = ('name', 'email', 'signedpet', 'is_confirmed',)

class SignByPublicUser(forms.ModelForm):
    
    class Meta:
        model = SignNewPetition
        exclude = ('signedpet', 'is_confirmed',)