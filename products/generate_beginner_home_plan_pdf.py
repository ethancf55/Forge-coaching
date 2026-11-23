#!/usr/bin/env python3
"""
Forge Coaching — 4-Week Beginner Full-Body Home Plan
Premium digital product PDF (Fiverr-ready).
"""

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = (
    Path(__file__).resolve().parent
    / "Forge-Coaching-4-Week-Beginner-Full-Body-Home-Plan.pdf"
)

W, H = letter  # 612 x 792

# Brand palette (Forge Coaching)
BG = HexColor("#0d0d0f")
BG_CARD = HexColor("#16161a")
BG_ELEV = HexColor("#1e1e24")
LINE = HexColor("#2a2a32")
ORANGE = HexColor("#f97316")
ORANGE_DIM = HexColor("#ea580c")
TEXT = HexColor("#f4f4f5")
MUTED = HexColor("#a1a1aa")
DIM = HexColor("#71717a")
GREEN = HexColor("#4ade80")
RED_SOFT = HexColor("#f87171")


def draw_bg(c: canvas.Canvas):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_footer(c: canvas.Canvas, page: int, total: int, label: str = ""):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(0.7 * inch, 0.55 * inch, W - 0.7 * inch, 0.55 * inch)
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    left = "FORGE COACHING"
    if label:
        left = f"FORGE COACHING  ·  {label}"
    c.drawString(0.7 * inch, 0.35 * inch, left)
    c.drawRightString(W - 0.7 * inch, 0.35 * inch, f"{page} / {total}")


def draw_header_bar(c: canvas.Canvas, title: str):
    c.setFillColor(BG_CARD)
    c.rect(0, H - 0.72 * inch, W, 0.72 * inch, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, H - 0.72 * inch, 4, 0.72 * inch, fill=1, stroke=0)
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawString(0.7 * inch, H - 0.32 * inch, "FORGE COACHING")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.7 * inch, H - 0.52 * inch, title)


def rounded_rect(c, x, y, w, h, r=8, fill=BG_CARD, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.8)
        c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)


