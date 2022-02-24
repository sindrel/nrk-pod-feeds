import os
import json

from common.helpers import *

def test_write_feeds_file():
    feeds_file = "tests/feeds.js"
    os.makedirs("tests/", exist_ok=True)

    podcasts = [{
        "id": "kongerekka",
        "title": "De 10 siste fra Kongerekka",
        "season": "LATEST_SEASON",
        "enabled": "true"
    }]

    os.remove(feeds_file)
    write_feeds_file(feeds_file, podcasts)
    saved = open(feeds_file, "r")
    str = saved.read()
    saved.close()

    assert str
    #assert str == f"const feeds = {podcasts}"

def test_get_podcasts_config():
    podcasts_cfg_file = "podcasts.json"
    with open(podcasts_cfg_file, 'r') as file:
        data = file.read()
        
    assert json.loads(data)