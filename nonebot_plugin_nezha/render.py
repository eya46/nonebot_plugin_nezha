from re import findall

from jsonpath import jsonpath
from nonebot import logger
from pydantic import BaseModel


def render(template: str, data: BaseModel) -> str:
    data = data.model_dump()
    # #(.*?)#
    for i in findall(r"(?<!\\)#\s*(.*?)\s*#", template):
        _ = jsonpath(data, i, use_eval=False)
        if not _ and len(_) > 0:
            logger.error(f"模板渲染失败,找不到{i}")
            res = "异常"
        else:
            res = _[0]
        template = template.replace(f"#{i}#", str(res), 1)
    return template.replace("\\#", "#")


def render_list(template: str, data: list[BaseModel]) -> str:
    return "\n".join(f"{i + 1}.{render(template, d)}" for i, d in enumerate(data))
