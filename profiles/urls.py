from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import profile_view, get_author

app_name = 'profiles'

urlpatterns = [
	path('profile/', profile_view, name = 'user-profile'),
	path('profile/<pk>/', get_author, name = 'get-author'),
	#path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
]
