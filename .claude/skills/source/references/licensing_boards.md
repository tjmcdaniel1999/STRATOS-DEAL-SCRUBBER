# State contractor-licensing references

Used for step 4 of SKILL.md ("NAME OWNER" companies — no C-level contact found in
ZoomInfo). Most US states require HVAC, plumbing, and electrical contractors to hold a
license, and the "qualifying agent" / responsible individual on that license is public record
and is usually the owner. The license number also makes a strong deduplication key — often
stronger than matching on company name, which varies across data sources.

**Verify the current URL and search mechanics before relying on this table** — state licensing
sites get restructured. Treat entries below as a starting pointer, and fill in new states as
they're worked so future runs don't redo the research.

| State | Agency | Relevant license types / prefixes | Public lookup |
|---|---|---|---|
| Arizona | Arizona Registrar of Contractors (ROC) | Classified by trade (e.g., C-39 plumbing, C-37 electrical, C-20/C-38 HVAC) | AZ ROC license search |
| California | CSLB (Contractors State License Board) | C-20 (HVAC), C-36 (plumbing), C-10 (electrical) | CSLB license lookup |
| Florida | DBPR (Dept. of Business & Professional Regulation) | CAC (A/C contractor), CFC (plumbing), EC (electrical), CBC (building), CMC (mechanical) | DBPR online license search |
| Georgia | Georgia State Construction Industry Licensing Board (under Secretary of State) | Conditioned Air (HVAC), Electrical, Plumbing — separate license classes | GA Secretary of State license search |
| North Carolina | NC Licensing Board for General Contractors (general); separate NC Board of Examiners for electrical, and NC State Board of Examiners of Plumbing, Heating & Fire Sprinkler Contractors | Trade-specific boards, not unified | Each board has its own lookup |
| South Carolina | SC LLR Contractor's Licensing Board | Mechanical (HVAC), plumbing, electrical classifications | SC LLR license lookup |
| Tennessee | TN Board for Licensing Contractors | HVAC, plumbing, electrical classifications | TN.gov license verification search |
| Texas | TDLR (electrical, A/C — "ACR" license), TSBPE (Texas State Board of Plumbing Examiners) | Split across two agencies: TDLR for electrical & HVAC (ACR), TSBPE for plumbing (RMP/journeyman) | Each agency has its own license lookup |
| *(any other state)* | Not yet researched | — | Find the state's contractor licensing board's public license-lookup tool and add a row here before relying on it |

## Notes

- The qualifying agent named on a license is a strong owner-identity signal, but confirm
  against ZoomInfo/other sources when possible — sometimes the qualifying agent is a
  contracted individual rather than the actual owner, especially at larger shops.
- When adding a new state, capture: the agency name, which trades are licensed separately vs.
  together, the license-prefix/class scheme, and whether the public lookup exposes the
  qualifying agent's name directly or requires a secondary step.
