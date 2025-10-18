from nonebot import get_plugin_config, on_notice
from nonebot.adapters.onebot.v11 import Bot, NoticeEvent
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="captcha",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

handle = on_notice()


@handle.handle()
async def handle_function(bot: Bot, event: NoticeEvent):
    print(event.get_event_name())
    if event.get_event_name():
        print("1")
