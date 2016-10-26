from typing import List, Dict, Tuple

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
            columns = [temporary_name + "." + column for column in columns]
        return ', '.join(columns)

    @classmethod
    def get_update_string_and_dict(cls, mapping: Table, data_object, fields_to_update=[], fields_to_exclude=[]) \
            -> Tuple[str, Dict]:
        """
        Returns string, which can be used in update statement and the dict object, which can be
        passed to params methods to bind these values to generated in the string.

        String is like this:

        param1 = :param1, param2 = :param2

        And dict: {"param1": "value1", "param2": "value2"}

        :param mapping: SQLAlchemy mapping
        :param object: object with data, which will be included in statement
        :param fields_to_update: fields, which should be considered (if empty - all will be considered)
        :param fields_to_exclude: fields, which will not be considered
        :return: String and dict
        """
        updates = []
        params_dict = {}
        for column in mapping.get_children():
            if column.key not in fields_to_exclude and (column.key in fields_to_update or len(fields_to_update) == 0):
                updates.append("%s = :%s" % (column.name, column.name))
                params_dict[column.name] = getattr(data_object, column.key)
        return ", ".join(updates), params_dict

    @classmethod
    def get_insert_strings_and_dict(cls, mapping: Table, data_object, fields_to_insert=[], fields_to_exclude=[]) \
            -> Tuple[str, Dict]:
        column_names = []
        params_dict = {}
        for column in mapping.get_children():
            if column.key not in fields_to_exclude and (column.key in fields_to_insert or len(fields_to_insert) == 0):
                column_names.append(column.name)
                params_dict[column.name] = getattr(data_object, column.key)
        substitutions = ", ".join([":" + column for column in column_names])
        columns = ", ".join(column_names)
        return columns, substitutions, params_dict
