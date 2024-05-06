import pandas as pd
from .database import Base
# from sqlalchemy import ForeignKey


def get_stock_tickers(name: str = "", limit: int = 10):
    df = pd.read_csv('./tickers_nasdaq.csv')
    return df[
        (df['Symbol'].str.contains(name, na=False)) |
        (df['Security Name'].str.lower().str.contains(name.lower(), na=False))
    ].head(limit)


def model_single_response(record: Base):
    # model.
    pass


def get_relationship_model_name(instance, relationship_name):
    relationship_property = getattr(
        instance.__class__, relationship_name).property
    return relationship_property.mapper.class_.__name__


def model_list_response(records: list[Base]):
    response = []
    for record in records:
        item = {
            "attributes": {},
            "relationships": {},
        }

        for column in record.__table__.columns:
            if column.name == "id":
                item[column.name] = getattr(record, column.name, None)
            elif column.name == "user":
                item["relationships"] = {
                    "user":  getattr(record, column.name, None),
                }
            else:
                item["attributes"][column.name] = getattr(
                    record, column.name, None)
        response.append(item)
    return response
