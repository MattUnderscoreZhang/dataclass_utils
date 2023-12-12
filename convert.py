from dataclasses import asdict, fields
import json
from typing import TypeVar, ClassVar, Protocol, Union, Callable, Any, cast
from uuid import UUID


class Dataclass(Protocol):
    __dataclass_fields__: ClassVar[dict]


T = TypeVar("T", bound=Dataclass)


def dataclass_from_dict(my_class: type[T], my_obj: Any) -> T:
    try:
        fieldtypes = {field.name: field.type for field in fields(my_class)}
        return my_class(
            **{
                key: dataclass_from_dict(fieldtypes[key], value)
                for key, value in my_obj.items()
            }
        )
    except:
        my_cast_class = cast(
            Union[Any, Any], my_class
        )  # only here to make mypy not freak out
        if hasattr(my_cast_class, "__origin__"):
            if my_cast_class.__origin__ == list:
                return my_cast_class(
                    [
                        dataclass_from_dict(my_cast_class.__args__[0], item)
                        for item in my_obj
                    ]
                )
            elif my_cast_class.__origin__ == dict:
                return my_cast_class(
                    {
                        key: dataclass_from_dict(my_cast_class.__args__[1], value)
                        for key, value in my_obj.items()
                    }
                )
        elif my_class == UUID:
            return cast(Callable, my_class)(my_obj)  # another mypy hack
        return my_obj


def uuid_serialize(obj: Any) -> str:
    if isinstance(obj, UUID):
        return str(obj)
    return obj


def dataclass_to_str(my_dataclass: Dataclass) -> str:
    return json.dumps(asdict(my_dataclass), default=uuid_serialize)
