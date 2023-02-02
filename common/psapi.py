import logging
import requests

from common.helpers import get_version

api_base_url = "https://psapi.nrk.no"
headers = {
    "User-Agent": f"nrk-pod-feeder {get_version()}"
}

def get_all_podcast_episodes(podcast_id):
    url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}/episodes?page=1&pageSize=30&sort=asc"

    episodes = []
    while True:
        r = requests.get(url)
        if not r.ok:
            logging.info(f"Unable to fetch podcast episodes ({url} returned {r.status_code})")
            return None

        for episode in r.json()["_embedded"]["episodes"]:
            episodes.append(episode)
        
        if not "next" in r.json()["_links"]:
            break

        url = api_base_url + r.json()["_links"]["next"]["href"]

    return episodes

def get_podcast_episodes(podcast_id, season = None, format = "json"):
    logging.info(f"Fetching episodes for podcast {podcast_id} ({season})...")

    url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}/episodes?page=1&pageSize=10&sort=desc"
    if season:
        url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}/seasons/{season}?page=1&pageSize=10&sort=desc"

    r = requests.get(url)
    if not r.ok:
        logging.info(f"Unable to fetch podcast episodes ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    if season:
        return r.json()["_embedded"]["episodes"]["_embedded"]["episodes"]

    return r.json()["_embedded"]["episodes"]

def get_episode_manifest(podcast_id, episode_id, format = "json"):
    logging.info(f"  Fetching assets for episode {episode_id}...")

    url = f"{api_base_url}/playback/manifest/podcast/{podcast_id}/{episode_id}"
    r = requests.get(url)

    if not r.ok:
        logging.info(f"  Unable to fetch episode manifest ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    return r.json()

def get_podcast_metadata(podcast_id, format = "json"):
    logging.info(f"Fetching metadata for podcast {podcast_id}...")

    url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}"
    r = requests.get(url)

    if not r.ok:
        logging.info(f"Unable to fetch podcast metadata ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    return r.json()

def get_all_podcasts():
    url = f"{api_base_url}/radio/search/categories/podcast?take=1000"

    podcasts = {}
    series_c = 0

    while True:
        r = requests.get(url)
        if not r.ok:
            logging.info(f"Unable to fetch podcasts ({url} returned {r.status_code})")
            return None

        for series in r.json()["series"]:
            if series['type'] != "podcast":
                continue

            logging.debug(f"Found seriesId {series['title']} ({series['seriesId']})")

            podcasts[series['seriesId']] = {
                "seriesId" : series['seriesId'],
                "title" : series['title'],
            }

            series_c+=1
        
        if not "next" in r.json()["_links"]:
            break

        url = api_base_url + r.json()["_links"]["next"]["href"]

    logging.info(f"Discovered {len(podcasts)} podcast(s) in a total of {series_c} items in search result")
    return podcasts