from nonebot import get_plugin_config, get_loaded_plugins, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.plugin import PluginMetadata, Plugin

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="menu",
    description="查看机器人的全部功能",
    usage="/menu or /help",
    config=Config,
)

config = get_plugin_config(Config)

menu = on_command("menu", aliases={"help"})


@menu.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    plugins: set[Plugin] = get_loaded_plugins()
    messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人功能菜单 ---")
    for plugin in plugins:
        if not plugin.metadata.description == "non-public":
            name = plugin.metadata.name or "无"
            description = plugin.metadata.description or "无"
            usage = plugin.metadata.usage or "无"
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   f"命令：/{name}\n介绍：{description}\n用法：{usage}")
    messages += MessageSegment.node_custom(event.self_id, "小源机器人", "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
    await bot.send(event, messages)
