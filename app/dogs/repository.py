from typing import List, Tuple

from sqlalchemy import text

from app import db
from app.dogs.models import Dog, DogMapping
from app.events.models import EventMapping, Event, ExpenditureEventMapping, Expenditure, FinancialEvent
from app.locations.models import LocationMapping, Location
from app.utils.query_helper import QueryHelper

__author__ = 'Xomak'


class DogsRepository:
    """
    Repository class for Dogs
    """

    @classmethod
    def get_all_dogs(cls) -> List[Dog]:
        """Gets all dogs, joined with location"""

        dog_columns_string = QueryHelper.get_columns_string(DogMapping, "dogs")
        location_columns_string = QueryHelper.get_columns_string(LocationMapping, "locations")
        stmt = text(
            "SELECT {dog_columns}, {location_columns} FROM {dogs_table} AS dogs LEFT OUTER JOIN {locations_table} "
            "AS locations ON dogs.location_id = locations.id "
            .format(dog_columns=dog_columns_string,
                    location_columns=location_columns_string,
                    dogs_table=DogMapping.description, locations_table=LocationMapping.description))
        result = db.session.query(Dog, Location).from_statement(stmt).all()

        requests = []
        for join_tuple in result:
            requests.append(cls._tuple_to_dog_and_location(join_tuple))
        return requests

    @classmethod
    def _tuple_to_dog_and_location(cls, join_tuple: Tuple[Dog, Location]):
        """
        Converts tuple (Dog, Location) to Dog with dog.location = location
        :param join_tuple: Input tuple
        :return: Dog with location
        """
        dog = join_tuple[0]
        dog.location = join_tuple[1]

        return dog

    @classmethod
    def _tuple_to_dog_and_location_and_events(cls, join_tuples: List[Tuple[Dog, Location, Event, Expenditure]]):
        """
        Converts tuple (Dog, Location, Event, Expenditure) to Dog with dog.location = location
        and dog.event_list = [event], dog.financial_event_list = [financial_event] accordingly

        :param join_tuple: Input tuple
        :return: Dog with location and event list
        """
        if len(join_tuples) == 0:
            return None
        dog = cls._tuple_to_dog_and_location(join_tuples[0])
        dog.event_list = []
        dog.financial_event_list = []
        for record in join_tuples:
            if record[3]:
                dog.financial_event_list.append(FinancialEvent(record[2], record[3]))
            else:
                dog.event_list.append(record[2])

        return dog

    @classmethod
    def get_dog_by_id(cls, dog_id) -> Dog:
        """Returns dog by given id or throws an exception"""

        dog_columns_string = QueryHelper.get_columns_string(DogMapping, "dogs")
        location_columns_string = QueryHelper.get_columns_string(LocationMapping, "locations")
        stmt = text("SELECT {dog_columns}, {location_columns} FROM {dogs_table} AS dogs LEFT JOIN {locations_table} "
                    "AS locations ON dogs.location_id = locations.id WHERE dogs.id = :id "
                    .format(dog_columns=dog_columns_string,
                            location_columns=location_columns_string,
                            dogs_table=DogMapping.description, locations_table=LocationMapping.description))
        dog_id = int(dog_id)
        result = db.session.query(Dog, Location).from_statement(stmt).params(id=dog_id).one()
        return cls._tuple_to_dog_and_location(result)

    @classmethod
    def get_dog_by_id_with_events(cls, dog_id: int) -> Dog:
        """Returns dog by given id with location and all events or throws an exception"""

        dog_columns_string = QueryHelper.get_columns_string(DogMapping, "dogs")
        location_columns_string = QueryHelper.get_columns_string(LocationMapping, "locations")
        events_columns_string = QueryHelper.get_columns_string(EventMapping, "events")
        expenditure_columns_string = QueryHelper.get_columns_string(ExpenditureEventMapping, "expenditures")

        stmt = text("SELECT {dog_columns}, {location_columns}, {event_columns}, {expenditure_columns} "
                    "FROM {dogs_table} AS dogs "
                    "LEFT JOIN {locations_table} AS locations ON dogs.location_id = locations.id "
                    "JOIN {event_table} AS events ON dogs.id = events.dog_id "
                    "LEFT JOIN {expenditure_table} AS expenditures ON events.expenditure_id = expenditures.id "
                    "WHERE dogs.id = :id "
                    .format(dog_columns=dog_columns_string,
                            location_columns=location_columns_string,
                            event_columns=events_columns_string,
                            expenditure_columns=expenditure_columns_string,
                            dogs_table=DogMapping.description,
                            locations_table=LocationMapping.description,
                            event_table=EventMapping.description,
                            expenditure_table=ExpenditureEventMapping.description
                            ))
        dog_id = int(dog_id)
        result = db.session.query(Dog, Location, Event, Expenditure).from_statement(stmt).params(id=dog_id).all()
        return cls._tuple_to_dog_and_location_and_events(result)

    @classmethod
    def update_dog(cls, dog):
        """Updates given Dog"""

        update_clause, params_dict = QueryHelper.get_update_string_and_dict(DogMapping, dog,
                                                                            fields_to_exclude=['id'])
        query = text("UPDATE %s SET %s WHERE id = :dog_id" % (DogMapping.description, update_clause))
        params_dict['dog_id'] = dog.id
        db.engine.execute(query.params(**params_dict))

    @classmethod
    def new_dog(cls, dog):
        """Add new dog to database"""

        columns, substitutions, params_dict = QueryHelper.get_insert_string_and_dict(DogMapping, dog,
                                                                                     fields_to_exclude=['id'])
        quert = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=DogMapping.description, columns=columns, substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))
