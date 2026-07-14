# Florida — worked example (first run of this protocol)

Prepared 13 July 2026. Kept as a reference for what "done" looks like and what to watch for,
not as data to re-use for a fresh Florida run (a re-run should re-pull current ZoomInfo data).

## Results at that snapshot

- 227 companies screened and deduped: 98 HVAC, 83 Electrical, 38 Plumbing, 8 multi-trade.
- Owner name identified for 116 (51%): 26 DIAL-READY (cell pulled, DNC-cleared), 35 callable
  mobile confirmed but not yet enriched, 55 DNC-flagged or no mobile on file.
- 111 companies with no owner name yet.
- 57 of 227 (37%) had ZoomInfo revenue figures that failed the RPE guard and were re-estimated.
- Apollo was unusable that entire run (free-plan API lockout) — ZoomInfo did the whole job.
- 30 ZoomInfo enrichment credits spent, 30/30 FULL_MATCH.
- Of 367 raw SIC-1731 records, 127 were not target trades at all.
- 9 confirmed roll-ups/franchises killed before enrichment (see `rollup_blocklist.md`).
- 2 ownership flags surfaced only through enriched email domains (see the "owner email domain"
  heuristic in `rollup_blocklist.md`) — neither would have been caught by company-level
  screening alone.
- Only ~460 raw records pulled against a statewide universe of 5,327 companies in the
  10–100-employee band (SIC 1711 alone had 3,004 in that band) — i.e., a first pass barely
  scratches the surface; expect the user to want the list deepened well beyond an initial pull.
- The prior Arizona list (82 rows, built before this protocol existed) had no DNC column at
  all — a good candidate for the free backfill sweep described in SKILL.md step 9.
- Top target by EBITDA (Erwin Electric) had **both** its president and founder DNC-flagged —
  a reminder that a high-value target can still be entirely off-limits for cold dialing.

## Multi-principal example patterns worth watching for again

- Two generations of the same family on one license/company (grandfather founder, father
  president, son owner).
- A "president" or "VP" who is callable while the actual registered owner(s) are DNC-flagged —
  the callable exec is the practical route in even though they're not the top title.
- 3-4 co-owners/partners on one company, all needing to sign off on a sale.

These patterns recur across states; capture every principal found, not just the top-titled one.
