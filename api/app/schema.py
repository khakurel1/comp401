# Import necessary modules and classes
from pydantic import BaseModel, Field, EmailStr, Json
import json


# Define the CreateEvaluationSchema class
class CreateEvaluationSchema(BaseModel):
    tickers: Json

    # Define the schema_extra attribute to provide an example of the expected input format
    class Config:
        schema_extra = {
            "example": {
                "tickers": json.dumps(
                    [
                        {
                            "name": "ticker 1",
                            "symbol": "TIC1"
                        },
                        {
                            "name": "ticker 2",
                            "symbol": "TIC2"

                        },
                        {
                            "name": "ticker 3",
                            "symbol": "TIC3"
                        },
                        {
                            "name": "ticker 4",
                            "symbol": "TIC4"
                        },
                    ]
                )
            }
        }


# Define the UserSchema class
class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    # Define the Config class to configure the behavior of the UserSchema class
    class Config:
        # Set orm_mode to True to enable automatic conversion of the model to and from database records
        orm_mode = True

        # Allow population of fields by field name
        allow_population_by_field_name = True

        # Allow arbitrary types in the model
        arbitrary_types_allowed = True

        # Define the schema_extra attribute to provide an example of the expected input format
        schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@mail.com",
                "password": "weakpassword"
            }
        }


# Define the UserLoginSchema class
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    # Define the schema_extra attribute to provide an example of the expected input format
    class Config:
        schema_extra = {
            "example": {
                "email": "testuser@mail.com",
                "password": "weakpassword"
            }
        }