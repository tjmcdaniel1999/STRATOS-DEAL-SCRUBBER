# STRATOS Deal Scrubber

Tooling for TJ's search-fund acquisition pipeline: sourcing, screening, and enriching
independently-owned home-services contractors (HVAC, plumbing, electrical) into a
call-ready acquisition-target list.

The reusable protocol lives at
[`.claude/skills/source`](.claude/skills/source/SKILL.md) as a Claude Code skill named
`source` — invoke it with `/source` (or just ask to build/deepen/enrich a state's list) in any
Claude Code session opened on this repo. It has no default or preferred state built in: give it
any US state and it runs the same ZoomInfo-driven sourcing → roll-up screening → owner
enrichment → RPE-guarded revenue → formatted xlsx workflow.
