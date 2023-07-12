from django.urls import path

from gallery.views import gallery_view #ImageView, ImageList, AlbumView, AlbumList, ImageCreate

app_name = 'gallery'
urlpatterns = [
    path('', gallery_view, name="gallery")
    #path('', AlbumList.as_view(), name='album_list'),
    #path('images/', ImageList.as_view(), name='image_list'),
    #path('image/<int:pk>/<slug>', ImageView.as_view(), name='image_detail'),
    #path('upload/', ImageCreate.as_view(), name='image_upload'),
    #path('album/<int:pk>/<slug>/', AlbumView.as_view(), name='album_detail'),
    #path('album/<int:apk>/<int:pk>/<slug>', ImageView.as_view(), name='album_image_detail'),
]
