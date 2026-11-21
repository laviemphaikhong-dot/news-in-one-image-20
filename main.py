# The world of Friday 20 November 2026 on one 1024x1024 newspaper page.
#
# Built after studying the top finishers of the 17 and 18 November editions: their pages are
# drawn, not listed. So this page draws too: every lead and grid story carries a small flat
# illustration drawn in code, a certainty label (CONFIRMED / OFFICIAL / REPORTED) with its
# sources, and a number that matches a pin on the dot world map. Around them sit the furniture
# the winners share: a visual UTC timeline, a big-figure DAY IN NUMBERS strip, story counts by
# region and by field, an ALSO ON FRIDAY column, and a red DATE CHECK box naming the stories
# left off the page because they belong to another day.
#
# The program reads nothing and writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png),
# the same bytes on every run. It draws at twice size and scales down so the type stays crisp,
# and it is laid out to read at three sizes: the date and the leads at thumbnail size, the
# sixteen drawn stories at half size, and all 49 stories at full size.

import os

from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersample factor: all coordinates below are final-page units, scaled by SS
W = 1024
H = 1024

PAPER = (246, 241, 230)
INK = (24, 22, 18)
BODY = (52, 48, 40)
MUTED = (96, 88, 74)
RULE = (38, 34, 28)
WINE = (128, 24, 32)
HAIR = (198, 188, 166)
PANEL = (238, 231, 214)

REGION_COLORS = {
    "Europe": (146, 32, 40),
    "North America": (28, 84, 140),
    "Asia-Pacific": (16, 116, 92),
    "Middle East": (196, 116, 16),
    "Africa": (120, 72, 160),
    "Latin America": (172, 128, 16),
    "Global": (90, 90, 90),
}

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size * SS))


def X(v):
    return v * SS


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W * SS, H * SS), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, font, fill=INK, anchor="la"):
        self.d.text((X(x), X(y)), s, font=font, fill=fill, anchor=anchor)

    def line(self, pts, fill=RULE, w=1):
        self.d.line([(X(a), X(b)) for a, b in pts], fill=fill, width=max(1, int(w * SS)), joint="curve")

    def rect(self, x0, y0, x1, y1, outline=None, fill=None, w=1):
        self.d.rectangle([X(x0), X(y0), X(x1), X(y1)], outline=outline, fill=fill, width=max(1, int(w * SS)))

    def ellipse(self, x0, y0, x1, y1, outline=None, fill=None, w=1):
        self.d.ellipse([X(x0), X(y0), X(x1), X(y1)], outline=outline, fill=fill, width=max(1, int(w * SS)))

    def poly(self, pts, fill=None, outline=None):
        self.d.polygon([(X(a), X(b)) for a, b in pts], fill=fill, outline=outline)

    def arc(self, x0, y0, x1, y1, start, end, fill, w=1.4):
        self.d.arc([X(x0), X(y0), X(x1), X(y1)], start, end, fill=fill, width=max(1, int(w * SS)))

    def dot(self, cx, cy, r, fill):
        self.ellipse(cx - r, cy - r, cx + r, cy + r, fill=fill)

    def tw(self, s, font):
        return self.d.textlength(s, font=font) / SS

    def wrap(self, s, font, width):
        words, lines, cur = s.split(), [], ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if self.tw(trial, font) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


# ---------------------------------------------------------------------------
# Flat illustrations, one per drawn story. Each draws inside the box
# (x, y, w, h) on a tinted panel, in ink with a wine or region accent.
# ---------------------------------------------------------------------------

def icon_missile(p, x, y, w, h, c):
    p.poly([(x + w * .18, y + h * .78), (x + w * .62, y + h * .34), (x + w * .78, y + h * .18),
            (x + w * .82, y + h * .38), (x + w * .66, y + h * .82), (x + w * .46, y + h * .86),
            (x + w * .30, y + h * .70)], fill=INK)
    p.poly([(x + w * .18, y + h * .78), (x + w * .06, y + h * .94), (x + w * .30, y + h * .94)], fill=WINE)
    for dx, dy in [(0.86, 0.62), (0.68, 0.10), (0.92, 0.30)]:
        cx, cy = x + w * dx, y + h * dy
        p.line([(cx - 4, cy), (cx + 4, cy)], fill=WINE, w=1.6)
        p.line([(cx, cy - 4), (cx, cy + 4)], fill=WINE, w=1.6)


def icon_chart(p, x, y, w, h, c):
    p.line([(x + w * .10, y + h * .12), (x + w * .10, y + h * .88), (x + w * .94, y + h * .88)], fill=INK, w=1.6)
    p.line([(x + w * .16, y + h * .26), (x + w * .38, y + h * .40), (x + w * .52, y + h * .34),
            (x + w * .70, y + h * .58), (x + w * .90, y + h * .80)], fill=WINE, w=2.6)
    p.poly([(x + w * .90, y + h * .80), (x + w * .78, y + h * .78), (x + w * .88, y + h * .66)], fill=WINE)


