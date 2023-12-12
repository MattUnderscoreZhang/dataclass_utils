from dataclasses import dataclass
from uuid import UUID

from convert import dataclass_from_dict


@dataclass
class MyClassOne:
    a: int
    b: UUID


@dataclass
class MyClassTwo:
    c: MyClassOne
    d: float


def test_dataclass_from_dict_simple_dataclass():
    my_class = dataclass_from_dict(
        MyClassOne,
        {
            "a": 1,
            "b": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert type(my_class) == MyClassOne
    assert my_class.a == 1
    assert my_class.b == UUID("00000000-0000-0000-0000-000000000000")


def test_dataclass_from_dict_nested_dataclass():
    my_class = dataclass_from_dict(
        MyClassTwo,
        {
            "c": {
                "a": 1,
                "b": "00000000-0000-0000-0000-000000000000",
            },
            "d": 1.0,
        },
    )
    assert type(my_class) == MyClassTwo
    assert type(my_class.c) == MyClassOne
    assert my_class.d == 1.0
    assert my_class.c.a == 1
    assert my_class.c.b == UUID("00000000-0000-0000-0000-000000000000")
