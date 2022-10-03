import logging

from . import psapi

def test_get_podcast_metadata():
    podcast_id = "kongerekka"

    metadata = psapi.get_podcast_metadata(podcast_id)

    assert metadata != None

def test_get_podcast_episodes():
    podcast_id = "kongerekka"

    episodes = psapi.get_podcast_episodes(podcast_id)

    assert len(episodes) == 10

def test_get_episode_manifest():
    podcast_id = "kongerekka"

    episodes = psapi.get_podcast_episodes(podcast_id)
    manifest = psapi.get_episode_manifest(podcast_id, episodes[0]["episodeId"])

    assert manifest != None

def test_get_podcast_episodes_by_season():
    podcast_id = "kongerekka"
    season_id = "2022"

    episodes = psapi.get_podcast_episodes(podcast_id, season_id)

    assert len(episodes) == 10

def test_get_all_podcast_episodes():
    podcast_id = "kongerekka"

    episodes = psapi.get_all_podcast_episodes(podcast_id)

    assert len(episodes) > 0