def icon_cloud(p, x, y, w, h, c):
    p.arc(x + w * .16, y + h * .18, x + w * .60, y + h * .62, 180, 360, INK, 2.2)
    p.arc(x + w * .44, y + h * .10, x + w * .84, y + h * .62, 180, 360, INK, 2.2)
    p.line([(x + w * .16, y + h * .40), (x + w * .84, y + h * .40)], fill=INK, w=2.2)
    for fx in (0.30, 0.48, 0.66):
        p.rect(x + w * fx, y + h * .58, x + w * fx + w * .07, y + h * .86, fill=INK)
    p.line([(x + w * .22, y + h * .86), (x + w * .78, y + h * .86)], fill=WINE, w=2.2)


def icon_gamepad(p, x, y, w, h, c):
    p.rect(x + w * .10, y + h * .26, x + w * .90, y + h * .72, outline=INK, w=2.4)
    p.line([(x + w * .24, y + h * .40), (x + w * .24, y + h * .58)], fill=INK, w=2.4)
    p.line([(x + w * .17, y + h * .49), (x + w * .31, y + h * .49)], fill=INK, w=2.4)
    p.dot(x + w * .68, y + h * .42, 3.4, WINE)
    p.dot(x + w * .78, y + h * .52, 3.4, c)
    p.dot(x + w * .62, y + h * .56, 3.4, INK)


def icon_flags(p, x, y, w, h, c):
    p.line([(x + w * .22, y + h * .10), (x + w * .22, y + h * .90)], fill=INK, w=2.2)
    p.line([(x + w * .62, y + h * .10), (x + w * .62, y + h * .90)], fill=INK, w=2.2)
    p.poly([(x + w * .22, y + h * .12), (x + w * .56, y + h * .18), (x + w * .22, y + h * .34)], fill=(28, 84, 140))
    p.poly([(x + w * .62, y + h * .12), (x + w * .94, y + h * .18), (x + w * .62, y + h * .34)], fill=WINE)
    p.dot(x + w * .36, y + h * .22, 2.2, (240, 200, 60))


def icon_jets(p, x, y, w, h, c):
    p.poly([(x + w * .12, y + h * .62), (x + w * .55, y + h * .30), (x + w * .88, y + h * .22),
            (x + w * .60, y + h * .44), (x + w * .88, y + h * .52), (x + w * .48, y + h * .58),
            (x + w * .30, y + h * .76)], fill=INK)
    p.line([(x + w * .10, y + h * .78), (x + w * .34, y + h * .70)], fill=c, w=1.8)
    p.line([(x + w * .08, y + h * .88), (x + w * .30, y + h * .80)], fill=c, w=1.8)


def icon_bridge(p, x, y, w, h, c):
    p.line([(x + w * .06, y + h * .66), (x + w * .94, y + h * .66)], fill=INK, w=2.4)
    for fx in (0.28, 0.72):
        p.line([(x + w * fx, y + h * .30), (x + w * fx, y + h * .84)], fill=INK, w=2.2)
    p.arc(x + w * .02, y + h * .30, x + w * .52, y + h * .66, 180, 360, WINE, 1.8)
    p.arc(x + w * .48, y + h * .30, x + w * .98, y + h * .66, 180, 360, WINE, 1.8)
    for fx in (0.16, 0.36, 0.56, 0.76, 0.90):
        p.line([(x + w * fx, y + h * .80), (x + w * (fx + .05), y + h * .80)], fill=c, w=1.8)


def icon_cyclone(p, x, y, w, h, c):
    cx, cy = x + w * .5, y + h * .48
    for r, a0 in [(w * .36, 20), (w * .27, 140), (w * .18, 260)]:
        p.arc(cx - r, cy - r * .8, cx + r, cy + r * .8, a0, a0 + 250, INK if r > w * .2 else WINE, 2.4)
    p.dot(cx, cy, 3.2, WINE)


def icon_candles(p, x, y, w, h, c):
    for i, (top, bot) in enumerate([(0.20, 0.52), (0.36, 0.66), (0.52, 0.84)]):
        bx = x + w * (0.18 + i * 0.26)
        p.line([(bx + w * .07, y + h * (top - .08)), (bx + w * .07, y + h * (bot + .06))], fill=WINE, w=1.6)
        p.rect(bx, y + h * top, bx + w * .14, y + h * bot, fill=WINE)
    p.line([(x + w * .08, y + h * .90), (x + w * .94, y + h * .90)], fill=INK, w=1.6)


def icon_mic(p, x, y, w, h, c):
    p.rect(x + w * .42, y + h * .10, x + w * .58, y + h * .46, outline=INK, w=2.2)
    p.arc(x + w * .30, y + h * .24, x + w * .70, y + h * .66, 0, 180, INK, 2)
    p.line([(x + w * .50, y + h * .64), (x + w * .50, y + h * .78)], fill=INK, w=2.2)
    p.line([(x + w * .16, y + h * .90), (x + w * .84, y + h * .90)], fill=WINE, w=2.4)
    p.line([(x + w * .24, y + h * .90), (x + w * .30, y + h * .78)], fill=INK, w=1.8)
    p.line([(x + w * .76, y + h * .90), (x + w * .70, y + h * .78)], fill=INK, w=1.8)


