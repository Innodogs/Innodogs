from typing import List

from sqlalchemy import text

from app import db
from app.events.models import Expenditure, ExpenditureEventMapping
from app.users.models import UserMapping, User
from app.utils.helpers import QueryHelper
from .models import Inpayment, InpaymentMapping, InpaymentAndExpenditure, InpaymentAndExpenditureMapping


class InpaymentRepository:
    """Repository for inpayments"""

    @classmethod
    def add_new_inpayment(cls, inpayment: Inpayment):
        """Add new type of events"""
        columns, substitutions, params_dict = QueryHelper.get_insert_strings_and_dict(InpaymentMapping, inpayment,
                                                                                      fields_to_exclude=['id'])
        query = text('INSERT INTO {table_name} ({columns}) VALUES ({substitutions}) RETURNING *'.format(
            table_name=InpaymentMapping.description,
            columns=columns,
            substitutions=substitutions))
        db.engine.execute(query.params(**params_dict))

    @classmethod
    def get_inpayment_by_id(cls, id: int):
        """Get inpayment by id"""
        columns = QueryHelper.get_columns_string(InpaymentMapping, "i")
        columns = columns.replace("i.amount", "i.amount::numeric")  # add cast
        stmt = text("SELECT {columns} FROM {table_name} i WHERE i.id = :id"
                    .format(columns=columns,
                            table_name=InpaymentMapping.description))
        result = db.session.query(Inpayment).from_statement(stmt).params(id=id).one()
        return result

    # add 17.11.2016
    @classmethod
    def get_all_inpayments(cls) -> List[Inpayment]:
        inpayment_columns = QueryHelper.get_columns_string(InpaymentAndExpenditureMapping, "inpayments",
                                                           excluded_keys=['type'])
        user_columns = QueryHelper.get_columns_string(UserMapping, "users")

        expenditure_columns = QueryHelper.get_columns_string(ExpenditureEventMapping, "expenditures")

        stmt = text(
            "SELECT * FROM((SELECT {inpayment_columns}, 'inpayment' AS finance_event_type, users.name AS user_name,users.id FROM {inpayment_table} AS inpayments "
            "LEFT OUTER JOIN \"{user_table}\" AS users ON inpayments.user_id = users.id) "
            "UNION ALL "
            "(SELECT {expenditure_columns},NULL,'expenditure',NULL,NULL FROM {expenditure_table} AS expenditures )) AS result"
            " ORDER BY result.finance_event_datetime DESC"
            .format(inpayment_columns=inpayment_columns,
                    user_columns=user_columns,
                    inpayment_table=InpaymentMapping.description,
                    user_table=UserMapping.description,
                    expenditure_columns=expenditure_columns,
                    expenditure_table=ExpenditureEventMapping.description
                    ))
        result = db.session.query(InpaymentAndExpenditure, User).from_statement(stmt).params().all()
        return result


    # add 17.11.2016
    @classmethod
    def get_all_inpayments_by_date(cls,date) -> List[Inpayment]:
        inpayment_columns = QueryHelper.get_columns_string(InpaymentAndExpenditureMapping, "inpayments",
                                                           excluded_keys=['type'])
        user_columns = QueryHelper.get_columns_string(UserMapping, "users")

        expenditure_columns = QueryHelper.get_columns_string(ExpenditureEventMapping, "expenditures")

        stmt = text(
            "SELECT * FROM((SELECT {inpayment_columns}, 'inpayment' AS finance_event_type, users.name AS user_name,users.id FROM {inpayment_table} AS inpayments "
            "LEFT OUTER JOIN \"{user_table}\" AS users ON inpayments.user_id = users.id) "
            "UNION ALL "
            "(SELECT {expenditure_columns},NULL,'expenditure',NULL,NULL FROM {expenditure_table} AS expenditures )) AS result"
            " where result.finance_event_datetime >= '{date} 00:00:00' "
            " AND result.finance_event_datetime <= '{date} 23:59:59' "
            " ORDER BY result.finance_event_datetime DESC"
            .format(inpayment_columns=inpayment_columns,
                    user_columns=user_columns,
                    inpayment_table=InpaymentMapping.description,
                    user_table=UserMapping.description,
                    date=date,
                    expenditure_columns=expenditure_columns,
                    expenditure_table=ExpenditureEventMapping.description
                    ))
        result = db.session.query(InpaymentAndExpenditure, User).from_statement(stmt).params().all()
        return result


    # add 17.11.2016
    @classmethod
    def get_all_expenditures(cls) -> List[Expenditure]:
        expenditure_columns = QueryHelper.get_columns_string(ExpenditureEventMapping, "exp")

        stmt = text("SELECT {expenditure_columns} FROM {expenditure_table} AS exp "
                    .format(expenditure_columns=expenditure_columns,
                            expenditure_table=ExpenditureEventMapping.description
                            ))
        result = db.session.query(Expenditure).from_statement(stmt).params().all()
        return result

    # add 17.11.2016
    @classmethod
    def get_all_inpayments_by_user_id(cls, user_id: int) -> List[Inpayment]:
        columns = QueryHelper.get_columns_string(InpaymentMapping, "i")
        columns = columns.replace("i.amount", "i.amount::numeric")  # add cast
        stmt = text("SELECT {columns} FROM {table_name} i WHERE i.user_id = :user_id"
                    .format(columns=columns,
                            table_name=InpaymentMapping.description))
        result = db.session.query(Inpayment).from_statement(stmt).params(user_id=user_id).all()
        return result

    @classmethod
    def update_inpayment(cls, inpayment: Inpayment):
        """Updates existing inpayment"""

        update_clause, params_dict = QueryHelper.get_update_string_and_dict(InpaymentMapping, inpayment)
        query = text("UPDATE {table_name} SET {clause} WHERE id = :id"
                     .format(table_name=InpaymentMapping.description,
                             clause=update_clause))
        db.engine.execute(query.params(**params_dict))
