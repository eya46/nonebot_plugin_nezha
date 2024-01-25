from json import loads
from pathlib import PurePosixPath
from typing import Literal, Any, Union, List, Optional, cast
from urllib.parse import urlparse, urlunparse

from nonebot import get_driver
from nonebot.internal.driver import Request, HTTPClientMixin
from pydantic import parse_obj_as

from .model import Server, ServerDetails

global_driver = get_driver()

assert isinstance(global_driver, HTTPClientMixin), "Driver has not HTTPClientMixin"

global_driver = cast(HTTPClientMixin, global_driver)


class API:

    def __init__(self, url: str, token: str):
        self.api = url
        self.token = token
        self.headers = {
            "Authorization": token
        }

    def get_api(self, path: str) -> str:
        u = urlparse(self.api)
        return urlunparse(u._replace(path=(PurePosixPath(u.path) / path).as_posix()))  # type:ignore

    async def call_api(
            self,
            path: str, method: Literal["GET", "PUT", "POST", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"], **data: Any
    ) -> Any:
        resp = await global_driver.request(Request(
            method, self.get_api(path),
            headers=self.headers,
            **({"params": data} if method == "GET" else {"json": data})
        ))

        res = loads(resp.content)

        assert res["code"] == 0, f"调用api失败<code:{res['code']}>: {res['message']}"

        return res.get("result")

    async def get_servers_by_tag(self, tag: Optional[str] = None) -> List[Server]:
        if tag is None:
            tag = ""
        return parse_obj_as(List[Server], await self.call_api("/api/v1/server/list", "GET", tag=tag))

    async def get_servers_details_by_tag(self, tag: Optional[str] = None) -> List[ServerDetails]:
        if tag is None:
            tag = ""
        return parse_obj_as(
            List[ServerDetails], await self.call_api("/api/v1/server/details", "GET", tag=tag)
        )

    async def get_servers_details_by_id(self, id_: Optional[Union[int, str]] = None) -> List[ServerDetails]:
        if id_ is None:
            id_ = ""
        return parse_obj_as(
            List[ServerDetails], await self.call_api("/api/v1/server/details", "GET", id=str(id_))
        )