def icon_tanker(p, x, y, w, h, c):
    p.poly([(x + w * .08, y + h * .58), (x + w * .92, y + h * .58), (x + w * .82, y + h * .76), (x + w * .18, y + h * .76)], fill=INK)
    p.rect(x + w * .20, y + h * .44, x + w * .66, y + h * .58, fill=c)
    p.rect(x + w * .70, y + h * .34, x + w * .80, y + h * .58, outline=INK, w=1.8)
    p.poly([(x + w * .50, y + h * .16), (x + w * .56, y + h * .34), (x + w * .44, y + h * .34)], fill=WINE)
    p.line([(x + w * .10, y + h * .86), (x + w * .30, y + h * .86), (x + w * .50, y + h * .86), (x + w * .70, y + h * .86), (x + w * .90, y + h * .86)], fill=(28, 84, 140), w=2)


def icon_houses(p, x, y, w, h, c):
    for i, fx in enumerate((0.10, 0.40, 0.68)):
        p.poly([(x + w * fx, y + h * .58), (x + w * (fx + .13), y + h * .42), (x + w * (fx + .26), y + h * .58)], fill=INK)
        p.rect(x + w * (fx + .03), y + h * .58, x + w * (fx + .23), y + h * .82, outline=INK, w=1.8)
    cx, cy = x + w * .82, y + h * .18
    for a in range(0, 360, 45):
        import math
        p.line([(cx, cy), (cx + 7 * math.cos(math.radians(a)), cy + 7 * math.sin(math.radians(a)))], fill=WINE, w=1.8)
    p.dot(cx, cy, 2.6, WINE)


def icon_virus(p, x, y, w, h, c):
    import math
    cx, cy = x + w * .5, y + h * .5
    for a in range(0, 360, 30):
        ex, ey = cx + w * .34 * math.cos(math.radians(a)), cy + h * .34 * math.sin(math.radians(a))
        p.line([(cx, cy), (ex, ey)], fill=c, w=2)
        p.dot(ex, ey, 3, c)
    p.dot(cx, cy, w * .17, c)
    p.dot(cx - 3, cy - 2, 2.2, PAPER)
    p.dot(cx + 4, cy + 3, 1.8, PAPER)


def icon_flood(p, x, y, w, h, c):
    p.poly([(x + w * .30, y + h * .40), (x + w * .50, y + h * .22), (x + w * .70, y + h * .40)], fill=INK)
    p.rect(x + w * .36, y + h * .40, x + w * .64, y + h * .58, outline=INK, w=1.8)
    for fy in (0.66, 0.80):
        pts = [(x + w * (0.06 + i * 0.055), y + h * fy + (3 if i % 2 else -3)) for i in range(17)]
        p.line(pts, fill=(28, 84, 140), w=2.2)


def icon_storm(p, x, y, w, h, c):
    p.poly([(x + w * .26, y + h * .52), (x + w * .48, y + h * .34), (x + w * .70, y + h * .52)], fill=INK)
    p.rect(x + w * .32, y + h * .52, x + w * .64, y + h * .78, outline=INK, w=1.8)
    for fy, ln in [(0.20, 0.30), (0.30, 0.22)]:
        p.arc(x + w * .58, y + h * (fy - .08), x + w * (.58 + ln), y + h * (fy + .10), 300, 120, c, 2)
    p.poly([(x + w * .16, y + h * .30), (x + w * .24, y + h * .30), (x + w * .18, y + h * .48), (x + w * .27, y + h * .44), (x + w * .14, y + h * .62), (x + w * .20, y + h * .42), (x + w * .13, y + h * .42)], fill=(206, 158, 24))


def icon_coin(p, x, y, w, h, c):
    cx, cy, r = x + w * .5, y + h * .5, w * .34
    p.ellipse(cx - r, cy - r, cx + r, cy + r, outline=(206, 158, 24), w=3)
    f = F(SERIF_B, h * .52)
    p.text(cx, cy - h * .27, "B", f, fill=(206, 158, 24), anchor="ma")
    p.line([(cx - 3, cy - r * .62), (cx - 3, cy + r * .62)], fill=(206, 158, 24), w=2)
    p.line([(cx + 3, cy - r * .62), (cx + 3, cy + r * .62)], fill=(206, 158, 24), w=2)


ICONS = {
    "missile": icon_missile, "chart": icon_chart, "cloud": icon_cloud, "gamepad": icon_gamepad,
    "flags": icon_flags, "jets": icon_jets, "bridge": icon_bridge, "cyclone": icon_cyclone,
    "candles": icon_candles, "mic": icon_mic, "tanker": icon_tanker, "houses": icon_houses,
    "virus": icon_virus, "flood": icon_flood, "storm": icon_storm, "coin": icon_coin,
}


# ---------------------------------------------------------------------------
# The day's stories: (headline, summary, region, field, certainty, sources, icon).
# Numbered in reading order: leads 1-4, the grid 5-16, Also on Friday 17-48.
# Every item was checked against the wire record for Friday 20 November 2026 (UTC).
# ---------------------------------------------------------------------------