def wrap_text(c, text, font, size, max_width):
    c.setFont(font, size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = f"{cur} {w}".strip()
        if c.stringWidth(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_paragraph(c, text, x, y, max_width, font="Helvetica", size=10, color=MUTED, leading=14):
    lines = wrap_text(c, text, font, size, max_width)
    c.setFillColor(color)
    c.setFont(font, size)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def draw_bullet(c, text, x, y, max_width, bullet="•", size=9.5, color=MUTED, leading=13):
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, bullet)
    return draw_paragraph(c, text, x + 12, y, max_width - 12, size=size, color=color, leading=leading)


# ---------------------------------------------------------------------------
# CONTENT
# ---------------------------------------------------------------------------

TOTAL = 10

EXERCISES = {
    "squat": {
        "name": "Bodyweight Squat (or Goblet Squat)",
        "cues": "Feet about shoulder-width. Sit hips back and down. Knees track over toes. Chest tall. Stand by driving through mid-foot.",
        "mistakes": "Heels lifting · Knees collapsing inward · Rounding the lower back · Rushing the bottom",
    },
    "push": {
        "name": "Push-Up (regress or progress as needed)",
        "cues": "Hands under shoulders. Body in a straight line. Lower chest toward floor with control. Press up without flaring elbows wide.",
        "mistakes": "Hips sagging · Half reps · Elbows flared to 90° · Holding breath",
    },
    "hinge": {
        "name": "Glute Bridge → Single-Leg Bridge",
        "cues": "Feet flat, ribs down. Squeeze glutes to lift hips. Pause 1 second at the top. Lower with control.",
        "mistakes": "Overarching the lower back · Pushing only through toes · No pause at top",
    },
    "row": {
        "name": "Inverted Row / Table Row / Backpack Row",
        "cues": "Pull elbows back. Squeeze shoulder blades together at the top. Keep ribs down. Lower under control.",
        "mistakes": "Shrugging hard · Yanking with arms only · Cutting the range short",
    },
    "press": {
        "name": "Pike Push-Up or Overhead Press (DB/backpack)",
        "cues": "Hips high for pike push-ups. Lower head toward floor between hands. Press up strong. Keep core braced.",
        "mistakes": "Collapsed core · Partial range · Elbows flaring without control",
    },
    "core": {
        "name": "Dead Bug or Front Plank",
        "cues": "Ribs down, low back gently pressed toward floor (dead bug). Move limbs slow. Breathe steadily.",
        "mistakes": "Arching the low back · Holding breath · Racing through reps",
    },
    "split": {
        "name": "Reverse Lunge or Split Squat",
        "cues": "Step back, lower rear knee under control. Front shin mostly vertical. Drive through front mid-foot to stand.",
        "mistakes": "Front knee collapsing · Tiny range · Leaning hard forward",
    },
    "carry": {
        "name": "Suitcase Carry or March in Place (loaded if possible)",
        "cues": "Tall posture. Brace core. Slow, controlled steps. Don’t lean into the load.",
        "mistakes": "Side-bending · Shuffling fast · Dropping the free shoulder",
    },
}

# Week prescriptions: (sets, reps, rest_sec, note)
WEEKS = {
    1: {
        "theme": "Learn the pattern. Clean reps beat hard reps.",
        "freq": "3 sessions · ~35–45 min",
        "focus": "Master form. Leave 2–3 reps in reserve on every set.",
        "prescription": {
            "squat": (3, "8–10", 90, "Bodyweight. 2-sec lower."),
            "push": (3, "6–10", 90, "Knees OK if needed. Full range."),
            "hinge": (3, "10–12", 60, "2-sec squeeze at top."),
            "row": (3, "8–10", 90, "Pause 1 sec at top."),
            "press": (2, "6–8", 90, "Pike or light OH press."),
            "core": (2, "8/side or 20–30s", 45, "Quality over time."),
        },
        "finisher": "Optional: 5–8 min brisk walk or easy bike after training.",
    },
    2: {
        "theme": "Add quality volume. Same moves, cleaner work.",
        "freq": "3 sessions · ~40–50 min",
        "focus": "Add 1–2 reps per set where form stays solid. Or slow the eccentric.",
        "prescription": {
            "squat": (3, "10–12", 90, "3-sec lower if bodyweight feels easy."),
            "push": (3, "8–12", 90, "Move toward standard push-ups."),
            "hinge": (3, "12–15", 60, "Add backpack on hips if easy."),
            "row": (3, "10–12", 90, "Harder angle or more load."),
            "press": (3, "6–10", 90, "One more set than Week 1."),
            "core": (3, "8/side or 30–40s", 45, "One extra set."),
        },
        "finisher": "Optional: 8–10 min walk. Keep it easy — this is recovery, not a second workout.",
    },
    3: {
        "theme": "Progress the variation. Make the same effort harder.",
        "freq": "3 sessions · ~45–55 min",
        "focus": "Harder variations or added load. Still leave ~1–2 clean reps in the tank.",
        "prescription": {
            "squat": (4, "8–12", 90, "Goblet/backpack if available. Or pause squats."),
            "push": (3, "8–12", 90, "Feet elevated if standard is easy."),
            "hinge": (3, "8–10/leg", 75, "Single-leg bridge progression."),
            "row": (4, "8–12", 90, "Heavier pack or steeper angle."),
            "press": (3, "6–10", 90, "Deeper pike or more load."),
            "core": (3, "10/side or 35–45s", 45, "Dead bug preferred."),
            "split": (2, "8–10/leg", 75, "Add reverse lunges this week."),
        },
        "finisher": "Optional suitcase carry: 2 x 30–40s/side if you have a loaded bag.",
    },
    4: {
        "theme": "Peak week. Best form under more demand.",
        "freq": "3 sessions · ~45–55 min",
        "focus": "Best sets of the block. Track reps. Note what improved since Week 1.",
        "prescription": {
            "squat": (4, "10–12", 90, "Hardest clean variation you own."),
            "push": (4, "8–12", 90, "Same — progress variation, not ego."),
            "hinge": (3, "10/leg or 12–15", 75, "Single-leg or loaded bridge."),
            "row": (4, "10–12", 90, "Controlled tempo every rep."),
            "press": (3, "8–10", 90, "Strong, full range."),
            "core": (3, "10/side or 40–50s", 45, "Steady breathing."),
            "split": (3, "8–10/leg", 75, "Even left/right quality."),
        },
        "finisher": "After session 3: retest Week 1 push-ups + squat reps. Write the numbers down.",
    },
}

ORDER_BASE = ["squat", "push", "hinge", "row", "press", "core"]
ORDER_ADV = ["squat", "push", "hinge", "row", "press", "split", "core"]


def page_cover(c: canvas.Canvas):
    draw_bg(c)

    # top accent strip
    c.setFillColor(ORANGE)
    c.rect(0, H - 8, W, 8, fill=1, stroke=0)

    # brand
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W / 2, H - 1.15 * inch, "FORGE COACHING")

    c.setFillColor(DIM)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, H - 1.4 * inch, "DIGITAL TRAINING PRODUCT  ·  HOME SERIES")

    # main title card
    rounded_rect(c, 0.65 * inch, H - 5.35 * inch, W - 1.3 * inch, 3.55 * inch, r=14, fill=BG_CARD)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.95 * inch, H - 2.15 * inch, "4-WEEK BEGINNER PROGRAM")

    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 26)
    # multi-line title
    title_lines = [
        "Build Strength at Home.",
        "No Gym. No Guesswork.",
        "Just 3 Days a Week.",
    ]
    y = H - 2.65 * inch
    for line in title_lines:
        c.drawString(0.95 * inch, y, line)
        y -= 32

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 11)
    y -= 6
    sub = (
        "A complete full-body plan for young men starting from zero — "
        "or coming back after a long break."
    )
    draw_paragraph(c, sub, 0.95 * inch, y, W - 2.2 * inch, size=11, color=MUTED, leading=15)

    # benefit chips
    chips = [
        ("3x / week", "Full-body sessions"),
        ("4 weeks", "Built-in progression"),
        ("Home only", "Minimal equipment"),
    ]
    cx = 0.95 * inch
    cy = H - 4.95 * inch
    for main, sub in chips:
        rounded_rect(c, cx, cy - 8, 1.85 * inch, 0.72 * inch, r=8, fill=BG_ELEV)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(cx + 10, cy + 22, main)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(cx + 10, cy + 8, sub)
        cx += 2.0 * inch

    # bottom value props
    y = H - 6.0 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.85 * inch, y, "What you get")
    y -= 18
    props = [
        "Exact sets, reps, rest, and weekly progression — not vague “train hard” advice",
        "Simple form cues and mistakes to avoid for every movement",
        "Nutrition, sleep, and consistency guidelines that actually fit real life",
        "Written like a coach’s plan — direct, realistic, no hype",
    ]
    for p in props:
        y = draw_bullet(c, p, 0.85 * inch, y, W - 1.8 * inch, size=9.5) - 6

    # bottom bar
    c.setFillColor(BG_CARD)
    c.rect(0, 0, W, 1.05 * inch, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, 1.05 * inch - 3, W, 3, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 0.55 * inch, "Ages 18–30  ·  Complete beginners & returners  ·  Equipment: bodyweight + optional backpack/dumbbells")
    c.setFillColor(DIM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W / 2, 0.32 * inch, "© Forge Coaching  ·  Training education only  ·  Not medical advice")


