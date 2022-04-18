import pytest

from app.crud.base import parse_condition, filter_by_condition
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


def test_filter_by_condition_with_int_value():
    base_query: Query = sqlalchemy.select(User)
    assert str(base_query.where(User.id == 1)) == str(filter_by_condition(base_query, "id__eq:1", {"id": User.id}))
    assert str(base_query.where(User.id != 1)) == str(filter_by_condition(base_query, "id__ne:1", {"id": User.id}))
    assert str(base_query.where(User.id > 1)) == str(filter_by_condition(base_query, "id__gt:1", {"id": User.id}))
    assert str(base_query.where(User.id >= 1)) == str(filter_by_condition(base_query, "id__ge:1", {"id": User.id}))
    assert str(base_query.where(User.id < 1)) == str(filter_by_condition(base_query, "id__lt:1", {"id": User.id}))
    assert str(base_query.where(User.id <= 1)) == str(filter_by_condition(base_query, "id__le:1", {"id": User.id}))
    # testing tests
    assert str(base_query.where(User.id > 1)) != str(filter_by_condition(base_query, "id__eq:1", {"id": User.id}))
    assert str(base_query) != str(filter_by_condition(base_query, "id__eq:1", {"id": User.id}))


def test_filter_by_condition_with_str_value():
    base_query: Query = sqlalchemy.select(User)
    assert str(base_query.where(User.username == "me")) == str(
        filter_by_condition(base_query, "username__eq:me", {"username": User.username}))
    assert str(base_query.where(User.username != "me")) == str(
        filter_by_condition(base_query, "username__ne:me", {"username": User.username}))
    assert str(base_query.where(User.username > "me")) == str(
        filter_by_condition(base_query, "username__gt:me", {"username": User.username}))
    assert str(base_query.where(User.username >= "me")) == str(
        filter_by_condition(base_query, "username__ge:me", {"username": User.username}))
    assert str(base_query.where(User.username < "me")) == str(
        filter_by_condition(base_query, "username__lt:me", {"username": User.username}))
    assert str(base_query.where(User.username <= "me")) == str(
        filter_by_condition(base_query, "username__le:me", {"username": User.username}))
    assert str(base_query.where(User.username.like("you"))) == str(
        filter_by_condition(base_query, "username__like:you", {"username": User.username}))


def test_failed_filter_not_allowed_field():
    base_query: Query = sqlalchemy.select(User)
    print(base_query.where(User.id == 1))
    assert str(base_query) == str(filter_by_condition(base_query, "id__eq:1", {"username": User.username}))
    assert str(base_query) == str(filter_by_condition(base_query, "username__eq:me", {"id": User.id}))
