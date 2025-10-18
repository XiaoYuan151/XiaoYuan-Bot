from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata
from twitchAPI.helper import first
from twitchAPI.twitch import Twitch

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="twitch",
    description="查询一个 Twitch 主播的状态",
    usage="/twitch <user_name>",
    config=Config,
)

config = get_plugin_config(Config)

twitch = on_command("twitch")


@twitch.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args or not len(args) == 1:
            await twitch.finish("参数错误！请使用：/twitch <user_name>")
        messages = []
        client = await Twitch("", "")
        user = await first(client.get_users(logins=[args[0]]))
        channel = await first(client.get_streams(user_id=user.id))
        if channel:
            messages += MessageSegment.image(channel.thumbnail_url.replace("-{width}x{height}", ""))
            messages += "用户 ID：" + user.id + "\n"
            messages += "用户名：" + user.login + "\n"
            messages += "正在直播：是\n"
            messages += "直播标题：" + channel.title + "\n"
            messages += "直播主题：" + channel.game_name + "\n"
            tags = ""
            for tag in channel.tags:
                tags += tag + " "
            messages += "直播标签：" + tags.strip() if tags else "无"
            messages += "\n"
            messages += "开始时间：" + str(channel.started_at) + "\n"
            messages += "观看人数：" + str(channel.viewer_count) + "\n"
        else:
            schedule = await first(await client.get_channel_stream_schedule(user.id))
            messages += MessageSegment.image(user.offline_image_url)
            messages += "用户 ID：" + user.id + "\n"
            messages += "用户名：" + user.login + "\n"
            messages += "正在直播：否\n"
            messages += "下一场直播标题：" + schedule.title + "\n"
            messages += "下一场直播开始：" + str(schedule.start_time) + "\n"
            messages += "下一场直播结束：" + str(schedule.end_time) + "\n"
            messages += "下一场直播主题：" + schedule.category.name + "\n"
        if messages:
            await bot.send(event, messages)
        else:
            await twitch.finish(f"无法查询 Twitch 直播状态，请检查用户名是否正确")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await twitch.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
