from typing import List, Optional, Union, Tuple

from arclet.alconna import CommandMeta
from nonebot import get_driver
from pydantic import BaseModel, Field, Extra, AnyHttpUrl

CMD_TYPE = Optional[Union[List[str], Tuple[bool, List[str]]]]


class Config(BaseModel, extra=Extra.ignore):
    nezha_api: AnyHttpUrl
    nezha_token: str

    nezha_use_start: bool = Field(default=True)
    # 是否使用紧凑模式(命令后是否可以紧跟参数)
    nezha_use_compact: bool = Field(default=True)

    nezha_at: bool = Field(default=False)
    nezha_replay: bool = Field(default=False)
    nezha_must_super_user: bool = Field(default=True)

    """
    None:不启用该插件
    List[str]:命令名
    Tuple[bool,List[str]]:是否只能管理使用,命令名
    """
    nezha_cmd_help: CMD_TYPE = Field(default=["哪吒帮助"])
    nezha_cmd_list: CMD_TYPE = Field(default=["vps列表"])
    nezha_cmd_details: CMD_TYPE = Field(default=["vps"])

    # 默认参数
    nezha_arg_default: Optional[Union[int, str]] = Field(default=None)

    nezha_template_server: str = Field(default=(
        "#$.name# #$.IfOnline#\n"
        "   ID: #$.id# TAG: #$.tag#\n"
        "   IPv4: #$.ipv4#\n"
        "   IPv6: #$.ipv6#"
    ))
    nezha_template_server_details: str = Field(default=(
        "#$.name# #$.IfOnline#\n"
        "   ID: #$.id# TAG: #$.tag#\n"
        "   负载: #$.status.Load1#,#$.status.Load5#,#$.status.Load15#\n"
        "   CPU: #$.CpuPercent#\n"
        "   内存: #$.MemoryPercent# 硬盘: #$.DiskPercent#\n"
        "   流量: #$.status.NetInTransfer#↓ ↑#$.status.NetOutTransfer#\n"
        "   IPv4: #$.ipv4#\n"
        "   IPv6: #$.ipv6#"
    ))
    # datetime.strftime(nezha_template_datetime)
    nezha_template_datetime: str = Field(default="%Y-%m-%d %H:%M:%S")
    nezha_template_datetime_placeholder: str = Field(default="无")
    nezha_template_online_offline: List[str] = Field(default=["在线", "离线"])

    # 浮点数小数位数、是否展示IP、是否省略IP中间部分、判断离线时间
    nezha_decimal_places: int = Field(default=1)
    nezha_show_ip: bool = Field(default=True)
    nezha_mask_ip: bool = Field(default=True)
    nezha_offline_time: float = Field(default=30)


config: Config = Config.parse_obj(get_driver().config)
_CM = CommandMeta(compact=config.nezha_use_compact, description="")

__all__ = ["Config", "config", "_CM", "CMD_TYPE"]
