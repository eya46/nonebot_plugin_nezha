from pathlib import PurePosixPath
from typing import Literal, Any, Union, List, Optional
from urllib.parse import urlparse, urlunparse

from httpx import AsyncClient
from pydantic import parse_obj_as

from .model import Server, ServerDetails


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
        data = {k: v for k, v in data.items() if v is not None}
        async with AsyncClient(headers=self.headers) as client:
            resp = await client.request(
                method, self.get_api(path), **({"params": data} if method == "GET" else {"json": data})
            )
            res = resp.json()
            assert res["code"] == 0, f"调用api失败<code:{res['code']}>: {res['message']}"
            return res.get("result")

    async def get_servers_by_tag(self, tag: Optional[str] = None) -> List[Server]:
        return parse_obj_as(List[Server], await self.call_api("/api/v1/server/list", "GET", tag=tag))

    async def get_servers_details_by_tag(self, tag: Optional[str] = None) -> List[ServerDetails]:
        return parse_obj_as(
            List[ServerDetails], await self.call_api("/api/v1/server/details", "GET", tag=tag)
        )

    async def get_servers_details_by_id(self, id_: Optional[Union[int, str]] = None) -> List[ServerDetails]:
        return parse_obj_as(
            List[ServerDetails], await self.call_api("/api/v1/server/details", "GET", id=str(id_))
        )
