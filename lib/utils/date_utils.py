from datetime import datetime, timedelta

__all__ = ['is_edt', 'find_transition_dates']

def find_transition_dates(year):
    """
    Find the dates for the transition between EST and EDT for a given year.
    EST to EDT: Second Sunday in March.
    EDT to EST: First Sunday in November.
    """
    # Second Sunday in March
    march_first = datetime(year, 3, 1)
    est_to_edt = march_first + timedelta(days=(6 - march_first.weekday()) % 7 + 7)

    # First Sunday in November
    november_first = datetime(year, 11, 1)
    edt_to_est = november_first + timedelta(days=(6 - november_first.weekday()) % 7)

    return est_to_edt, edt_to_est


def is_edt(date):
    """
    Determine if a given date is in Eastern Daylight Time (EDT).
    """
    year = date.year
    est_to_edt, edt_to_est = find_transition_dates(year)

    return est_to_edt <= date < edt_to_est
