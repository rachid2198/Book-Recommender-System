from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from .models import Livre, Auteur, Genre,Note,Profil,Langue,BX_Book_Ratings,BX_Users,BX_Books,Comment,aLirePlusTard,Favoris
from .recommander.recommander2 import get_predict_list,get_demogrephic_list
from django.contrib.auth.models import User
from django.db.models import F,Aggregate,Avg
import math
from django.contrib.auth import authenticate
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.db.models import F,Avg,Aggregate,Count
import datetime


# end import

def saveInfos(request,type):
  if(type=="rating"):
    user = User.objects.get(username=request.POST["user"])
    livre = Livre.objects.get(id=request.POST["book"])
    note = Note.objects.filter(user=user, livre=livre)
    if note:
        user_note = Note.objects.get(user=user, livre=livre)
        user_note.note = request.POST["note"]
        user_note.save()
    else:
        user_note = Note(livre=livre, user=user, note=request.POST["note"])
        user_note.save()
  elif (type == "favoris"):
      user = User.objects.get(id=request.POST["user"])
      livre = Livre.objects.get(id=request.POST["book"])
      in_favoris = Favoris.objects.filter(user=user, livre=livre)
      if in_favoris:
          instance = Favoris.objects.get(user=user, livre=livre)
          instance.delete()
      else:
          instance = Favoris(livre=livre, user=user)
          instance.save()
  else:
      user = User.objects.get(id=request.POST["user"])
      livre = Livre.objects.get(id=request.POST["book"])
      in_aLirePlusTard = aLirePlusTard.objects.filter(user=user, livre=livre)
      if in_aLirePlusTard:
          instance = aLirePlusTard.objects.get(user=user, livre=livre)
          instance.delete()
      else:
          instance = aLirePlusTard(livre=livre, user=user)
          instance.save()




def get_genre():
    genres = Genre.objects.all()
    return genres

def get_auters():
    auteurs = Auteur.objects.all()
    return auteurs


def profile(request):
  langues=Langue.objects.all()
  genres=Genre.objects.all()
  a_lire = aLirePlusTard.objects.filter(user=request.user).order_by('-date')[:5]
  favoris = Favoris.objects.filter(user=request.user)[:5]
  if request.POST:
    profil=Profil.objects.get(user=request.user)
    profil.age=request.POST['age']
    profil.pays = request.POST['pays']
    profil.specialite = request.POST['specialite']
    profil.langues.clear()
    profil.genre.clear()
    for langue in request.POST.getlist('langueList'):
        profil.langues.add(Langue.objects.get(nom=langue))
    for genre in request.POST.getlist('genreList'):
        profil.genre.add(Genre.objects.get(nom=genre))
    profil.save()
  else:
    user=request.user
    profil=Profil.objects.get(user=user)
  return render(request,'recommandation/profile.html',{"profil":profil,"alire":a_lire,"Favoris":favoris,"langues":langues,"genres":genres})


def home(request):
    return render(request, 'recommandation/home.html')

