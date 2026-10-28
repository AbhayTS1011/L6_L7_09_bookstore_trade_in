# L6_L7_09 — Bookstore Trade-In

Lab 6: Code and Branch Coverage

## About

A small Python module that evaluates used book trade-in values across formats, wear conditions, and counterfeit alerts, and monitors optical barcode scanners for misread rates.

## Files

| File | Description |
|------|-------------|
| `bookstore_trade_in.py` | The module under test |
| `test_bookstore_trade.py` | Starter test file |

Keep all your Lab 6 work in this folder. The upstream repository contains Lab 6 only; Lab 7 is not included.

Refer to the lab handout for instructions.
## Coverage deliverables

The code-coverage and branch-coverage test suites are kept separately as required by the Lab 6 handout. Run these commands from this folder:

```powershell
python -m coverage erase
python -m coverage run -m pytest -q CodeCoverageTest_bookstore_trade_in.py
python -m coverage report -m bookstore_trade_in.py

python -m coverage erase
python -m coverage run --branch -m pytest -q BranchCoverageTest_bookstore_trade_in.py
python -m coverage report -m bookstore_trade_in.py
```

Both suites currently pass 27 tests and report 100% line and branch coverage. The corresponding result images are in `screenshots/`.

