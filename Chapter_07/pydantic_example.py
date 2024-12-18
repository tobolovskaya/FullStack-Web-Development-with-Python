from typing import Optional

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from pydantic_core import ValidationError


class User(BaseModel):
    name: str
    email: EmailStr
    website: HttpUrl
    age: Optional[int] = Field(None, ge=13, le=90)
    friends: Optional[int] = 0


user = User(name="John", email="john@example.com", website="https://john.com", age=25, friends=10)
print(user)
# Output: User(name='John', email='john@example.com', website='https://john.com', age=25, friends=10)

try:
    # Validation error (age is below the minimum)
    user = User(name="Jane", email="jane@example.com", website="https://jane.com", age=12)
    print(user)
    # Output: pydantic.error_wrappers.ValidationError: 1 validation error for User
    # age
    #   ensure this value is greater than or equal to 13 (type=value_error.number.not_ge; limit_value=13)
except ValidationError as e:
    print(e)

try:
    # Validation error (website is not a valid URL)
    user = User(name="Bob", email="bob@example.com", website="invalid url", age=20)
    print(user)
    # Output: pydantic.error_wrappers.ValidationError: 1 validation error for User
    # website
    #   invalid or missing URL scheme (type=value_error.url.scheme)
except ValidationError as e:
    print(e)