LEADS = [
    ("Russian missiles fall on Poland as Moscow rains 400 drones on Ukraine",
     "A Kh-101 missile, a second missile and a jet drone came down in south-eastern Poland overnight, near a multinational exercise; PM Tusk called it an \u201cintentional provocation\u201d. The barrage behind it \u2014 400+ drones, 110+ missiles \u2014 killed at least 8 in Kyiv and Lviv.",
     "Europe", "War & security", "CONFIRMED", "AP \u00b7 Al Jazeera \u00b7 AFP", "missile"),
    ("Wall Street crashes: Nasdaq \u22125.28%, Nvidia plunges 14%",
     "The Nasdaq lost 1,261 points \u2014 its second-largest point fall ever \u2014 and the S&P 500 slid 3.70% into correction. Nvidia fell 14% on reports of an SEC accounting probe; gold posted its worst week since March.",
     "North America", "Markets", "CONFIRMED", "AP \u00b7 WSJ", "chart"),
    ("COP31 blows its deadline: plenary suspended, fossil fuels struck from the text",
     "Antalya's closing plenary was suspended overnight after the 18:00 deadline passed with no deal. Friday's draft deleted every mention of fossil fuels and the $120bn adaptation goal.",
     "Global", "Climate", "REPORTED", "Xinhua \u00b7 UN News", "cloud"),
    ("GTA VI is the biggest entertainment launch in history: $3.79bn in 24 hours",
     "Take-Two confirmed Friday that Thursday's launch grossed $3.79 billion and sold 32.5 million copies in 24 hours \u2014 records for any entertainment product. Its shares even rose as markets crashed.",
     "North America", "Culture", "OFFICIAL", "Take-Two via WSJ", "gamepad"),
]

GRID = [
    ("UK and EU sign post-Brexit \u201creset\u201d deal in Brussels",
     "A common food-trade area, linked carbon markets from 2028 and youth mobility for 100,000 people each way from 2030; PM Burnham says it adds \u00a317bn to UK GDP.",
     "Europe", "Diplomacy", "CONFIRMED", "Le Monde \u00b7 CGTN", "flags"),
    ("NATO scrambles jets over Poland; Rutte condemns \u201cgrave violations\u201d",
     "Polish, Swedish and Dutch jets scrambled after the overnight incursions; the NATO secretary-general was due in Warsaw on Saturday.",
     "Europe", "War & security", "CONFIRMED", "Al Jazeera \u00b7 ISW", "jets"),
    ("Kyiv's Dnipro bridges and a water plant hit; nuclear output cut",
     "Three bridges and a water facility were struck, killing 3 workers; a hospital was hit in Zaporizhzhia region, and Kyiv plus 10 regions lost power.",
     "Europe", "War & security", "CONFIRMED", "AFP \u00b7 NHK", "bridge"),
    ("Cyclone Akvan comes ashore in Odisha; some 370,000 evacuated",
     "Landfall near Gopalpur at 02:00\u201303:00 UTC, winds gusting to 90 km/h; 423 rescue teams deployed and no major loss of life reported.",
     "Asia-Pacific", "Climate", "OFFICIAL", "IMD via The Hindu", "cyclone"),
    ("Asian bourses plunge: Nikkei \u22125.06%, KOSPI \u22125.21%, Taiwan \u22126.2%",
     "Taiwan's Taiex posted its worst week since 1990, down 17.5%; MSCI Asia-Pacific ex-Japan had its worst week since March 2020.",
     "Asia-Pacific", "Markets", "CONFIRMED", "Reuters", "candles"),
    ("Trump defends Shenzhen summit in a 90-minute White House presser",
     "He displayed the peace declaration on an easel, praised \u201cfantastic relationships\u201d with Xi and Putin, and threatened a tax on US firms building data centres abroad.",
     "North America", "Diplomacy", "CONFIRMED", "AP \u00b7 AFP", "mic"),
    ("Tanker struck and set ablaze off Khasab as the Hormuz crisis grows",
     "An outbound tanker was hit by an unknown projectile 8 nautical miles north of Khasab and caught fire on deck; no casualties were reported.",
     "Middle East", "War & security", "REPORTED", "Reuters", "tanker"),
    ("Israeli strikes kill six in Gaza despite the ceasefire",
     "Gaza's civil defence reported six dead near Bureij camp, Deir al-Balah and Nuseirat; the IDF said it had struck Hamas operatives at a meeting.",
     "Middle East", "War & security", "CONFIRMED", "AFP \u00b7 Al Jazeera", "houses"),
    ("Ebola in Congo: 11,613 cases and 5,678 deaths \u2014 as of 17 November",
     "WHO's latest bulletin keeps the outbreak a global health emergency: 68 health zones across 8 provinces, with transmission ongoing in 48 of them.",
     "Africa", "Health", "OFFICIAL", "WHO", "virus"),
    ("Vietnam floods: 10,529 people evacuated in Gia Lai alone on Friday",
     "Police and authorities moved 2,850 households and rescued 766 trapped residents as some 68,000 homes stood submerged across three provinces.",
     "Asia-Pacific", "Climate", "REPORTED", "VOV", "flood"),
    ("Storm kills 3 and destroys some 5,000 homes in southern Brazil",
     "Winds of 114 km/h \u2014 possibly a tornado \u2014 struck Tupanciret\u00e3, Rio Grande do Sul, before dawn, leaving the town without power or water.",
     "Latin America", "Climate", "REPORTED", "AFP", "storm"),
    ("Bitcoin crashes through $60,000 to a two-year low near $55,830",
     "About $2\u20132.4bn of leveraged crypto bets were liquidated in 24 hours as the AI-stock rout spread; the Fear & Greed index hit 11 \u2014 extreme fear.",
     "Global", "Markets", "CONFIRMED", "Reuters \u00b7 CoinDesk", "coin"),
]

