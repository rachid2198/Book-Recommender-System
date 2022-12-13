from django.contrib import admin
from .models import Livre,Auteur,Genre,Note,Comment,Profil,Langue,BX_Users,BX_Books,BX_Book_Ratings,Favoris,aLirePlusTard



admin.site.register(Livre)
admin.site.register(Auteur)
admin.site.register(Genre)
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Profil)
admin.site.register(Langue)
admin.site.register(BX_Book_Ratings)
admin.site.register(Favoris)
admin.site.register(aLirePlusTard)