def page_intro(c: canvas.Canvas, page: int):
    draw_bg(c)
    draw_header_bar(c, "Why this plan works")
    draw_footer(c, page, TOTAL, "INTRO")

    y = H - 1.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.7 * inch, y, "Simple. Hard enough. Repeatable.")
    y -= 22
    y = draw_paragraph(
        c,
        "Most beginner programs fail for one reason: they ask too much, too soon, with too little clarity. "
        "This plan fixes that. Three full-body sessions per week. The same movement patterns every week. "
        "Clear progression so you never wonder “what do I do next?”",
        0.7 * inch,
        y,
        W - 1.4 * inch,
        size=10.5,
        color=MUTED,
        leading=15,
    )

    y -= 18
    # two columns of cards
    cards = [
        (
            "Who this is for",
            [
                "Men 18–30 starting from scratch",
                "Returning after months or years off",
                "Training at home with limited gear",
                "Want structure without a gym membership",
            ],
        ),
        (
            "Who this is not for",
            [
                "Advanced lifters chasing PRs",
                "People with unaddressed injuries",
                "Anyone wanting “shredded in 7 days” hype",
                "Those unwilling to train 3 days consistently",
            ],
        ),
    ]
    card_w = (W - 1.6 * inch) / 2
    x0 = 0.7 * inch
    for i, (title, items) in enumerate(cards):
        x = x0 + i * (card_w + 0.2 * inch)
        rounded_rect(c, x, y - 2.35 * inch, card_w, 2.45 * inch, r=10, fill=BG_CARD)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12, y - 0.15 * inch, title.upper())
        iy = y - 0.4 * inch
        for item in items:
            iy = draw_bullet(c, item, x + 12, iy, card_w - 28, size=9) - 8

    y -= 2.7 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.7 * inch, y, "What results are realistic in 4 weeks")
    y -= 16
    results = [
        "Better movement quality on squats, hinges, push-ups, and rows",
        "Noticeable strength on the same exercises (more clean reps or harder variations)",
        "Improved work capacity — sessions feel more controlled by Week 4",
        "A proven weekly habit: train → recover → show up again",
        "Not realistic: dramatic physique overhauls, six-pack guarantees, or “transformation” photos overnight",
    ]
    for r in results:
        y = draw_bullet(c, r, 0.7 * inch, y, W - 1.5 * inch, size=9.5) - 5

    y -= 14
    rounded_rect(c, 0.7 * inch, y - 1.55 * inch, W - 1.4 * inch, 1.65 * inch, r=10, fill=BG_CARD)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y - 0.2 * inch, "THE COACHING RULE")
    draw_paragraph(
        c,
        "Every set should look clean. If form breaks, stop the set or regress the movement. "
        "Progress is adding quality work over four weeks — more clean reps, slower control, harder variations, "
        "or light load — not grinding ugly reps to hit a number. That’s how beginners actually get stronger.",
        0.9 * inch,
        y - 0.45 * inch,
        W - 1.9 * inch,
        size=10,
        color=MUTED,
        leading=14,
    )


