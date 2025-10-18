from time import sleep

from googletrans import Translator
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="grass",
    description="调用谷歌生草机翻译你的文本",
    usage="/grass <text>",
    config=Config,
)

config = get_plugin_config(Config)

grass = on_command("grass")


@grass.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    args = event.get_plaintext().split(" ")
    args.pop(0)
    args = list(filter(None, args))
    if not args:
        await grass.finish("参数错误！请使用：/grass <text>")
    translator = Translator()
    origin = ""
    ret = ""
    for arg in args:
        origin += arg + " "
    origin = origin.strip()
    detect = await translator.detect(origin)
    if not detect.lang == "en":
        en = await translator.translate(origin, src=detect.lang, dest="en")
        en_text = en.text
    else:
        en_text = origin
    texts = en_text.split(" ")
    for text in texts:
        zh_cn = await translator.translate(text, src="en", dest="zh-CN")
        ret += zh_cn.text
        sleep(1)
    # await Communicate(ret, voice="zh-CN-YunxiNeural", volume="+50%").save(f"{getcwd()}/src/plugins/grass/temp.mp3")
    # await bot.send(event, MessageSegment.record(f"{getcwd()}/src/plugins/grass/temp.mp3"))
    # remove(f"{getcwd()}/src/plugins/grass/temp.mp3")
    await grass.finish(f"谷歌生草机翻译完毕！\n原文：{origin}\n译文：{ret}")
