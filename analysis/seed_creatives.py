"""Emit SQL to backfill ads.creatives + ads.creative_metrics from the YouTube catalog.

Source: Google Sheet 1n3GXwOyC8r8FT_DE4-iPJcFIFeY5wyMzPiJvakkUVE4, read 2026-08-28.
This is the prototype of the Phase 02 collector: once the YouTube Data API
credentials land, classify() and the row shape stay, only the fetch changes.

Usage: python3 analysis/seed_creatives.py > /tmp/seed.sql
"""

import re

# (title, url, published, views)
ROWS = [
    ("September 6, 2023", "https://youtu.be/elVg9wt8kDg", "2023-09-06", 55),
    ("January 3, 2024", "https://youtu.be/BnmeyQ23nLc", "2024-01-03", 18),
    ("#sports Not everyone will squat ATG with a vertical body angle.", "https://youtu.be/3L7WgUxVRG4", "2024-01-04", 25),
    ("1 Arm Row Exercise Demo", "https://youtu.be/pXdi2IykcNk", "2025-03-05", 0),
    ("1 Arm Row Tutorial", "https://youtu.be/cxYFSSAmgms", "2025-03-05", 7),
    ("110 Clean and Jerk for Nikhil at the 2024 Arnold", "https://youtu.be/meYWGODqgaA", "2024-03-07", 3233),
    ("118 kg Clean and Jerk PR for Felix at AO 2", "https://youtu.be/UPTIDVV_SR0", "2024-09-06", 2386),
    ("125 kg Snatch for Ryan at the 2024 Arnold", "https://youtu.be/u7W-Ls8UvmA", "2024-03-17", 5219),
    ("130 kg Snatch for Eli at the 2024 Arnold Classic", "https://youtu.be/UUZs6CmN4Nk", "2024-03-17", 975),
    ("150 kg Clean and Jerk", "https://youtu.be/8hwldbayApo", "2024-03-17", 13),
    ("48 kg Snatch PR for Shannon at the 2024 Arnold", "https://youtu.be/m15tHzyl8rk", "2024-03-07", 472),
    ("50 kg competition Snatch PR for Isabel at the 2024 Arnold", "https://youtu.be/k0chR2KWjwU", "2024-03-07", 425),
    ("60 kg Snatch PR for Lisa at the 2024 Arnold", "https://youtu.be/rwt9-7xRicU", "2024-03-07", 22),
    ("75 kg Snatch at the 2024 Arnold", "https://youtu.be/i07_T8DdeDs", "2024-03-17", 715),
    ("92 kg competition Snatch PR for Felix at AO2", "https://youtu.be/7t1bNI9Iam0", "2024-09-07", 586),
    ("Aimless Talk with Richie", "https://youtu.be/GQ2qPX2W5H8", "2024-04-13", 14),
    ("Bent Knee Calf Raise", "https://youtu.be/GutA_m81c8g", "2025-03-13", 581),
    ("Bent Press in side plank and half kneeling", "https://youtu.be/sG9vJoEe8Nk", "2025-08-26", 335),
    ("Cable Zercher Kickstand RDL", "https://youtu.be/p9sR_UqUiwc", "2025-09-17", 1396),
    ("Casey 110 kg Snatch at the Arnold", "https://youtu.be/0OSHIYo7CYo", "2024-03-17", 12),
    ("Clean and Jerk - pause at knee", "https://youtu.be/8rKaT0rOaCA", "2024-07-17", 39),
    ("Copenhagen Plank - Long and Short Lever", "https://youtu.be/GepwdtUJlIo", "2024-07-10", 50),
    ("DB Alternating Row - Palms Neutral", "https://youtu.be/lUZdxjtRQ4E", "2024-07-10", 7),
    ("Deep Tier Split Squat Jump", "https://youtu.be/TG65LX096VU", "2024-07-10", 186),
    ("Delaying Knee Extension - Lower body extension pattern", "https://youtu.be/GDp2tYkitjM", "2024-04-03", 36),
    ("FFE Split Squat Exercise Demo", "https://youtu.be/_u4DBUz64DQ", "2025-03-06", 5),
    ("Forward Stepping Lunge - Front Loaded", "https://youtu.be/rXW1qBDlRwA", "2024-07-10", 7),
    ("Front Foot & Heel Elevated Split Squat", "https://youtu.be/agoZx49je2M", "2024-06-28", 14),
    ("Front Foot Elevated Split Squat Tutorial Video", "https://youtu.be/9-ekJDztNj0", "2025-03-05", 16),
    ("Goblet ISO Squat", "https://youtu.be/_3ZYvh4eSfA", "2025-03-13", 71),
    ("Heavy singles weekly? Great for some-exhausting for others. Cycle them with purpose.", "https://youtu.be/PKLtS-PNzU0", "2025-08-20", 1126),
    ("Heels Elevated Goblet Squat Demo", "https://youtu.be/DxgeI-Zd1Wk", "2025-03-06", 8),
    ("Heels Elevated Goblet Squat Tutorial", "https://youtu.be/Q8aGuYKC348", "2025-03-06", 5),
    ("Heels Elevated Single Leg RDL", "https://youtu.be/9GTo3_SCqxA", "2025-09-12", 57),
    ("Hip Hinge - Goblet Loaded", "https://youtu.be/Mhi9tyfsaqI", "2024-07-10", 456),
    ("Hooklying reach with dumbbells", "https://youtu.be/EKWVp4XWwBY", "2025-08-26", 208),
    ("KB Rolling Armbar", "https://youtu.be/ahG7R6k5CsU", "2024-06-10", 1268),
    ("KB Suitcase Swing - Palms Neutral", "https://youtu.be/XORKhqXHzMI", "2024-07-10", 11),
    ("Kickstand Hinge Video Tutorial", "https://youtu.be/4RBhrEpN-oc", "2025-03-06", 54),
    ("Kickstand ISO Hinge", "https://youtu.be/u_jcdKT4ZfQ", "2024-07-10", 17),
    ("Kickstand RDL - Shown with Medball hug", "https://youtu.be/12O27AUC7x8", "2024-07-17", 27),
    ("Kickstand RDL Exercise Demo", "https://youtu.be/yX8kMfOoAOA", "2025-03-06", 6),
    ("Lateral Lunge to Elevation", "https://youtu.be/Dz4RgwcqoDg", "2025-03-13", 35),
    ("Low blocks can be your best friend or your worst enemy.", "https://youtu.be/ZbtffkBPAcw", "2025-08-20", 1553),
    ("Lunge ISO w/ wall support", "https://youtu.be/lNA0YUVFe60", "2025-12-22", 204),
    ("Midreach with Supinated Hands", "https://youtu.be/N7xzzcJjnGk", "2025-03-12", 308),
    ("Miss a lift and go up? What do you do?", "https://youtu.be/E2oLxZuzRAc", "2025-09-04", 3074),
    ("More than a party trick! They improve squat patterns.", "https://youtu.be/kGXIp487rJY", "2025-08-29", 1032),
    ("Offset Squat. Great warm up to drive some motion in the hips.", "https://youtu.be/xx5DduSbmIc", "2025-08-19", 76),
    ("Power Snatch + Snatch - Pause in catch of power", "https://youtu.be/PVWeYJsTzys", "2024-07-17", 21),
    ("PowerClean w/ pause at hip", "https://youtu.be/wTTZuqpBrdk", "2024-07-17", 29),
    ("Push Up - Isometric in Bottom", "https://youtu.be/ALof6pjSLaI", "2024-07-10", 441),
    ("Push Up to Downdog", "https://youtu.be/OYCBRTusWYA", "2024-07-10", 4),
    ("Reverse Crunch", "https://youtu.be/CjvDawtoNS0", "2024-07-10", 7),
    ("Seated 1 Arm Cable Tricep Extension", "https://youtu.be/3qqOeXeijFU", "2025-10-20", 1399),
    ("Seated DB Overhead Press - Palms Neutral", "https://youtu.be/0fIVTZkPTIY", "2024-07-10", 238),
    ("Seated Overhead Bicep Curl", "https://youtu.be/BWMGGFxrWWE", "2025-01-20", 537),
    ("Sift through the endless metrics. Find which are useful and discard the rest.", "https://youtu.be/OBu0HCABHe8", "2025-08-23", 25593),
    ("Snatch Deadlift", "https://youtu.be/R0lHyRVkinU", "2024-07-17", 420),
    ("Solid Saturday session gearing up for meet day", "https://youtu.be/ks4s-NOq1g0", "2024-10-08", 528),
    ("Superman Split Squat - Stay slouched keep front foot loaded", "https://youtu.be/xjF9vtZxO1o", "2024-07-15", 101),
    ("Tall lifters, listen up! Your long limbs mean different rules for the snatch.", "https://youtu.be/9Zyzzf0B2bU", "2025-08-24", 1872),
    ("Toes Elevated ISO Lunge", "https://youtu.be/29tuknSzSUQ", "2025-03-13", 46),
    ("Toes Elevated Kickstand RDL", "https://youtu.be/yXyT_LVPoWU", "2025-03-13", 263),
    ("Training Elastic Athletes", "https://youtu.be/7f-ftIdfAV0", "2023-12-01", 9),
    ("Underloaded RFE Split Squat. A real burner", "https://youtu.be/Bp8_Car7kUY", "2025-12-11", 1307),
    ("Wall supported Single leg RDL", "https://youtu.be/1W7rBLd3ec4", "2024-07-01", 434),
    ("Which trap are you caught in? Only taking big or small jumps? Try the opposite.", "https://youtu.be/IVWBEjMKdKY", "2025-06-18", 5120),
    ("Zercher Split Stance RDL", "https://youtu.be/yf9Tg_jD3gM", "2025-06-18", 41),
]

