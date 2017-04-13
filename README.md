# SNH48 Live

This repository hosts technical documentation and helpers for the [SNH48 Live](https://www.youtube.com/channel/UC10BBCJQasWk_08Fdz0XCsQ) YouTube channel.

## Docs

- [`about.md`](about.md): general description of the channel.
- [`video-source.md`](video-source.md): technical info on how videos on the channel are extracted, and qualities thereof.
- [`videos.txt`](videos.txt): short list of all content videos (channel info videos are not included).
- [`videos/metadata/*.json`](videos/metadata): metadata of content videos directly from YouTube API v3.
- [`partially-blocked.txt`](partially-blocked.txt): short list of videos that are blocked in some countries (see `claims.md` for details). To get around region blocks, use a VPN service, e.g. [Private Internet Access](https://www.privateinternetaccess.com/).
- [`claims.md`](claims.md): list of videos and their associated copyright claims.
- [`claims.json`](claims.json): list of videos and their associated copyright claims, in JSON format.

## Helpers

- [`extract-claims`](bin/extract-claims): extract video info and associated copyright claims from a YouTube copyright claims page, and automatically populate related datastores.
- [`fetch-metadata`](bin/fetch-metadata): fetch metadata of all content videos.
- [`stats`](bin/stats): fetch and display channel analytics data.
- [`thumbnail`](bin/thumbnail): generate custom thumbnails.
