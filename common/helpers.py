import os
import logging
import json
import xml.etree.ElementTree as ET

def init():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level)

def get_last_feed(feeds_dir, podcast_id):
    try:
        path = f"{feeds_dir}/{podcast_id}.xml"
        tree = ET.parse(path)
        root = tree.getroot()
        return root
    except:
        logging.info(f"No existing feed found for podcast {podcast_id}")
        return None

def get_podcasts_config(podcasts_cfg_file):
    with open(podcasts_cfg_file, 'r') as file:
        data = file.read()
        return json.loads(data)

def write_podcasts_config(config_file, podcasts):
    f = open(config_file, "w")
    str = json.dumps(podcasts, ensure_ascii=False, indent=4)
    f.write(str)
    f.close()
    
    logging.info(f"Podcasts config written to file: {config_file}")

def write_feeds_file(feeds_file, podcasts):
    f = open(feeds_file, "w")
    str = json.dumps(podcasts, ensure_ascii=False, indent=2)
    f.write(f"const feeds = {str}")
    f.close()
    
    logging.info(f"Podcast feeds written to file: {feeds_file}")

def get_version():
    with open("version.txt") as file:
        return file.read()
