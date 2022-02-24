import logging
import json

assets_base_path = "assets/tests/api/podcast"

def get_podcast_episodes(podcast_id, season = None, format = "json"):
    logging.info(f"Fetching episodes for podcast {podcast_id}...")

    path = f"{assets_base_path}/{podcast_id}/episodes.json"
    f = open(path)

    if not f:
        logging.info(f"Unable to fetch podcast episodes ({path})")
        return None

    return json.load(f)["_embedded"]["episodes"]

def get_episode_manifest(podcast_id, episode_id):
    logging.info(f"  Fetching assets for episode {episode_id}...")

    path = f"{assets_base_path}/{podcast_id}/episodes/{episode_id}.json"
    f = open(path)

    if not f:
        logging.info(f"  Unable to fetch episode manifest ({path})")
        return None

    return json.load(f)

def get_podcast_metadata(podcast_id):
    logging.info(f"Fetching metadata for podcast {podcast_id}...")

    path = f"{assets_base_path}/{podcast_id}/metadata.json"
    f = open(path)

    if not f:
        logging.info(f"Unable to fetch podcast metadata ({path})")
        return None

    return json.load(f)