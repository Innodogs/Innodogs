from sqlalchemy import text

from app import db
from app.utils.helpers import QueryHelper
from .models import UserMapping, User

__author__ = 'Xomak'


class UsersRepository:
    """
    Repository class for Users
    """

    @classmethod
    def get_user_by_google_id(cls, google_id: str) -> User:
        """Returns add_request by given id or none"""

        users_column_list = QueryHelper.get_columns_string(UserMapping, "u")
        stmt = text('SELECT {cols} '
                    'FROM "{users_table}" AS u '
                    'WHERE u.google_id = :google_id'.format(cols=users_column_list,
                                                            users_table=UserMapping.description))
        user = db.session.query(User).from_statement(stmt).params(google_id=google_id).first()
        return user

    @classmethod
    def save_user(cls, user: User) -> User:
        """Saves given user and returns user with id"""

        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(UserMapping, user,
                                                                                      fields_to_exclude=['id'])
        query = text(
            'INSERT INTO "{table_name}" ({columns}) VALUES ({substitutions}) RETURNING *'.format(
                table_name=UserMapping.description,
                columns=columns,
                substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))  # didn't find how to do it correctly with sqlalchemy :(
        return cls.get_user_by_google_id(user.google_id)

    @classmethod
    def get_all_users(cls):
        """Return list of users in base"""
        users_column_list = QueryHelper.get_columns_string(UserMapping, "u")
        stmt = text('SELECT {cols} '
                    'FROM "{users_table}" AS u'
                    .format(cols=users_column_list, users_table=UserMapping.description))
        user = db.session.query(User).from_statement(stmt).params().all()
        return user

    @classmethod
    def get_users_by_criteria(cls, name, is_volunteer, is_admin, is_active):
        """Return list of users according given criteries"""
        users_column_list = QueryHelper.get_columns_string(UserMapping, "u")
        where_clause = ""

        if name:
            where_clause = " u.name='{uname}'".format(uname=name)

        if is_volunteer:
            if where_clause:
                where_clause += " AND "
            where_clause += " u.is_volunteer=true"

        if is_admin:
            if where_clause:
                where_clause += " AND "
            where_clause += " u.is_admin=true"

        if is_active:
            if where_clause:
                where_clause += " AND "
            where_clause += " u._is_active=true"

        if where_clause:
            where_clause = "WHERE " + where_clause

        stmt = text('SELECT {cols} '
                    'FROM "{users_table}" AS u {where_cl}'
                    .format(cols=users_column_list, users_table=UserMapping.description,
                    where_cl=where_clause))

        user = db.session.query(User).from_statement(stmt).params().all()
        return user

