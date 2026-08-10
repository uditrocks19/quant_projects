from datetime import date
import calendar


def add_months(d, months):
    """Step a date forward (or back, for negative months) by whole months."""
    month_index = d.month - 1 + months
    year = d.year + month_index // 12
    month = month_index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def year_fraction(start_date, end_date, convention="ACT/365"):
    """
    Convert a date span into a year fraction under the given day count convention.

    convention:
        "ACT/365" - actual days / 365 (default, matches this repo's prior behavior)
        "ACT/360" - actual days / 360, common for money-market instruments
        "30/360"  - each month treated as 30 days, common for corporate bonds
    """
    convention = convention.upper()

    if convention == "ACT/365":
        return (end_date - start_date).days / 365.0

    if convention == "ACT/360":
        return (end_date - start_date).days / 360.0

    if convention == "30/360":
        d1 = min(start_date.day, 30)
        d2 = min(end_date.day, 30) if d1 == 30 else end_date.day
        days = (end_date.year - start_date.year) * 360 \
            + (end_date.month - start_date.month) * 30 \
            + (d2 - d1)
        return days / 360.0

    raise ValueError(f"Unsupported day count convention: {convention}")
