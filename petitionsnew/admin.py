from django.contrib import admin
from petitionsnew.models import NewPetition, SignNewPetition, DecisionMaker, PetitionType, DM2

admin.site.register(NewPetition)
admin.site.register(SignNewPetition)
admin.site.register(DecisionMaker)
admin.site.register(PetitionType)
admin.site.register(DM2)
