from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import last_played_song, last_songs, save_to_database, detail_page_functionality, remove_song_from_playlist, remove_song_from_favourite, get_singers, get_languages, search_in_all_songs_page, get_songs_on_homepage
# Create your views here.


def home(request):

    recent_songs = last_songs(request)

    first_time = False

    last_played_song()

    songs = Song.objects.all()

    songs_on_home_page = get_songs_on_homepage()

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(
            Q(name__icontains=search_query)).distinct()
        context = {
            'last_played_song': last_played_song,
            'all_songs': filtered_songs,
            'query_search': True
        }
        return render(request, 'home.html', context)

    context = {
        'songs': songs_on_home_page,
        'recent_songs': recent_songs['recent_songs'],
        'last_played_song': last_played_song,
        'first_time': first_time,
        'query_search': False
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def play_song(request, song_id):
    save_to_database(request, song_id)
    return redirect('home')


@login_required(login_url='login')
def play_song_index(request, song_id):
    save_to_database(request, song_id)
    return redirect('all_songs')


@login_required(login_url='login')
def play_recent_song(request, song_id):
    save_to_database(request, song_id)
    return redirect('recent')


def all_songs(request):
    songs = Song.objects.all()

    first_time = False
    last_played_song()

    all_singers = get_singers()
    all_languages = get_languages()

    if len(request.GET) > 0:
        filtered_songs = search_in_all_songs_page(request, songs)

        context = {
            'songs': filtered_songs,
            'last_played_song': last_played_song,
            'all_singers': all_singers,
            'all_languages': all_languages,
            'query_search': True,
        }
        return render(request, 'all_songs.html', context)

    context = {
        'songs': songs,
        'last_played_song': last_played_song,
        'first_time': first_time,
        'all_singers': all_singers,
        'all_languages': all_languages,
        'query_search': False,
    }
    return render(request, 'all_songs.html', context=context)


def recent(request):

    last_played_song()

    recent_songs = last_songs(request)
    recent_songs_unsorted = recent_songs['recent_songs_unsorted']

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = recent_songs_unsorted.filter(
            Q(name__icontains=search_query)).distinct()
        context = {
            'recent_songs': filtered_songs,
            'last_played_song': last_played_song,
            'query_search': True
        }
        return render(request, 'recent.html', context)

    context = {
        'recent_songs': recent_songs['recent_songs'],
        'last_played_song': last_played_song,
        'query_search': False
    }
    return render(request, 'recent.html', context=context)


@login_required(login_url='login')
def detail(request, song_id):
    song = Song.objects.filter(id=song_id).first()

    save_to_database(request, song_id)

    last_played_song()

    playlists = Playlist.objects.filter(
        user=request.user).values('name').distinct
    is_favourite = Favourite.objects.filter(
        user=request.user).filter(song=song_id).values('is_fav')

    detail_page_functionality(request, song, song_id)

    context = {
        'last_played_song': last_played_song,
        'song': song,
        'playlists': playlists,
        'is_favourite': is_favourite
    }

    return render(request, 'detail.html', context)


def my_music(request):

    last_played_song()

    context = {'last_played_song': last_played_song}
    return render(request, 'mymusic.html', context)


def playlists(request):

    playlists = Playlist.objects.filter(
        user=request.user).values('name').distinct

    last_played_song()

    context = {
        'last_played_song': last_played_song,
        'playlists': playlists
    }
    return render(request, 'playlist.html', context)


def playlist_songs(request, name):

    songs = Song.objects.filter(
        playlist__name=name, playlist__user=request.user).distinct()

    remove_song_from_playlist(request, name)

    last_played_song()

    context = {
        'last_played_song': last_played_song,
        'name': name,
        'songs': songs
    }
    return render(request, 'playlist_songs.html', context)


def favourite(request):

    songs = Song.objects.filter(
        favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'Favourite songs - {songs}')

    remove_song_from_favourite(request)

    last_played_song()

    context = {
        'last_played_song': last_played_song,
        'songs': songs,
    }
    return render(request, 'favourite.html', context)


def albums(request):

    albums = Album.objects.values('name').distinct

    last_played_song()

    context = {
        'last_played_song': last_played_song,
        'albums': albums
    }
    return render(request, 'albums.html', context)


def albums_songs(request, name):

    songs = Song.objects.filter(album__name=name).distinct()

    last_played_song()

    context = {
        'last_played_song': last_played_song,
        'name': name,
        'songs': songs
    }
    return render(request, 'playlist_songs.html', context)