def page_schedule(c: canvas.Canvas, page: int):
    draw_bg(c)
    draw_header_bar(c, "Weekly schedule & setup")
    draw_footer(c, page, TOTAL, "SCHEDULE")

    y = H - 1.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, y, "Train 3 non-consecutive days")
    y -= 18
    y = draw_paragraph(
        c,
        "Example: Monday · Wednesday · Friday. Or Tuesday · Thursday · Saturday. "
        "Leave at least one rest day between sessions. Same full-body session every training day — "
        "simplicity is the point.",
        0.7 * inch,
        y,
        W - 1.4 * inch,
        size=10,
        color=MUTED,
        leading=14,
    )

    y -= 16
    # week overview table as cards
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # pattern: T R T R T R R
    pattern = ["TRAIN", "REST", "TRAIN", "REST", "TRAIN", "REST", "REST"]
    cell_w = (W - 1.4 * inch) / 7
    for i, (d, p) in enumerate(zip(days, pattern)):
        x = 0.7 * inch + i * cell_w
        fill = BG_ELEV if p == "TRAIN" else BG_CARD
        rounded_rect(c, x + 2, y - 0.85 * inch, cell_w - 6, 0.95 * inch, r=6, fill=fill)
        c.setFillColor(DIM)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + cell_w / 2, y - 0.2 * inch, d)
        c.setFillColor(ORANGE if p == "TRAIN" else MUTED)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + cell_w / 2, y - 0.5 * inch, p)

    y -= 1.2 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7 * inch, y, "4-week progression map")
    y -= 14

    for wk, data in WEEKS.items():
        rounded_rect(c, 0.7 * inch, y - 0.72 * inch, W - 1.4 * inch, 0.8 * inch, r=8, fill=BG_CARD)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.9 * inch, y - 0.28 * inch, f"WEEK {wk}")
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 9.5)
        c.drawString(1.85 * inch, y - 0.28 * inch, data["theme"])
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawString(0.9 * inch, y - 0.52 * inch, f"{data['freq']}  ·  {data['focus']}")
        y -= 0.92 * inch

    y -= 6
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7 * inch, y, "Equipment (keep it minimal)")
    y -= 14
    equip = [
        "Required: floor space, a sturdy table/bar for rows (or a backpack for rows), and a timer",
        "Optional (recommended for progression): one backpack + books/water bottles, or a pair of dumbbells",
        "Surface: non-slip floor or yoga mat. Shoes optional for lower body if stable and comfortable",
    ]
    for e in equip:
        y = draw_bullet(c, e, 0.7 * inch, y, W - 1.5 * inch, size=9.5) - 5

    y -= 12
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7 * inch, y, "Session structure (every training day)")
    y -= 12
    steps = [
        ("5 min", "Warm-up: easy march or jog in place, arm circles, bodyweight good mornings, 10 easy squats"),
        ("25–40 min", "Main work: exercises in order, full rest between sets"),
        ("Optional", "Easy walk finisher — never turn this into a second hard workout"),
        ("2 min", "Note: exercises completed, hardest clean set, how you felt (1–10)"),
    ]
    for label, text in steps:
        rounded_rect(c, 0.7 * inch, y - 0.48 * inch, W - 1.4 * inch, 0.55 * inch, r=6, fill=BG_CARD)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0.85 * inch, y - 0.28 * inch, label)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8.5)
        c.drawString(1.75 * inch, y - 0.28 * inch, text)
        y -= 0.62 * inch


