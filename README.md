# STRATOS Deal Scrubber

Tooling for TJ's search-fund acquisition pipeline: sourcing, screening, and enriching
independently-owned home-services contractors (HVAC, plumbing, electrical) into a
call-ready acquisition-target list.

The reusable protocol lives at
[`.claude/skills/trade-acquisition-pipeline`](.claude/skills/trade-acquisition-pipeline/SKILL.md)
as a Claude Code skill — it fires automatically in any Claude Code session opened on this repo
when asked to build, deepen, or enrich a target list for a state (e.g. "build a list for
<state>", "deepen the <state> pool", "enrich the callable owners"). It has no default or
preferred state built in: point it at any US state and it runs the same ZoomInfo-driven
sourcing → roll-up screening → owner enrichment → RPE-guarded revenue → formatted xlsx
workflow.
