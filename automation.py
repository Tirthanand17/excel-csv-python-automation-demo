from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def _snake_case(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "_", str(value).strip())
    return re.sub(r"_+", "_", value).strip("_").lower()


def _read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Input must be a CSV, XLSX, or XLS file.")


def _write_table(df: pd.DataFrame, path: Path) -> None:
    suffix = path.suffix.lower()
    path.parent.mkdir(parents=True, exist_ok=True)
    if suffix == ".csv":
        df.to_csv(path, index=False)
        return
    if suffix == ".xlsx":
        df.to_excel(path, index=False)
        return
    raise ValueError("Output must be CSV or XLSX.")


def clean_dataframe(
    df: pd.DataFrame,
    dedupe_columns: Iterable[str] | None = None,
) -> tuple[pd.DataFrame, dict]:
    original_rows = len(df)
    cleaned = df.copy()
    cleaned.columns = [_snake_case(c) for c in cleaned.columns]

    for col in cleaned.select_dtypes(include="object").columns:
        cleaned[col] = cleaned[col].map(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    if "email" in cleaned.columns:
        cleaned["email"] = cleaned["email"].map(
            lambda x: x.lower() if isinstance(x, str) else x
        )

    requested = [_snake_case(c) for c in (dedupe_columns or [])]
    usable = [c for c in requested if c in cleaned.columns]

    if usable:
        cleaned = cleaned.drop_duplicates(subset=usable, keep="first")
    else:
        cleaned = cleaned.drop_duplicates(keep="first")

    cleaned = cleaned.reset_index(drop=True)

    summary = {
        "rows_before": original_rows,
        "rows_after": len(cleaned),
        "duplicates_removed": original_rows - len(cleaned),
        "columns": list(cleaned.columns),
        "dedupe_columns_used": usable,
    }
    return cleaned, summary


def run(
    input_path: str | Path,
    output_path: str | Path,
    dedupe_columns: Iterable[str] | None = None,
) -> dict:
    input_path = Path(input_path)
    output_path = Path(output_path)

    df = _read_table(input_path)
    cleaned, summary = clean_dataframe(df, dedupe_columns)
    _write_table(cleaned, output_path)

    summary_path = output_path.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Clean, standardize, and deduplicate Excel/CSV files."
    )
    parser.add_argument("input", help="Input CSV/XLSX/XLS file")
    parser.add_argument("output", help="Output CSV/XLSX file")
    parser.add_argument(
        "--dedupe",
        nargs="*",
        default=[],
        help="Optional column names used for duplicate detection",
    )
    args = parser.parse_args()
    summary = run(args.input, args.output, args.dedupe)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
