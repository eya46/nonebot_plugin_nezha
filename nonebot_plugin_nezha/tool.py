from functools import wraps
from typing import Any, Union, Callable, Optional, List, Tuple, TypeVar, Type

from arclet.alconna import Alconna
from nonebot.permission import SUPERUSER
from nonebot.typing import T_Handler
from nonebot_plugin_alconna import UniMessage, on_alconna
from nonebot_plugin_alconna.uniseg import Receipt

from .config import config, CMD_TYPE, _CM
from .depend import _raw_command

T = TypeVar("T")


def parse_obj(type_: Type[T], data: Any) -> T:
    from pydantic import VERSION
    _ = VERSION.split(".")[0]
    if _ == "2":
        from pydantic import TypeAdapter
        return TypeAdapter(type_).validate_python(data)
    else:
        from pydantic import parse_obj_as
        return parse_obj_as(type_, data)


async def send(msg: Union[Any, UniMessage]) -> Optional[Receipt]:
    if not isinstance(msg, UniMessage):
        msg = UniMessage(msg)
    if str(msg) == "":
        return None
    return await msg.send(at_sender=config.at, reply_to=config.replay)


def get_cmd(cmd: CMD_TYPE) -> Optional[Tuple[bool, List[str]]]:
    if isinstance(cmd, list):
        return False, cmd
    else:
        return cmd


HELPS: List[str] = []


def wrap_cmd(cmd: CMD_TYPE, *acl_arg: Any) -> Callable:
    help_cmd = get_cmd(cmd)

    def wrapper(func: T_Handler) -> T_Handler:
        if help_cmd is None:
            return func

        @wraps(func)
        async def _catch(*args, **kwargs):
            try:
                await func(*args, **kwargs)
            except AssertionError as e:
                await send(
                    f"命令 {_raw_command()} 失败 ->\n{e}"
                )

        _ = Alconna(help_cmd[1], *acl_arg, meta=_CM)
        HELPS.append(_.get_help().strip())
        on_alconna(
            _, permission=SUPERUSER if (config.must_super_user or help_cmd[0]) else None,
            use_cmd_start=config.use_start, block=True, priority=100 - max(len(i) for i in help_cmd[1])
        ).handle()(_catch)
        return func

    return wrapper


__all__ = ["get_cmd", "send", "wrap_cmd", "HELPS", "parse_obj"]
