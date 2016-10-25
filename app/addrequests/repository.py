from typing import List

from sqlalchemy import text

from app import db
from app.addrequests.models import AddRequest, AddRequestMapping
from app.users.models import UserMapping, User
from app.utils.query_helper import QueryHelper

__author__ = 'Xomak'


class AddRequestsRepository:
    """
    Repository class for AddRequest
    """

    @classmethod
    def get_all_add_requests(cls) -> List[AddRequest]:
        """Gets all AddRequest, joined with user"""

        requests_column_list = QueryHelper.get_columns_string(AddRequestMapping, "requests")
        users_column_list = QueryHelper.get_columns_string(UserMapping, "users")
        stmt = text("SELECT %s, %s FROM %s AS requests INNER JOIN \"%s\" AS users ON requests.user_id = users.id " %
                                   (requests_column_list, users_column_list, AddRequestMapping.description,
                                    UserMapping.description))
        result = db.session.query(AddRequest, User).from_statement(stmt).all()

        requests = []
        for join_tuple in result:
            current_request = join_tuple[0]
            current_request.user = join_tuple[1]
            requests.append(current_request)
        return requests

    @classmethod
    def get_add_request_by_id(cls, add_request_id) -> AddRequest:
        """Returns add_request by given id or thorws an exception"""

        requests_column_list = QueryHelper.get_columns_string(AddRequestMapping, "requests")
        users_column_list = QueryHelper.get_columns_string(UserMapping, "users")
        stmt = text("SELECT %s, %s FROM %s AS requests INNER JOIN \"%s\" AS users ON requests.user_id = users.id "
                    "WHERE requests.id = :id" %
                    (requests_column_list, users_column_list, AddRequestMapping.description,
                     UserMapping.description))
        add_request_id = int(add_request_id)
        result = db.session.query(AddRequest, User).from_statement(stmt).params(id=add_request_id).one()
        request = result[0]
        request.user = result[1]
        return request

    @classmethod
    def update_add_request(cls, add_request):
        """Updates given AddRequest"""

        update_clause = QueryHelper.get_update_string(AddRequestMapping, add_request, fields_to_exclude=['id'])
        query = "UPDATE %s SET %s WHERE id = %s" % (AddRequestMapping.description, update_clause, add_request.id)
        db.engine.execute(query)
