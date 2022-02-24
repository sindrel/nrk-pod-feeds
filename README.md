# Open NRK Podcast Feeds
Publishes RSS feeds with the last 10 episodes of every configured podcast, without delay. For personal use.

## Feeds
**Go to [this page](https://sindrel.github.io/nrk-pod-feeds) for a list of available feeds.**

## Contribute
Feel free to open a pull request or create an issue.

## Development
<details>
  <summary>Instructions</summary>

## Getting started
### Install dependencies
```python3 -m pip install -r requirements.txt```

### Run tests
```pytest -v --disable-warnings --log-cli-level=DEBUG```

### Build or update podcast feeds
```python3 generate_feeds.py```

</details>
