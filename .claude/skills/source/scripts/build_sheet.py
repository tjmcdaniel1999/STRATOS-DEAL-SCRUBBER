#!/usr/bin/env python3
"""Build the formatted acquisition-target workbook for the /source skill.

Reads a JSON array of company records (see references/schema.md for the field contract),
applies the revenue-per-employee guard, computes EBITDA and Next Action, sorts, and writes a
zebra-striped .xlsx with a preserved colour-key row. See SKILL.md step 8 for the workflow this
plugs into.

Usage:
    python3 build_sheet.py --input records.json --output STATE_Acquisition_Targets.xlsx \\
        [--existing previous_version.xlsx] [--state "<state name>"]
"""
import argparse
import json
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

COLUMNS = [
    ("ID", "id"),
    ("Company", "company"),
    ("Trade", "trade"),
    ("City", "city"),
    ("State", "state"),
    ("Owner (Best)", "owner_best"),
    ("Owner Cell", "owner_cell"),
    ("Cell DNC", "cell_dnc"),
    ("Cell Source", "cell_source"),
    ("Owner Email", "owner_email"),
    ("Employees (Best)", "employees_best"),
    ("Revenue (Best) $", "revenue_best"),
    ("Revenue Basis", "revenue_basis"),
    ("Est. EBITDA 12% $", "ebitda_12pct"),
    ("Owner Confidence", "owner_confidence"),
    ("Size Confidence", "size_confidence"),
    ("ZI Mobile?", "zi_mobile"),
    ("ZI Owner / Title", "zi_owner_title"),
    ("ZI Emp", "zi_emp"),
    ("ZI Rev $", "zi_rev"),
    ("ZI Company ID", "zi_company_id"),
    ("Website", "website"),
    ("Next Action", "next_action"),
    ("Notes / Flags", "notes_flags"),
]
FIELD_TO_HEADER = {field: header for header, field in COLUMNS}

RPE_LOW = 100_000
RPE_HIGH = 500_000
RPE_ESTIMATE_PER_EMPLOYEE = 225_000
EBITDA_MARGIN = 0.12

ZEBRA_WHITE = "FFFFFFFF"
ZEBRA_GREY = "FFF2F2F2"
ZEBRA_FILLS = {ZEBRA_WHITE, ZEBRA_GREY, "00000000", None}

NEXT_ACTION_PRIORITY = {
    "DIAL-READY": 0,
    "ENRICH CELL (callable)": 1,
    "Office line / email only": 2,
    "NAME OWNER (state license lookup)": 3,
}


def apply_rpe_guard(record: dict) -> None:
    """Fill Revenue (Best), Revenue Basis, and Est. EBITDA 12% from ZI Rev $ / employees."""
    employees = record.get("employees_best") or record.get("zi_emp")
    zi_rev = record.get("zi_rev")

    revenue_best = None
    revenue_basis = None

    if employees and zi_rev:
        rpe = zi_rev / employees
        if RPE_LOW <= rpe <= RPE_HIGH:
            revenue_best = zi_rev
            revenue_basis = "ZI"
        else:
            revenue_best = employees * RPE_ESTIMATE_PER_EMPLOYEE
            revenue_basis = "ESTIMATED"
    elif employees:
        revenue_best = employees * RPE_ESTIMATE_PER_EMPLOYEE
        revenue_basis = "ESTIMATED"

    record["revenue_best"] = revenue_best
    record["revenue_basis"] = revenue_basis
    record["ebitda_12pct"] = round(revenue_best * EBITDA_MARGIN) if revenue_best else None


def classify_next_action(record: dict) -> str:
    """Derive Next Action from owner/cell/DNC state, unless already set explicitly."""
    if record.get("next_action"):
        return record["next_action"]

    has_cell = bool(record.get("owner_cell"))
    is_dnc = str(record.get("cell_dnc", "")).strip().lower() == "yes"
    has_owner = bool(record.get("owner_best") or record.get("zi_owner_title"))
    zi_mobile = str(record.get("zi_mobile", "")).strip().lower() == "yes"

    if has_cell and not is_dnc:
        return "DIAL-READY"
    if has_owner and zi_mobile and not is_dnc and not has_cell:
        return "ENRICH CELL (callable)"
    if has_owner and (is_dnc or not zi_mobile):
        return "Office line / email only"
    return "NAME OWNER (state license lookup)"


def sort_key(record: dict):
    priority = NEXT_ACTION_PRIORITY.get(record.get("next_action"), 99)
    ebitda = record.get("ebitda_12pct") or 0
    return (priority, -ebitda)


def load_manual_colors(existing_path: Path) -> dict:
    """Map record id -> fill colour (hex) for any row whose fill isn't plain zebra striping."""
    manual_colors = {}
    wb = load_workbook(existing_path)
    ws = wb.active
    header = [c.value for c in ws[2]]  # row 1 is the colour key, row 2 is the column header
    try:
        id_col = header.index("ID")
    except ValueError:
        return manual_colors

    for row in ws.iter_rows(min_row=3):
        record_id = row[id_col].value
        if record_id is None:
            continue
        fill = row[id_col].fill
        color = fill.fgColor.rgb if fill and fill.fgColor else None
        if color not in ZEBRA_FILLS:
            manual_colors[str(record_id)] = color
    return manual_colors


def build_workbook(records: list, state: str, manual_colors: dict) -> Workbook:
    wb = Workbook()
    ws = wb.active
    ws.title = "Acquisition Targets"

    headers = [h for h, _ in COLUMNS]

    # Row 1: colour KEY row. This is the ONLY coloured region the pipeline itself writes —
    # everything else is left for the user to colour by hand. We only seed placeholder text
    # here; do not assign fill colours to these cells programmatically.
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
    key_cell = ws.cell(row=1, column=1)
    key_cell.value = (
        f"COLOUR KEY — {state}: row colours below are assigned by hand; "
        "their meaning is the user's, not auto-generated."
    )
    key_cell.font = Font(italic=True, size=9)

    # Row 2: header
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col_idx, value=header)
        cell.font = Font(bold=True)

    ordered = sorted(records, key=sort_key)

    for i, record in enumerate(ordered):
        row_idx = i + 3
        record_id = str(record.get("id", ""))
        manual_fill = manual_colors.get(record_id)
        fill_color = manual_fill if manual_fill else (ZEBRA_GREY if i % 2 else ZEBRA_WHITE)
        fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")

        for col_idx, (_, field) in enumerate(COLUMNS, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=record.get(field))
            cell.fill = fill

    for col_idx, header in enumerate(headers, start=1):
        width = max(12, min(32, len(header) + 4))
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.freeze_panes = "A3"
    return wb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON array of records")
    parser.add_argument("--output", required=True, type=Path, help="Output .xlsx path")
    parser.add_argument("--existing", type=Path, help="Previous workbook to preserve manual row colours from")
    parser.add_argument("--state", default="", help="State name for the colour-key row label")
    args = parser.parse_args()

    records = json.loads(args.input.read_text())
    if not isinstance(records, list):
        sys.exit("Input JSON must be an array of record objects")

    for record in records:
        apply_rpe_guard(record)
        record["next_action"] = classify_next_action(record)

    manual_colors = {}
    if args.existing and args.existing.exists():
        manual_colors = load_manual_colors(args.existing)

    wb = build_workbook(records, args.state, manual_colors)
    wb.save(args.output)
    print(f"Wrote {len(records)} rows to {args.output}")


if __name__ == "__main__":
    main()