def draw_exercise_block(c, x, y, width, key, sets, reps, rest, note, compact=False):
    ex = EXERCISES[key]
    h = 0.98 * inch if compact else 1.12 * inch
    rounded_rect(c, x, y - h, width, h, r=7, fill=BG_CARD)

    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 9.5 if compact else 10)
    c.drawString(x + 10, y - 14, ex["name"])

    # meta chips
    meta_y = y - 30
    chip_x = x + 10
    for label, val in [("SETS", str(sets)), ("REPS", str(reps)), ("REST", f"{rest}s")]:
        tw = c.stringWidth(f"{label} {val}", "Helvetica-Bold", 7) + 12
        c.setFillColor(BG_ELEV)
        c.roundRect(chip_x, meta_y - 3, tw, 14, 3, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawString(chip_x + 4, meta_y + 1, label)
        c.setFillColor(TEXT)
        c.setFont("Helvetica", 7)
        c.drawString(
            chip_x + 4 + c.stringWidth(label + " ", "Helvetica-Bold", 6.5),
            meta_y + 1,
            val,
        )
        chip_x += tw + 5

    c.setFillColor(DIM)
    c.setFont("Helvetica-Oblique", 7.5)
    c.drawString(x + 10, y - 46, note)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    cue_lines = wrap_text(c, f"Cues: {ex['cues']}", "Helvetica", 7.5, width - 24)
    cy = y - 60
    for line in cue_lines[:2 if not compact else 1]:
        c.drawString(x + 10, cy, line)
        cy -= 10

    c.setFillColor(RED_SOFT)
    c.setFont("Helvetica", 7)
    mist = wrap_text(c, f"Avoid: {ex['mistakes']}", "Helvetica", 7, width - 24)
    for line in mist[:1 if compact else 2]:
        c.drawString(x + 10, cy, line)
        cy -= 9

    return y - h - 6


def page_week(c: canvas.Canvas, week: int, page: int):
    draw_bg(c)
    draw_header_bar(c, f"Week {week} — Training day")
    draw_footer(c, page, TOTAL, f"WEEK {week}")

    data = WEEKS[week]
    y = H - 1.05 * inch

    # week banner
    rounded_rect(c, 0.65 * inch, y - 0.62 * inch, W - 1.3 * inch, 0.7 * inch, r=10, fill=BG_CARD)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.85 * inch, y - 0.24 * inch, f"WEEK {week}")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(1.9 * inch, y - 0.24 * inch, data["theme"])
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(0.85 * inch, y - 0.46 * inch, f"{data['freq']}  ·  {data['focus']}")
    y -= 0.82 * inch

    order = ORDER_ADV if "split" in data["prescription"] else ORDER_BASE
    width = W - 1.3 * inch
    n_moves = sum(1 for k in order if k in data["prescription"])
    compact = n_moves >= 7

    for key in order:
        if key not in data["prescription"]:
            continue
        sets, reps, rest, note = data["prescription"][key]
        y = draw_exercise_block(
            c, 0.65 * inch, y, width, key, sets, reps, rest, note, compact=compact
        )

    # finisher always pinned above footer
    rounded_rect(c, 0.65 * inch, 0.68 * inch, width, 0.4 * inch, r=6, fill=BG_ELEV)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(0.8 * inch, 0.88 * inch, "FINISHER / NOTE")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    fin = data["finisher"]
    if c.stringWidth(fin, "Helvetica", 7.5) > width - 1.35 * inch:
        # truncate safely
        while fin and c.stringWidth(fin + "…", "Helvetica", 7.5) > width - 1.35 * inch:
            fin = fin[:-1]
        fin = fin.rstrip() + "…"
    c.drawString(1.85 * inch, 0.88 * inch, fin)

