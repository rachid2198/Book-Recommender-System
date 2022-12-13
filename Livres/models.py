from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    nom=models.CharField(primary_key=True,max_length=40)
    def __str__(self):
        return self.nom

class Auteur(models.Model):
    nom=models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nom

class Livre(models.Model):
    titre=models.CharField(max_length=200)
    image = models.ImageField(upload_to='livre_image',null=True, blank=True)
    image_livre = models.CharField(max_length=1000, null=True, blank=True)
    editeur= models.CharField(max_length=200, null=True, blank=True)
    nombre_pages = models.IntegerField(null=True, blank=True)
    date_parution= models.DateField(null=True, blank=True)
    anee_parution=models.IntegerField(null=True)
    date_ajout = models.DateTimeField(auto_now_add=True , null=True)
    genres = models.ManyToManyField(Genre ,related_name='livres')
    auteurs= models.ManyToManyField(Auteur ,related_name='livres', blank=True)
    limite_age=models.IntegerField(max_length=200, null=True, blank=True)
    desctiption = models.CharField(max_length=2000, null=True)
    langue=models.CharField(max_length=200, null=True, blank=True)
    public_cible=models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        tt =self.titre
        return tt

class Note(models.Model):
    note = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        u=self.livre.titre
        return u



class Langue(models.Model):
    nom = models.CharField(max_length=50)
    def __str__(self):
        l=self.nom
        return l

class Profil(models.Model):
    age = models.IntegerField()
    pays = models.CharField(max_length=50)
    specialite =models.CharField(max_length=100,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    langues = models.ManyToManyField(Langue,related_name='profils')
    genre =models.ManyToManyField(Genre,related_name='profils',null=True)
    def __str__(self):
        u=self.user.username
        return u

class Comment(models.Model):
    contenue=models.CharField(max_length=5000 ,null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)
    note=models.IntegerField(null=True)


class Favoris(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class aLirePlusTard(models.Model):
    date = models.DateTimeField(auto_now_add=True, null=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)




##########################test#############################

class BX_Books(models.Model):
    ISBN=models.CharField(max_length=200,null=True)
    def __str__(self):
        tt =self.ISBN
        return tt

class BX_Users(models.Model):
    User_ID = models.IntegerField( null=True)
    def __str__(self):
        u=self.User_ID
        return u

class BX_Book_Ratings(models.Model):
    Book_Rating = models.IntegerField()
    ISBN = models.CharField(max_length=200,null=True)
    User_ID = models.IntegerField()
    def __str__(self):
        u=self.User_ID
        return u