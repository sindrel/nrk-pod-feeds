import requests
from helpers import get_version

api_base_url = "https://psapi.nrk.no"
headers = {
    "User-Agent": f"nrk-pod-feeder {get_version()}"
}

def get_podcast_episodes(podcast_id, season = None, format = "json"):
    print(f"Fetching episodes for podcast {podcast_id}...")

    url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}/episodes?page=1&pageSize=10&sort=desc"
    if season:
        url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}/seasons/{season}?page=1&pageSize=10&sort=desc"

    r = requests.get(url)

    if not r.ok:
        print(f"Unable to fetch podcast episodes ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    if season:
        return r.json()["_embedded"]["episodes"]["_embedded"]["episodes"]

    return r.json()["_embedded"]["episodes"]

def get_episode_manifest(podcast_id, episode_id, format = "json"):
    print(f"  Fetching assets for episode {episode_id}...")

    url = f"{api_base_url}/playback/manifest/podcast/{podcast_id}/{episode_id}"
    r = requests.get(url)

    if not r.ok:
        print(f"  Unable to fetch episode manifest ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    return r.json()

def get_podcast_metadata(podcast_id, format = "json"):
    print(f"Fetching metadata for podcast {podcast_id}...")

    url = f"{api_base_url}/radio/catalog/podcast/{podcast_id}"
    r = requests.get(url)

    if not r.ok:
        print(f"Unable to fetch podcast metadata ({url} returned {r.status_code})")
        return None

    if format == "text":
        return r.text

    return r.json()