from typing import List, Optional, Union, Tuple, Type, Any

from nonebot.typing import T
from pydantic import VERSION

CMD_TYPE = Optional[Union[List[str], Tuple[bool, List[str]]]]

PYD_MAIN_VERSION = VERSION.split(".")[0]

if PYD_MAIN_VERSION == "1":
    from pydantic import root_validator as _validator

    validator = _validator(pre=True)
else:
    from pydantic import model_validator as _validator

    validator = _validator(mode="before")


def parse_obj(type_: Type[T], data: Any) -> T:
    if PYD_MAIN_VERSION == "1":
        from pydantic import parse_obj_as
        return parse_obj_as(type_, data)
    else:
        from pydantic import TypeAdapter
        return TypeAdapter(type_).validate_python(data)
