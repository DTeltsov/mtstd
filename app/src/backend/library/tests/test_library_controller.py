import pytest

from app.src.backend.library.controller import Library


@pytest.fixture
def library():
    return Library()


def test_set_display_album(library):
    album_name = "Test Album"
    album_data = {"title": album_name, "authors": [{"name": "Test Artist"}]}
    song_data = {"title": "Test Song", "albums": [album_data]}
    library.setup([song_data])
    library.set_display_album(album_name)
    assert library.displayAlbum.title == album_name


def test_get_song_by_name(library):
    song_name = "Test Song"
    song_data = {"title": song_name, "albums": [{"title": "Test Album", "authors": [{"name": "Test Artist"}]}]}
    library.setup([song_data])
    song = library.get_song_by_name(song_name)
    assert song is not None
    assert song.title == song_name


def test_get_album_by_name(library):
    album_name = "Test Album"
    album_data = {"title": album_name, "authors": [{"name": "Test Artist"}]}
    song_data = {"title": "Test Song", "albums": [album_data]}
    library.setup([song_data])
    album = library.get_album_by_name(album_name)
    assert album is not None
    assert album.title == album_name


def test_library_setup():
    # Arrange
    library = Library()
    songs = [
        {'title': 'Song 1', 'albums': [{'title': 'Album 1', 'authors': [{'name': 'Artist 1'}]}]},
        {'title': 'Song 2', 'albums': [{'title': 'Album 2', 'authors': [{'name': 'Artist 2'}]}]},
        # Add more songs with different albums and artists
    ]

    # Act
    library.setup(songs)

    # Assert
    # Check if albums and songs are populated correctly
    assert len(library.albums) == 2
    assert len(library.songs) == 2
    assert library.albums[0].title == 'Album 1'
    assert library.albums[1].title == 'Album 2'
    assert library.albums[0].songs[0].title == 'Song 1'
    assert library.albums[1].songs[0].title == 'Song 2'


def test_library_display_album():
    # Arrange
    library = Library()
    songs = [
        {'title': 'Song 1', 'albums': [{'title': 'Album 1', 'authors': [{'name': 'Artist 1'}]}]},
        {'title': 'Song 2', 'albums': [{'title': 'Album 2', 'authors': [{'name': 'Artist 2'}]}]},
        # Add more songs with different albums and artists
    ]
    library.setup(songs)

    # Act
    library.set_display_album('Album 2')

    # Assert
    # Check if displayAlbum is set correctly
    assert library.displayAlbum.title == 'Album 2'
    assert library.displayAlbum.songs[0].title == 'Song 2'
