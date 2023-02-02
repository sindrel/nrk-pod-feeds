import logging

from . import psapi

def test_get_podcast_metadata():
    podcast_id = "kongerekka"

    metadata = psapi.get_podcast_metadata(podcast_id)

    assert "title" in metadata["series"]["titles"]
    assert "url" in metadata["series"]["squareImage"][4]
    assert "href" in metadata["_links"]["share"]
    assert "name" in metadata["_links"]["seasons"][0]

def test_get_podcast_episodes():
    podcast_id = "berrum_beyer_snakker_om_greier"

    episodes = psapi.get_podcast_episodes(podcast_id)

    for episode in episodes:
        assert "title" in episode['titles']
        assert "subtitle" in episode['titles']
        assert "date" in episode
        assert "episodeId" in episode
        assert "durationInSeconds" in episode

    assert len(episodes) == 10

def test_get_episode_manifest():
    podcast_id = "kongerekka"

    episodes = psapi.get_podcast_episodes(podcast_id)
    manifest = psapi.get_episode_manifest(podcast_id, episodes[0]["episodeId"])

    assert "mimeType" in manifest["playable"]["assets"][0]
    assert "url" in manifest["playable"]["assets"][0]

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
    
    for episode in episodes:
        assert "title" in episode['titles']
        assert "subtitle" in episode['titles']
        assert "date" in episode
        assert "episodeId" in episode
        assert "durationInSeconds" in episode

    assert len(episodes) > 0

def test_get_all_podcasts():
    podcasts = psapi.get_all_podcasts()

    for podcast_k, podcast in podcasts.items():
        assert "seriesId" in podcast
        assert "title" in podcast

    assert len(podcasts) > 0