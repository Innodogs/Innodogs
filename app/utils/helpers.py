import os
import uuid
from collections import namedtuple
from typing import List, Dict, Tuple

from flask import current_app
from sqlalchemy import Table
from werkzeug.utils import secure_filename

__author__ = 'Xomak'


class QueryHelper:
    @classmethod
    def get_columns_list(cls, mapping: Table, excluded_keys=None) -> List[str]:
        """
        Returns list of columns's names from given SQLAlchemy Table object
        :param excluded_keys: Keys, which will be excluded from the list
        :param mapping: SQLAlchemy table
        :return: List of names
        """
        result = []
        for column in mapping.get_children():
            if excluded_keys is None or column.key not in excluded_keys:
                result.append(column.name)

        return result

    @classmethod
    def get_column_by_key(cls, mapping: Table, key: str) -> str:
        """
        Returns column name by given key for mapping
        :param mapping: Mapping
        :param key: Key
        :return: Column's name or None
        """
        for column in mapping.get_children():
            if column.key == key:
                return column.name
        return None

    @classmethod
    def get_columns_string(cls, mapping: Table, temporary_name=None,excluded_keys=None) -> str:
        """
        Returns string of columns, which can be used in SQL statement, like:

        'requests.id AS request_id, request.name AS request_name'

        where 'requests' is temporary_name parameter
        and request is actual name of the table
        this is done to satisfy requirements of SQLAlchemy's mapper (case of outer join)

        :param excluded_keys: Keys, which will be excluded from the list
        :param mapping: SQLAlchemy table
        :param temporary_name: Temporary name for table in the statement
        :return: String
        """

        def get_column_description(column):
            return temporary_name + "." + column + " AS " + mapping.description + "_" + column

        columns = cls.get_columns_list(mapping, excluded_keys=excluded_keys)

        if temporary_name:
            columns = [get_column_description(column) for column in columns]
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
        :param data_object: object with data, which will be included in statement
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
    def get_limit_query_part(cls, from_row=None, number_of_rows=None) -> Tuple[str, Dict]:
        """
        Returns limit query part like
        LIMIT 0, 30
        :param from_row: From row
        :param number_of_rows: Number of rows
        :return: Query string and params' dict
        """
        query_params = {}
        limit_query_string = ""
        if number_of_rows is not None:
            limit_query_string = "LIMIT :limit_number_of_rows"
            query_params['limit_number_of_rows'] = number_of_rows

        if number_of_rows is not None:
            if len(limit_query_string) > 0:
                limit_query_string += " "
            limit_query_string += "OFFSET :limit_from_row"
            query_params['limit_from_row'] = from_row
        return limit_query_string, query_params

    @classmethod
    def get_insert_strings_and_dict(cls, mapping: Table, data_object, fields_to_insert=[], fields_to_exclude=[]) \
            -> Tuple[str, str, Dict]:
        """
        Typical insert statement: `INSERT INTO "{table_name}" ({columns}) VALUES ({substitutions})`

        This method returns columns:

        `param1, param2, param3, ...`

        Returns substitutions:

        `:param1, :param2, :param3`

        And dict: `{"param1": "value1", "param2": "value2"}`


        :param mapping: SQLAlchemy mapping
        :param data_object: object with data, which will be included in statement
        :param fields_to_insert: fields, which should be considered (if empty - all will be considered)
        :param fields_to_exclude: fields, which will not be considered
        :return: String and dict
        """
        column_names = []
        params_dict = {}
        for column in mapping.get_children():
            if column.key not in fields_to_exclude and (column.key in fields_to_insert or len(fields_to_insert) == 0):
                column_names.append(column.name)
                params_dict[column.name] = getattr(data_object, column.key)
        substitutions = ", ".join([":" + column for column in column_names])
        columns = ", ".join(column_names)
        return columns, substitutions, params_dict

SavedFile = namedtuple('SavedFile', ['abspath', 'relpath'])


def save_pictures(request, list_name='pictures') -> List[SavedFile]:
    images = filter(lambda img: bool(img.filename), request.files.getlist(list_name))
    saved = []
    if images:
        for img in images:
            # Create Images
            file_name = str(uuid.uuid4()) + secure_filename(img.filename)
            abspath_image_file = current_app.config['UPLOAD_FOLDER_ABSOLUTE'] + "/" + file_name
            relpath_image_file = current_app.config['UPLOAD_FOLDER'] + "/" + file_name
            img.save(abspath_image_file)
            saved.append(SavedFile(abspath_image_file, relpath_image_file))
    return saved
