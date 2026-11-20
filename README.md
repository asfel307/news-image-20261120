# The World Today — Friday, 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/asfel307/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/asfel307/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page summing up the world's news of
**Friday, 20 November 2026** — one lead story and five more, drawn with
Pillow from scratch: ivory newsprint, dark ink, a brick-red accent and a
single teal secondary. No network, no downloaded assets; every pictogram
is drawn with Pillow primitives and every glyph comes from the local
DejaVu fonts.

## The six stories

1. **Lead — UK pledges 1,000+ long-range drones for Ukraine.**
   PM Andy Burnham announced a £260m package in Berlin at the Coalition
   of the Willing meeting. The drones fly 1,000+ km — as far as London
   to Berlin — and carry heavy warheads. The package also includes
   maritime, logistical and surveillance drones; 80%+ of the funding is
   spent in the UK. *(GOV.UK, BBC)*
2. **Taiwan stocks plunge 2,200 points intraday, below 37,000** —
   lowest since mid-April; shed 7,000+ points in a week; the regulator
   unveiled five rescue measures.
3. **Houthi strikes hit Saudi Arabia** — four targets claimed,
   including Riyadh's tallest skyscraper damaged; foreign investors
   warned to leave. *(TASS, News.Az)*
4. **Trump pardons baseball legend Pete Rose posthumously** — MLB
   all-time hits leader, 4,256 hits; 1990 tax case; Hall of Fame vote
   next December 2027. *(Reuters, AP)*
5. **Denmark ratifies Greenland security deal 109–0** — the US gains
   two bases including "Golden Dome" missile defence; Danish
   sovereignty and Greenlanders' self-determination reaffirmed.
   *(Folketing record, Reuters)*
6. **Migrant boat capsizes off Senegal** — about 100 aboard off Yenne,
   dozens missing, search continues; 11,000+ reached the Canary
   Islands in the first half of November. *(Reuters, AFP)*

## Run it

```sh
python3 render.py            # rebuilds entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

`main.py` is Python 3.13, standard library only, and deterministic: two
runs produce byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
