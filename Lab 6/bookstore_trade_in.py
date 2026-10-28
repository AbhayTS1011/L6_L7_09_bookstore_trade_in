FORMAT_BASE_VALUES = {
    "textbook": 40.0,
    "hardcover": 15.0,
    "paperback": 8.0,
}


def process_book_buybacks(batches, store_credit_bonus):
    """Evaluate used book trade-in buybacks."""
    if not isinstance(batches, list) or store_credit_bonus < 0:
        raise ValueError("Invalid batches list or credit bonus")

    total_payout = 0.0
    rejected_items = 0

    for batch in batches:
        if not batch.get("intake_approved", False):
            continue

        format_type = batch.get("format", "paperback")
        base_value = FORMAT_BASE_VALUES.get(format_type)

        if base_value is None:
            rejected_items += 1
            continue

        books = batch.get("books", [])

        batch_credit = 0.0

        for book in books:
            pages_missing = book.get("missing_pages", 0)
            condition = book.get("condition", "good")
            is_counterfeit = book.get("counterfeit", False)

            if pages_missing > 0:
                rejected_items += 1
                continue

            if is_counterfeit:
                rejected_items += 1
                batch_credit = 0.0
                break
            elif condition == "mint":
                batch_credit += base_value * 1.25
            elif condition == "poor":
                batch_credit += base_value * 0.40
            else:
                batch_credit += base_value

        if batch.get("payout_in_credit", False):
            batch_credit += store_credit_bonus

        total_payout += batch_credit

    if rejected_items > 4:
        status = "AUDIT_REJECTED"
    elif total_payout == 0.0:
        status = "ZERO_CREDIT"
    else:
        status = "COMPLETED"
    return {"total_payout": round(total_payout, 2), "status": status}


def inspect_scanner_calibration(scanner_matrix):
    """Monitor optical barcode scanner calibration status."""
    if not scanner_matrix:
        return "NO_DATA"

    for device_readings in scanner_matrix:
        misread_streak = 0
        for error_rate in device_readings:
            if error_rate > 5:
                misread_streak += 1
                if misread_streak >= 2:
                    return "RECALIBRATE"
            else:
                misread_streak = 0
    return "CALIBRATED"
