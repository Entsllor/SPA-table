from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(slots=True, kw_only=True)
class BaseOptions:
    def as_dict(self, ignore_none: bool | list[str] | tuple[str] = False) -> dict:
        result = asdict(self)
        if not ignore_none:
            return result
        elif isinstance(ignore_none, Iterable):
            skipped_nullable_fields = ignore_none
            result = {
                key: value for key, value in result.items()
                if not (value is None and key in skipped_nullable_fields)
            }
        elif ignore_none:
            result = {key: value for key, value in result.items() if value is not None}
        return result


@dataclass(slots=True, kw_only=True)
class GetOneOptions(BaseOptions):
    raise_if_many: bool = None
    raise_if_none: bool = None


@dataclass(slots=True, kw_only=True)
class PaginationOptions(BaseOptions):
    limit: int = None
    offset: int = None


@dataclass(slots=True, kw_only=True)
class GetManyOptions(PaginationOptions):
    ordering_fields: Iterable[str] = tuple()