# Athlete competition clips: a name and a lift, or a named meet.
ATHLETE = re.compile(
    r"\b(arnold|ao ?2|nationals|worlds|meet day|competition|comp )\b|"
    r"^\d+\s*kg?\b|^\d+\s+(clean|snatch)", re.I)
# Opinion / technique shorts: they ask something or argue something.
OPINION = re.compile(
    r"\?|listen up|great for some|best friend|party trick|discard the rest|"
    r"not everyone will", re.I)
# Everything else naming an exercise or a drill cue is library, not reach.
# Checked after ATHLETE, so lift names here cannot steal competition clips.
DEMO = re.compile(
    r"\b(demo|tutorial|rdl|squat|lunge|hinge|press|curl|row|plank|crunch|"
    r"swing|raise|deadlift|push up|downdog|armbar|midreach|reach|calf|"
    r"extension|pause|snatch|clean|jerk)\b", re.I)


def classify(title: str) -> str:
    if OPINION.search(title):
        return "opinion"
    if ATHLETE.search(title):
        return "athlete"
    if DEMO.search(title):
        return "demo"
    return "other"


def q(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


def main() -> None:
    print("-- Generated by analysis/seed_creatives.py. Idempotent.")
    print("insert into ads.creatives "
          "(platform, platform_id, title, url, published_at, format) values")
    vals = []
    for title, url, pub, _ in ROWS:
        vid = url.rsplit("/", 1)[-1]
        vals.append(f"  ('youtube', {q(vid)}, {q(title)}, {q(url)}, "
                    f"{q(pub)}::timestamptz, {q(classify(title))})")
    print(",\n".join(vals))
    print("on conflict (platform, platform_id) do update set "
          "title = excluded.title, format = excluded.format;\n")

    print("insert into ads.creative_metrics (creative_id, captured_on, views)")
    print("select c.id, date '2026-08-28', v.views from (values")
    mv = [f"  ({q(url.rsplit('/', 1)[-1])}, {views})" for _, url, _, views in ROWS]
    print(",\n".join(mv))
    print(") as v(platform_id, views)")
    print("join ads.creatives c on c.platform = 'youtube' "
          "and c.platform_id = v.platform_id")
    print("on conflict (creative_id, captured_on) do update set "
          "views = excluded.views;")


if __name__ == "__main__":
    main()
