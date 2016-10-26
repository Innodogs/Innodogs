from sqlalchemy import text

from app import db
from app.utils.query_helper import QueryHelper
from .models import UserMapping, User

__author__ = 'Xomak'


class UsersRepository:
    """
    Repository class for Users
    """

    # @classmethod
    # def get_all_add_requests(cls) -> List[AddRequest]:
    #     """Gets all AddRequest, joined with user"""
    #
    #     requests_column_list = QueryHelper.get_columns_string(AddRequestMapping, "requests")
    #     users_column_list = QueryHelper.get_columns_string(UserMapping, "users")
    #     stmt = text("SELECT %s, %s FROM %s AS requests INNER JOIN \"%s\" AS users ON requests.user_id = users.id " %
    #                                (requests_column_list, users_column_list, AddRequestMapping.description,
    #                                 UserMapping.description))
    #     result = db.session.query(AddRequest, User).from_statement(stmt).all()
    #
    #     requests = []
    #     for join_tuple in result:
    #         current_request = join_tuple[0]
    #         current_request.user = join_tuple[1]
    #         requests.append(current_request)
    #     return requests

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
        """Saves given user"""

        insert_clause, params_dict = QueryHelper.get_update_string_and_dict(UserMapping, user, fields_to_exclude=['id'])
        query = text('INSERT INTO {fields} SET {insert_clause}'.format(fields=UserMapping.description,
                                                                       insert_clause=insert_clause))
        execute = db.engine.execute(query.params(**params_dict))
        return user

        # @classmethod
        # def update_add_request(cls, add_request):
        #     """Updates given AddRequest"""
        #
        #     update_clause, params_dict = QueryHelper.get_update_string_and_dict(AddRequestMapping, add_request,
        #                                                                         fields_to_exclude=['id'])
        #     query = text("UPDATE %s SET %s WHERE id = :request_id" % (AddRequestMapping.description, update_clause))
        #     params_dict['request_id'] = add_request.id
        #     db.engine.execute(query.params(**params_dict))
