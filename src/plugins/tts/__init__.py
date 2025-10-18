from os import getcwd, remove
from time import time

from edge_tts import Communicate
from googletrans import Translator
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata

from .config import Config
from .tts import gen_tts

__plugin_meta__ = PluginMetadata(
    name="tts",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

tts = on_command("tts")


@tts.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args:
            await tts.finish("参数错误！请使用：/tts <text>")
        text = ""
        for arg in args:
            text += arg + " "
        translator = Translator()
        lang = await translator.detect(text)
        if lang.lang == "zh-CN":
            await Communicate(text.strip(), voice="zh-CN-YunxiNeural", volume="+100%").save(
                f"{getcwd()}/src/plugins/tts/temp.mp3")
        else:
            ret = gen_tts(text.strip(), f"{getcwd()}/src/plugins/tts/temp.mp3")
            if not ret[0] == 200:
                await Communicate(text.strip(), voice="en-US-AvaMultilingualNeural", volume="+100%").save(
                    f"{getcwd()}/src/plugins/tts/temp.mp3")
                # raise GenerateException(ret[1])
        await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/tts/temp.mp3"))
        remove(f"{getcwd()}/src/plugins/tts/temp.mp3")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await tts.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


class GenerateException(RuntimeError):
    def __init__(self, arg):
        self.args = arg
