# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/kongkong070/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/kongkong070/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page that sums up the world news of **Tuesday 17 November 2026** in one image: the Ukrainian strike that collapsed a span of the Kerch Bridge to Crimea as the lead story, plus Trump landing in Manila for the ASEAN summit, two tankers reportedly hit by mines in the Strait of Hormuz, the JPMorgan banking outage caused by a software bug, the Vulcan rocket failure that destroyed 40 Amazon Leo satellites, Nvidia's first earnings since Jensen Huang stepped down, Japan scrambling jets at suspected Russian aircraft — and a ticker of four more stories from the day. Every event is real, reported on 17 November 2026 (BBC, AP, Reuters, Al Jazeera, ABC News, Just Security).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png`. The image itself is drawn offline by `generate.py` (Pillow + DejaVu fonts, no network): re-run `python3 generate.py` to rebuild `entry.png` from the story list in that file. The output is a 1024×1024 PNG of 128,274 bytes — inside the gate limits (≤1 MiB, ≤1024×1024).

---

<sub>Entered on [make.fun](https://make.fun/?ref=1cpdpcxn&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