# Also on Friday: (one line, region, field). Numbers 17-48.
ALSO = [
    ("UNICEF: 1,144 Ukrainian children killed or injured in 2026 \u2014 a three-year high", "Europe", "Society"),
    ("Russia rushes 20bn roubles (~$244m) to a road bypassing the Kerch bridge", "Europe", "War & security"),
    ("Ryabkov: even \u201calmost NATO\u201d status for Ukraine is unacceptable", "Europe", "Diplomacy"),
    ("Kane tears ankle ligaments as Bayern are held 1\u20131 by Cologne; out for months", "Europe", "Sport"),
    ("Nations League quarter-final draw: Spain v France, England v Norway", "Europe", "Sport"),
    ("Medvedev beats Tiafoe in Turin to complete the ATP Finals semi-final line-up", "Europe", "Sport"),
    ("Drone secretly films Pochettino's first Manchester United training session", "Europe", "Sport"),
    ("UK retail sales beat forecasts; October public borrowing \u00a317.0bn \u2014 ONS", "Europe", "Markets"),
    ("Gold falls about 4% to near $3,540/oz \u2014 its worst week since March", "North America", "Markets"),
    ("Anthropic slides ~9% on day two of trading; oil bucks the rout, WTI +1.1%", "North America", "Markets"),
    ("Lawmakers near a bipartisan deal to ban Chinese cars, sparing Mercedes-Benz", "North America", "Markets"),
    ("St. Johns River at record 18.75 ft as Florida flooding continues; 150+ rescues", "North America", "Climate"),
    ("Russell fastest in final Las Vegas practice; stewards review Verstappen clash", "North America", "Sport"),
    ("Xi meets Malaysia's Anwar Ibrahim in Shenzhen, offers deeper cooperation", "Asia-Pacific", "Diplomacy"),
    ("Xi and Singapore's Lawrence Wong agree talks on a \u201cVersion 4.0\u201d trade upgrade", "Asia-Pacific", "Diplomacy"),
    ("China and Indonesia launch talks on a comprehensive economic partnership", "Asia-Pacific", "Diplomacy"),
    ("Myanmar's junta calls the ICJ Rohingya ruling \u201cunfair\u201d; China criticises it too", "Asia-Pacific", "Diplomacy"),
    ("Malaysia to relocate 10,000 Rohingya refugees to T\u00fcrkiye", "Asia-Pacific", "Diplomacy"),
    ("Australia takes delivery of two more MH-60R Seahawk helicopters", "Asia-Pacific", "War & security"),
    ("Australia marks one billion identity checks on its verification service", "Asia-Pacific", "Society"),
    ("Australia opens an independent review of abuse-related veterans' claims", "Asia-Pacific", "Society"),
    ("All 84 residents of Nassau, Cook Islands, safe as Cyclone Xavier weakens", "Asia-Pacific", "Climate"),
    ("Missile strikes Iran's Qeshm island in the Strait of Hormuz", "Middle East", "War & security"),
    ("Qatari delegation holds two hours of mediation talks in Tehran", "Middle East", "Diplomacy"),
    ("Peace board adviser: unblock Gaza rebuilding or the UN takes over", "Middle East", "Diplomacy"),
    ("Army coalition opens new fronts in eastern DR Congo, FRN statement says", "Africa", "War & security"),
    ("Six people shot dead in an overnight village attack in North Kivu, DR Congo", "Africa", "War & security"),
    ("Three killed in Gombe, Nigeria, in alleged air force shooting", "Africa", "Society"),
    ("UN Security Council holds closed consultations on Sudan", "Africa", "Diplomacy"),
    ("Tesla opens its first store in Argentina; Model 3 priced from $40,990", "Latin America", "Markets"),
    ("Caravan of some 300 migrants crosses into southern Mexico, heading north", "Latin America", "Society"),
    ("M6.7 earthquake strikes Peru's Jun\u00edn region at 19:09 local time; felt in Lima", "Latin America", "Climate"),
    ("World stocks fall for a seventh straight session \u2014 longest streak since 2023", "Global", "Markets"),
]

TIMELINE = [
    ("Overnight", "Missiles down in Poland"),
    ("02:30", "Cyclone Akvan landfall"),
    ("06:00", "Assault on Bunyakiri"),
    ("13:00", "UK\u2013EU reset signed"),
    ("17:00", "Trump defends summit"),
    ("18:00", "COP31 deadline passes"),
    ("19:39", "Qeshm island struck"),
]

