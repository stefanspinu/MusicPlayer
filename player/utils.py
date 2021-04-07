from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q


def last_played_song():
    last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(id=last_played_id)
    else:
        last_played_song = Song.objects.get(id=1)
    return last_played_song


def last_songs(request):
    context = {}
    if not request.user.is_anonymous:
        recent = list(Recent.objects.filter(
            user=request.user).values('song_id').order_by('-id'))
        recent_id = [each['song_id'] for each in recent][:5]
        recent_songs_unsorted = Song.objects.filter(
            id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(id=id))
        context = {
            'recent': recent,
            'recent_songs': recent_songs,
            'recent_id': recent_id,
            'recent_songs_unsorted': recent_songs_unsorted
        }
    else:
        recent = None
        recent_songs = None
        context = {
            'recent': recent,
            'recent_songs': recent_songs,
        }
    return context


def save_to_database(request, song_id):
    song = Song.objects.filter(id=song_id).first()
    if list(Recent.objects.filter(song=song, user=request.user).values()):
        data = Recent.objects.filter(song=song, user=request.user)
        data.delete()

    data = Recent(song=song, user=request.user)
    data.save()


def detail_page_functionality(request, song, song_id):
    if request.method == 'POST':
        if 'playlist' in request.POST:
            name = request.POST["playlist"]
            songg = Song.objects.filter(id=song_id)
            q, created = Playlist.objects.get_or_create(
                user=request.user, name=name)
            for s in songg:
                q.song.add(s)
            messages.success(
                request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=song, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', song_id=song_id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(
                user=request.user, song=song, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {song.id} - {song}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', song_id=song_id)


def remove_song_from_playlist(request, name):
    if request.method == 'POST':
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.get(
            name=name, user=request.user)
        if playlist_song.song.count() == 1:
            playlist_song.delete()
        else:
            playlist_song.song.remove(song_id)
            messages.success(
                request, 'Song removed from playlist!')


def remove_song_from_favourite(request):
    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(
            user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")


def get_singers():
    qs_singers = Song.objects.values_list('singer').all()
    s_list = [s.split(',') for singer in qs_singers for s in singer]
    all_singers = sorted(
        list(set([s.strip() for singer in s_list for s in singer])))
    return all_singers


def get_languages():
    qs_languages = Song.objects.values_list('language').all()
    all_languages = sorted(
        list(set([l.strip() for lang in qs_languages for l in lang])))
    return all_languages


def search_in_all_songs_page(request, songs):
    search_query = request.GET.get('q')
    search_singer = request.GET.get('singers') or ''
    search_language = request.GET.get('languages') or ''
    filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(
        Q(language__icontains=search_language)).filter(Q(singer__icontains=search_singer)).distinct()
    return filtered_songs


def get_songs_on_homepage():
    all_songs = list(Song.objects.all().values('id').order_by('?'))
    sliced_ids = [each['id'] for each in all_songs][:5]
    songs_on_home_page = Song.objects.filter(id__in=sliced_ids)
    return songs_on_home_page
