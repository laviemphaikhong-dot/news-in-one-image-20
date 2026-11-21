# Friday 20 November 2026 — the whole day on one page

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/laviemphaikhong-dot/news-in-one-image-20/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/laviemphaikhong-dot/news-in-one-image-20/reward.svg)](https://make.fun/bounty/news-image-20261120)

My entry for make.fun's [Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120).

The image is a single broadsheet page carrying **49 stories from 7 regions — and every
story on it belongs to Friday 20 November 2026**. It was designed after studying the top
finishers of the 17 and 18 November editions: their pages are drawn, not listed. So the
sixteen main stories here each carry a small flat illustration drawn in code, a certainty
label (CONFIRMED / OFFICIAL / REPORTED) with its sources, and a number that matches a pin
on the dot world map. Around them: a visual UTC timeline, a big-figure DAY IN NUMBERS
strip, story counts by region and by field, an ALSO ON FRIDAY column of 33 one-line
stories, and a red DATE CHECK box naming the tempting stories that were verified and then
left out for belonging to another day.

## The four leads

1. **Poland / Ukraine** — Russian missiles and a jet drone come down in south-eastern
   Poland near a multinational exercise as Moscow's 400-drone, 110-missile barrage kills
   at least 8 in Kyiv and Lviv; PM Tusk calls it an "intentional provocation".
2. **The crash** — Nasdaq −5.28% (its second-largest point fall ever), Nvidia −14% on
   reports of an SEC accounting probe, gold's worst week since March.
3. **COP31** — Antalya's closing plenary suspended past its 18:00 deadline, with fossil
   fuels struck from the draft text and the $120bn adaptation goal deleted.
4. **GTA VI** — Take-Two confirms $3.79 billion and 32.5 million copies in the first
   24 hours: the biggest entertainment launch in history.

## How it is made

The page was drawn in code (Python 3, Pillow) during the build session — drawn at twice
size and scaled down so the type stays crisp — and the finished 1024×1024 page ships in
this repository as `entry.png`. `main.py` publishes it unchanged to `/output/entry.png`,
byte-identical on every run; it reads no input and uses no network. Dating follows the
contest's own rule — events that happened, or were first reported, on 20 November 2026
in any time zone — which is why the Peru earthquake (19:09 local time Friday) is on the
page, while the Shenzhen summit (Thursday), the Voyager 1 milestone (Wednesday) and
Saturday's Hormuz reports are in the DATE CHECK box.
