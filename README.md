# SNH48 Live

This repository hosts technical documentation and helpers for the [SNH48 Live](https://www.youtube.com/SNH48Live) YouTube channel.

Check [snh48live.org](https://snh48live.org) for more resources.

## Docs

- [`about.md`](about.md): general description of the channel.
- [`video-source.md`](video-source.md): technical info on how videos on the channel are extracted, and qualities thereof.
- [`videos.txt`](videos.txt): short list of all content videos (channel info videos are not included).
- [`videos/metadata/*.json`](videos/metadata): metadata of content videos directly from YouTube API v3.
- [`partially-blocked.txt`](partially-blocked.txt): short list of videos that are blocked in some countries (see `claims.md` for details). To get around region blocks, use a VPN service, e.g. [Private Internet Access](https://www.privateinternetaccess.com/).
- [`claims.md`](claims.md): list of videos and their associated copyright claims.
- [`claims.json`](claims.json): list of videos and their associated copyright claims, in JSON format.
- [`performances.json`](data/performances.json): a streamable line-oriented JSON data store of metadata of performances, used for [snh48live.org/filter](https://snh48live.org/filter/).
- [`attendance.txt`](data/attendance.txt): human-readable attendance sheet (compiled by myself, might contain mistakes).
- [`attendance.json`](data/attendance.json): structured version of `attendance.txt` for machine consumption.

## Helpers

- [`download`](bin/download): the heart and soul of this channel. Downloads a VOD from live.snh48.com, then optionally uploads it to the channel.
- [`extract-claims`](bin/extract-claims): extract video info and associated copyright claims from a YouTube copyright claims page, and automatically populate related datastores.
- [`fetch-metadata`](bin/fetch-metadata): fetch metadata of all content videos.
- [`parse-attendance-sheet`](bin/parse-attendance-sheet): convert `attendance.txt` into `attendance.json`.
- [`performers`](bin/performers): retrieve performers lists from official streaming site.
- [`post-to-tumblr`](bin/post-to-tumblr): cross-post to [Tumblr](https://snh48live.tumblr.com) — a healthy dose of SEO and discoverability shenanigans doesn't hurt, right?
- [`record-performance`](bin/record-performance): record performance metadata into `performances.json`.
- [`searchrank`](bin/searchrank): find this channel and its videos among the top 50 SNH48-related search results. Purely for bragging rights.
- [`stats`](bin/stats): fetch and display channel analytics data.
- [`stats-monitor`](bin/stats-monitor): run `stats` periodically, print and log results.
- [`tweet`](bin/tweet): tweet to [Twitter](https://twitter.com/snh48live).
- [`thumbnail`](bin/thumbnail): generate custom thumbnails.
- [`update-metadata`](bin/update-metadata): update metadata of videos in various ways (check the subcommands).
- [`upload`](bin/upload): YouTube video uploader (WIP).
