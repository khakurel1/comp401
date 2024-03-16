from pydantic import BaseModel, Field, EmailStr, Json
import json


class CreateEvaluationSchema(BaseModel):
    tickers: Json

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


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@mail.com",
                "password": "weakpassword"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "testuser@mail.com",
                "password": "weakpassword"
            }
        }
