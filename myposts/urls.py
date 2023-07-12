"""from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import(
		index, 
		blog,
		search, 
		sort_by_category,
		post_detail,
		post_create,
		post_update,
		#PostUpdateView,
		post_delete
		#PostDeleteView
	) 


app_name = 'myposts'

handler404 = views.handler404 
handler500 = views.handler500

urlpatterns = [
	path('', index, name = 'index'),
	path('blog/', blog, name = 'post-list'),
	path('search/', search, name = 'search'),
	path('category/', sort_by_category, name = 'category'),
	path('post/<int:id>/', post_detail, name = 'post-detail'),
	path("create/", post_create, name ='post-create'),
	path("post/<int:id>/update", post_update, name = 'post-update'),
	path("post/<int:id>/delete", post_delete, name = 'post-delete')
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import (
    index,
    search,
    blog,
    sort_by_category,
    data_deletion,
    #post_detail,
    #post_create,
    #post_update,
    #post_delete,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

app_name = 'myposts'


urlpatterns = [
    path('', index, name = 'index'),
    path('blog/', blog, name='post-list'),
    path('search/', search, name='search'),
    #path('category/', sort_by_category, name = 'category'),
    path('category/<category>', sort_by_category, name = 'category'),
    # path('create/', post_create, name='post-create'),
    path('data-deletion', data_deletion, name='data-deletion'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]