-- Phase 02 scorer. Run nightly after the collector writes a new snapshot.
--
-- Ranks on views per day rather than lifetime views. Raw views reward age:
-- a 2024 competition clip has had two years to accumulate and will always
-- beat a strong post from last month. Velocity is what actually predicts
-- whether paying to amplify a post is worth it.
--
-- Once the Instagram Graph API lands, add engagement_per_impression
-- (saves + shares + comments over impressions) as the primary term and
-- demote views_per_day to a tiebreaker. Views measure delivery; saves and
-- shares measure whether the post was worth someone's attention.

with latest as (
  -- most recent snapshot per creative, so this stays correct once the
  -- collector is appending nightly rows rather than a single backfill
  select distinct on (m.creative_id)
         m.creative_id, m.views, m.captured_on
  from ads.creative_metrics m
  order by m.creative_id, m.captured_on desc
),
scored as (
  select c.id,
         -- floor the denominator at 7 days: a post published yesterday has a
         -- tiny divisor and would otherwise top the table on noise alone
         round(l.views::numeric
               / greatest(l.captured_on - c.published_at::date, 7), 3) as vpd
  from ads.creatives c
  join latest l on l.creative_id = c.id
  where c.published_at is not null
)
insert into ads.creative_scores (creative_id, scored_on, views_per_day, score, rank)
select id, current_date, vpd, vpd,
       rank() over (order by vpd desc)
from scored
on conflict (creative_id, scored_on) do update
  set views_per_day = excluded.views_per_day,
      score         = excluded.score,
      rank          = excluded.rank;

-- Promotion candidates, split by lane.
--   opinion → cold traffic. These earn the reach.
--   athlete → retargeting. Smaller audience, far more qualified.
--   demo    → never promoted. Coaching infrastructure, not reach.
--
-- select s.rank, c.format, s.views_per_day, c.title, c.url
-- from ads.creative_scores s
-- join ads.creatives c on c.id = s.creative_id
-- where s.scored_on = current_date
--   and c.format in ('opinion', 'athlete')
-- order by s.rank;
