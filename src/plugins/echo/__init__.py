from nonebot import get_plugin_config, on_command
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="echo",
    description="重复你说的话（由于安全原因，此插件已被禁用）",
    usage="/echo <message>",
    config=Config,
)

config = get_plugin_config(Config)

echo = on_command("echo")


@echo.handle()
async def handle_function():
    await echo.finish("由于安全原因，此插件已被禁用！")
