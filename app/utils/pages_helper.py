import math
from typing import List

__author__ = 'Xomak'


class Pages:
    """
    Pages class is intended to store data, relevant to pagination
    """

    def __init__(self, endpoint, rows_per_page, current_page, total_number, request_args):
        """
        Creates Pages object.
        :param endpoint: Flask endpoint to refer in pagination
        :param rows_per_page: Number of items per page
        :param current_page: Current page
        :param total_number: Total number of paginated objects
        :param request_args: Request args, which will be included in generated requests
        """
        self.start_row = (current_page - 1) * rows_per_page
        self.rows_per_page = rows_per_page
        self.current_page = current_page
        self.endpoint = endpoint
        self.last_page_number = math.ceil(total_number / rows_per_page)
        if self.start_row < 0 or self.start_row > total_number:
            raise ValueError("Current page is out of range")

        request_args = dict(request_args)
        if 'page' in request_args:
            del request_args['page']
        self.request_args = request_args

    def get_start_row(self) -> int:
        return self.start_row

    def get_rows_number(self) -> int:
        return self.rows_per_page

    def get_pages_list(self, difference=3) -> List[int]:
        """
        Returns reduced list of available pages numbers, like:
        1 .. n-3 n-2 n-1 n n+1 n+2 n+3 .. 10
        Where 3 is variable and is called difference
        :param difference: Difference
        :return: List of pages' numbers
        """
        pages_list = [1]
        for current_page in range(self.current_page - difference, self.current_page + difference):
            if 0 < current_page <= self.last_page_number and current_page not in pages_list:
                pages_list.append(current_page)
        if self.last_page_number != 0 and self.last_page_number not in pages_list:
            pages_list.append(self.last_page_number)
        return pages_list

    def has_previous(self) -> bool:
        return self.current_page > 1

    def has_next(self) -> bool:
        return self.current_page != self.last_page_number and self.last_page_number != 0