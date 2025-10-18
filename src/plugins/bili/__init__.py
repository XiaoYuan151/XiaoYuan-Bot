from os import getcwd, remove
from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, MessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata
from requests import get

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="bili",
    description="查询一个哔哩哔哩视频的基本信息",
    usage="/bili <vid or url> [true | false]",
    config=Config,
)

config = get_plugin_config(Config)

bili = on_command("bili")


@bili.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args:
            await bili.finish("参数错误！请使用：/bili <vid or url> [true | false]")
        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": "Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-HK;q=0.5",
            "referer": "https://www.bilibili.com"
        }
        bvid = ""
        cid = 0
        messages = []
        if args[0].startswith("http"):
            bvid = args[0].split("video/")[1].replace("/", "").strip()
        else:
            bvid = args[0]
        g_json = get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", headers=headers)
        if g_json.status_code == 200:
            json = g_json.json()
            messages += MessageSegment.image(json["data"]["pic"])
            bvid = json["data"]["bvid"]
            messages += "BV 号：" + bvid + "\n"
            cid = json["data"]["cid"]
            messages += "AV 号：" + str(json["data"]["aid"]) + "\n"
            messages += "作者：" + json["data"]["owner"]["name"] + "\n"
            messages += "标题：" + json["data"]["title"] + "\n"
            messages += "简介：" + json["data"]["desc"] + "\n"
            messages += "分区：" + json["data"]["tname"] + "\n"
            messages += "播放量：" + str(json["data"]["stat"]["view"]) + "\n"
            messages += "点赞数：" + str(json["data"]["stat"]["like"]) + "\n"
            messages += "点踩数：" + str(json["data"]["stat"]["dislike"]) + "\n"
            messages += "投币数：" + str(json["data"]["stat"]["coin"]) + "\n"
            messages += "收藏数：" + str(json["data"]["stat"]["favorite"]) + "\n"
            messages += "分享数：" + str(json["data"]["stat"]["share"]) + "\n"
            messages += "弹幕数：" + str(json["data"]["stat"]["danmaku"]) + "\n"
            messages += "评论数：" + str(json["data"]["stat"]["reply"])
        if messages:
            await bot.send(event, messages)
            if len(args) == 2 and args[1] == "true":
                # g_vid = get(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=120&fourk=1", headers=headers)
                g_vid = get(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}", headers=headers)
                j_vid = g_vid.json()
                vid = get(j_vid["data"]["durl"][0]["backup_url"][0], headers=headers)
                with open(f"{getcwd()}/src/plugins/bili/temp.mp4", "wb") as file:
                    file.write(vid.content)
                await bot.send(event, MessageSegment.video(f"{getcwd()}/src/plugins/bili/temp.mp4"))
                remove(f"{getcwd()}/src/plugins/bili/temp.mp4")
        else:
            await bili.finish(f"无法查询哔哩哔哩视频信息，请检查 BV 号是否正确")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await bili.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
