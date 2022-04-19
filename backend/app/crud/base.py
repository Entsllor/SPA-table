import itertools
from typing import Iterable

from sqlalchemy import select, update, insert, delete, text, Integer
from sqlalchemy.orm import Query

from app.core.database import Base, get_session
from app.utils.exceptions import ExpectedOneInstance, InstanceNotFound
from app.utils.options import GetManyOptions, GetOneOptions


class BaseCrudDB:
    model: Base

    @property
    def _select(self) -> Query:
        return select(self.model)

    @property
    def _update(self) -> Query:
        return update(self.model)

    @property
    def _insert(self) -> Query:
        return insert(self.model)

    @property
    def _delete(self) -> Query:
        return delete(self.model)

    async def get_one(self, _options: GetOneOptions = None, **filters):
        query = self._select.filter_by(**filters)
        return await get_one_by_query(query, options=_options)

    async def get_many(self, _options: GetManyOptions = None, **filters):
        query = self._select.filter_by(**filters)
        return await get_many_by_query(query, options=_options)

    async def delete(self, **filters) -> None:
        query = self._delete.filter_by(**filters)
        return await delete_by_query(query)

    async def update(self, filters: dict, new_values: dict):
        query = self._update.filter_by(**filters).values(new_values)
        return await update_by_query(query)


def order_by_fields(query: Query, ordering_fields: Iterable[str]) -> Query:
    available_field = list(itertools.chain(*[fields.columns.keys() for fields in query.froms]))
    for field_name in ordering_fields:
        order = 'asc'
        if field_name.startswith('-'):
            order = 'desc'
            field_name = field_name.removeprefix('-')
        if field_name in available_field:
            query = query.order_by(text(f"{field_name} {order}"))
    return query


FILTER_OPERATORS = {
    "eq": "__eq__",  # ==
    "ne": "__ne__",  # !=
    "gt": "__gt__",  # <
    "ge": "__ge__",  # <=
    "lt": "__lt__",  # >
    "le": "__le__",  # >=
    "like": "like",  # Model.column.like as SQL like
}


def parse_condition(condition: str) -> tuple[str, str, str | list] | None:
    try:
        value_separator_index = condition.index(":")
        value = condition[value_separator_index + 1:]
        operator_separator_index = condition[:value_separator_index].rindex("__")
        operator = condition[operator_separator_index + 2:value_separator_index]
        field_name = condition[:operator_separator_index]
    except (ValueError, IndexError):
        raise ValueError(f"Condition '{condition}' is invalid")
    if operator not in FILTER_OPERATORS:
        raise ValueError(f"Condition operator '{operator}' if not allowed")
    return field_name, operator, value


def filter_by_condition(query: Query, condition: str, allowed_fields: dict) -> Query:
    try:
        field_name, operator_name, value = parse_condition(condition)
        field = allowed_fields.get(field_name)
        operation = FILTER_OPERATORS.get(operator_name)
        criterion = getattr(field, operation, None)
        if isinstance(field.type, Integer):
            value = int(value)
    except ValueError:
        return query
    if field and criterion:
        return query.where(criterion(value))
    return query


async def get_many_by_query(query: Query, options: GetManyOptions | dict = None) -> list:
    if isinstance(options, dict):
        options = GetManyOptions(**options)
    elif options is None:
        options = GetManyOptions()
    if options.limit is not None:
        query = query.limit(options.limit)
    if options.offset is not None:
        query = query.offset(options.offset)
    if options.ordering_fields:
        query = order_by_fields(query, options.ordering_fields)
    result = await get_session().execute(query)
    return result.scalars().all()


async def get_one_by_query(query: Query, options: GetOneOptions | dict = None) -> Base:
    if isinstance(options, dict):
        options = GetOneOptions(**options)
    elif options is None:
        options = GetOneOptions()
    limit = 2 if options.raise_if_many else 1
    instances = await get_many_by_query(query=query, options=GetManyOptions(limit=limit))
    if options.raise_if_many and len(instances) > 2:
        raise ExpectedOneInstance
    if not instances:
        if options.raise_if_none:
            raise InstanceNotFound
        return None
    return instances[0]


async def delete_by_query(q: Query):
    return await get_session().execute(q)


async def update_by_query(query: Query):
    query.execution_options(synchronize_session="fetch")
    return await get_session().execute(query)


async def update_instance(instance, **values):
    for key, value in values.items():
        setattr(instance, key, value)
    await get_session().flush(objects=[instance])
    await get_session().refresh(instance)
    return instance


async def create_instance(instance):
    get_session().add(instance)
    await get_session().flush()
    await get_session().refresh(instance)
    return instance
