# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/0xfari/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/0xfari/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up Sunday 22 November 2026's world news: "THE SUNDAY
WORLD", a broadsheet front page with a map-led hero.

The hero is the Gulf on the night Iran struck across it — a drawn map of the
strait, Bahrain, and the two tankers hit near Hormuz. Below it, nine pictured
stories span the day: COP31 in overtime in Antalya, the freighter Sparta II
burning in the Baltic, Poland's airspace row with NATO, the capture of
FBI-listed drug lord Fausto Isidro in Mexico, a magnitude 6.7 quake in Peru,
the Hartha power-station fire in Iraq, toxic alcohol deaths in Manipur,
record floods in Florida, and the stock market's worst week since April 2025.
An ALSO TODAY strip carries five more items. Every story was verified against
live reporting on 22 November 2026; the 19 November ICJ ruling and Shenzhen
summit were deliberately left out — they are not this day's news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) validates `entry.png` — PNG
signature, 1024×1024 IHDR with matching CRCs, size cap, IEND trailer —
clears only the *contents* of the output directory, and copies the image
there byte for byte, verifying the copy. `render.py` (Python 3, Pillow) drew
the image from code with the DejaVu fonts bundled in `fonts/`.
