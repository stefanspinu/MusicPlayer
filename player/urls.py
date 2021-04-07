from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:song_id>/', views.detail, name='detail'),
    path('my_music/', views.my_music, name='my_music'),
    path('playlists/', views.playlists, name='playlists'),
    path('playlists/<str:name>/', views.playlist_songs, name='playlist_songs'),
    path('favourite/', views.favourite, name='favourite'),
    path('albums/', views.albums, name='albums'),
    path('albums/<str:name>/', views.albums_songs, name='albums_songs'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('recent/', views.recent, name='recent'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('play_song/<int:song_id>/', views.play_song_index, name='play_song_index'),
    path('play_recent_song/<int:song_id>/',
         views.play_recent_song, name='play_recent_song'),
]
