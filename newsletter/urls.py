from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import fetch_signup_data

app_name = 'signups'

urlpatterns = [
	path('signups/', fetch_signup_data, name = 'signups'),
]
