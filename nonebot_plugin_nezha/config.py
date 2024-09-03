from typing import Optional, Union

from arclet.alconna import CommandMeta
from nonebot import logger
from nonebot.plugin import get_plugin_config
from pydantic import AnyHttpUrl, BaseModel, Field

CMD_TYPE = Optional[Union[list[str], tuple[bool, list[str]]]]


class Config(BaseModel):
    api: AnyHttpUrl = Field(alias="nezha_api")
    token: str = Field(alias="nezha_token")

    use_start: bool = Field(default=True, alias="nezha_use_start")
    # 是否使用紧凑模式(命令后是否可以紧跟参数)
    use_compact: bool = Field(default=True, alias="nezha_use_compact")

    at: bool = Field(default=False, alias="nezha_at")
    replay: bool = Field(default=False, alias="nezha_replay")
    must_super_user: bool = Field(default=True, alias="nezha_must_super_user")

    """
    None:不启用该插件
    List[str]:命令名
    Tuple[bool,List[str]]:是否只能管理使用,命令名
    """
    cmd_help: CMD_TYPE = Field(default=["哪吒帮助"], alias="nezha_cmd_help")
    cmd_list: CMD_TYPE = Field(default=["vps列表"], alias="nezha_cmd_list")
    cmd_details: CMD_TYPE = Field(default=["vps"], alias="nezha_cmd_details")

    # 默认参数
    arg_default: Optional[Union[int, str]] = Field(default=None, alias="nezha_arg_default")

    template_server: str = Field(
        default="#$.name# #$.IfOnline#\n   ID: #$.id# TAG: #$.tag#\n   IPv4: #$.ipv4#\n   IPv6: #$.ipv6#",
        alias="nezha_template_server",
    )
    template_server_details: str = Field(
        default=(
            "#$.name# #$.IfOnline#\n"
            "   ID: #$.id# TAG: #$.tag#\n"
            "   负载: #$.status.Load1#,#$.status.Load5#,#$.status.Load15#\n"
            "   CPU: #$.CpuPercent#\n"
            "   内存: #$.MemoryPercent# 硬盘: #$.DiskPercent#\n"
            "   流量: #$.status.NetInTransfer#↓ ↑#$.status.NetOutTransfer#\n"
            "   IPv4: #$.ipv4#\n"
            "   IPv6: #$.ipv6#"
        ),
        alias="nezha_template_server_details",
    )
    # datetime.strftime(nezha_template_datetime)
    template_datetime: str = Field(default="%Y-%m-%d %H:%M:%S", alias="nezha_template_datetime")
    template_datetime_placeholder: str = Field(default="无", alias="nezha_template_datetime_placeholder")
    nezha_template_online_offline: list[str] = Field(default=["在线", "离线"], alias="nezha_template_online_offline")

    # 浮点数小数位数、是否展示IP、是否省略IP中间部分、判断离线时间
    decimal_places: int = Field(default=1, alias="nezha_decimal_places")
    show_ip: bool = Field(default=True, alias="nezha_show_ip")
    mask_ip: bool = Field(default=True, alias="nezha_mask_ip")
    offline_time: float = Field(default=30, alias="nezha_offline_time")


LOAD_SUCCESS = False
_CM = CommandMeta(description="")

try:
    config: Config = get_plugin_config(Config)
    LOAD_SUCCESS = True
    _CM.compact = config.use_compact
except Exception as e:
    logger.error("nezha插件配置加载失败, 请检查配置.")
    logger.exception(e)

__all__ = ["Config", "config", "_CM", "CMD_TYPE", "LOAD_SUCCESS"]
