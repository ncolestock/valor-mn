# Valor MN

Podcast of Valor Classical Academy. Public RSS feed for Apple Podcasts, Spotify, and any other app that reads RSS.

- Show: **Valor MN**
- Site: https://valormn.org
- Feed: https://ncolestock.github.io/valor-mn/feed.xml
- Cover: `cover.jpg` (3000×3000, icon only, no wordmark)

## Add an episode

1. Drop the AAC/M4A into `episodes/YYYY-MM-DD.m4a`.
2. Write `episodes/YYYY-MM-DD.json` (`guid`, `title`, `date`, `summary`, `file`, `duration` in seconds).
3. `python3 scripts/build_feed.py`
4. Commit and push `main`. GitHub Pages updates in about a minute.

## Directories (after the feed is live)

These require Nathan’s own login. Paste the feed URL:

`https://ncolestock.github.io/valor-mn/feed.xml`

1. **Apple Podcasts** — [podcastsconnect.apple.com](https://podcastsconnect.apple.com) → Add a Show → RSS. Validation email goes to `nathan.colestock@valormn.org`. Review is usually 1–2 days.
2. **Spotify** — [creators.spotify.com](https://creators.spotify.com) → Add a podcast → RSS.
3. **Amazon Music** — [podcasters.amazon.com](https://podcasters.amazon.com)
4. **YouTube Podcasts** — YouTube Studio → Content → Podcasts (connect the RSS).
5. **Podcast Index** — [podcastindex.org/add](https://podcastindex.org/add) (feeds Overcast, Fountain, and others).

Pocket Casts, Overcast, Castro, and Accidental Tech Podcast–style apps can subscribe from the RSS URL immediately. They do not need a directory listing.
