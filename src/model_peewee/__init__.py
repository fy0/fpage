# coding:utf-8

import math
import config
import peewee
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict

db = connect(config.DATABASE_URI)


class BaseModel(peewee.Model):
    class Meta:
        database = db

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_by_pk(cls, value):
        try:
            return cls.get(cls._meta.primary_key == value)
        except cls.DoesNotExist:
            return

    @classmethod
    def exists_by_pk(cls, value):
        return cls.select().where(cls._meta.primary_key == value).exists()


def pagination_calc(count_all, page_size, cur_page=1, nearby=2):
    """
    :param nearby:
    :param count_all: count of all items
    :param page_size: size of one page
    :param cur_page: current page number, accept string digit
    :return: num of pages, an iterator
    """
    if type(cur_page) == str:
        # noinspection PyUnresolvedReferences
        cur_page = int(cur_page) if cur_page.isdigit() else 1
    elif type(cur_page) == int:
        if cur_page <= 0:
            cur_page = 1
    else:
        cur_page = 1

    page_count = int(math.ceil(count_all / page_size))
    items_length = nearby * 2 + 1

    # if first page in page items, first_page is None,
    # it means the "go to first page" button should not be available.
    first_page = None
    last_page = None

    prev_page = cur_page - 1 if cur_page != 1 else None
    next_page = cur_page + 1 if cur_page != page_count else None

    if page_count <= items_length:
        items = range(1, page_count + 1)
    elif cur_page <= nearby:
        # start of items
        items = range(1, items_length + 1)
        last_page = True
    elif cur_page >= page_count - nearby:
        # end of items
        items = range(page_count - items_length + 1, page_count + 1)
        first_page = True
    else:
        items = range(cur_page - nearby, cur_page + nearby + 1)
        first_page, last_page = True, True

    if first_page:
        first_page = 1
    if last_page:
        last_page = page_count

    return {
        'cur_page': cur_page,
        'prev_page': prev_page,
        'next_page': next_page,

        'first_page': first_page,
        'last_page': last_page,

        'page_numbers': list(items),
        'page_count': page_count,

        'info': {
            'page_size': page_size,
            'count_all': count_all,
        }
    }


def pagination_peewee(count_all, query, page_size, cur_page=1, nearby=2):
    pg = pagination_calc(count_all, page_size, cur_page, nearby)
    pg['items'] = query.paginate(pg['cur_page'], page_size)
    return pg
