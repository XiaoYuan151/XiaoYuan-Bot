from os import remove
from tempfile import NamedTemporaryFile
from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, MessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata
from requests import get
from yt_dlp import YoutubeDL

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="player",
    description="从网易云音乐播放一个音乐",
    usage="/player play <music_name or url>",
    config=Config,
)

config = get_plugin_config(Config)

player = on_command("player", aliases={"play"})


@player.handle()
async def handle_function(bot: Bot, event: MessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args:
            await player.finish("参数错误！请使用：/player play <music_name or url>")
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
        keyword = ""
        for arg in args:
            keyword += arg + " "
        music_id = 0
        music_name = ""
        music_pic = ""
        music_lrc = ""
        if keyword.startswith("http"):
            if not keyword.find("youtube") == -1 or not keyword.find("youtu.be") == -1:
                file = NamedTemporaryFile(suffix=".mp4", delete=True)
                file.close()
                options = {
                    "format": "bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]",
                    "outtmpl": file.name,
                    "quiet": True,
                    "no_warnings": True
                }
                with YoutubeDL(options) as ydl:
                    ydl.download(keyword)
                await bot.send(event, MessageSegment.video(file.name))
                remove(file.name)
            elif not keyword.find("bilibili") == -1:
                bvid = keyword.split("video/")[1].replace("/", "").strip()
                g_json = get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}",
                             headers=headers)
                if g_json.status_code == 200:
                    json = g_json.json()
                    g_vid = get(
                        f'https://api.bilibili.com/x/player/playurl?bvid={json["data"]["bvid"]}&cid={json["data"]["cid"]}',
                        headers=headers)
                    j_vid = g_vid.json()
                    vid = get(j_vid["data"]["durl"][0]["backup_url"][0], headers=headers)
                    with NamedTemporaryFile("wb", suffix=".mp4", delete=True) as file:
                        file.write(vid.content)
                        await bot.send(event, MessageSegment.video(file.name))
        else:
            j_search = get(f"https://ncma.xiaoyuan151.net/cloudsearch?keywords={keyword.strip()}")
            search = j_search.json()
            if search["code"] == 200:
                music_id = search["result"]["songs"][0]["id"]
                music_name = search["result"]["songs"][0]["ar"][0]["name"] + " - " + search["result"]["songs"][0][
                    "name"]
                music_pic = search["result"]["songs"][0]["al"]["picUrl"]
            j_lyric = get(f"https://ncma.xiaoyuan151.net/lyric/new?id={music_id}")
            lyric = j_lyric.json()
            if lyric["code"] == 200:
                music_lrc = lyric["lrc"]["lyric"]
            j_match = get(f"https://unma.xiaoyuan151.net/match?id={music_id}&server=qq,pyncmd")
            match = j_match.json()
            if match["code"] == 200 and match["message"] == "匹配成功":
                messages = []
                messages += MessageSegment.node_custom(event.self_id, "小源机器人", music_lrc)
                messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                       Message(MessageSegment.image(music_pic)))
                messages += MessageSegment.node_custom(event.self_id, "小源机器人", Message(
                    MessageSegment.music_custom(f"https://music.xiaoyuan151.com/song?id={music_id}",
                                                match["data"]["url"], music_name, img_url=music_pic)))
                await bot.send(event, messages)
            else:
                await player.finish(f"找不到音乐 {keyword}，请确定名称后再试一次")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await player.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
