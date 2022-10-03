import logging

from . import psapi

def test_get_podcast_metadata():
    podcast_id = "kongerekka"

    metadata = psapi.get_podcast_metadata(podcast_id)

    assert metadata != None

def test_get_podcast_episodes():
    podcast_id = "berrum_beyer_snakker_om_greier"

    episodes = psapi.get_podcast_episodes(podcast_id)

    assert len(episodes) == 10

def test_get_episode_manifest():
    podcast_id = "kongerekka"

    episodes = psapi.get_podcast_episodes(podcast_id)
    manifest = psapi.get_episode_manifest(podcast_id, episodes[0]["episodeId"])

    assert manifest != None

def test_get_latest_podcast_season():
    podcast_id = "kongerekka"

    metadata = psapi.get_podcast_metadata(podcast_id)
    latest_season = metadata["_links"]["seasons"][0]["name"]

    assert latest_season == "2022"

def test_get_podcast_episodes_by_season():
    podcast_id = "kongerekka"
    season_id = "2020"

    episodes = psapi.get_podcast_episodes(podcast_id, season_id)

    assert len(episodes) == 10

def test_get_all_podcast_episodes():
    podcast_id = "kongerekka"

    episodes = psapi.get_all_podcast_episodes(podcast_id)

    assert len(episodes) > 0
