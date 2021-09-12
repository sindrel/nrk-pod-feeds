import os
import sys
import json
from psapi import get_podcast_metadata, get_episode_manifest, get_podcast_episodes

podcasts = ["oppdatert", "verdiboersen"]
assets_base_path = "assets/tests/api/podcast"

def write_to_file(path, str):
    textfile = open(path, "w")
    textfile.write(str)
    textfile.close()

print("Fetching test data...")
for podcast_id in podcasts:
    path = f"{assets_base_path}/{podcast_id}/episodes"
    os.makedirs(path)

    metadata = get_podcast_metadata(podcast_id, "text")
    if not metadata:
        sys.exit()

    path = f"{assets_base_path}/{podcast_id}/metadata.json"
    write_to_file(path, metadata)

    episodes = get_podcast_episodes(podcast_id, None, "text")
    if not episodes:
        sys.exit()
    
    path = f"{assets_base_path}/{podcast_id}/episodes.json"
    write_to_file(path, episodes)

    episodes = json.loads(episodes)["_embedded"]["episodes"]

    for episode in episodes:
        episode_id = episode["episodeId"]
        manifest = get_episode_manifest(podcast_id, episode_id, "text")
        if not manifest:
            sys.exit()

        path = f"{assets_base_path}/{podcast_id}/episodes/{episode_id}.json"
        write_to_file(path, manifest)

print("Done")