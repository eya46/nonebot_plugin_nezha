from abc import abstractmethod
from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, root_validator

from .config import config

_n = config.nezha_decimal_places


def _rd(x):
    return round(x, _n)


class M(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.transfer

    @classmethod
    @abstractmethod
    def transfer(cls, _):
        pass


class ToTime(M):
    @classmethod
    def transfer(cls, _: Union[int, float]):
        if _ < 60:
            return f"{_}s"
        elif _ < 60 * 60:
            return f"{_rd(_ / 60)}m"
        elif _ < 60 * 60 * 24:
            return f"{_rd(_ / 60 / 60)}h"
        else:
            return f"{_rd(_ / 60 / 60 / 24)}d"


class ToDatetime(M):

    @classmethod
    def transfer(cls, _: int):
        _ = datetime.fromtimestamp(_)
        return _.strftime(config.nezha_template_datetime) if _.timestamp() > 0 else "无"


class ToTotal(M):
    @classmethod
    def transfer(cls, _: int):
        # bytes to str
        if _ < 1024:
            return f"{_}B"
        elif _ < 1024 * 1024:
            return f"{_rd(_ / 1024)}K"
        elif _ < 1024 * 1024 * 1024:
            return f"{_rd(_ / 1024 / 1024)}M"
        elif _ < 1024 * 1024 * 1024 * 1024:
            return f"{_rd(_ / 1024 / 1024 / 1024)}G"
        else:
            return f"{_rd(_ / 1024 / 1024 / 1024 / 1024)}T"


class ToSpeed(M):
    @classmethod
    def transfer(cls, _: int):
        # speed to str
        if _ < 1024:
            return f"{_}B/s"
        elif _ < 1024 * 1024:
            return f"{_rd(_ / 1024)}K/s"
        elif _ < 1024 * 1024 * 1024:
            return f"{_rd(_ / 1024 / 1024)}M/s"
        elif _ < 1024 * 1024 * 1024 * 1024:
            return f"{_rd(_ / 1024 / 1024 / 1024)}G/s"
        else:
            return f"{_rd(_ / 1024 / 1024 / 1024 / 1024)}T/s"


class ToFloat(M):
    @classmethod
    def transfer(cls, _: float):
        return str(_rd(_))


class ToIP(M):
    @classmethod
    def transfer(cls, _: str):
        if _ == "":
            return "无"
        if not config.nezha_show_ip:
            return "***"
        if not config.nezha_mask_ip:
            return _
        if ":" in _:
            return _.split(":")[0] + ":***:" + _.split(":")[-1]
        return _.split(".")[0] + ".*.*." + _.split(".")[-1]


class ToOnlineStatus(M):
    @classmethod
    def transfer(cls, _: bool):
        return config.nezha_template_online_offline[0 if _ else 1]


class Host(BaseModel):
    Platform: str
    PlatformVersion: str
    CPU: List[str]
    MemTotal: ToTotal
    DiskTotal: ToTotal
    SwapTotal: ToTotal
    Arch: str
    Virtualization: str
    BootTime: ToDatetime
    CountryCode: str
    Version: str


class Status(BaseModel):
    CPU: ToFloat
    MemUsed: ToTotal
    SwapUsed: ToTotal
    DiskUsed: ToTotal
    NetInTransfer: ToTotal
    NetOutTransfer: ToTotal
    NetInSpeed: ToSpeed
    NetOutSpeed: ToSpeed
    Uptime: ToTime
    Load1: ToFloat
    Load5: ToFloat
    Load15: ToFloat
    TcpConnCount: int
    UdpConnCount: int
    ProcessCount: int


class Server(BaseModel):
    id: int
    name: str
    tag: str
    last_active: ToDatetime
    ipv4: ToIP
    ipv6: ToIP
    valid_ip: ToIP

    IfOnline: ToOnlineStatus

    @root_validator(pre=True)
    def _validator(cls, data):
        data["IfOnline"] = datetime.now().timestamp() - data["last_active"] < config.nezha_offline_time
        return data


class ServerDetails(Server):
    host: Host
    status: Status

    MemoryPercent: str
    CpuPercent: str
    DiskPercent: str

    @root_validator(pre=True)
    def _validator(cls, data):
        data["MemoryPercent"] = f'{_rd(data["status"]["MemUsed"] / data["host"]["MemTotal"] * 100)}%'
        data["CpuPercent"] = f'{_rd(data["status"]["CPU"])}%'
        data["DiskPercent"] = f'{_rd(data["status"]["DiskUsed"] / data["host"]["DiskTotal"] * 100)}%'
        data["IfOnline"] = datetime.now().timestamp() - data["last_active"] < config.nezha_offline_time
        return data
