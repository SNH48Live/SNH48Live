# SNH48 Live

This repository hosts technical documentation and helpers for the [SNH48 Live](https://www.youtube.com/channel/UC10BBCJQasWk_08Fdz0XCsQ) YouTube channel.

## Docs

- [`partially-blocked.txt`](partially-blocked.txt): short list of videos that are blocked in some countries (see `claims.md` for details).
- [`claims.md`](claims.md): list of videos and their associated copyright claims.
- [`claims.json`](claims.json): list of videos and their associated copyright claims, in JSON format.

## Helpers

- [`extract-claims`](bin/extract-claims): extract video info and associated copyright claims from a YouTube copyright claims page, and automatically populate related datastores.
