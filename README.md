<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin nezha

哪吒监控插件

![License](https://img.shields.io/github/license/eya46/nonebot_plugin_nezha)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![NoneBot](https://img.shields.io/badge/nonebot-2.0.1+-blueviolet)
</div>

## 安装方式

### 依赖管理

- `pip install nonebot-plugin-nezha`
- `poetry add nonebot-plugin-nezha`
- `pdm add nonebot-plugin-nezha`

> 在 `bot.py` 中添加 `nonebot.load_plugin("nonebot_plugin_nezha")`

### nb-cli

- `nb plugin install nonebot-plugin-nezha`

## 使用方式

- 哪吒帮助 [index: int]
- vps列表 [tag: str]
- vps [arg: int|str]

## 配置项

### 必要配置项

- `nezha_api`: 哪吒监控 api地址
- `nezha_token`: 哪吒监控 api token

## 依赖项

- [nonebot2](https://github.com/nonebot/nonebot2) >=2.0.1
- [plugin-alconna](https://github.com/nonebot/plugin-alconna) ^0.36.0

## 相关

- [哪吒监控官网](https://nezha.wiki/)
- [哪吒监控项目地址](https://github.com/naiba/nezha)