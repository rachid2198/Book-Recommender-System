from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView,View
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from Livres.models import Profil, Langue, Genre
from  .forms import SignUpForm,SignInForm

class SignUpFormView(View):
    form_class=SignUpForm
    def get(self,request):
        not_used_email = False
        correct_repeat = False
        username_not_taken=False
        email=""
        password=""
        username=""
        genres = Genre.objects.all()
        langues = Langue.objects.all()
        form = self.form_class(None)
        return render(request, 'signup.html', {'form': form,"correct_repeat":correct_repeat,
                                               "not_used_email":not_used_email,"username_not_taken":username_not_taken,
                                                "email":email,"password":password,"username":username,"genres":genres,"langues":langues})
    def post(self,request):
        not_used_email=True
        correct_repeat=True
        username_not_taken=True
        form=self.form_class(request.POST)
        if not User.objects.filter(email=request.POST['email']):
                 not_used_email=False
        if request.POST['password'] == request.POST['repeatpassword']:
                 correct_repeat=False
        #correct_repeat = False
        if not User.objects.filter(username=request.POST['username']):
                username_not_taken=False
        if (not not_used_email) & (not correct_repeat) & (not username_not_taken):
                 user = form.save(commit=False)
                 username=form.cleaned_data['username']
                 raw_password=form.cleaned_data['password']
                 user.set_password(raw_password)
                 user.save()
                 user=authenticate(request,username=username,password=raw_password)
                 if user is not None:
                   if user.is_active:
                       login(request,user)
                       profil=Profil.objects.create(specialite=request.POST['specialité'],age=request.POST['age'],pays=request.POST['pays'],user=user)
                       for langue in request.POST.getlist('languageList'):
                         profil.langues.add(Langue.objects.get(nom=langue))
                       for genre in request.POST.getlist('genreList'):
                         profil.genre.add(Genre.objects.get(nom=genre))
                       profil.save()
                       return redirect('Livres:index')
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        return render(request,'signup.html',{'form': form,"correct_repeat":correct_repeat,
                                               "not_used_email":not_used_email,"username_not_taken":username_not_taken,
                                                "email":email,"password":password,"username":username})

class SignInFormView(View):
    error=True
    def get(self, request):
        self.error=False
        return render(request,'registration/login.html',{'error':self.error})
    def post(self,request):
        username = request.POST['username']
        raw_password = request.POST['password']
        user = authenticate(request,username=username, password=raw_password)
        if user is not None:
                self.error=False
                if user.is_active:
                    login(request, user)
                    return redirect('Livres:index')
        return render(request,'registration/login.html',{'error':self.error})
