from datetime import datetime

def is_date(string):
    """
    Check if the string is a date.
    """
    try:
        datetime.strptime(string, "%Y/%m/%d")
        return True
    except ValueError:
        return False