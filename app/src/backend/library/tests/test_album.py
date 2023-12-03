from collections import Counter
import pytest
from unittest.mock import MagicMock

from app.src.backend.library import Album

@pytest.fixture
def album_data():
    return {
        "title": "Test Album",
        "songs": [
            {"cover": "cover1.jpg", "artist": "Artist1"},
            {"cover": "cover2.jpg", "artist": "Artist2"},
            {"cover": "cover1.jpg", "artist": "Artist1"},
        ]
    }


@pytest.fixture
def album(album_data):
    return Album(album_data)


def test_album_initialization(album_data):
    album = Album(album_data)
    assert album.title == album_data["title"]


def test_choose_cover_and_artist(album, album_data):
    album.songs = [MagicMock(cover=song["cover"], artist=song["artist"]) for song in album_data["songs"]]
    album.choose_cover_and_artist()
    assert album.cover == Counter([song["cover"] for song in album_data["songs"]]).most_common(1)[0][0]
    assert album.artist == Counter([song["artist"] for song in album_data["songs"]]).most_common(1)[0][0]
