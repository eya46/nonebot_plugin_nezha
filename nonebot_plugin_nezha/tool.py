from functools import wraps
from typing import Any, Callable, Optional, Union

from arclet.alconna import Alconna
from nonebot.compat import PYDANTIC_V2
from nonebot.permission import SUPERUSER
from nonebot.typing import T_Handler
from nonebot_plugin_alconna import UniMessage, on_alconna
from nonebot_plugin_alconna.uniseg import Receipt

from .config import _CM, CMD_TYPE, config
from .depend import _raw_command

if PYDANTIC_V2:
    from pydantic import model_validator as _validator

    validator = _validator(mode="before")
else:
    from pydantic import root_validator as _validator

    validator = _validator(pre=True)


async def send(msg: Union[Any, UniMessage]) -> Optional[Receipt]:
    if not isinstance(msg, UniMessage):
        msg = UniMessage(msg)
    if str(msg) == "":
        return None
    return await msg.send(at_sender=config.at, reply_to=config.replay)


def get_cmd(cmd: CMD_TYPE) -> Optional[tuple[bool, list[str]]]:
    if isinstance(cmd, list):
        return False, cmd
    else:
        return cmd


HELPS: list[str] = []


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
                await send(f"命令 {_raw_command()} 失败 ->\n{e}")

        _ = Alconna(help_cmd[1], *acl_arg, meta=_CM)
        HELPS.append(_.get_help().strip())
        on_alconna(
            _,
            permission=SUPERUSER if (config.must_super_user or help_cmd[0]) else None,
            use_cmd_start=config.use_start,
            block=True,
            priority=100 - max(len(i) for i in help_cmd[1]),
        ).handle()(_catch)
        return func

    return wrapper


__all__ = ["get_cmd", "send", "wrap_cmd", "HELPS"]
