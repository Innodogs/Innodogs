from typing import List, Tuple, Iterable, Dict

from sqlalchemy import text

from app import db
from app.dogs.proxy_models import DogWithSignificantEvents
from app.events.models import EventMapping, Event, ExpenditureEventMapping, Expenditure, FinancialEvent, \
    EventTypeMapping, EventType
from app.dogs.models import Dog, DogMapping, DogPictureMapping, DogPicture
from app.events.proxy_models import EventWithEventType
from app.dogs.models import Dog, DogMapping, DogPictureMapping, DogPicture
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
        """Gets all dogs, joined with location and main_picture"""

        dog_columns_string = QueryHelper.get_columns_string(DogMapping, "dogs")
        location_columns_string = QueryHelper.get_columns_string(LocationMapping, "locations")
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")
        stmt = text(
            "SELECT {dog_columns}, {location_columns}, {picture_columns} FROM {dogs_table} AS dogs "
            "LEFT OUTER JOIN {locations_table} AS locations ON dogs.location_id = locations.id "
            "LEFT OUTER JOIN {pictures_table} AS dog_pictures ON dogs.id = dog_pictures.dog_id AND dog_pictures.is_main = true"
                .format(dog_columns=dog_columns_string,
                        location_columns=location_columns_string,
                        picture_columns=picture_columns,
                        dogs_table=DogMapping.description,
                        locations_table=LocationMapping.description,
                        pictures_table=DogPictureMapping.description
                        ))
        result = db.session.query(Dog, Location, DogPicture).from_statement(stmt).all()

        requests = []
        for join_tuple in result:
            requests.append(cls._tuple_to_dog_and_location_and_picture(join_tuple))
        return requests

    @classmethod
    def get_dogs_count_satisfying_criteria(cls, **kwargs) -> int:
        """
        Returns count of dogs, satisfying given criteria.
        See get_dogs_with_significant_events method for criteria
        :param kwargs: Criteria
        :return: Dogs' count
        """
        stmt, bind_values = cls._get_query_part_for_criteria(**kwargs, fields_to_select=['count(*) OVER()'])
        result = db.engine.execute(text(stmt).params(bind_values)).fetchone()
        if result is not None:
            return result[0]
        else:
            return 0

    @classmethod
    def get_dogs_with_significant_events(cls, dogs_statement: str = None, bind_values: Dict = None,
                                         from_row: int = None, rows_count: int = None) -> List[
        DogWithSignificantEvents]:
        """
        Get DogWithSignificantEvents proxy model list, containing dog and related significant event.
        Query string could be passed to filter this list.
        :param rows_count: Number of dogs
        :param from_row: Get dogs from given row number
        :param dogs_statement: String with query, returning ids of dogs,
        that should be included in result list
        :param bind_values: Dictionary with values, which should be binded to this query
        :return: List of DogWithSignificantEvents, satisfying given query
        """

        dogs_limit_query_string = ""

        query_params = {}
        if bind_values is not None:
            query_params = {**bind_values, **query_params}

        if dogs_statement is None or len(dogs_statement) == 0:
            dogs_statement = ""
        else:
            dogs_statement = " WHERE id IN (%s)" % dogs_statement

        if from_row is not None:
            limit_statement, limit_params = QueryHelper.get_limit_query_part(from_row, rows_count)
            dogs_statement += limit_statement
            query_params = {**limit_params, **query_params}

        dog_columns_string_prefixed = QueryHelper.get_columns_string(DogMapping, "dogs")
        event_columns_string_prefixed = QueryHelper.get_columns_string(EventMapping, "events")
        event_type_columns_string_prefixed = QueryHelper.get_columns_string(EventTypeMapping, "event_types")
        location_columns_string_prefixed = QueryHelper.get_columns_string(LocationMapping, "locations")
        picture_columns_string_prefixed = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")

        dog_columns_string = ", ".join(QueryHelper.get_columns_list(DogMapping))
        event_columns_string = ", ".join(QueryHelper.get_columns_list(EventMapping))
        event_type_columns_string = ", ".join(QueryHelper.get_columns_list(EventTypeMapping))

        stmt = text(
            "SELECT {dog_columns_prefixed}, {location_columns_prefixed}, {picture_columns_prefixed}, events.* FROM "
            "(SELECT {dog_columns} FROM {dogs_table}{dogs_statement}) AS dogs "
            "LEFT JOIN (SELECT {event_columns_prefixed}, {event_type_columns_prefixed} FROM {events_table} AS events "
            "INNER JOIN {event_types_table} AS event_types ON events.event_type_id = event_types.id AND event_types.is_significant = TRUE) AS events "
            "ON events.event_dog_id = dogs.id "
            "LEFT OUTER JOIN {locations_table} AS locations ON dogs.location_id = locations.id "
            "LEFT OUTER JOIN {pictures_table} AS dog_pictures ON dogs.id = dog_pictures.dog_id "
            "AND dog_pictures.is_main = true ORDER BY dogs.id"
                .format(dog_columns_prefixed=dog_columns_string_prefixed,
                        dog_columns=dog_columns_string,
                        event_columns=event_columns_string,
                        event_type_columns=event_type_columns_string,
                        event_type_columns_prefixed=event_type_columns_string_prefixed,
                        location_columns_prefixed=location_columns_string_prefixed,
                        picture_columns_prefixed=picture_columns_string_prefixed,
                        dogs_table=DogMapping.description,
                        locations_table=LocationMapping.description,
                        pictures_table=DogPictureMapping.description,
                        events_table=EventMapping.description,
                        event_types_table=EventTypeMapping.description,
                        dogs_limit=dogs_limit_query_string,
                        event_columns_prefixed=event_columns_string_prefixed,
                        dogs_statement=dogs_statement
                        ))
        result = db.session.query(Dog, Location, DogPicture, Event, EventType).from_statement(stmt).params(
            **query_params).all()

        dogs = list()
        active_dog = None
        for join_tuple in result:
            current_dog = join_tuple[0]
            current_location = join_tuple[1]
            current_picture = join_tuple[2]
            current_event = join_tuple[3]
            current_event_type = join_tuple[4]

            if active_dog is None or current_dog != active_dog.dog:
                if active_dog is not None:
                    dogs.append(active_dog)
                active_dog = DogWithSignificantEvents(
                    cls._args_tuple_to_dog_and_location_and_picture(current_dog, current_location, current_picture))
            if current_event is not None:
                active_dog.add_event(EventWithEventType(current_event, current_event_type))

        if active_dog is not None:
            dogs.append(active_dog)
        return dogs

    @classmethod
    def get_dogs_with_significant_events_by_criteria(cls, name: str = None, is_adopted: bool = None, sex: str = None,
                                                     event_types_ids: List[int] = None, from_row=None, rows_count=None)\
            -> List[DogWithSignificantEvents]:
        """
        Get DogWithSignificantEvents list, satisfying given criteria
        :param rows_count: Maximum count of dogs
        :param from_row: Start row
        :param name: Dog's name (LIKE query is used)
        :param is_adopted: Is dog adopted
        :param sex: Dog's sex
        :param event_types_ids: List of event types' ids, such all of them should be presented in
        dog's history
        :return: List of DogWithSignificantEvents, satisfying given criteria
        """
        stmt, bind_values = cls._get_query_part_for_criteria(name, is_adopted, sex, event_types_ids)
        return cls.get_dogs_with_significant_events(stmt, bind_values, from_row=from_row, rows_count=rows_count)

    @classmethod
    def _get_query_part_for_criteria(cls, name: str = None, is_adopted: bool = None, sex: str = None,
                                     event_types_ids: List[int] = None, fields_to_select: List[str] = None) -> Tuple[
        str, Dict]:
        """
        Get query, which finds all dogs' ids, satisfying given criteria
        :param name: Dog's name (LIKE query is used)
        :param is_adopted: Is dog adopted
        :param sex: Dog's sex
        :param event_types_ids: List of event types' ids, such all of them should be presented in
        dog's history
        :return: Query and Param's dict
        """
        in_substitutes_string = ""
        where_clause = ""
        bind_values = {}

        if event_types_ids is not None and len(event_types_ids) > 0:
            event_index = 0
            for event_type_id in event_types_ids:
                if len(in_substitutes_string) > 0:
                    in_substitutes_string += " ,"
                in_substitutes_string += ":event_type_id_%s" % event_index
                bind_values["event_type_id_%s" % event_index] = event_type_id
                event_index += 1

            bind_values['dog_lines_count'] = len(event_types_ids)
        else:
            event_types_ids = []

        if fields_to_select is None:
            fields_to_select = ['dogs.id']

        if name is not None:
            where_clause = " dogs.name LIKE :dog_name"
            bind_values['dog_name'] = '%' + name + '%'

        if sex is not None:
            if len(where_clause) > 0:
                where_clause += " AND"
            where_clause += " dogs.sex = :dog_sex"
            bind_values['dog_sex'] = sex

        if is_adopted is not None:
            if len(where_clause) > 0:
                where_clause += " AND"
            where_clause += " dogs.is_adopted = :is_adopted"
            bind_values['is_adopted'] = is_adopted

        stmt = "SELECT {fields_to_select} FROM {dogs_table} AS dogs"
        if len(event_types_ids) > 0:
            stmt += " INNER JOIN (SELECT DISTINCT(event_type_id), dog_id FROM {events_table}) " \
                    "AS events ON events.dog_id = dogs.id AND events.event_type_id IN ({in_substitutes})"
        if len(where_clause) > 0:
            stmt += " WHERE {where_clause}"
        if len(event_types_ids) > 0:
            stmt += " GROUP BY dogs.id HAVING count(*) = :dog_lines_count"
        stmt = stmt.format(
            dogs_table=DogMapping.description,
            events_table=EventMapping.description,
            where_clause=where_clause,
            in_substitutes=in_substitutes_string,
            fields_to_select=', '.join(fields_to_select)
        )

        return stmt, bind_values

    @classmethod
    def _tuple_to_dog_and_location(cls, join_tuple: Tuple[Dog, Location]):
        """
        Converts tuple (Dog, Location) to Dog with dog.location = location
        :param join_tuple: Input tuple
        :return: Dog with location
        """
        dog = join_tuple[0]
        dog.location = join_tuple[1]

        return cls._args_tuple_to_dog_and_location_and_picture(join_tuple[0], join_tuple[1])

    @classmethod
    def _args_tuple_to_dog_and_location_and_picture(cls, dog, location=None, main_picture=None):
        """
        Sets given params as dog's properties
        :param dog: Dog to set parameters on
        :param location: Location
        :param main_picture: Main picture
        :return: Same dog
        """
        dog.location = location
        dog.main_picture = main_picture
        return dog

    @classmethod
    def _tuple_to_dog_and_location_and_picture(cls, join_tuple):
        """
        Converts tuple (Dog, Location, DogPicture) to Dog with dog.location = location and
        dog.main_picture = picture
        :param join_tuple: Input tuple
        :return: Dog with location and picture
        """

        return cls._args_tuple_to_dog_and_location_and_picture(join_tuple[0], join_tuple[1], join_tuple[2])

    @classmethod
    def get_dog_by_id_with_pictures(cls, dog_id) -> Dog:
        """Returns dog by given id with pictures or throws an exception"""

        dog_columns_string = QueryHelper.get_columns_string(DogMapping, "dogs")
        location_columns_string = QueryHelper.get_columns_string(LocationMapping, "locations")
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")
        stmt = text(
            "SELECT {dog_columns}, {location_columns}, {picture_columns} FROM {dogs_table} AS dogs "
            "LEFT JOIN {locations_table} AS locations ON dogs.location_id = locations.id "
            "LEFT JOIN {pictures_table} AS dog_pictures ON dogs.id = dog_pictures.dog_id "
            "WHERE dogs.id = :id "
                .format(dog_columns=dog_columns_string,
                        location_columns=location_columns_string,
                        picture_columns=picture_columns,
                        pictures_table=DogPictureMapping.description,
                        dogs_table=DogMapping.description, locations_table=LocationMapping.description))
        dog_id = int(dog_id)
        result_tuples = db.session.query(Dog, Location, DogPicture).from_statement(stmt).params(id=dog_id).all()
        dog = None
        for result_tuple in result_tuples:
            if dog is None:
                dog = result_tuple[0]
                dog.pictures = []

            if not hasattr(dog, "location"):
                dog.location = result_tuple[1]

            picture = result_tuple[2]
            if picture is not None:
                if picture.is_main:
                    dog.main_picture = picture
                else:
                    dog.pictures.append(picture)

        return dog

    @classmethod
    def get_dog_by_id_and_pics_and_events_and_location(cls, dog_id: int) -> Dog:
        dog = cls.get_dog_by_id_with_events(dog_id)
        pictures = DogPictureRepository.get_pictures_by_dog_id(dog_id)
        dog.main_picture = next(pic for pic in pictures if pic.is_main)
        dog.pictures = [pic for pic in pictures if not pic.is_main]
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
                event = record[2]
                expenditure = record[3]
                fin_event = FinancialEvent()
                fin_event.post_init(event, expenditure)
                dog.financial_event_list.append(fin_event)
            elif record[2]:
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
                    "LEFT JOIN {event_table} AS events ON dogs.id = events.dog_id "
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
    def new_dog(cls, dog: Dog) -> Dog:
        """Add new dog to database"""

        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(DogMapping, dog,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=DogMapping.description, columns=columns, substitutions=substitutions))

        result = db.engine.execute(query.params(**params_dict))
        id = next(iter(result))[0]
        return cls.get_dog_by_id(id)


