from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata
from requests import get

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="minecraft",
    description="查看一个 Minecraft 服务器的信息",
    usage="/minecraft <address> or /mc <address>",
    config=Config,
)

minecraft = get_plugin_config(Config)

minecraft = on_command("minecraft", aliases={"mc"})


@minecraft.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args or not len(args) == 1:
            await minecraft.finish("参数错误！请使用：/minecraft <address> or /mc <address>")
        messages = []
        g_img = get(f"https://api.mcstatus.io/v2/widget/java/{args[0]}")
        g_json = get(f"https://api.mcstatus.io/v2/status/java/{args[0]}")
        if g_img.status_code == 200:
            messages += MessageSegment.image(g_img.content)
        if g_json.status_code == 200:
            json = g_json.json()
            if json["online"]:
                messages += "地址：" + json["host"] + "\n"
                messages += "IP 地址：" + json["ip_address"] + "\n"
                if json["srv_record"]:
                    messages += "真实地址：" + json["srv_record"]["host"] + "\n"
                    messages += "端口号：" + str(json["srv_record"]["port"]) + "\n"
                else:
                    messages += "端口号：" + str(json["port"]) + "\n"
                messages += "版本号：" + json["version"]["name_clean"] + "\n"
                messages += "简介：" + json["motd"]["clean"] + "\n"
                eula_blocked = "是" if json["eula_blocked"] else "否"
                messages += "是否被 Mojang 封禁：" + eula_blocked + "\n"
                messages += "在线玩家："
                players = ""
                if not json["players"]["online"] == 0:
                    for player in json["players"]["list"]:
                        players += player["name_clean"] + " "
                    players.strip().replace(" ", ", ")
                messages += players if players else "无"
                messages += "\n"
                if json["software"]:
                    messages += "服务器软件：" + json["software"] + "\n"
                messages += "模组列表："
                mods = ""
                if json["mods"]:
                    for mod in json["mods"]:
                        mods += mod["name"] + "@" + mod["version"] + " "
                messages += mods.strip() if mods else "无"
                messages += "\n"
                messages += "插件列表："
                plugins = ""
                if json["plugins"]:
                    for plugin in json["plugins"]:
                        plugins += plugin["name"] + "@" + plugin["version"] + " "
                messages += plugins.strip() if plugins else "无"
        if messages:
            await bot.send(event, messages)
        else:
            await minecraft.finish(f"无法查询 Minecraft 服务器状态，请检查服务器地址是否正确")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await minecraft.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
