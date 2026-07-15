# Roll-up / franchise blocklist and detection heuristics

Roll-ups and franchises look exactly like independents in ZoomInfo/Apollo data. They are
**not acquirable from the operator** — the operator doesn't own it, a PE platform or
franchisor does — so outreach to them wastes both enrichment credit and the owner's time.
Screen for these at the sourcing stage, before spending any enrichment credit.

This list will go stale — PE-backed home-services platforms buy and rebrand shops constantly.
Treat the named entries as a starting seed, not a complete or permanent list, and confirm
current ownership when in doubt (a quick web check on "[brand] + [PE firm name]" or "[brand]
acquired by" usually settles it). The **heuristics matter more than the list**, since they
catch platforms and rebrands this document doesn't know about yet.

## Detection heuristics (apply to every candidate, every state)

1. **Parent-company mismatch.** The registered corporate entity behind the brand name is a
   holding company, "services group," or investment vehicle rather than a plausibly
   owner-named local business.
2. **Impossible size for the brand.** A single-location-looking brand reports employee counts
   or revenue far above what one shop of that type would run, or turns out to have many
   ZoomInfo-listed locations under the same brand.
3. **HQ city ≠ operating city.** The company's registered HQ is out of state or in a different
   metro than the location being screened — a common signature of a platform's acquired local
   subsidiary.
4. **Brand + city naming pattern.** Platforms frequently stamp their brand onto acquired
   locals in a templated way (e.g., a generic trade name repeated with different city suffixes
   across a state, or a name that reads like a franchise rather than a founder's name).
5. **C-suite too large for the headcount.** A "company" of 15–20 employees with a multi-person
   C-suite roster (CEO, CFO, COO, VP of M&A, etc.) in ZoomInfo is a platform-level entity, not
   the operating shop.
6. **Owner email domain doesn't match the company.** Caught only once you have contact-level
   data (`search_contacts`/`enrich_contacts`), not from company data alone:
   - Two "co-owners" of different-sounding companies share the same non-obvious email domain
     → they likely both work for whichever company that domain belongs to, and the other
     "company" is a subsidiary of it, not an independent peer.
   - An owner's email domain matches a known franchisor/dealer network (e.g., a national brand
     dealer domain) rather than the company's own domain → almost certainly a dealer/franchise
     relationship, not a clean independent, even if the storefront brand looks local.
   Always read the enriched email domain on every target before finalizing status — this flag
   is invisible at the company-screening stage.

## Seed list: national/multi-state PE platforms and franchise systems

Home-services HVAC/plumbing/electrical consolidation is a well-known PE thesis; the same
platforms show up across many states under many different local brand names. Known platform
families as of this writing (verify currency before relying on a name below — ownership
changes hands):

- **Wrench Group** — multi-brand HVAC/plumbing platform operating similarly-structured local
  brands across many states.
- **Leap Partners** — PE owner of home-services roll-ups.
- **Authority Brands** — franchisor of Benjamin Franklin Plumbing, One Hour Heating & Air
  Conditioning, Mister Sparky (electrical), America's Swimming Pool Co., and others —
  national franchise system, not independent at the local level.
- **Neighborly** — franchisor of Mr. Rooter Plumbing, Aire Serv, Mr. Electric — same pattern.
- **ARS/Rescue Rooter** — national HVAC/plumbing rollup.
- **Apex Service Partners**, **Redwood Services**, **PowerTeam Services** (electrical
  roll-up), **CoolSys** (commercial HVAC/refrigeration roll-up) — active multi-state
  consolidators; check any target with an unusually corporate-sounding "Services" or
  "Partners" name against these.
- **Z Plumberz**, **All Dry USA** — national franchise systems.
- Membership/warranty companies that aren't contractors at all, e.g. **Home-Tech** — screen
  these out entirely regardless of trade code, they don't operate as a contractor.

## State-specific confirmed kills (add to this section as states are worked)

Add a subsection per state as you confirm roll-ups/franchises there, so future runs don't
re-discover the same ones from scratch:

```
### <State>
| Company | Why it's ineligible |
|---|---|
| ... | PE-owned / franchise / platform subsidiary — not acquirable from the operator |
```

Some regions are more consolidated than others and deserve extra scrutiny, but don't assume
any state is "clean" by default — consolidation is spreading, and regional roll-ups exist even
where no national platform has moved in yet. Ask the user if they know of state-specific
roll-ups not covered by the seed list above.