def best_ratings(request):
    livres_list = Livre.objects.all().order_by('date_ajout')
    rating_sum = {}
    for livre in livres_list:
        sum = Note.objects.filter(livre=livre, note__gt=0.0).values('livre_id', 'note').aggregate(avg=Avg('note'))
        if sum['avg']:
            rating_sum[livre.id] = sum['avg']

    sorted_rating_sum = sorted(rating_sum.items(), key=lambda t: t[1], reverse=True)
    top_dict = dict(sorted_rating_sum[:5])
    top_dict_all = dict(sorted_rating_sum)
    top_livres = Livre.objects.filter(pk__in=top_dict)
    top_livres_all = Livre.objects.filter(pk__in=top_dict_all)

    results_found = True
    if request.POST:
        user = User.objects.get(username=request.POST["user"])
        livre = Livre.objects.get(id=request.POST["book"])
        note = Note.objects.filter(user=user, livre=livre)
        if note:
            user_note = Note.objects.get(user=user, livre=livre)
            user_note.note = request.POST["note"]
            user_note.save()
        else:
            user_note = Note(livre=livre, user=user, note=request.POST["note"])
            user_note.save()
    elif request.GET:
        query = request.GET.get('query')
        if not query:
            livres_exist = Livre.objects.filter(pk__in=top_dict_all)
        else:
            # title contains the query and query is not sensitive to case.
            livres_exist = Livre.objects.filter(titre__icontains=query)
        if not livres_exist.exists():
            results_found = False
        else:
            livres_list = top_livres_all

    paginator = Paginator(livres_list, 5)
    page = request.GET.get('page')

    try:
        livres = paginator.page(page)
    except PageNotAnInteger:
        livres = paginator.page(1)
    except EmptyPage:
        livres = paginator.page(paginator.num_pages)


    context = {
        'livres': livres,
        'results_found': results_found,
        'top_livres':top_livres
    }


    return render(request, 'recommandation/index.html', context)

def plus_note():
    livres = Note.objects.annotate(num=Count('user')).order_by('num')[:10]
    return livres

def mieux_notee():
    livres_list = Livre.objects.all().order_by('date_ajout')
    rating_sum = {}
    for livre in livres_list:
        sum = Note.objects.filter(livre=livre, note__gt=0.0).values('livre_id', 'note').aggregate(avg=Avg('note'))
        if sum['avg']:
            rating_sum[livre.id] = sum['avg']

    sorted_rating_sum = sorted(rating_sum.items(), key=lambda t: t[1], reverse=True)
    top_dict = dict(sorted_rating_sum[:10])
    top_livres = Livre.objects.filter(pk__in=top_dict)
    return top_livres

def favoris(request):
    favoris= Favoris.objects.filter(user=request.user)
    if request.POST:
        saveInfos(request, request.POST["type"])

    context={
        'favoris':favoris
    }
    return render(request,'recommandation/list_favoris.html',context)

def list_note(request):
    notes = Note.objects.filter(user=request.user)
    if request.POST:
        saveInfos(request, request.POST["type"])

    context={
        'notes':notes
    }
    return render(request,'recommandation/list_note.html',context)

def a_lire(request):
    a_lire= aLirePlusTard.objects.filter(user=request.user)
    if request.POST:
        saveInfos(request, request.POST["type"])

    context={
        'a_lire':a_lire
    }
    return render(request,'recommandation/list_a_lire.html',context)


def index(request):
    livres_list = Livre.objects.all().order_by('-date_ajout')
    results_found = True
    if request.POST:
        saveInfos(request, request.POST["type"])


    elif request.GET:
        if ("type" in request.GET.keys()):

            if (request.GET["type"] == "search"):
                query = request.GET.get('query')
                if not query:
                    livres_exist = Livre.objects.all().order_by('date_ajout')
                else:
                    # title contains the query and query is not sensitive to case.
                    livres_exist = Livre.objects.filter(titre__icontains=query)
                if not livres_exist.exists():
                    results_found = False
                else:
                    livres_list = livres_exist
            elif (request.GET["type"] == "auteur"):
                author = Auteur.objects.get(id=request.GET["nom_auteur"])
                livres_list = author.livres.all()
            else:
                genre = Genre.objects.get(nom=str(request.GET["nom_genre"]))
                livres_list = genre.livres.all()

    paginator = Paginator(livres_list, 10)
    page = request.GET.get('page')

    try:
        livres = paginator.page(page)
    except PageNotAnInteger:
        livres = paginator.page(1)
    except EmptyPage:
        livres = paginator.page(paginator.num_pages)
    context = {
        'livres': livres,
        'results_found': results_found,
        'top_livres':mieux_notee(),
        'plus_note':plus_note(),
        'genres':get_genre()
    }
    return render(request, 'recommandation/index.html', context)




