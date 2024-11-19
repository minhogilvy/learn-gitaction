import re
from datetime import datetime
from typing import List

from app.schemas.data_country import CountryDetail


def is_valid_name(name: str) -> bool:
    # Ensure the name only contains alphabetic characters from any language
    # This will match any Unicode letter characters
    return bool(re.match(r'^[^\W\d_]+$', name, re.UNICODE))


def is_valid_phone_number(phone_number: str) -> bool:
    """Validate phone number format."""
    # This is a simple regex for demonstration. Adjust according to your needs.
    phone_pattern = re.compile(r"^\+?1?\d{9,15}$")
    return bool(phone_pattern.match(phone_number))


def is_valid_email(email: str) -> bool:
    # A basic email format validation
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))


def is_valid_country(country: str, valid_countries: List[CountryDetail]) -> bool:
    # Check if the provided country is in the list of valid countries by name
    return country.lower() in [valid_country.name.lower() for valid_country in valid_countries]


def is_valid_date_of_birth(date_of_birth: str) -> bool:
    try:
        # Check if the date is in MM/DD/YYYY format and is a valid date
        datetime.strptime(date_of_birth, '%m/%d/%Y')
        return True
    except ValueError:
        return False


def is_age_valid_range(date_of_birth: str) -> bool:
    try:
        birth_date = datetime.strptime(date_of_birth, '%m/%d/%Y')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Check if the age is within the valid range
        if age < 5 or age > 120:
            return False
        
        # Check if the age is 18 or older
        return True
    except ValueError:
        return False


def is_age_valid_and_18_or_older(date_of_birth: str) -> bool:
    try:
        birth_date = datetime.strptime(date_of_birth, '%m/%d/%Y')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Check if the age is 18 or older
        return age >= 18
    except ValueError:
        return False


def check_valid(user_response_id, interactive):
    for section in interactive.action.sections:
        for row in section.rows:
            if user_response_id == row.id:
                return True
    return False


def check_valid_interactive(user_response_id, interactive):
    for section in interactive.action.buttons:
        if user_response_id == section.reply.id:
            return True
    return False
