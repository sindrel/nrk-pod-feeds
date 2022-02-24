import os

from generate_feeds import *

def test_get_podcast():
    feeds_dir = "tests/rss"
    os.makedirs(feeds_dir, exist_ok=True)

    podcast_id = "kongerekka"
    season_id = "sesong-2"

    podcast = get_podcast(podcast_id, season_id, feeds_dir, 10)
    assert podcast

    write_podcast_xml(feeds_dir, f"{podcast_id}_test", podcast)
    file = write_podcast_xml(feeds_dir, podcast_id, podcast)
    os.remove(file)
    
def test_get_podcast_void():
    feeds_dir = "tests/rss"

    podcast_id = "kongerdekka"
    season_id = "sesong-2"

    podcast = get_podcast(podcast_id, season_id, feeds_dir, 10)
    assert podcast == None
