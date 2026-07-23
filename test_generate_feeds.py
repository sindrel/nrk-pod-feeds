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

def test_get_podcast_latest_season_matches_unscoped_fetch(tmp_path):
    # Regression test: LATEST_SEASON must fetch recent episodes across all seasons
    # via NRK's flat /episodes endpoint -- exactly as season=None does -- instead of
    # resolving a single season that may be an empty placeholder (which silently
    # emptied the Abels tårn feed). Asserting the two paths agree keeps the test from
    # depending on how NRK happens to split the series into seasons at any moment.
    podcast_id = "abels_taarn"

    # tmp_path is an empty feeds_dir, so no prior lastBuildDate suppresses the episodes.
    # get_podcast only reads feeds_dir, so both calls can share the same empty dir.
    latest = get_podcast(podcast_id, "LATEST_SEASON", tmp_path, 10)
    unscoped = get_podcast(podcast_id, None, tmp_path, 10)

    assert latest
    assert latest.episodes
    assert [e.title for e in latest.episodes] == [e.title for e in unscoped.episodes]
