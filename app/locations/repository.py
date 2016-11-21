from typing import List

from sqlalchemy import text

from app import db
from app.utils.helpers import QueryHelper
from app.dogs.models import DogMapping
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

    @classmethod
    def add_new_location(cls, location):
        """
	    Add new repository to data base
	"""
        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(LocationMapping, location, fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
	             table_name=LocationMapping.description,
		     columns=columns,
		     substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))

    @classmethod
    def update_location(cls, location):
        """Update existing location"""
        update_clause, params_dict = QueryHelper.get_update_string_and_dict(LocationMapping, location, fields_to_exclude=['id'])
        query = text('UPDATE {table_name} SET {update} WHERE id=:id'.format(
	              table_name=LocationMapping.description, 
		      update=update_clause))
        params_dict['id'] = location.id
        db.engine.execute(query.params(**params_dict))
    
    @classmethod
    def delete_location(cls, location_id):
        """Delete location from database"""
        query = text('DELETE FROM {table_name} AS l WHERE l.id = {id}'.format(
                      table_name=LocationMapping.description,
                      id=location_id))
        db.engine.execute(query)

    @classmethod
    def get_location_by_id(cls, location_id):
        """Return object of location by its ID"""
        loc_column_string = QueryHelper.get_columns_string(LocationMapping, "location")
        query = text("SELECT {loc_column} FROM {table_name} WHERE id = :id".format(
                      table_name=LocationMapping.description,
                      loc_column=loc_column_string))
        result = db.session.query(Location).from_statement(query).params(id=location_id).one()
        return result

    @classmethod
    def is_location_free(cls, location_id):
        """Check if location is not used"""
        query = text("SELECT d.id FROM {dog_table} AS d WHERE location_id = {id}".format(
                      dog_table=DogMapping.description,
                      id=location_id))
        result = db.engine.execute(query).fetchall()
        return len(result) == 0