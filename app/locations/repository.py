from sqlalchemy import text

from app import db
from app.utils.query_helper import QueryHelper
from .models import LocationMapping, Location


class LocationsRepository:
    """Repository for locations"""

    @classmethod
    def get_all_locations(cls):
        columns = QueryHelper.get_columns_string(LocationMapping, "locations")
        stmt = text("SELECT {columns} FROM {table} locations"
                    .format(columns=columns,
                            table=LocationMapping.description))
        result = db.session.query(Location).from_statement(stmt).all()
        return result
