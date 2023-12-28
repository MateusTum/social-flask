import random
import string
from datetime import datetime


def generate_unique_filename(file_extension, length=10):
    characters = string.ascii_letters + string.digits
    random_sequence = ''.join(random.choice(characters) for _ in range(length))
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{timestamp}_{random_sequence}{file_extension}"


def format_current_datetime(date):
    """
    Get the current date and time and format it as month/day/year.

    Returns:
    str: Formatted date string in the "month/day/year" format.
    """
    # Get the current date and time
    current_datetime = date

    # Format the date as month/day/year
    formatted_date = current_datetime.strftime("%m/%d/%Y")

    return formatted_date
