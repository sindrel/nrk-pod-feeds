[![Talk from JavaZone 2023](assets/vimeo.png)](https://vimeo.com/861697003)

# Open NRK Podcast Feeds
![update-podcast-feeds badge](https://github.com/sindrel/nrk-pod-feeds/actions/workflows/update_feeds.yml/badge.svg)
![discover-podcast-feeds badge](https://github.com/sindrel/nrk-pod-feeds/actions/workflows/discover_feeds.yml/badge.svg)
![python version badge](https://badgen.net/pypi/python/black)

Publishes RSS feeds with the last 10 episodes of every configured podcast, without delay. For personal use.  

## Feeds
**Go to [this page](https://sindrel.github.io/nrk-pod-feeds) for a list of available feeds.**

### Discovery  
New podcasts are discovered automatically. Changes are listed [here](DISCOVERY.md).  

### Archived feeds  
Some additional feeds include all episodes, such as Radioresepsjonen, Tazte Priv, etc.  

## How it works  
![A simplified sequence diagram](assets/nrk-pod-feeds.png?raw=true "Sequence Diagram")  

### Discovery routine  
* Runs once a day
* Auto-configures which podcasts to fetch
* Reduces API load and pipeline execution time

### Feed updates  
* Runs every hour
* Fetches new episodes and adds them to RSS feeds

## In the media  
* [kode24 (September 2023)](https://www.kode24.no/artikkel/nrk-slar-ned-pa-podcast-prosjekter-sindre-fikk-epost-for-foredrag/80166051)

## Contribute
Feel free to open a pull request or create an issue.

## Development
<details>
  <summary>Instructions</summary>

## Getting started
### Set up venv and install dependencies (Linux & MacOS)
```shell
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install pytest
```

### Run tests
```shell
pytest -v --disable-warnings --log-cli-level=DEBUG
```

### Build or update podcast feeds
```shell
python3 generate_feeds.py
```

</details>
