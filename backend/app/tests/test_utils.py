import pytest

from app.crud.base import parse_condition, add_filter
from app.models.users import User
import sqlalchemy
from sqlalchemy.orm import Query


def test_parse_valid_condition():
    assert parse_condition("name__like:nn") == ('name', 'like', 'nn')
    assert parse_condition('weight__gt:20') == ('weight', 'gt', '20')
    assert parse_condition("user__profile__likes__count__ge:5") == ('user__profile__likes__count', 'ge', '5')
    assert parse_condition("title__eq:test:with:colon") == ('title', 'eq', 'test:with:colon')


def test_failed_parse_condition_invalid_operator():
    with pytest.raises(ValueError):
        assert parse_condition("name__such:nn")
    with pytest.raises(ValueError):
        assert parse_condition("name__xor:nn")


def test_failed_parse_condition_invalid_syntax():
    with pytest.raises(ValueError):
        assert parse_condition("name__eq=nn")
    with pytest.raises(ValueError):
        assert parse_condition("name_eq:nn")
    with pytest.raises(ValueError):
        assert parse_condition("name_eq:nn")


def test_query_str_is_a_sql_code():
    query_str = str(sqlalchemy.select(User).where(User.username == "Knight")).lower()
    assert 'select' in query_str
    assert 'from' in query_str
    assert 'where' in query_str
    assert 'username' in query_str


def is_queries_equal(query_1: Query, query_2: Query) -> bool:
    return str(query_1) == str(query_2) and query_1.compile().params == query_2.compile().params


def test_comparing_queries():
    base_query: Query = sqlalchemy.select(User)
    assert is_queries_equal(base_query.where(User.id == 1), add_filter(base_query, "id__eq:1", {"id": User.id}))
    assert not is_queries_equal(base_query.where(User.id > 1), add_filter(base_query, "id__eq:1", {"id": User.id}))
    assert not is_queries_equal(base_query.where(User.id == 2), add_filter(base_query, "id__eq:1", {"id": User.id}))
    assert not is_queries_equal(base_query.where(User.email == 2), add_filter(base_query, "id__eq:1", {"id": User.id}))
    assert not is_queries_equal(base_query, add_filter(base_query, "id__eq:1", {"id": User.id}))


def test_filter_by_condition_with_int_value():
    base_query: Query = sqlalchemy.select(User)
    assert is_queries_equal(base_query.where(User.id == 1), add_filter(base_query, "id__eq:1", {"id": User.id}))
    assert is_queries_equal(base_query.where(User.id != 1), add_filter(base_query, "id__ne:1", {"id": User.id}))
    assert is_queries_equal(base_query.where(User.id > 1), add_filter(base_query, "id__gt:1", {"id": User.id}))
    assert is_queries_equal(base_query.where(User.id >= 1), add_filter(base_query, "id__ge:1", {"id": User.id}))
    assert is_queries_equal(base_query.where(User.id < 1), add_filter(base_query, "id__lt:1", {"id": User.id}))
    assert is_queries_equal(base_query.where(User.id <= 1), add_filter(base_query, "id__le:1", {"id": User.id}))


def test_filter_by_condition_with_str_value():
    query: Query = sqlalchemy.select(User)
    name_field = User.username
    fields = {"username": name_field}
    assert is_queries_equal(query.where(name_field == "me"), add_filter(query, "username__eq:me", fields))
    assert is_queries_equal(query.where(name_field != "me"), add_filter(query, "username__ne:me", fields))
    assert is_queries_equal(query.where(name_field > "me"), add_filter(query, "username__gt:me", fields))
    assert is_queries_equal(query.where(name_field >= "me"), add_filter(query, "username__ge:me", fields))
    assert is_queries_equal(query.where(name_field < "me"), add_filter(query, "username__lt:me", fields))
    assert is_queries_equal(query.where(name_field <= "me"), add_filter(query, "username__le:me", fields))
    assert is_queries_equal(query.where(name_field.like("you")), add_filter(query, "username__like:you", fields))
    assert is_queries_equal(query.where(name_field.like("%you")), add_filter(query, "username__like:%you", fields))
    assert is_queries_equal(query.where(name_field.like("%you%")), add_filter(query, "username__like:%you%", fields))
    assert is_queries_equal(query.where(name_field.like("%y_u%")), add_filter(query, "username__like:%y_u%", fields))
    assert is_queries_equal(query.where(name_field.like("%y%u%")), add_filter(query, "username__like:%y%u%", fields))


def test_failed_filter_not_allowed_field():
    base_query: Query = sqlalchemy.select(User)
    print(base_query.where(User.id == 1))
    assert str(base_query) == str(add_filter(base_query, "id__eq:1", {"username": User.username}))
    assert str(base_query) == str(add_filter(base_query, "username__eq:me", {"id": User.id}))