def page_nutrition(c: canvas.Canvas, page: int):
    draw_bg(c)
    draw_header_bar(c, "Nutrition that supports the plan")
    draw_footer(c, page, TOTAL, "NUTRITION")

    y = H - 1.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, y, "Fuel the work. Don’t overcomplicate it.")
    y -= 18
    y = draw_paragraph(
        c,
        "You don’t need a perfect meal plan. You need enough protein, mostly whole food, "
        "and a calorie target that matches your goal. Keep it boring and consistent for 4 weeks.",
        0.7 * inch,
        y,
        W - 1.4 * inch,
        size=10.5,
        color=MUTED,
        leading=14,
    )

    y -= 16
    # macro cards
    macros = [
        ("Protein", "0.7–1.0 g per lb\nbodyweight", "Chicken, eggs, Greek yogurt, lean beef, whey, beans + rice"),
        ("Carbs", "Build around training", "Rice, potatoes, oats, fruit, bread — more on hard days"),
        ("Fats", "Don’t zero them out", "Olive oil, egg yolks, nuts, avocado — steady energy & hormones"),
        ("Calories", "Match your goal", "Fat loss: slight deficit · Recomp/gain: maintenance or small surplus"),
    ]
    card_w = (W - 1.7 * inch) / 2
    card_h = 1.35 * inch
    for i, (title, line, detail) in enumerate(macros):
        col = i % 2
        row = i // 2
        x = 0.7 * inch + col * (card_w + 0.2 * inch)
        cy = y - row * (card_h + 0.12 * inch)
        rounded_rect(c, x, cy - card_h, card_w, card_h, r=10, fill=BG_CARD)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x + 12, cy - 0.28 * inch, title.upper())
        c.setFillColor(TEXT)
        c.setFont("Helvetica-Bold", 11)
        # first line of target
        c.drawString(x + 12, cy - 0.52 * inch, line.split("\n")[0])
        if "\n" in line:
            c.setFont("Helvetica", 9)
            c.setFillColor(MUTED)
            c.drawString(x + 12, cy - 0.7 * inch, line.split("\n")[1])
        c.setFillColor(DIM)
        c.setFont("Helvetica", 8)
        dlines = wrap_text(c, detail, "Helvetica", 8, card_w - 28)
        dy = cy - 0.95 * inch
        for dl in dlines[:2]:
            c.drawString(x + 12, dy, dl)
            dy -= 11

    y -= 2 * (card_h + 0.12 * inch) + 0.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7 * inch, y, "Easy guidelines that work")
    y -= 14
    rules = [
        "Eat a protein source at each meal (palm-sized portion is a usable visual for most men).",
        "Drink water across the day. A simple start: half your bodyweight (lb) in ounces as a baseline.",
        "On training days, include carbs around the session if energy is low.",
        "Limit liquid calories and constant snacking if fat loss is the goal.",
        "One flexible meal per week is fine. Consistency across 20+ meals beats perfection at 2.",
        "Supplements are optional. Creatine monohydrate and protein powder are the only ones worth considering early — still not required.",
    ]
    for r in rules:
        y = draw_bullet(c, r, 0.7 * inch, y, W - 1.5 * inch, size=9.5) - 5

    y -= 12
    rounded_rect(c, 0.7 * inch, y - 1.1 * inch, W - 1.4 * inch, 1.2 * inch, r=10, fill=BG_CARD)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y - 0.25 * inch, "EXAMPLE DAY (NOT A PRESCRIPTION)")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    example = (
        "Breakfast: eggs + toast + fruit  ·  Lunch: rice + chicken + vegetables  ·  "
        "Snack: Greek yogurt or protein shake  ·  Dinner: potatoes + lean meat + salad  ·  "
        "Adjust portions up or down based on weekly scale trend and energy."
    )
    draw_paragraph(c, example, 0.9 * inch, y - 0.5 * inch, W - 1.9 * inch, size=9, color=MUTED, leading=13)


