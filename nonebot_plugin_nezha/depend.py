from typing import Optional

from nonebot.internal.matcher import current_matcher
from nonebot.internal.params import Depends
from nonebot.typing import T_State
from nonebot_plugin_alconna import ALCONNA_RESULT


def _raw_command(state: Optional[T_State] = None) -> str:
    return (state if state else current_matcher.get().state)[ALCONNA_RESULT].result.header_match.result


def RawCommand() -> str:
    return Depends(_raw_command)
