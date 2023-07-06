import os
import json

from datetime import datetime
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

    if os.path.exists(feeds_file):
        os.remove(feeds_file)
    write_feeds_file(feeds_file, podcasts)
    saved = open(feeds_file, "r")
    str = saved.read()
    saved.close()

    assert str

def test_write_podcasts_changelog():
    file = "tests/DISCOVERY_UNIT.md"
    os.makedirs("tests/", exist_ok=True)

    today = datetime.now()
    ch_date = today.date()

    if os.path.exists(file):
        os.remove(file)

    old_changes = [
        "Added podcast foo",
        "Deprecated podcast bar"
    ]

    new_changes = [
        "Added podcast foobar",
        "Deprecated podcast barfoo"
    ]

    write_podcasts_changelog(file, today, old_changes)
    write_podcasts_changelog(file, today, new_changes)

    saved = open(file, "r")
    str = saved.read()
    saved.close()

    expected = f"""# Podcast Discovery Changelog  
### {ch_date}  
- Added podcast foobar  
- Deprecated podcast barfoo  
### {ch_date}  
- Added podcast foo  
- Deprecated podcast bar  
"""

    assert str == expected

def test_get_podcasts_config():
    podcasts_cfg_file = "podcasts.json"
    with open(podcasts_cfg_file, 'r') as file:
        data = file.read()
        
    assert json.loads(data)