NUMBERS = [
    ("\u22125.28%", "Nasdaq's fall \u2014 1,261 points, its 2nd-largest point drop ever"),
    ("$3.79bn", "GTA VI's first 24 hours \u2014 32.5 million copies sold"),
    ("400+", "drones fired at Ukraine overnight, with 110+ missiles"),
    ("\u221214%", "Nvidia in one day, on reports of an SEC accounting probe"),
    ("370,000", "people evacuated in Odisha ahead of Cyclone Akvan"),
    ("11,613", "Ebola cases in DR Congo, with 5,678 deaths (as of 17 Nov)"),
]

DATE_CHECK = [
    "Shenzhen summit & its peace declaration \u2014 Thu 19 Nov (Friday brought the aftermath)",
    "Voyager 1's one-light-day milestone \u2014 Wed 18 Nov",
    "ICJ Rohingya judgment \u2014 Thu 19 Nov (Friday brought the reactions)",
    "Anthropic's Nasdaq debut \u2014 Thu 19 Nov (Friday: its 9% slide)",
    "Two more tankers hit at Hormuz \u2014 reported Sat 21 Nov",
    "ADF attack on Cantine, DR Congo \u2014 reported without a date",
]

# Pins for the drawn stories 1-15: (fraction across the map box, fraction down, region).
# Story 16 (bitcoin) has no pin: it trades everywhere.
PINS = {
    1: (0.578, 0.225, "Europe"), 2: (0.302, 0.265, "North America"), 3: (0.560, 0.335, "Global"),
    4: (0.270, 0.405, "North America"), 5: (0.494, 0.20, "Europe"), 6: (0.540, 0.16, "Europe"),
    7: (0.606, 0.262, "Europe"), 8: (0.736, 0.44, "Asia-Pacific"), 9: (0.888, 0.33, "Asia-Pacific"),
    10: (0.272, 0.325, "North America"), 11: (0.656, 0.40, "Middle East"), 12: (0.598, 0.378, "Middle East"),
    13: (0.569, 0.585, "Africa"), 14: (0.80, 0.485, "Asia-Pacific"), 15: (0.351, 0.795, "Latin America"),
}

# A dot-matrix world: rows run north to south on an equirectangular grid; '#' is land.
MAP_ROWS = [
    "..........................................................................................",
    "..........####............................................................................",
    "......###########.......####..............................................................",
    "....###############....#################......##########################################..",
    "...################..####################...#############################################.",
    "....################.#####################.##############################################.",
    ".....##############..####################..############################################...",
    "......##########......#################.....######..##################################....",
    ".......########........###############........###....#####..########..################....",
    "........######..........#############.................###.....#####......###########......",
    ".........#####...........###########..................##.......###.........########.......",
    "..........####............#########........................................#######........",
    "...........###.............#######..........................................######........",
    "...........##...............#####..............................##............#####........",
    ".............................###..............................####............####........",
    ".............................##..............................######............###........",
    "............................###.............................##########.....................",
    "............................###............................############....................",
    "............................####..........................############....................",
    "............................#####........................#########..##....................",
    "............................######......................#########.........................",
    "............................#######....................########...........................",
    ".............................######....................#######............................",
    ".............................#####.....................######.....................####......",
    "..............................####.....................#####....................##########...",
    "..............................###......................####....................##########...",
    "..............................##.......................###......................########....",
    "........................................................##.........................####.......",
    "..........................................................................................",
    "..........................................................................................",
]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def tag_line(p, x, y, region, cert, sources, size=6.8):
    f_b = F(SANS_B, size)
    p.text(x, y, region.upper(), f_b, fill=REGION_COLORS[region])
    x += p.tw(region.upper(), f_b)
    p.text(x, y, "  \u00b7  " + cert, f_b, fill=WINE)
    x += p.tw("  \u00b7  " + cert, f_b)
    p.text(x, y, "  \u00b7  " + sources, F(SANS, size), fill=MUTED)


def draw_map(p, x, y, w, h):
    rows = MAP_ROWS
    cols = len(rows[0])
    cw, ch = w / cols, h / len(rows)
    r = min(cw, ch) * 0.30
    for ri, row in enumerate(rows):
        for ci, chh in enumerate(row):
            if chh == "#":
                p.dot(x + (ci + 0.5) * cw, y + (ri + 0.5) * ch, r, (178, 168, 142))
    for num, (fx, fy, region) in PINS.items():
        cx, cy = x + fx * w, y + fy * h
        p.dot(cx, cy, 7.6, REGION_COLORS[region])
        f = F(SANS_B, 7.2)
        label = str(num)
        p.text(cx - p.tw(label, f) / 2, cy - 4.2, label, f, fill=(255, 255, 255))


def lead_one(p):
    item = LEADS[0]
    p.rect(28, 100, 168, 240, fill=PANEL)
    ICONS[item[6]](p, 40, 112, 116, 116, REGION_COLORS[item[2]])
    x = 184
    p.text(x, 98, "1", F(SERIF_B, 17), fill=WINE)
    f_h = F(SERIF_B, 20.5)
    ly = 96
    for ln in p.wrap(item[0], f_h, 372)[:3]:
        p.text(x + 22, ly, ln, f_h)
        ly += 24
    tag_line(p, x + 22, ly + 1, item[2], item[4], item[5], size=7.4)
    ly += 15
    for ln in p.wrap(item[1], F(SANS, 10), 398)[:6]:
        p.text(x, ly, ln, F(SANS, 10), fill=BODY)
        ly += 13.2


