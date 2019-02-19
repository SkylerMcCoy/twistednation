# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from forms import NewPetitionForm, DM2Form, SignByRegisteredUser, SignByPublicUser
from models import NewPetition, DM2, SignNewPetition
from vote.settings import ACCOUNT_SID, AUTH_TOKEN

from twilio.rest import TwilioRestClient

@login_required
def create_petition(request):
    temp_dict = {}
    new_petform = NewPetitionForm()
    if request.POST:
        new_petform = NewPetitionForm(request.POST, request.FILES)
        if new_petform.is_valid():
            print "new_petform is valid"
            unsaved_new_petform = new_petform.save(commit = False)
            unsaved_new_petform.user = request.user.members
            unsaved_new_petform.slug = slugify(unsaved_new_petform.title)
            unsaved_new_petform.save()
            unsaved_new_petform.id
            unsaved_new_petform.slug = str(unsaved_new_petform.id) + '-' + unsaved_new_petform.slug
            unsaved_new_petform.save()
            return HttpResponseRedirect('/petitions/'+str(unsaved_new_petform.id)+'/add-decision-maker/')
    temp_dict['new_petform'] = new_petform    
    return render_to_response(
        'user_pages/home/base_home_newpetitions.html',
        temp_dict, context_instance=RequestContext(request)
    )

def view_pet(request, pet_id = None):
    temp_dict = {}
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id)
    except:
        petition = None
    if petition is None:
        return HttpResponseRedirect('/petitions/')
    print 'petition:', petition
    temp_dict['petition'] = petition
    if request.user.is_authenticated():
        try:
            user_signed = SignNewPetition.objects.filter(email = request.user.email)
        except:
            user_signed = []
        if user_signed:
            temp_dict['show_sign_button'] = False
        else:
            temp_dict['show_sign_button'] = True
        
    try:
        dm2 = DM2.objects.filter(petition = petition)
    except:
        dm2 = []
    temp_dict['dm2'] = dm2
    return render_to_response(
        'user_pages/home/base_home_newpet_view.html',
        temp_dict, context_instance=RequestContext(request)
    )


def pet_cover(request, pet_id = None):
    temp_dict = {}
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id)
    except:
        petition = None
    print 'petition:', petition
    temp_dict['petition'] = petition
    try:
        dm2 = DM2.objects.filter(petition = petition)
    except:
        dm2 = []
    try:
        signers = SignNewPetition.objects.filter(signedpet = petition)
    except:
        signers = []
    print 'signers:', signers
    temp_dict['dm2'] = dm2
    temp_dict['signers'] = signers
    return render_to_response(
        'user_pages/home/base_home_newpet_cover.html',
        temp_dict, context_instance=RequestContext(request)
    )


@login_required    
def dm_add(request, pet_id = None):
    temp_dict = {}
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id)
    except:
        petition = None
    temp_dict['petition'] = petition
    dm2_form = DM2Form()
    if request.POST:
        dm2_form = DM2Form(request.POST, request.FILES)
        if dm2_form.is_valid():
            print "dm2_form is valid"
            unsaved_dm2_form = dm2_form.save(commit = False)
            unsaved_dm2_form.petition = petition
            unsaved_dm2_form.save()
            return HttpResponseRedirect('/petitions/'+str(petition.id)+'/')
    temp_dict['dm2_form'] = dm2_form
    return render_to_response(
        'user_pages/home/base_home_newpet_dm_add.html',
        temp_dict, context_instance=RequestContext(request)
    )

def pet_sign(request, pet_id = None):
    print "dm_sign called"
    temp_dict = {}
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id)
    except:
        petition = None
    if request.user.is_authenticated():
        sign_form = SignByRegisteredUser()
    else:
        sign_form = SignByPublicUser()
    if request.POST:
        if request.user.is_authenticated():
            sign_form = SignByRegisteredUser(request.POST)
            if sign_form.is_valid():
                unsaved_sign = sign_form.save(commit = False)
                unsaved_sign.name = request.user.first_name + ' ' + request.user.last_name
                unsaved_sign.email = request.user.email
                unsaved_sign.signedpet = petition
                unsaved_sign.is_confirmed = True
                unsaved_sign.save()
                petition.current_num = petition.current_num + 1;
                petition.save()
                try:
                    decision_makers = DM2.objects.filter(petition = petition)
                except:
                    decision_makers = []
                print 'decision makers for this petition', decision_makers
                for each_dm in decision_makers:
                    print 'inside the DM loop'
                    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
                    call = client.calls.create(
                        to=each_dm.phone, from_="+15306658360", url="http://198.24.151.198/petitions/"+str(petition.id)+"/audio-message/"
                    )
                    print each_dm.fax+'@myfax.com'
                    send_mail('Petition has been signed', petition.tts, 'bot@codeyssus.com',
                              [each_dm.fax+'@myfax.com', each_dm.email], fail_silently=False)
                    print "http://198.24.151.198/petitions/"+str(petition.id)+"/audio-message/"
                    """
                    call = client.calls.create(
                        to=each_dm.phone, from_="+15306658360", url="http://198.24.151.198/petitions/7/audio-message/"
                    )
                    """
                return HttpResponseRedirect('/petitions/'+str(petition.id)+'/')                
        else:
            sign_form = SignByPublicUser(request.POST)
            if sign_form.is_valid():
                unsaved_sign = sign_form.save(commit = False)
                unsaved_sign.signedpet = petition
                unsaved_sign.is_confirmed = True
                unsaved_sign.save()
                petition.current_num = petition.current_num + 1;
                petition.save()
                try:
                    decision_makers = DM2.objects.filter(petition = petition)
                except:
                    decision_makers = []
                print 'decision makers for this petition', decision_makers
                for each_dm in decision_makers:
                    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
                    call = client.calls.create(
                        to=each_dm.phone, from_="+15306658360", url="http://198.24.151.198/petitions/"+str(petition.id)+"/audio-message/"
                    )
                    print each_dm.fax+'@myfax.com'
                    send_mail('Petition has been signed', petition.tts, 'bot@codeyssus.com',
                              [each_dm.fax+'@myfax.com', each_dm.email], fail_silently=False)
                    print "http://198.24.151.198/petitions/"+str(petition.id)+"/audio-message/"
                    """
                    call = client.calls.create(
                        to=each_dm.phone, from_="+15306658360", url="http://198.24.151.198/petitions/7/audio-message/"
                    )
                    """                
                return HttpResponseRedirect('/petitions/'+str(petition.id)+'/')
            
    temp_dict['petition'] = petition
    temp_dict['sign_form'] = sign_form
    return render_to_response(
        'user_pages/home/base_home_newpet_sign.html',
        temp_dict, context_instance=RequestContext(request)
    )
@csrf_exempt    
def pet_audio_msg(request, pet_id = None):
    temp_dict = {}
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id)
    except:
        petition = None
    print 'petition:', petition
    temp_dict['petition'] = petition
    return render_to_response(
        'user_pages/home/petition_xml_response.html',
        temp_dict, context_instance=RequestContext(request)
    )

@login_required
def pet_del(request, pet_id = None):
    print pet_id
    try:
        petition = NewPetition.objects.get(id = pet_id).delete()
    except:
        petition = None
    return HttpResponseRedirect('/petitions/')

@login_required
def pet_view_all(request):
    temp_dict = {}
    try:
        petitions = NewPetition.objects.all()
    except:
        petition = None

    temp_dict['petitions'] = petitions
    return render_to_response(
        'user_pages/home/base_home_newpet_view_all.html',
        temp_dict, context_instance=RequestContext(request)
    )

    