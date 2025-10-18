from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="fakemsg",
    description="发送伪造的转发消息，可多条同时发送",
    usage="/fakemsg <user_id>,<nickname>,<content> ...",
    config=Config,
)

config = get_plugin_config(Config)

fakemsg = on_command("fakemsg")


@fakemsg.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args:
            await fakemsg.finish("参数错误！请使用：/fakemsg <user_id>,<nickname>,<content> ...")
        messages = []
        if not GROUP_ADMIN(bot, event) or not GROUP_OWNER(bot, event):
            messages += MessageSegment.node_custom(event.self_id, "小源机器人", "以下消息均为伪造消息，请勿当真！")
        for arg in args:
            s_args = arg.split(",")
            if len(s_args) < 3:
                await fakemsg.finish("参数错误！请使用：/fakemsg <user_id>,<nickname>,<content> ...")
            messages += MessageSegment.node_custom(s_args[0], s_args[1], s_args[2])
        await bot.send(event, messages)
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await fakemsg.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
