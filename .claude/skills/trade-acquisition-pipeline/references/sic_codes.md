# SIC codes for sourcing

National codes, not state-specific — use these in `search_companies` regardless of which
state is being worked.

| SIC | Trade | Known contamination |
|---|---|---|
| 1711 | Plumbing, Heating, Air-Conditioning | Cleaner than 1731, but still screen for HVAC-adjacent non-targets (e.g., commercial refrigeration-only shops, fire sprinkler-only contractors) if the buy-box is residential-focused. |
| 1731 | Electrical Work | Dirty. Sweeps in AV installers, alarm/security firms, telecom contractors, fire protection, and solar installers, plus outright non-targets (lamp distributors, research institutions, trade associations). Expect to screen out a large fraction of raw hits regardless of state. |

Multi-trade companies (offering more than one of HVAC/plumbing/electrical) will often show up
under only one SIC code in ZoomInfo — check the company description/services text, not just
the code, before tagging `Trade` in the schema.
