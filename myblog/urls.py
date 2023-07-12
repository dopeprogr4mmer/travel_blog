"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from allauth.account import views as allauth_views
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from filebrowser.sites import site

handler404 = 'myposts.views.handler404'
handler500 = 'myposts.views.handler500'

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/filebrowser/', site.urls),
	path('tinymce/',include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/login/', allauth_views.LoginView.as_view(template_name='login.html'), name='account_login'),
    path('', include('newsletter.urls', namespace = 'signups')),
    path('',include('myposts.urls', namespace = 'myposts')),
    path('',include('profiles.urls', namespace ='profiles')),
    path('',include('weatherapp.urls', namespace='weatherapp')),
    path('gallery/', include('gallery.urls')),
    path('',include('contactus.urls', namespace='contactus'))
]