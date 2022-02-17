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

### Build or update podcast feeds
```python3 generate_feeds.py```

## Using the mock API
### Dump local test data for use by mock API
```python3 fetch_test_data.py```

### Toggle use of the mock API
Comment/uncomment the import statement in `generate_feeds.py`.

</details>