def lead_block(p, x, y, w, num, item):
    p.rect(x, y, x + w, y + 46, fill=PANEL)
    ICONS[item[6]](p, x + 8, y + 4, 38, 38, REGION_COLORS[item[2]])
    p.text(x + w - 8, y + 6, str(num), F(SERIF_B, 19), fill=WINE, anchor="ra")
    f_h = F(SERIF_B, 12.5)
    ly = y + 52
    for ln in p.wrap(item[0], f_h, w)[:2]:
        p.text(x, ly, ln, f_h)
        ly += 15
    tag_line(p, x, ly + 1, item[2], item[4], item[5])
    ly += 13
    for ln in p.wrap(item[1], F(SANS, 9), w)[:4]:
        p.text(x, ly, ln, F(SANS, 9), fill=BODY)
        ly += 11.8


def grid_block(p, x, y, w, num, item):
    p.rect(x, y, x + 54, y + 54, fill=PANEL)
    ICONS[item[6]](p, x + 6, y + 6, 42, 42, REGION_COLORS[item[2]])
    tx = x + 62
    tw_ = w - 62
    p.text(tx, y - 1, str(num), F(SERIF_B, 12.5), fill=WINE)
    nw = p.tw(str(num), F(SERIF_B, 12.5)) + 4
    f_h = F(SERIF_B, 10.8)
    ly = y
    for ln in p.wrap(item[0], f_h, tw_ - nw)[:2]:
        p.text(tx + nw, ly, ln, f_h)
        ly += 13
    if len(p.wrap(item[0], f_h, tw_ - nw)) == 1:
        ly = y + 13
    tag_line(p, tx, ly + 1, item[2], item[4], item[5], size=6.4)
    ly += 12
    for ln in p.wrap(item[1], F(SANS, 8.5), tw_)[:3]:
        p.text(tx, ly, ln, F(SANS, 8.5), fill=BODY)
        ly += 10.8


