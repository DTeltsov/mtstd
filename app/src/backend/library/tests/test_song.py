import pytest

from app.src.backend.library import Song


@pytest.fixture
def song_data():
    return {
        "file": "test_song.mp3",
        "cover": "test_cover.jpg",
        "length": 180.0,
        "title": "Test Song",
    }


@pytest.fixture
def album():
    return "Test Album"


@pytest.fixture
def artist():
    return "Test Artist"


@pytest.fixture
def song(song_data, album, artist):
    return Song(song_data, album, artist)


def test_song_initialization(song, song_data, album, artist):
    assert song.file_url == song_data["file"].replace('localstack', 'localhost')
    assert song.cover == song_data["cover"].replace('localstack', 'localhost')
    assert song.length == song_data["length"]
    assert song.title == song_data["title"]
    assert song.album == album
    assert song.artist == artist
    assert song.media_content == ''

