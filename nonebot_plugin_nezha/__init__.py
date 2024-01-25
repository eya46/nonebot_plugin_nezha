from typing import Annotated, Union, Literal

from arclet.alconna import Args
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import Match, AlconnaMatch

from .config import Config, config
from .tool import wrap_cmd, send, HELPS
from .render import render_list
from .api import API

api = API(config.nezha_api, config.nezha_token)


@wrap_cmd(config.nezha_cmd_help, Args["index?", int])
async def help_cmd_handle(index: Annotated[Match[int], AlconnaMatch("index")]):
    if index.available:
        await send(f"{index.result}.{HELPS[index.result]}")
    else:
        await send("\n".join(f"{i}.{h}" for i, h in enumerate(HELPS)))


@wrap_cmd(config.nezha_cmd_list, Args["tag?", Union[str, Literal["all"]], config.nezha_arg_default])
async def list_cmd_handle(tag: Annotated[Match[str], AlconnaMatch("tag")]):
    if tag.available:
        servers = await api.get_servers_by_tag("" if tag.result == "all" else tag.result)
    else:
        servers = await api.get_servers_by_tag()

    await send(render_list(config.nezha_template_server, servers) if len(servers) > 0 else "无服务器或未找到")


@wrap_cmd(config.nezha_cmd_details, Args["arg?", Union[int, str, Literal["all"]], config.nezha_arg_default])
async def details_cmd_handle(arg: Annotated[Match[Union[int, str]], AlconnaMatch("arg")]):
    if arg.available:
        if isinstance(arg.result, int) or "," in arg.result:
            servers = await api.get_servers_details_by_id(arg.result)
        else:
            servers = await api.get_servers_details_by_tag("" if arg.result == "all" else arg.result)
    else:
        servers = await api.get_servers_details_by_id()

    await send(render_list(config.nezha_template_server_details, servers) if len(servers) > 0 else "无服务器或未找到")


__plugin_meta__ = PluginMetadata(
    name="哪吒监控插件",
    description="哪吒监控插件，使用哪吒监控API。",
    usage="\n".join(f"{i}.{h}" for i, h in enumerate(HELPS)),
    type="application",
    homepage="https://github.com/eya46/nonebot_plugin_nezha",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
)
