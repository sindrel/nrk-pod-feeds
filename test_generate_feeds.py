import os

from generate_feeds import *

def test_get_podcast():
    feeds_dir = "tests/rss"
    os.makedirs(feeds_dir, exist_ok=True)

    podcast_id = "radiodokumentaren"
    season_id = "liv"

    podcast = get_podcast(podcast_id, season_id, feeds_dir, 10)
    assert podcast

    write_podcast_xml(feeds_dir, f"{podcast_id}_test", podcast)
    file = write_podcast_xml(feeds_dir, podcast_id, podcast)
    os.remove(file)
    
def test_get_podcast_void():
    feeds_dir = "tests/rss"

    podcast_id = "kongerdekka"
    season_id = "2020"

    podcast = get_podcast(podcast_id, season_id, feeds_dir, 10)
    assert podcast == None


def _ep(title, season_title):
    return {"titles": {"title": title}, "_links": {"season": {"title": season_title}}}


def test_build_episode_title_standard_unchanged():
    assert build_episode_title(_ep("KI i krig", "Sesong 2026"), "standard") == "KI i krig"


def test_build_episode_title_umbrella_prepends_season():
    assert build_episode_title(
        _ep("Guds plan med det hele (5:5)", "Demonutdriveren"), "umbrella"
    ) == "Demonutdriveren: Guds plan med det hele (5:5)"


def test_build_episode_title_umbrella_skips_generic_season():
    # "Andre episoder" / calendar buckets / "Sesong N" carry no info
    assert build_episode_title(_ep("Maria Sand", "Andre episoder"), "umbrella") == "Maria Sand"
    assert build_episode_title(_ep("Foo", "Sesong 2025"), "umbrella") == "Foo"
    assert build_episode_title(_ep("Foo", "Mai 2026"), "umbrella") == "Foo"
    assert build_episode_title(_ep("Foo", "2. kvartal 2026"), "umbrella") == "Foo"


def test_build_episode_title_umbrella_skips_when_title_contains_season():
    # tyrann case — title already says "Khomeini"
    assert build_episode_title(_ep("Khomeini (6:6)", "Khomeini"), "umbrella") == "Khomeini (6:6)"
    # leseklubben case — season has "Lydboka:" prefix, title has the book name
    assert build_episode_title(
        _ep("«Kafka på stranden» (41:49)", "Lydboka: «Kafka på stranden»"), "umbrella"
    ) == "«Kafka på stranden» (41:49)"
