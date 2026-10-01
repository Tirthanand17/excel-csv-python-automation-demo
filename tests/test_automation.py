import json
from pathlib import Path

import pandas as pd

from automation import clean_dataframe, run


def test_clean_dataframe_standardizes_and_deduplicates():
    df = pd.DataFrame(
        {
            "Customer ID": [1, 1, 2],
            "Name": [" Alice ", "Alice", " Bob "],
            "Email": ["A@EXAMPLE.COM", "a@example.com", "B@example.com"],
        }
    )

    cleaned, summary = clean_dataframe(df, ["Customer ID", "Email"])

    assert list(cleaned.columns) == ["customer_id", "name", "email"]
    assert cleaned.loc[0, "name"] == "Alice"
    assert cleaned.loc[0, "email"] == "a@example.com"
    assert len(cleaned) == 2
    assert summary["duplicates_removed"] == 1


def test_run_writes_output_and_summary(tmp_path: Path):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    source.write_text(
        "ID,Name,Email\n1, Alice ,A@EXAMPLE.COM\n1,Alice,a@example.com\n",
        encoding="utf-8",
    )

    summary = run(source, output, ["ID", "Email"])

    assert output.exists()
    assert output.with_suffix(".summary.json").exists()
    assert summary["rows_after"] == 1
    saved = json.loads(output.with_suffix(".summary.json").read_text())
    assert saved["duplicates_removed"] == 1
