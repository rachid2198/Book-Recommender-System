from django import template
from django.contrib.auth.models import User
from Livres.models import Livre,Note,Favoris,aLirePlusTard
from django.db.models import F,Avg,Aggregate
register = template.Library()

@register.simple_tag
def get_obj(liv, user):
    objs = Note.objects.filter(user=user,livre=liv)
    if objs:
        obj = Note.objects.get(user=user,livre=liv).note
        return obj
    return 0

@register.simple_tag
def in_Favoris(liv, user):
    objs = Favoris.objects.filter(user=user,livre=liv)
    if objs:
        return 1
    return 0

@register.simple_tag
def in_aLirePlusTard(liv, user):
    objs = aLirePlusTard.objects.filter(user=user,livre=liv)
    if objs:
        return 1
    return 0
