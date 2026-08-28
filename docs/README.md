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

## Decisions (rev 2)

| Question | Answer |
|---|---|
| Goal | Fill 1:1 coaching slots. Learn to Lift is the second-order outcome. |
| Budget | $8/day (~$240/mo), read over 90 days. |
| Control | Human approves every launch; the system pauses on its own. |
| Access | Platform APIs, not a browser session. |

Consequences of aiming at 1:1 on a trickle budget:

- **Find Your Phase becomes a router, not a destination.** Improve/Compete phases
  route to the 15-min call; Learn phase routes to nurture and Learn to Lift.
- **Optimise on quiz completions, measure on booked calls.** Booked calls are far
  too sparse at this budget to train Meta's optimiser (~50 conversions/week/ad set
  is the working threshold).
- **One ad set, not three.** $8/day split three ways starves all of them.
- **Athlete competition clips move into retargeting** as the close layer; opinion
  shorts stay top-of-funnel.
- **The Governor gains a capacity switch** — ads pause when open slots hit zero.

## Status

Plan only. No ad code, no credentials, no spend.

## Open

- 1:1 rate, average athlete tenure, and open slot count. The slot count configures
  the capacity switch; the other two turn cost-per-signing into a payback figure.
  Enabling the Stripe connector would cover the revenue side.

## Not available during planning

- Instagram-native metrics (saves, shares, profile visits) — resolved by the API
  decision above; the Instagram Graph API returns these in Phase 01.
- Revenue figures — the Stripe connector was not enabled for the planning session.
