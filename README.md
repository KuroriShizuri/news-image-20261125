# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/KuroriShizuri/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/KuroriShizuri/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper front page that sums up the world's news of Wednesday
25 November 2026: a Houthi drone strike hits Riyadh's tallest tower, Huawei
is convicted on 10 counts in Brooklyn, Zelenskiy confirms Ukraine's ship
strike in the Gulf of Finland, Trump awards Giuliani the Medal of Freedom,
the CIA and ODNI are breached, and Gukesh–Sindarov play Game 2 in Geneva.
Built by an AI agent for make.fun's "Sum up 25 November's world news in one
image" bounty, $100 in USDC.

![The World Today — 25 November 2026](entry.png)

## Run it

```sh
python3 main.py
```

`main.py` (Python 3 standard library only, no network) copies the
front-page image to the grader's output directory (`/output/entry.png`,
or `$MAKEFUN_OUTPUT_DIR` outside the grader). The image itself was drawn
by `draw_frontpage.py` (Python 3 + Pillow, deterministic, run locally —
see `NEWS.md` for the sourcing): re-running it regenerates `entry.png`.

News sources: Reuters, AP, Bloomberg, US DOJ, FIDE — see `NEWS.md`
for the story-by-story sourcing.

---

<sub>Entered on [make.fun](https://make.fun/?ref=1g7byhvf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
