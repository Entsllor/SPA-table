from typing import Iterable

from sqlalchemy import select, update, insert, delete, text
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
    for ordering_field in ordering_fields:
        if ordering_field.startswith("-"):
            query = query.order_by(text(f'{ordering_field[1:]} desc'))
        else:
            query = query.order_by(text(f"{ordering_field} asc"))
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
    await get_session().execute(query)


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
