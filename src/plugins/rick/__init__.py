from os import getcwd

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="rick",
    description="Get Rickroll LOL",
    usage="/rick",
    config=Config,
)

config = get_plugin_config(Config)

rick = on_command("rick")


@rick.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/rick/files/rick.amr"))
    await bot.send(event, MessageSegment.video(f"{getcwd()}/src/plugins/rick/files/rick.mp4"))


free_minecraft_download = on_command("free_minecraft_download", aliases={"free_neuro_download"})


@free_minecraft_download.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/rick/files/rickroll.amr"))


fuck = on_command("fuck", aliases={"filtered"})


@fuck.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/rick/files/but.amr"))


yarino = on_command("yarino")


@yarino.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/rick/files/other.amr"))


kim = on_command("kim")


@kim.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/rick/files/kim.amr"))
    with open(f"{getcwd()}/src/plugins/rick/files/kim.txt", "r") as t_kim:
        await kim.finish(t_kim.read())
