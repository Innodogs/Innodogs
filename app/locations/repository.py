from typing import List

from sqlalchemy import text

from app import db
from app.utils.helpers import QueryHelper
from .models import LocationMapping, Location


class LocationsRepository:
    """Repository for locations"""

    @classmethod
    def get_all_locations(cls) -> List[Location]:
        columns = QueryHelper.get_columns_string(LocationMapping, "locations")
        stmt = text("SELECT {columns} FROM {table} locations"
                    .format(columns=columns,
                            table=LocationMapping.description))
        result = db.session.query(Location).from_statement(stmt).all()
        return result

    @classmethod
    def is_cyclic_dependency(cls, location_id: int, parent_id: int) -> bool:
        """
        Checks, whether ou will be cyclic dependency, if location with location id is have
        given parent_id.
        :param location_id: Location id of checked node
        :param parent_id: Potential parent id for thid node
        :return: True, if cyclic dependency will take place, False - otherwise
        """
        return cls.is_sublocation(parent_id, location_id)

    @classmethod
    def is_sublocation(cls, checked_id: int, location_id: int) -> bool:
        """
        Checks, whether location with given checked_id is sublocation
        location with given location_id
        :param checked_id:
        :param location_id:
        :return: True, if location with given checked_id is a sublocation of
        location with given location_id
        """
        stmt = text("WITH RECURSIVE r AS "
                    "(SELECT id, parent_id FROM {locations_table} AS locations WHERE parent_id = :location_id "
                    "UNION "
                    "SELECT locations.id, locations.parent_id FROM {locations_table} AS locations "
                    "JOIN r ON locations.parent_id = r.id) "
                    "SELECT count(*) FROM r WHERE id = :checked_id"
                    .format(locations_table=LocationMapping.description))
        result = db.engine.execute(stmt.params(location_id=location_id, checked_id=checked_id))
        return True if next(iter(result))[0] != 0 else False
