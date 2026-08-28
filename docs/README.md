# Automated advertising system — planning

**Pitch:** `ad-system-plan.html` — the paid acquisition plan (Meta first, YouTube second).

## Thesis

Organic view count is a free creative pretest. 70 published videos, 65,665 lifetime
views, and 60% of those views come from 8 opinion/technique shorts. Ads should
amplify posts that already passed the organic test rather than fund new creative.

## Analysis

`../analysis/youtube_catalog_analysis.py` — categorises the YouTube catalog sheet
(ID `1n3GXwOyC8r8FT_DE4-iPJcFIFeY5wyMzPiJvakkUVE4`) by format and reports views per
format. Run with `python3 analysis/youtube_catalog_analysis.py`.

Result as of 2026-08-28:

| Format                    | Videos | Views  | Median | Mean  |
|---------------------------|-------:|-------:|-------:|------:|
| Opinion / technique short |      8 | 39,395 |  1,872 | 4,924 |
| Athlete competition clip  |     12 | 14,586 |    586 | 1,216 |
| Exercise demo / tutorial  |     46 | 11,588 |     54 |   252 |
| Other                     |      4 |     96 |     18 |    24 |

## Status

Plan only. No ad code, no credentials, no spend. Four decisions are open — see the
"Before I build" section of the pitch.

## Not yet done

- Instagram-native metrics (saves, shares, follows, profile visits) — needs either
  Instagram Graph API access or a local Chrome session.
- Revenue figures — the Stripe connector was not enabled for the planning session.
