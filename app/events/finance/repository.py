from sqlalchemy import text

from app import db
from app.utils.helpers import QueryHelper
from .models import Inpayment, InpaymentMapping


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

    @classmethod
    def update_inpayment(cls, inpayment: Inpayment):
        """Updates existing inpayment"""

        update_clause, params_dict = QueryHelper.get_update_string_and_dict(InpaymentMapping, inpayment)
        query = text("UPDATE {table_name} SET {clause} WHERE id = :id"
                     .format(table_name=InpaymentMapping.description,
                             clause=update_clause))
        db.engine.execute(query.params(**params_dict))
