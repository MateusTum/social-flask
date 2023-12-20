import random
import string
from datetime import datetime


def generate_unique_filename(file_extension, length=10):
    characters = string.ascii_letters + string.digits
    random_sequence = ''.join(random.choice(characters) for _ in range(length))
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{timestamp}_{random_sequence}{file_extension}"
