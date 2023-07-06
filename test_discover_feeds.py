import logging

from discover_feeds import *

def test_update_podcasts_config():
    configured = [
        {
            "id": "abels_taarn",
            "title": "De 10 siste fra Abels Tårn",
            "season": None,
            "enabled": True,
        },
        {
            "id": "berrum_beyer_snakker_om_greier",
            "title": "De 10 siste fra Foo og Bar",
            "season": None,
            "enabled": False,
            "ignore": True,
        },
    ]
    discovered = {
        "hele_historien" : {
            "seriesId": "hele_historien",
            "title": "De 10 siste fra Hele Historien",
        },
        "abels_taarn" : {
            "seriesId": "abels_taarn",
            "title": "De 10 siste fra Abels Tårn",
        }, 
        "berrum_beyer_snakker_om_greier" : {
            "seriesId": "berrum_beyer_snakker_om_greier",
            "title": "De 10 siste fra Foo og Bar",
        },
        "dagsnytt_atten" : {
            "seriesId": "dagsnytt_atten",
            "title": "De 10 siste fra dagsnytt_atten",
        }
    }

    updated, changes = update_podcasts_config(configured, discovered)
    helpers.write_podcasts_changelog("tests/DISCOVERY.md", datetime.now(), changes)
    logging.debug(updated)
    
    added = False
    for feed in updated:
        if feed['id'] == "hele_historien":
            added = True # Ensure discovered feed has been added
        if feed['id'] == "berrum_beyer_snakker_om_greier":
            assert feed['enabled'] == False # Ensure ignore flag is respected

    assert added == True