def build():
    p = Page()

    # --- Masthead ------------------------------------------------------------
    p.text(W / 2, 12, "T H E   D A I L Y   W O R L D", F(SERIF_B, 25), anchor="ma")
    p.line([(28, 48), (W - 28, 48)], w=2.2)
    p.line([(28, 52), (W - 28, 52)], w=0.7)
    p.text(28, 58, "Friday 20 November 2026", F(SERIF_I, 11.5))
    p.text(W / 2, 59, "49 stories \u00b7 7 regions \u00b7 every story checked against the wire record for this date",
           F(SANS, 9.3), fill=MUTED, anchor="ma")
    p.text(W - 28, 58, "UTC day edition", F(SERIF_I, 11.5), anchor="ra")

    counts, fcounts = {}, {}
    for it in LEADS + GRID:
        counts[it[2]] = counts.get(it[2], 0) + 1
        fcounts[it[3]] = fcounts.get(it[3], 0) + 1
    for _, region, field in ALSO:
        counts[region] = counts.get(region, 0) + 1
        fcounts[field] = fcounts.get(field, 0) + 1
    reg_line = "  \u00b7  ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
    p.text(28, 79, reg_line, F(SANS_B, 7.6), fill=MUTED)
    sure = "HOW SURE \u2014 CONFIRMED: 2+ outlets \u00b7 OFFICIAL: on record \u00b7 REPORTED: one wire"
    p.text(W - 28, 79, sure, F(SANS, 7.6), fill=WINE, anchor="ra")
    fld_line = "BY FIELD \u2014 " + " \u00b7 ".join(f"{k} {v}" for k, v in sorted(fcounts.items(), key=lambda kv: -kv[1]))
    p.text(28, 89, fld_line, F(SANS, 7.6), fill=MUTED)
    p.line([(28, 96), (W - 28, 96)], w=0.8)

    # --- Lead story + map ------------------------------------------------------
    lead_one(p)
    p.rect(612, 96, 996, 250, outline=HAIR, w=0.8)
    p.text(622, 101, "WHERE IT HAPPENED", F(SANS_B, 8), fill=MUTED)
    draw_map(p, 622, 114, 364, 112)
    p.text(622, 231, "Pins 1\u201315 mark where the drawn stories happened;", F(SERIF_I, 8.3), fill=MUTED)
    p.text(622, 241, "story 16 (bitcoin) trades everywhere.", F(SERIF_I, 8.3), fill=MUTED)

    # --- Leads 2-4 ---------------------------------------------------------------
    p.line([(28, 256), (W - 28, 256)], w=0.8)
    colw = (W - 56 - 40) / 3
    for i, item in enumerate(LEADS[1:4]):
        x = 28 + i * (colw + 20)
        lead_block(p, x, 262, colw, i + 2, item)
        if i:
            p.line([(x - 10, 262), (x - 10, 396)], fill=HAIR, w=0.7)

    # --- UTC timeline --------------------------------------------------------------
    p.line([(28, 406), (W - 28, 406)], w=0.8)
    p.text(28, 414, "THE DAY\nIN UTC", F(SANS_B, 8.5), fill=WINE)
    tx0, tx1 = 118, 988
    p.line([(tx0, 424), (tx1, 424)], fill=RULE, w=1.1)
    step = (tx1 - tx0) / (len(TIMELINE) - 1)
    for i, (utc, label) in enumerate(TIMELINE):
        cx = tx0 + i * step
        p.dot(cx, 424, 3.4, WINE)
        p.text(cx, 411, utc, F(SANS_B, 8.8), anchor="ma")
        for j, ln in enumerate(p.wrap(label, F(SANS, 7.4), 118)):
            p.text(cx, 430 + j * 9.2, ln, F(SANS, 7.4), fill=MUTED, anchor="ma")

    # --- Grid 5-16 -------------------------------------------------------------------
    gy = 458
    for r in range(4):
        y = gy + r * 74
        if r:
            p.line([(28, y - 5), (W - 28, y - 5)], fill=HAIR, w=0.7)
        for c in range(3):
            idx = r * 3 + c
            x = 28 + c * (colw + 20)
            grid_block(p, x, y, colw, idx + 5, GRID[idx])
            if c:
                p.line([(x - 10, y), (x - 10, y + 62)], fill=HAIR, w=0.7)

    # --- Day in numbers ------------------------------------------------------------------
    ny = 758
    p.line([(28, ny), (W - 28, ny)], w=0.8)
    p.text(28, ny + 4, "THE DAY IN NUMBERS", F(SANS_B, 8.5), fill=WINE)
    bw = (W - 56 - 5 * 8) / 6
    for i, (fig, cap) in enumerate(NUMBERS):
        x = 28 + i * (bw + 8)
        p.text(x + bw / 2, ny + 12, fig, F(SERIF_B, 15.5), anchor="ma")
        for j, ln in enumerate(p.wrap(cap, F(SANS, 7.1), bw - 4)[:2]):
            p.text(x + bw / 2, ny + 33 + j * 8.4, ln, F(SANS, 7.1), fill=MUTED, anchor="ma")

    # --- Also on Friday ---------------------------------------------------------------------
    ay = 816
    p.line([(28, ay), (W - 28, ay)], w=1.6)
    p.text(28, ay + 4, "ALSO ON FRIDAY", F(SERIF_B, 12.5), fill=WINE)
    p.text(W - 28, ay + 7, "stories 17\u201349 \u00b7 the rest of the day, one line each", F(SANS, 8.3), fill=MUTED, anchor="ra")
    acolw = (W - 56 - 24) / 3
    per = (len(ALSO) + 2) // 3
    for col in range(3):
        x = 28 + col * (acolw + 12)
        yy = ay + 24
        for j, (line_, region, _f) in enumerate(ALSO[col * per:(col + 1) * per]):
            num = 17 + col * per + j
            f_n = F(SANS_B, 7.3)
            tag = f"{num} "
            p.text(x, yy, tag, f_n, fill=WINE)
            nw = p.tw(tag, f_n)
            lines = p.wrap(line_, F(SANS, 7.3), acolw - nw)
            for k, ln in enumerate(lines[:2]):
                p.text(x + nw, yy + k * 8.6, ln, F(SANS, 7.3), fill=BODY)
            yy += 8.6 * len(lines[:2]) + 1.2

    # --- Date check ----------------------------------------------------------------------------
    dy = 950
    p.rect(28, dy, W - 28, dy + 42, outline=WINE, w=1.2)
    p.text(38, dy + 5, "DATE CHECK", F(SANS_B, 9), fill=WINE)
    p.text(38 + p.tw("DATE CHECK", F(SANS_B, 9)) + 6, dy + 5.5,
           "\u2014 checked, and left out as older news or not yet Friday:", F(SANS, 8), fill=MUTED)
    per_col = (len(DATE_CHECK) + 2) // 3
    for col in range(3):
        x = 38 + col * ((W - 76) / 3 + 2)
        for j, item in enumerate(DATE_CHECK[col * per_col:(col + 1) * per_col]):
            p.text(x, dy + 19 + j * 10.2, "\u00b7 " + item, F(SANS, 7.0), fill=BODY)

    # --- Footer -----------------------------------------------------------------------------------
    p.text(W / 2, 998,
           "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 Al Jazeera \u00b7 WSJ \u00b7 Xinhua \u00b7 UN News \u00b7 WHO \u00b7 UNICEF \u00b7 VOV \u00b7 Le Monde \u00b7 CoinDesk \u00b7 ISW \u2014 original drawings, made in code",
           F(SANS, 7.3), fill=MUTED, anchor="ma")
    p.text(W / 2, 1009,
           "Reads at three sizes: the date and 4 leads at thumbnail \u00b7 the 16 drawn stories at half size \u00b7 all 49 stories at full size",
           F(SERIF_I, 8), fill=MUTED, anchor="ma")

    return p.img.resize((W, H), Image.LANCZOS)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    build().save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
