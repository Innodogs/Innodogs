from typing import List

from sqlalchemy import text

from app import db
from app.utils.helpers import QueryHelper
from .models import EventType, EventTypeMapping, EventMapping, Event

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
    def get_significant_event_types(cls) -> List[EventType]:
        """Gets significant events types"""

        et_columns_string = QueryHelper.get_columns_string(EventTypeMapping, "event_type")
        stmt = text("SELECT {et_columns} FROM {et_table} WHERE {is_significant_column} = TRUE"
                    .format(et_columns=et_columns_string,
                            et_table=EventTypeMapping.description,
                            is_significant_column=QueryHelper.get_column_by_key(EventTypeMapping, 'is_significant')))
        result = db.session.query(EventType).from_statement(stmt).all()
        return result

    @classmethod
    def get_event_type_by_id(cls, event_type_id):
        """Get type of event"""
        et_columns_string = QueryHelper.get_columns_string(EventTypeMapping, "event_type")
        stmt = text("SELECT {et_columns} FROM {et_table} WHERE id = :id"
                    .format(et_columns=et_columns_string,
                            et_table=EventTypeMapping.description))
        result = db.session.query(EventType).from_statement(stmt).params(id=event_type_id).one()
        return result

    @classmethod
    def add_new_event_type(cls, eventtype):
        """Add new type of events"""
        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(EventTypeMapping, eventtype,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=EventTypeMapping.description,
            columns=columns,
            substitutions=substitutions))
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
        query = text(
            "DELETE FROM {table_name} AS e WHERE e.id = {id}".format(table_name=EventTypeMapping.description,
                                                                     id=type_id))
        db.engine.execute(query)

    @classmethod
    def is_event_type_free(cls, type_id):
        """Check if this type of events is used"""
        query = text("SELECT e.id FROM {event_table_name} AS e WHERE event_type_id = {id}".format(
            event_table_name=EventMapping.description,
            id=type_id))
        result = db.engine.execute(query).fetchall()
        return len(result) == 0


class EventRepository:

    @classmethod
    def get_event_by_id(cls, event_id: int):
        """Get event by id"""

        event_columns_string = QueryHelper.get_columns_string(EventMapping, "events")
        stmt = text("SELECT {event_columns} FROM {events_table} AS events WHERE id = :id"
                    .format(event_columns=event_columns_string,
                            events_table=EventMapping.description))
        result = db.session.query(Event).from_statement(stmt).params(id=event_id).one()
        return result

    @classmethod
    def add_new_event(cls, event: Event):
        """Add new event"""
        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(EventMapping, event,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=EventMapping.description,
            columns=columns,
            substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))

    @classmethod
    def update_event(cls, event: Event):
        """Updates existing event"""

        update_clause, params_dict = QueryHelper.get_update_string_and_dict(EventMapping, event,
                                                                            fields_to_exclude=['id'])
        query = text("UPDATE %s SET %s WHERE id = :id" % (EventMapping.description, update_clause))
        params_dict['id'] = event.id
        db.engine.execute(query.params(**params_dict))