def page_recovery(c: canvas.Canvas, page: int):
    draw_bg(c)
    draw_header_bar(c, "Recovery, sleep & consistency")
    draw_footer(c, page, TOTAL, "RECOVERY")

    y = H - 1.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, y, "Progress is built between sessions")
    y -= 18
    y = draw_paragraph(
        c,
        "Training is the stimulus. Sleep, food, and showing up on schedule are the recovery system. "
        "Miss those and even a perfect program stalls.",
        0.7 * inch,
        y,
        W - 1.4 * inch,
        size=10.5,
        color=MUTED,
        leading=14,
    )

    y -= 16
    sections = [
        (
            "Sleep",
            [
                "Target 7–9 hours. Protect a consistent bedtime more than a perfect routine.",
                "Dim screens 30–60 minutes before bed when you can.",
                "If sleep is wrecked, keep training but don’t add extra intensity that week.",
            ],
        ),
        (
            "Recovery days",
            [
                "Rest days are not “do nothing forever.” Easy walks are encouraged.",
                "Avoid turning rest days into secret hard workouts.",
                "Mild soreness is normal. Sharp joint pain is a stop-and-assess signal.",
            ],
        ),
        (
            "Consistency rules",
            [
                "3 sessions most weeks beats 5 sessions for two weeks then quitting.",
                "Schedule training like an appointment. Same times help.",
                "Missed a day? Shift the week — don’t “make up” with double sessions.",
                "Track the basics: sessions completed, hardest clean set, bodyweight 1–2x/week.",
            ],
        ),
        (
            "When to regress",
            [
                "Form collapses before the target reps → easier variation or fewer reps.",
                "Pain (not effort) during a movement → stop that pattern and substitute.",
                "Illness/fever → rest. Come back one week easier if needed.",
            ],
        ),
    ]

    for title, items in sections:
        rounded_rect(c, 0.7 * inch, y - 1.35 * inch, W - 1.4 * inch, 1.42 * inch, r=10, fill=BG_CARD)
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.9 * inch, y - 0.22 * inch, title.upper())
        iy = y - 0.45 * inch
        for item in items:
            iy = draw_bullet(c, item, 0.9 * inch, iy, W - 1.9 * inch, size=9) - 4
        y -= 1.55 * inch

    y -= 4
    rounded_rect(c, 0.7 * inch, y - 0.85 * inch, W - 1.4 * inch, 0.95 * inch, r=10, fill=BG_ELEV)
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y - 0.28 * inch, "Week 4 checkpoint")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    draw_paragraph(
        c,
        "Compare Week 4 performance to Week 1: same exercises, cleaner reps, harder variations, "
        "or better control. That’s progress. Then either repeat the plan with harder variations "
        "or move into a new block with the same full-body structure.",
        0.9 * inch,
        y - 0.5 * inch,
        W - 1.9 * inch,
        size=9,
        color=MUTED,
        leading=12,
    )


