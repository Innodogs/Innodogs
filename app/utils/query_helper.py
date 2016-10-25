from typing import List

from sqlalchemy import Table

__author__ = 'Xomak'


class QueryHelper:

    @classmethod
    def get_columns_list(cls, mapping: Table) -> List[str]:
        """
        Returns list of columns's names from given SQLAlchemy Table object
        :param mapping: SQLAlchemy table
        :return: List of names
        """
        return [column.name for column in mapping.get_children()]

    @classmethod
    def get_columns_string(cls, mapping: Table, temporary_name=None) -> str:
        """
        Returns string of columns, which can be used in SQL statement, like:

        'requests.id, requests.name'

        where 'requests' is temporary_name parameter

        :param mapping: SQLAlchemy table
        :param temporary_name: Temporary name for table in the statement
        :return: String
        """

        columns = cls.get_columns_list(mapping)
        if temporary_name:
            columns = [temporary_name+"."+column for column in columns]
        return ', '.join(columns)

    @classmethod
    def get_update_string(cls, mapping: Table, object, fields_to_update=[], fields_to_exclude=[]) -> str:
        """
        Returns string, which can be used in update statement, like:

        param1 = 'value1', param2 = 'value2'

        :param mapping: SQLAlchemy mapping
        :param object: object with data, which will be included in statement
        :param fields_to_update: fields, which should be considered (if empty - all will be considered)
        :param fields_to_exclude: fields, which will not be considered
        :return: String
        """

        updates = []
        for column in mapping.get_children():
            if column.key not in fields_to_exclude and (column.key in fields_to_update or len(fields_to_update) == 0):
                updates.append("%s = '%s'" % (column.name, getattr(object, column.key)))
        return ", ".join(updates)
