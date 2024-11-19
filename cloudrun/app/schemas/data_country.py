from typing import List
from pydantic import BaseModel


class CountryDetail(BaseModel):
    name: str
    alpha_code: str


class Country(BaseModel):
    valid_countries: List[CountryDetail]