def page_disclaimer(c: canvas.Canvas, page: int):
    draw_bg(c)
    draw_header_bar(c, "Disclaimer & next steps")
    draw_footer(c, page, TOTAL, "DISCLAIMER")

    y = H - 1.15 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.7 * inch, y, "Professional disclaimer")
    y -= 18

    rounded_rect(c, 0.7 * inch, y - 3.2 * inch, W - 1.4 * inch, 3.3 * inch, r=10, fill=BG_CARD)
    paras = [
        "This product is for educational and general fitness information only. It is not medical advice, "
        "physical therapy, diagnosis, or a personalized healthcare plan.",
        "Always consult a qualified healthcare professional before starting any new exercise or nutrition program, "
        "especially if you have a medical condition, injury history, take medication, or are unsure whether training is safe for you.",
        "Stop any exercise that causes sharp pain, dizziness, chest pain, or unusual symptoms and seek medical care if needed.",
        "Results vary based on age, training history, nutrition, sleep, genetics, and consistency. "
        "No specific outcome is guaranteed.",
        "You are responsible for using equipment and surfaces safely (tables, backpacks, dumbbells, flooring). "
        "Forge Coaching and its authors accept no liability for injuries or damages arising from use or misuse of this material.",
        "This plan is intended for healthy adults. It is not designed for minors without appropriate professional and parental guidance.",
    ]
    py = y - 0.3 * inch
    for p in paras:
        py = draw_paragraph(c, p, 0.9 * inch, py, W - 1.9 * inch, size=9, color=MUTED, leading=12) - 10

    y -= 3.5 * inch
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.7 * inch, y, "How to use this for the next 28 days")
    y -= 14
    steps = [
        "Pick your 3 training days this week. Put them in your calendar.",
        "Do Week 1 exactly as written. Film one set of squats and push-ups if you want form feedback later.",
        "Progress only when reps are clean. Write down your best sets each session.",
        "Hit protein and sleep most days. Don’t wait for perfect conditions.",
        "At the end of Week 4, retest and decide: repeat with harder variations or level up with coaching.",
    ]
    for i, s in enumerate(steps, 1):
        c.setFillColor(ORANGE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(0.7 * inch, y, f"{i}.")
        y = draw_paragraph(c, s, 0.95 * inch, y, W - 1.8 * inch, size=10, color=MUTED, leading=13) - 8

    y -= 12
    rounded_rect(c, 0.7 * inch, y - 1.15 * inch, W - 1.4 * inch, 1.25 * inch, r=10, fill=BG_CARD)
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(0.9 * inch, y - 0.28 * inch, "FORGE COACHING")
    c.setFillColor(TEXT)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.9 * inch, y - 0.52 * inch, "Show up. Train clean. Progress weekly.")
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 9)
    draw_paragraph(
        c,
        "This is the standard: simple full-body work, honest effort, and enough recovery to adapt. "
        "Do the work for four weeks before you rewrite the plan.",
        0.9 * inch,
        y - 0.75 * inch,
        W - 1.9 * inch,
        size=9,
        color=MUTED,
        leading=12,
    )


def build():
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Forge Coaching — 4-Week Beginner Full-Body Home Plan")
    c.setAuthor("Forge Coaching")
    c.setSubject("Beginner home full-body training program for young men")
    c.setCreator("Forge Coaching Digital Products")

    page_cover(c)
    c.showPage()

    page_intro(c, 2)
    c.showPage()

    page_schedule(c, 3)
    c.showPage()

    for wk, pg in [(1, 4), (2, 5), (3, 6), (4, 7)]:
        page_week(c, wk, pg)
        c.showPage()

    page_nutrition(c, 8)
    c.showPage()

    page_recovery(c, 9)
    c.showPage()

    page_disclaimer(c, 10)
    c.showPage()

    c.save()
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    build()
