from typing import List, Tuple, Iterable

from sqlalchemy import text

from app import db
from app.events.models import EventMapping, Event, ExpenditureEventMapping, Expenditure, FinancialEvent
from app.dogs.models import Dog, DogMapping, DogPictureMapping, DogPicture
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
    def _tuple_to_dog_and_location_and_picture(cls, join_tuple):
        """
        Converts tuple (Dog, Location, DogPicture) to Dog with dog.location = location and
        dog.main_picture = picture
        :param join_tuple: Input tuple
        :return: Dog with location and picture
        """
        dog = join_tuple[0]
        dog.location = join_tuple[1]
        dog.main_picture = join_tuple[2]

        return dog

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

        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(DogMapping, dog,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=DogMapping.description, columns=columns, substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))


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
        stmt = text("SELECT {picture_columns} FROM {pictures_table} WHERE id = :picture_id".format(
            picture_columns=picture_columns,
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
        stmt = text("SELECT {picture_columns} FROM {pictures_table} WHERE dog_id = :dog_id".format(
            picture_columns=picture_columns,
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
        picture_columns = QueryHelper.get_columns_string(DogPictureMapping, "dog_pictures")
        stmt = text("SELECT {picture_columns} FROM {pictures_table} WHERE request_id=:request_id".format(
            picture_columns=picture_columns,
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

        if not_main_pictures_count > 0 and main_pictures_count != 1:
            return False
        return True

    @classmethod
    def insert_picture(cls, picture) -> bool:
        """
        Adds picture to the database. Performs check before that.
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
        connection.execute(query.params(**params_dict))
        if picture.dog_id is None or cls._check_main_picture_rule(picture.dog_id, connection):
            trans.commit()
            return True
        else:
            trans.rollback()
            return False

    @classmethod
    def safe_picture_update(cls, picture, new_main_picture_id):
        raise NotImplementedError()
        # connection = db.engine.connect()
        # trans = connection.begin()
        #TODO Implement

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
        old_dog_id = None
        if picture.dog_id is None:
            old_dog_id = cls.get_picture_by_id(picture.id).dog_id

        cls._update_picture(picture, connection)

        if picture.dog_id is not None and picture.dog_id != old_dog_id:
            if not cls._check_main_picture_rule(picture.dog_id, connection):
                trans.rollback()
                return False
        if old_dog_id is not None and picture.dog_id != old_dog_id:
            if not cls._check_main_picture_rule(old_dog_id, connection):
                trans.rollback()
                return False

        trans.commit()
        return True

