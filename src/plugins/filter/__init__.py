from os import getcwd

from nonebot import get_plugin_config, on_command, on_message
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="filter",
    description="启用聊天过滤器（需要有管理员权限）",
    usage="/filter <option>",
    config=Config,
)

config = get_plugin_config(Config)

o_filter = on_command("filter", permission=GROUP_OWNER | GROUP_ADMIN)


@o_filter.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    args = event.get_plaintext().split(" ")
    args.pop(0)
    args = list(filter(None, args))
    commands = [["on", "开启过滤器", "/filter on"],
                ["off", "关闭过滤器", "/filter off"],
                ["menu", "显示此菜单", "/filter menu or /filter help"]]
    if not args or args[0] == "menu" or args[0] == "help":
        messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人过滤器工具菜单 ---")
        for command in commands:
            name = command[0] or "无"
            description = command[1] or "无"
            usage = command[2] or "无"
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   f"命令：/filter {name}\n介绍：{description}\n用法：{usage}")
        messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                               "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
        await bot.send(event, messages)
    elif args[0] == "on":
        await bot.send(event, "过滤器已开启")
    elif args[0] == "off":
        await bot.send(event, "过滤器已关闭")


handle = on_message()


@handle.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    filtered = ["过滤器测试"]
    for filters in filtered:
        if filters in event.get_plaintext():
            await bot.delete_msg(message_id=event.message_id)
            await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/filter/files/filtered.amr"))
