# Lab 6 branch coverage suite. Run from this folder with:
# python -m coverage run --branch -m pytest -q BranchCoverageTest_bookstore_trade_in.py
import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration


def test_invalid_batches_not_list():
    with pytest.raises(ValueError):
        process_book_buybacks("not_a_list", 5.0)


def test_negative_store_credit_bonus():
    with pytest.raises(ValueError):
        process_book_buybacks([], -1.0)


def test_batch_not_approved():
    batches = [{"intake_approved": False, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_textbook_mint_condition():
    batches = [{"intake_approved": True, "format": "textbook", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 50.0


def test_textbook_poor_condition():
    batches = [{"intake_approved": True, "format": "textbook", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 16.0


def test_textbook_counterfeit():
    batches = [{"intake_approved": True, "format": "textbook", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_hardcover_mint_condition():
    batches = [{"intake_approved": True, "format": "hardcover", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 18.75


def test_hardcover_poor_condition():
    batches = [{"intake_approved": True, "format": "hardcover", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 6.0


def test_paperback_mint_condition():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 10.0


def test_paperback_poor_condition():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 3.2


def test_unknown_format():
    batches = [{"intake_approved": True, "format": "unknown", "payout_in_credit": False}]
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_book_with_missing_pages():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 1, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "ZERO_CREDIT"


def test_counterfeit_paperback():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0


def test_counterfeit_hardcover():
    batches = [{"intake_approved": True, "format": "hardcover", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 0.0


def test_payout_in_credit_true():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": True}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 13.0


def test_audit_rejected_six_rejections():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
        }
    ]
    books = [{"missing_pages": 1, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    batches.append({"intake_approved": True, "format": "paperback", "payout_in_credit": False})
    batches[1]["books"] = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches.append({"intake_approved": True, "format": "unknown", "payout_in_credit": False})
    batches.append({"intake_approved": True, "format": "paperback", "payout_in_credit": False})
    books_poor = [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
    batches[2]["books"] = books_poor
    batches.append({"intake_approved": True, "format": "paperback", "payout_in_credit": False})
    books_cf = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches[3]["books"] = books_cf
    batches.append({"intake_approved": True, "format": "paperback", "payout_in_credit": False})
    books_gf = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches[4]["books"] = books_gf
    batches.append({"intake_approved": True, "format": "unknown", "payout_in_credit": False})
    result = process_book_buybacks(batches, 5.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_zero_credit_all_batches():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": True}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_completed_status():
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_inspect_scanner_calibration_empty():
    result = inspect_scanner_calibration([])
    assert result == "NO_DATA"


def test_inspect_scanner_calibration_recalibrate():
    matrix = [[6, 6], [3, 4]]
    result = inspect_scanner_calibration(matrix)
    assert result == "RECALIBRATE"


def test_inspect_scanner_calibrate_good():
    matrix = [[3, 4], [2, 1]]
    result = inspect_scanner_calibration(matrix)
    assert result == "CALIBRATED"


def test_inspect_scanner_calibration_mixed():
    matrix = [[6, 3], [4, 2]]
    result = inspect_scanner_calibration(matrix)
    assert result == "CALIBRATED"


def test_multiple_books_same_format():
    """Test batch with multiple books of the same format and condition."""
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [
        {"missing_pages": 0, "condition": "mint", "counterfeit": False},
        {"missing_pages": 0, "condition": "good", "counterfeit": False},
        {"missing_pages": 0, "condition": "poor", "counterfeit": False},
    ]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 21.2


def test_mixed_formats_single_book():
    """Test batch with mixed format types (only one format counted)."""
    batches = [{"intake_approved": True, "format": "hardcover", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    batches[0]["books"] = books
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 18.75


def test_multiple_batches():
    """Test multiple batches processed in sequence."""
    batches = [{"intake_approved": True, "format": "paperback", "payout_in_credit": False}]
    books = [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
    batches[0]["books"] = books
    batches.append({"intake_approved": True, "format": "textbook", "payout_in_credit": False})
    books2 = [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
    batches[1]["books"] = books2
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 58.0


def test_inspect_scanner_single_high_error():
    """Test scanner calibration with single high error rate (should be CALIBRATED)."""
    matrix = [[3, 6], [2, 1]]
    result = inspect_scanner_calibration(matrix)
    assert result == "CALIBRATED"


def test_inspect_scanner_consecutive_high_errors():
    """Test scanner calibration with 2 consecutive high error rates in same row."""
    matrix = [[3, 6, 7], [2, 1]]
    result = inspect_scanner_calibration(matrix)
    assert result == "RECALIBRATE"
