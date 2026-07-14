# STRATOS Deal Scrubber

Tooling for TJ's search-fund acquisition pipeline: sourcing, screening, and enriching
independently-owned home-services contractors (HVAC, plumbing, electrical) into a
call-ready acquisition-target list.

The reusable protocol lives at
[`.claude/skills/trade-acquisition-pipeline`](.claude/skills/trade-acquisition-pipeline/SKILL.md)
as a Claude Code skill — it fires automatically in any Claude Code session opened on this repo
when asked to build, deepen, or enrich a state's target list (e.g. "build a Georgia list",
"deepen the Florida pool", "enrich the callable owners"). It is state-agnostic: point it at any
US state and it runs the same ZoomInfo-driven sourcing → roll-up screening → owner
enrichment → RPE-guarded revenue → formatted xlsx workflow.

See `references/florida_case_study.md` inside the skill for the first worked run (Florida,
227 companies screened).
