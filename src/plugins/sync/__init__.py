from json import loads
from os import getcwd, path, makedirs

from mcrcon import MCRcon
from nonebot import get_plugin_config, on_command, on_message
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, GroupMessageEvent, PrivateMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot_plugin_userinfo import get_user_info
from websockets import connect

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="sync",
    description="将本群聊天内容同步的其他位置（需要完成配置，且仅对当前所在群生效）",
    usage="/sync <option>",
    config=Config,
)

config = get_plugin_config(Config)
c_path = f"{getcwd()}/src/plugins/sync/configs"
if not path.exists(c_path):
    makedirs(c_path)

sync = on_command("sync")


@sync.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    args = event.get_plaintext().split(" ")
    args.pop(0)
    args = list(filter(None, args))
    commands = [["/set_sync mc", "配置 Minecraft 服务器聊天同步（请在私信中使用以确保你的 Rcon 安全）",
                 "/set_sync mc <host> <password> <port>"],
                ["/set_sync discord", "配置 Discord 服务器聊天同步（请在私信中使用以确保你的密钥安全）",
                 "/set_sync discord <token> <channel_id>"],
                ["/sync reset", "重置本群的配置文件（此命令将会从服务器删除你的配置文件）", "/sync reset"],
                ["/sync menu", "显示此菜单", "/sync menu or /sync help"]]
    if not args or args[0] == "menu" or args[0] == "help":
        messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人聊天同步工具菜单 ---")
        for command in commands:
            name = command[0] or "无"
            description = command[1] or "无"
            usage = command[2] or "无"
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   f"命令：{name}\n介绍：{description}\n用法：{usage}")
        messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                               "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
        await bot.send(event, messages)


set_sync = on_command("set_sync")


@set_sync.handle()
async def handle_function(bot: Bot, event: PrivateMessageEvent):
    args = event.get_plaintext().split(" ")
    args.pop(0)
    args = list(filter(None, args))
    if not args or len(args) == 1:
        await set_sync.finish(
            "参数错误！请使用：/set_sync mc <host> <password> <port> or /set_sync discord <token> <channel_id>")
    elif args[0] == "mc":
        await set_sync.finish("已完成 Rcon 配置，请前往游戏服务器查看是否生效")


handle = on_message()


@handle.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    session_id = event.get_session_id()
    session = session_id.split("_")
    if not len(session) == 1:
        user_id = session[2]
        group_id = session[1]
        if path.isfile(c_path + f"/{group_id}.json"):
            with open(c_path + f"/{group_id}.json", "r") as f_json:
                json = loads(f_json.read())
                if json["minecraft"] and event.get_plaintext():
                    rcon = MCRcon(json["minecraft"]["host"], json["minecraft"]["password"], json["minecraft"]["port"])
                    rcon.connect()
                    user_info = await get_user_info(bot, event, user_id)
                    rcon.command(
                        "tellraw @a [\"\",{\"text\":\"聊天同步 - " + user_info.user_name + " 说：\",\"color\":\"yellow\"},{\"text\":\"" + event.get_plaintext() + "\"}]")
                    rcon.disconnect()
                if json["discord"] and event.get_plaintext():
                    async with connect('ws://127.0.0.1:47392') as websocket:
                        await websocket.send(json["discord"]["channel_id"] + "|" + event.get_plaintext())
