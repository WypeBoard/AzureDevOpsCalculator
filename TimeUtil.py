from datetime import datetime, date


def parse_to_date(timestamp: str) -> date:
    # Extract only the date part from the timestamp
    date_part = timestamp.split("T")[0]
    # Parse the date part to datetime.date object
    return datetime.strptime(date_part, "%Y-%m-%d").date()

def clean_date(timestamp: str) -> str:
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",  # Full format with milliseconds and Z
        "%Y-%m-%dT%H:%M:%SZ",      # Without milliseconds
        "%Y-%m-%d",                # Date only
        "%Y-%m-%dT%H:%M:%S"        # Without milliseconds and Z
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp, fmt)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        except TypeError:
            print("fuck!")
            continue
    
    raise ValueError("Invalid date format")