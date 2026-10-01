# Python Excel & CSV Automation Demo

A small, production-style portfolio project that turns repetitive spreadsheet cleanup into a reusable Python workflow.

## What it does

- Reads CSV, XLSX, or XLS input files
- Standardizes column names to clean snake_case
- Trims extra whitespace in text fields
- Normalizes email addresses to lowercase
- Removes duplicate records
- Supports custom duplicate keys
- Writes clean CSV or XLSX output
- Produces a JSON run summary for traceability
- Includes automated tests and GitHub Actions CI

## Quick start

~~~bash
python -m pip install -r requirements.txt
python automation.py sample_input.csv sample_output.csv --dedupe "Customer ID" Email
~~~

The command produces:

- sample_output.csv
- sample_output.summary.json

## Example transformation

Input:

| Customer ID | Name | Email |
|---|---|---|
| 1001 | Alice Smith | ALICE@example.com |
| 1001 | Alice Smith | alice@example.com |

Output:

| customer_id | name | email |
|---|---|---|
| 1001 | Alice Smith | alice@example.com |

## Typical client use cases

- Repetitive Excel/CSV cleanup
- CRM import preparation
- Contact-list deduplication
- Spreadsheet normalization
- Recurring report preparation
- Multi-file preprocessing before analytics

## Run tests

~~~bash
pytest -q
~~~

## Project structure

- automation.py
- sample_input.csv
- sample_output.csv
- sample_output.summary.json
- requirements.txt
- tests/test_automation.py
- .github/workflows/tests.yml

## Delivery style

This demo reflects the same delivery approach used for client work: reusable code, validation, clear outputs, tests, and simple handoff instructions.
