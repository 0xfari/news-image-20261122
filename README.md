# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/0xfari/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/0xfari/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up Sunday 22 November 2026's world news: a picture-led
front page, "THE WORLD TODAY".

The hero is the night the Gulf war widened — Iran's overnight missile and
drone strikes on US bases in Bahrain, with tankers hit near Hormuz — drawn
as a night scene over the sea. Below it, six pictured top stories: COP31
reaching a final deal in Antalya, the Russian freighter Sparta II still
burning in the Baltic, record floods lingering in Florida, Modi opening the
Nitish Setu bridge, states pledging rules on killer robots, and France's
protests shrinking. An ALSO TODAY strip carries four more items. Every story
was verified against live reporting on 22 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) validates `entry.png` — PNG
signature, dimensions, size, IEND trailer — clears only the *contents* of the
output directory, and copies the image there byte for byte, verifying the copy.
