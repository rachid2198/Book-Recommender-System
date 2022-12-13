from django.urls import path,include
from django.conf.urls import url,include
from . import views
from django.conf import settings
app_name="Livres"


urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index , name='index'),
    path('home/', views.home , name='home'),
    path('genre/<str:genre_nom>/', views.livre_par_genres, name='genre_livre'),
    url(r'^(?P<livre_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^auteur/(?P<auteur_id>[0-9]+)/$', views.livre_par_auteur, name='livre_par_auteur'),
    url(r'^recommandation/$', views.recommandation, name='recommandation'),
    url(r'^best_ratings/$', views.best_ratings, name='best_ratings'),
    path('favoris/', views.favoris, name='favoris'),
    path('a_lire/', views.a_lire, name='a_lire'),
    path('livres_note/', views.list_note, name='list_note'),
    path('profile/', views.profile, name='profile'),
    path('pls/', views.plus_note, name='pls'),
]


