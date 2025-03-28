import random

# Helper function to generate unique ID
# generate_unique_id = lambda start, end: f"{random.randint(start, end)}"

def generate_unique_id(start: int = 1000, end: int = 9999) -> int:
    return random.randint(start, end)


