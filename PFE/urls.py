"""PFE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='Livres/', permanent=False)),
    path('admin/', admin.site.urls ,name="admin"),
    path('Livres/', include('Livres.urls')),
    path('recom/', include('Livres.urls')),
    path('register/', views.SignUpFormView.as_view(), name="register"),
    path('login/', views.SignInFormView.as_view(), name='login'),
    path('logout/', auth_views.logout, {'next_page': '/login'}, name='logout'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
