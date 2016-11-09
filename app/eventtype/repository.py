from typing import List

from sqlalchemy import text

from app import db
from app.eventtype.models import EventType, EventTypeMapping
from app.utils.query_helper import QueryHelper

__author__ = 'Xomak'


class EventTypeRepository:
    """
    Repository class for EventType
    """

    @classmethod
    def get_all_event_types(cls) -> List[EventType]:
        """Gets all types of events"""

        et_columns_string = QueryHelper.get_columns_string(EventTypeMapping, "event_type")
        stmt = text("SELECT {et_columns} FROM {et_table}"
                    .format(et_columns=et_columns_string,
                            et_table=EventTypeMapping.description))
        result = db.session.query(EventType).from_statement(stmt).all()
        return result

    @classmethod
    def add_new_event_type(cls, eventtype):
        """Add new type of events"""
        columns, substitutions, params_dict = QueryHelper.get_insert_string_and_dict(EventTypeMapping, eventtype, fields_to_exclude=['id'])
        quert = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
                     table_name=EventTypeMapping.description, columns=columns, substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))


    @classmethod
    def update_event_type(cls, eventtype):
        """Updates existed event type"""

        update_clause, params_dict = QueryHelper.get_update_string_and_dict(EventTypeMapping, eventtype,
                                                                            fields_to_exclude=['id'])
        query = text("UPDATE %s SET %s WHERE id = :id" % (EventTypeMapping.description, update_clause))
        params_dict['id'] = eventtype.id
        db.engine.execute(query.params(**params_dict))

    @classmethod
    def delete_event_type(cls, type_id):
        """Delete event type"""
        query = text("DELETE FROM {table_name} WHERE id = {id}".format(table_name=EventTypeMapping.description, id=type_id))
        db.engine.execute(query)
