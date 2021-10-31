from podgen import Podcast, Episode, Media
from dateutil import parser
from datetime import timedelta

from helpers import get_last_feed,get_podcasts_config,write_feeds_file,get_version
from psapi import get_podcast_metadata, get_episode_manifest, get_podcast_episodes
#from psapi_mock import get_podcast_metadata, get_episode_manifest, get_podcast_episodes

def get_podcast(podcast_id, season):
    existing_feed = get_last_feed(feeds_dir, podcast_id)

    last_feed_update = parser.parse("1970-01-01 00:00:01+00:00")
    if existing_feed:
        for channel in existing_feed.findall('channel'):
            last_build_date = channel.find('lastBuildDate').text
            last_feed_update = parser.parse(last_build_date)
            print(f"Feed was last built {last_feed_update}")

    metadata = get_podcast_metadata(podcast_id)
    if not metadata:
        return None

    original_title = metadata["series"]["titles"]["title"]
    title = f"De 10 siste fra {original_title}"
    image = metadata["series"]["squareImage"][4]["url"]
    website = metadata["_links"]["share"]["href"]

    subtitle = f"Uoffisiell feed med de siste 10 episodene fra podkasten {original_title}. Opphavsrett på innhold eies av NRK og ev. andre rettighetshavere. Se {website} for mer informasjon."

    print(f"  Title: {title}")
    print(f"  Image: {image}")

    p = Podcast(
        generator=podgen_agent,
        name=title,
        description=subtitle,
        website=web_url,
        image=image,
        withhold_from_itunes=True,
        explicit=False
    )

    if season == "LAST_SEASON":
        season = metadata["_embedded"]["seasons"][0]["id"]

    episodes = get_podcast_episodes(podcast_id, season)
    if not episodes:
        return None

    latest_episode = parser.parse(episodes[0]["date"])
    print(f"  The latest episode found is from {latest_episode}")

    if latest_episode <= last_feed_update:
        print("  No new episodes found since feed was last updated")
        return None

    ep_i = 0
    for episode in episodes:
        print(f"Episode #{ep_i}:")

        episode_id = episode["episodeId"]
        episode_title = episode["titles"]["title"]
        episode_subtitle = episode["titles"]["subtitle"]
        duration = episode["durationInSeconds"]
        date = episode["date"]

        manifest = get_episode_manifest(podcast_id, episode_id)
        if not manifest:
            continue

        audio_mime = manifest["playable"]["assets"][0]["mimeType"]
        audio_url = manifest["playable"]["assets"][0]["url"]

        if audio_mime != "audio/mp3":
            print(f"Unrecognized audio MIME type ({audio_mime})")
            continue

        print(f"  Episode title: {episode_title}")
        print(f"  Episode duration: {duration}")
        print(f"  Episode date: {date}")
        print(f"  Audio file URL: {audio_url}")

        p.episodes += [
            Episode(
                title=episode_title,
                media=Media(audio_url, 0, duration=timedelta(seconds=duration)),
                summary=episode_subtitle,
                publication_date=parser.parse(date)
            ),
        ]

        ep_i +=1

    return p

podgen_agent = f"nrk-pod-feeder v{get_version()} (with help from python-podgen)"
podcasts_cfg_file = "podcasts.json"
feeds_dir = "docs/rss"
feeds_file = "docs/feeds.js"
web_url = "https://sindrel.github.io/nrk-pod-feeds"

if __name__ == '__main__':
    podcasts = get_podcasts_config(podcasts_cfg_file)

    for p in podcasts:
        if not p["enabled"]:
            continue

        podcast_id = p["id"]
        podcast_season = p["season"]
        podcast = get_podcast(podcast_id, podcast_season)

        if not podcast:
            print(f"Got empty result when fetching podcast {podcast_id}")
            continue

        output_path = f"{feeds_dir}/{podcast_id}.xml"
        podcast.rss_file(output_path, minimize=False)

        print(f"Podcast XML successfully written to file: {output_path}\n---")

    write_feeds_file(feeds_file, podcasts)
    print("Done")
