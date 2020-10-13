from typing import List

from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


class People(BaseModel):
    people: List[Person]