def detail(request, livre_id):
    livre_detail = get_object_or_404(Livre, pk=livre_id)
    comments = Comment.objects.filter(livre=livre_id).order_by('-date')

    if request.POST:
        if request.POST["type"] == "comment":
            user = User.objects.get(username=request.POST["user"])
            livre = Livre.objects.get(id=request.POST["book"])
            user_comment = Comment(livre=livre, user=user, date=datetime.datetime.now(), contenue=request.POST["contenue"], note=request.POST["note"])
            user_comment.save()
        else:
            saveInfos(request, request.POST["type"])

    context = {
        'livre': livre_detail,
        'top_livres': mieux_notee(),
        'plus_note': plus_note(),
        'genres': get_genre(),
        'comments':comments
    }

    return render(request, 'recommandation/detail.html', context)


def livre_par_genres(request,genre_nom):
    genre = Genre.objects.get(nom=genre_nom)
    livres_list = genre.livres.all()

    results_found = True
    if request.POST:
        saveInfos(request, request.POST["type"])
    elif request.GET:
        if ("type" in request.GET.keys()):

            if (request.GET["type"] == "search"):
                query = request.GET.get('query')
                if not query:
                    livres_exist = Livre.objects.all().order_by('date_ajout')
                else:
                    # title contains the query and query is not sensitive to case.
                    livres_exist = Livre.objects.filter(titre__icontains=query)
                if not livres_exist.exists():
                    results_found = False
                else:
                    livres_list = livres_exist


    paginator = Paginator(livres_list, 10)
    page = request.GET.get('page')

    try:
        livres = paginator.page(page)
    except PageNotAnInteger:
        livres = paginator.page(1)
    except EmptyPage:
        livres = paginator.page(paginator.num_pages)
    context = {
        'livres': livres,
        'results_found': results_found,
        'top_livres': mieux_notee(),
        'plus_note': plus_note(),
        'genres': get_genre()
    }
    return render(request, 'recommandation/index.html', context)

def livre_par_auteur(request,auteur_id):
    auteur = Auteur.objects.get(id=auteur_id)
    livres_list = auteur.livres.all()
    results_found = True
    if request.POST:
        saveInfos(request, request.POST["type"])
    elif request.GET:
        if ("type" in request.GET.keys()):

            if (request.GET["type"] == "search"):
                query = request.GET.get('query')
                if not query:
                    livres_exist = Livre.objects.all().order_by('date_ajout')
                else:
                    # title contains the query and query is not sensitive to case.
                    livres_exist = Livre.objects.filter(titre__icontains=query)
                if not livres_exist.exists():
                    results_found = False
                else:
                    livres_list = livres_exist


    paginator = Paginator(livres_list, 10)
    page = request.GET.get('page')

    try:
        livres = paginator.page(page)
    except PageNotAnInteger:
        livres = paginator.page(1)
    except EmptyPage:
        livres = paginator.page(paginator.num_pages)
    context = {
        'livres': livres,
        'results_found': results_found,
        'top_livres': mieux_notee(),
        'plus_note': plus_note(),
        'genres': get_genre()
    }
    return render(request, 'recommandation/index.html', context)


    return HttpResponse(genre_nom)



# ------------------------------------------------systeme de recommanadtion----------------------------------------------------------------------------
# ------------------------------------------------filtrage collab-----------------------------------------------------------------
def recommandation(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    predict_list = get_predict_list(request.user)
    demographic_liste=get_demogrephic_list(request.user)
#hybridation mixed
    for item in demographic_liste.keys():
        if item not in predict_list:
            predict_list.append(item)
    livres = Livre.objects.filter(pk__in=predict_list)
    context = {
        'livres': livres,
        'top_livres': mieux_notee(),
        'plus_note': plus_note(),
        'genres': get_genre()

    }

    return render(request, 'recommandation/recommandation.html', context)






# ------------------------------------------------ici fin filtrage collab----------------------------------------------------------

# ------------------------------------------------ici fin systeme de recommanadtion----------------------------------------------------------------------------