class DogPictureRepository:
    """
    Repository for dog's pictures
    """

    @classmethod
    def get_picture_by_id(cls, picture_id) -> DogPicture:
        """
        Returns DogPicture by its id
        :param picture_id: Picture_id
        :return: Returns DogPicture with given id
        """
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")
        stmt = text("SELECT {picture_columns} "
                    "FROM {pictures_table} dog_pictures "
                    "WHERE dog_pictures.id = :picture_id"
                    .format(picture_columns=picture_columns,
                            pictures_table=DogPictureMapping.description
                            ))
        return db.session.query(DogPicture).from_statement(stmt).params(picture_id=picture_id).one()

    @classmethod
    def get_pictures_by_dog_id(cls, dog_id) -> Iterable[DogPicture]:
        """
        Returns all DogPicture's by dog_id
        :param dog_id: Dog id
        :return: Iterable of DogPicture
        """
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")
        stmt = text("SELECT {picture_columns} "
                    "FROM {pictures_table} dog_pictures "
                    "WHERE dog_pictures.dog_id = :dog_id"
                    .format(picture_columns=picture_columns,
                            pictures_table=DogPictureMapping.description
                            ))
        return db.session.query(DogPicture).from_statement(stmt).params(dog_id=dog_id).all()

    @classmethod
    def get_pictures_by_request_id(cls, request_id) -> Iterable[DogPicture]:
        """
        Returns all DogPicture's by request_id
        :param request_id: Request id
        :return: Iterable of DogPicture
        """
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dp")
        stmt = text("SELECT {picture_columns} "
                    "FROM {pictures_table} dp "
                    "WHERE dp.request_id = :request_id"
                    .format(picture_columns=picture_columns,
                            pictures_table=DogPictureMapping.description
                            ))
        return db.session.query(DogPicture).from_statement(stmt).params(request_id=request_id).all()

    @classmethod
    def _check_main_picture_rule(cls, dog_id, connection=None) -> bool:
        """
        Checks, whether there is one and only one main picture for given dog_id, if
        any other picture exists
        :param dog_id: Dog id
        :param connection: Connection to use. It is useful to perform checking, during the transaction
        :return: True, if the rule is forced
        """
        if connection is None:
            connection = db.engine
        stmt = text(
            "SELECT count(*) AS pictures_count FROM {pictures_table} "
            "WHERE {dog_id_column} = :dog_id AND {is_main_column} = True".format(
                pictures_table=DogPictureMapping.description,
                dog_id_column=QueryHelper.get_column_by_key(DogPictureMapping, "dog_id"),
                is_main_column=QueryHelper.get_column_by_key(DogPictureMapping, "is_main")
            ))
        result = connection.execute(stmt.params(dog_id=dog_id))
        main_pictures_count = next(iter(result))['pictures_count']
        not_main_pictures_count = 0
        for row in result:
            if row['is_main']:
                main_pictures_count = row['pictures_count']
            else:
                not_main_pictures_count = row['pictures_count']
        if main_pictures_count > 1 or (not_main_pictures_count > 0 and main_pictures_count == 0):
            return False
        return True

    @classmethod
    def _check_main_picture_rule_for_all(cls, connection=None) -> bool:
        """
        Check, if for every dog with picture there is one and only one main picture
        :param connection: Connection, used for the query
        :return: True, if rule is forced, False - otherwise
        """
        if connection is None:
            connection = db.engine
        stmt = text("SELECT DISTINCT {dog_id_column} FROM {dog_picture_table} WHERE {dog_id_column} NOT IN "
                    "(SELECT {dog_id_column} FROM dog_picture WHERE {dog_id_column} IS NOT NULL "
                    "GROUP BY {dog_id_column} HAVING count({is_main_column} = True or NULL) = 1)".format(
            dog_id_column=QueryHelper.get_column_by_key(DogPictureMapping, "dog_id"),
            dog_picture_table=DogPictureMapping.description,
            is_main_column=QueryHelper.get_column_by_key(DogPictureMapping, "is_main")
        ))
        result = connection.execute(stmt)
        if result.rowcount > 0:
            return False
        else:
            return True

    @classmethod
    def insert_picture(cls, picture) -> bool:
        """
        Adds picture to the database and sets proper id to id.
        Performs check before that.
        :param picture: Picture to insert
        :return: True, if insertion was successful, False - otherwise
        """
        connection = db.engine.connect()
        trans = connection.begin()
        db.session.begin(subtransactions=True)

        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(DogPictureMapping, picture,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=DogPictureMapping.description, columns=columns, substitutions=substitutions))
        result = connection.execute(query.params(**params_dict))
        if picture.dog_id is None or cls._check_main_picture_rule(picture.dog_id, connection):
            trans.commit()
            picture.id = result.fetchone()['id']
            return True
        else:
            trans.rollback()
            return False

    @classmethod
    def transactional_pictures_update(cls, picture1, picture2):
        """
        Updates two pictures, during the one transaction.
        It is required, if we want to change main picture for any dog.
        :param picture1: First picture to update
        :param picture2: Second picture to update
        :return: True, if updates performed successfully, False - otherwise
        """

        connection = db.engine.connect()
        trans = connection.begin()
        cls._update_picture(picture1, connection)
        cls._update_picture(picture2, connection)
        if cls._check_main_picture_rule_for_all(connection):
            trans.commit()
            return True
        else:
            trans.rollback()
            return False

    @classmethod
    def _update_picture(cls, picture, connection):
        """
        Unconditionally updates given picture, using given connection
        :param picture: Picture
        :param connection: Connection
        :return:
        """
        update_data, params_dict = QueryHelper.get_update_string_and_dict(DogPictureMapping, picture,
                                                                          fields_to_exclude=['id'])
        query = text("UPDATE {pictures_table} SET {update_data} WHERE id = :picture_id".format(
            pictures_table=DogPictureMapping.description,
            update_data=update_data
        ))
        params_dict['picture_id'] = picture.id

        connection.execute(query.params(**params_dict))

    @classmethod
    def update_picture(cls, picture) -> bool:
        """
        Update picture in the database. Performs check before that.
        :param picture: Picture to update
        :return: True, if update was successful, False - otherwise
        """
        connection = db.engine.connect()
        trans = connection.begin()

        cls._update_picture(picture, connection)

        if cls._check_main_picture_rule_for_all(connection):
            trans.commit()
            return True
        else:
            trans.rollback()
            return False
