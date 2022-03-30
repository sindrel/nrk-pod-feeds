import logging

from podgen import Podcast, Episode, Media
from dateutil import parser
from datetime import timedelta

from common.helpers import init, get_last_feed, get_podcasts_config, write_feeds_file, get_version
from common.psapi import get_podcast_metadata, get_episode_manifest, get_podcast_episodes, get_all_podcast_episodes

podgen_agent = f"nrk-pod-feeder v{get_version()} (with help from python-podgen)"
podcasts_cfg_file = "podcasts.json"
filter_teasers = True
web_url = "https://sindrel.github.io/nrk-pod-feeds"

def get_podcast(podcast_id, season, feeds_dir, ep_count = 10):
    existing_feed = get_last_feed(feeds_dir, podcast_id)

    last_feed_update = parser.parse("1970-01-01 00:00:01+00:00")
    if existing_feed:
        for channel in existing_feed.findall('channel'):
            last_build_date = channel.find('lastBuildDate').text
            last_feed_update = parser.parse(last_build_date)
            logging.info(f"Feed was last built {last_feed_update}")

    metadata = get_podcast_metadata(podcast_id)
    if not metadata:
        return None

    original_title = metadata["series"]["titles"]["title"]
    image = metadata["series"]["squareImage"][4]["url"]
    website = metadata["_links"]["share"]["href"]

    logging.info(f"  Title: {original_title}")
    logging.info(f"  Image: {image}")

    p = Podcast(
        generator=podgen_agent,
        website=web_url,
        image=image,
        withhold_from_itunes=True,
        explicit=False
    )

    if season == "LATEST_SEASON":
        season = metadata["_embedded"]["seasons"][0]["id"]

    if ep_count == 0:
        episodes = get_all_podcast_episodes(podcast_id)
    else:
        episodes = get_podcast_episodes(podcast_id, season)

    if not episodes:
        return None

    new_episode = False
    for episode in episodes:
        episode_title = episode["titles"]["title"]
        episode_date = episode["date"]
        if parser.parse(episode_date) >= last_feed_update:
            logging.info(f"  Found new episode {episode_title} from {episode_date}")
            new_episode = True

    if not new_episode:
        logging.info("  No new episodes found since feed was last updated")
        return None

    ep_i = 0
    for episode in episodes:
        logging.info(f"Episode #{ep_i}:")

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

        logging.info(f"  Episode title: {episode_title}")
        logging.info(f"  Episode duration: {duration}")
        logging.info(f"  Episode date: {date}")
        logging.info(f"  Audio file URL: {audio_url}")

        if audio_mime != "audio/mp3":
            logging.info(f"  Unrecognized audio MIME type ({audio_mime})")
            continue

        if filter_teasers and episode_title.startswith("Neste episode: "):
            logging.info("  Skipping teaser")
            continue

        p.episodes += [
            Episode(
                title=episode_title,
                media=Media(audio_url, 0, duration=timedelta(seconds=duration)),
                summary=episode_subtitle,
                publication_date=parser.parse(date)
            ),
        ]

        ep_i +=1

    episodes_c = len(episodes)
    title = f"De {episodes_c} siste fra {original_title}"
    subtitle = f"Uoffisiell feed med de siste {episodes_c} episodene fra podkasten {original_title}. Opphavsrett på innhold eies av NRK og ev. andre rettighetshavere. Se {website} for mer informasjon."

    p.name = title
    p.description = subtitle

    return p

def write_podcast_xml(feeds_dir, podcast_id, podcast):
    output_path = f"{feeds_dir}/{podcast_id}.xml"
    podcast.rss_file(output_path, minimize=False)

    logging.info(f"Podcast XML successfully written to file: {output_path}\n---")
    return output_path

if __name__ == '__main__':
    init()

    feeds_dir = "docs/rss"
    feeds_file = "docs/feeds.js"

    podcasts = get_podcasts_config(podcasts_cfg_file)

    for p in podcasts:
        if not p["enabled"]:
            continue

        podcast_id = p["id"]
        podcast_season = p["season"]
        ep_count = 10

        if "episodes" in p:
            ep_count = p["episodes"]

        podcast = get_podcast(podcast_id, podcast_season, feeds_dir, ep_count)
        if not podcast:
            logging.info(f"Got empty result when fetching podcast {podcast_id}")
            continue

        write_podcast_xml(feeds_dir, podcast_id, podcast)

    write_feeds_file(feeds_file, podcasts)
    logging.info("Done")
