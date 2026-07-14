# Spreadsheet schema

24 columns, in this order. This is the contract between the sourcing/enrichment steps and
`scripts/build_sheet.py` — the JSON records fed to the script use the snake_case field names
in parentheses.

| # | Column | Field name | Notes |
|---|---|---|---|
| 1 | ID | `id` | Stable identifier. Prefer the state license number once known (§4 of SKILL.md) — it's a stronger dedup key than company name. Falls back to a sequential id. |
| 2 | Company | `company` | |
| 3 | Trade | `trade` | One of `HVAC`, `Plumbing`, `Electrical`, or a combination like `HVAC+Plumbing`, `HVAC+Electrical`. |
| 4 | City | `city` | |
| 5 | State | `state` | Two-letter or full name, consistent within a sheet. |
| 6 | Owner (Best) | `owner_best` | The single best-known owner/principal name. If multiple principals exist, put the primary callable one here and list the rest in `Notes / Flags`. |
| 7 | Owner Cell | `owner_cell` | Populated only after `enrich_contacts`. Blank until then. |
| 8 | Cell DNC | `cell_dnc` | `Yes` / `No` / blank (unknown). Comes free from `search_contacts` — populate this even before enriching the number. |
| 9 | Cell Source | `cell_source` | e.g. `ZoomInfo enrich_contacts`. |
| 10 | Owner Email | `owner_email` | Read the domain — it can reveal a roll-up/franchise/dealer relationship not visible in company-level data (see rollup_blocklist.md). |
| 11 | Employees (Best) | `employees_best` | |
| 12 | Revenue (Best) $ | *(computed by build_sheet.py)* | ZI-reported if it passes the RPE guard, else `employees × 225000`. |
| 13 | Revenue Basis | *(computed)* | `ZI` or `ESTIMATED`. |
| 14 | Est. EBITDA 12% $ | *(computed)* | `Revenue (Best) × 0.12`. Flat placeholder margin, not diligenced. |
| 15 | Owner Confidence | `owner_confidence` | Independent of Size Confidence. e.g. `High` / `Medium` / `Low`. |
| 16 | Size Confidence | `size_confidence` | Independent of Owner Confidence. |
| 17 | ZI Mobile? | `zi_mobile` | `Yes`/`No` from `search_contacts` `hasMobilePhone`, before any enrichment spend. |
| 18 | ZI Owner / Title | `zi_owner_title` | Raw ZoomInfo owner name + title, kept separate from the curated `Owner (Best)` in case they diverge. |
| 19 | ZI Emp | `zi_emp` | Raw ZoomInfo employee count (may differ from `employees_best` if hand-corrected). |
| 20 | ZI Rev $ | `zi_rev` | Raw ZoomInfo reported revenue, pre-RPE-guard. Keep even when overridden, so the override is auditable. |
| 21 | ZI Company ID | `zi_company_id` | |
| 22 | Website | `website` | |
| 23 | Next Action | *(computed, overridable)* | `DIAL-READY` / `ENRICH CELL (callable)` / `Office line / email only` / `NAME OWNER (state license lookup)`. Drives the sort order. |
| 24 | Notes / Flags | `notes_flags` | Multi-principal lists, roll-up/franchise suspicion, shared-email-domain flags, anything that doesn't fit elsewhere. |

## Input record shape (JSON fed to build_sheet.py)

```json
{
  "id": "CFC1234567",
  "company": "Example Plumbing & Air",
  "trade": "HVAC+Plumbing",
  "city": "Tampa",
  "state": "Florida",
  "owner_best": "Jane Smith",
  "owner_cell": "(813) 555-0100",
  "cell_dnc": "No",
  "cell_source": "ZoomInfo enrich_contacts",
  "owner_email": "jane@exampleplumbing.com",
  "employees_best": 42,
  "owner_confidence": "High",
  "size_confidence": "Medium",
  "zi_mobile": "Yes",
  "zi_owner_title": "Jane Smith, Owner",
  "zi_emp": 42,
  "zi_rev": 9500000,
  "zi_company_id": "123456789",
  "website": "https://exampleplumbing.com",
  "notes_flags": "Co-owner Bob Smith also on title, not yet contacted."
}
```

Leave a field out (or use `null`/`""`) when it isn't known yet — e.g. a brand-new sourcing pass
will have `owner_cell`, `cell_source` empty and `zi_mobile`/`cell_dnc` populated from the free
contact search. `build_sheet.py` fills in `Revenue (Best)`, `Revenue Basis`,
`Est. EBITDA 12% $`, and `Next Action` (unless you pass an explicit override) — don't compute
those by hand.

## Formatting rules (enforced by build_sheet.py)

- The colour KEY row at the top is the **only** coloured region in the workbook.
- Company rows get plain white/light-grey zebra striping and nothing else. The user assigns
  row colours by hand after delivery; their meaning is his, not the pipeline's. Never
  auto-colour a company row based on trade, confidence, or anything else.
- Default sort: `Next Action` priority (`DIAL-READY` → `ENRICH CELL (callable)` → everything
  else), then `Est. EBITDA 12% $` descending within each group.
- When rebuilding an existing sheet (`--existing`), any row whose fill colour is not the
  standard zebra white/grey is treated as a manual annotation and is preserved on that same
  company record even after re-sorting.
