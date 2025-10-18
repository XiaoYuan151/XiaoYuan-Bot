from json import loads, dumps
from os import getcwd, path, makedirs
from random import choice

from nonebot import get_plugin_config, on_command, on_message, on_notice
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, GroupMessageEvent, NoticeEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.plugin import PluginMetadata
from nonebot_plugin_userinfo import get_user_info

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="handle",
    description="接管群消息（需要有管理员权限）",
    usage="/handle <option>",
    config=Config,
)

config = get_plugin_config(Config)
c_path = f"{getcwd()}/src/plugins/sync/configs"
if not path.exists(c_path):
    makedirs(c_path)

handle = on_command("handle", permission=GROUP_OWNER | GROUP_ADMIN)


@handle.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    args = event.get_plaintext().split(" ")
    args.pop(0)
    args = list(filter(None, args))
    commands = [["on", "启用接管群消息", "/handle on"],
                ["off", "关闭接管群消息", "/handle off"],
                ["menu", "显示此菜单", "/handle menu or /handle help"]]
    if not args or args[0] == "menu" or args[0] == "help":
        messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人接管工具菜单 ---")
        for command in commands:
            name = command[0] or "无"
            description = command[1] or "无"
            usage = command[2] or "无"
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   f"命令：/handle {name}\n介绍：{description}\n用法：{usage}")
        messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                               "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
        await bot.send(event, messages)
    elif args[0] == "on":
        session_id = event.get_session_id()
        session = session_id.split("_")
        if not len(session) == 1:
            user_id = session[2]
            group_id = session[1]
            with open(c_path + f"/{group_id}.json", "w+") as f_json:
                if f_json.read():
                    json = loads(f_json.read())
                json["on"] = True
                f_json.write(dumps(json))
                await handle.finish("已启用接管群消息")
    elif args[0] == "off":
        session_id = event.get_session_id()
        session = session_id.split("_")
        if not len(session) == 1:
            user_id = session[2]
            group_id = session[1]
            with open(c_path + f"/{group_id}.json", "w+") as f_json:
                if f_json.read():
                    json = loads(f_json.read())
                json["on"] = False
                f_json.write(dumps(json))
                await bot.send(event, "已关闭接管群消息")


handle_message = on_message()


@handle_message.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    # print("接收到消息：", event.get_message())
    session_id = event.get_session_id()
    session = session_id.split("_")
    if not len(session) == 1:
        user_id = session[2]
        group_id = session[1]
        if path.isfile(c_path + f"/{group_id}.json"):
            with open(c_path + f"/{group_id}.json", "r") as f_json:
                json = loads(f_json.read())
                if json["on"]:
                    if event.get_message().get("image"):
                        for image in event.get_message().get("image"):
                            await bot.send(event, MessageSegment.image(image.data.get(
                                "file")) + f"接收到图片：{image.data.get('file')}\n下载链接：{image.data.get('url')}\n文件大小：{int(image.data.get('file_size')) / 1024} KB")
                            print("Image URL:", image.data.get("url"))
                    if event.get_message().get("record"):
                        for record in event.get_message().get("record"):
                            await bot.send(event,
                                           MessageSegment.node_custom(event.self_id, "小源机器人",
                                                                      MessageSegment.record(
                                                                          record.data.get(
                                                                              "file"))) + MessageSegment.node_custom(
                                               event.self_id,
                                               "小源机器人",
                                               f"接收到语音：{record.data.get('file')}\n下载链接：{record.data.get('url')}\n文件大小：{int(record.data.get('file_size')) / 1024} KB"))
                    if event.get_message().get("video"):
                        for video in event.get_message().get("video"):
                            await bot.send(event,
                                           MessageSegment.node_custom(event.self_id, "小源机器人", MessageSegment.video(
                                               video.data.get("file"))) + MessageSegment.node_custom(event.self_id,
                                                                                                     "小源机器人",
                                                                                                     f"接收到视频：{video.data.get('file')}\n下载链接：{video.data.get('url')}\n文件大小：{int(video.data.get('file_size')) / 1024} KB"))
                    if event.get_message().get("file"):
                        for file in event.get_message().get("file"):
                            await bot.send(event,
                                           f"接收到文件：{file.data.get('file')}\n下载链接：{file.data.get('url')}\n文件大小：{int(file.data.get('file_size')) / 1024} KB")


handle_notice = on_notice()


@handle_notice.handle()
async def handle_function(bot: Bot, event: NoticeEvent):
    session_id = event.get_session_id()
    session = session_id.split("_")
    if not len(session) == 1:
        user_id = session[2]
        group_id = session[1]
        if path.isfile(c_path + f"/{group_id}.json"):
            with open(c_path + f"/{group_id}.json", "r") as f_json:
                json = loads(f_json.read())
                if json["on"]:
                    w_msg = [
                        f"太棒了，你做到啦，{MessageSegment.at(event.get_user_id())} ",
                        f"{MessageSegment.at(event.get_user_id())} 来啦。",
                        f"{MessageSegment.at(event.get_user_id())} 跳进了群组。",
                        f"一只野生的{MessageSegment.at(event.get_user_id())} 出现了。",
                        f"欢迎大驾光临，{MessageSegment.at(event.get_user_id())} 。",
                        f"{MessageSegment.at(event.get_user_id())} 加入了队伍。",
                        f"很高兴见到你，{MessageSegment.at(event.get_user_id())} 。",
                        f"欢迎，{MessageSegment.at(event.get_user_id())} 。我们希望你带了个披萨来。",
                        f"{MessageSegment.at(event.get_user_id())} 出现了！",
                        f"{MessageSegment.at(event.get_user_id())} 刚刚滑入群组中。",
                        f"{MessageSegment.at(event.get_user_id())} 刚刚降落了。",
                        f"欢迎你，{MessageSegment.at(event.get_user_id())} 。来打个招呼吧！",
                        f"大家快来欢迎{MessageSegment.at(event.get_user_id())} ！",
                    ]
                    if event.get_event_name() == "notice.group_decrease.kick":
                        user_info = await get_user_info(bot, event, event.get_user_id())
                        await handle_notice.finish(f"{user_info.user_name} ({user_info.user_id}) 已被管理员踢出本群")
                    if event.get_event_name() == "notice.group_increase.approve" or event.get_event_name() == "notice.group_increase.invite":
                        await bot.send(event, Message(choice(w_msg).strip()))
                    if event.get_event_name() == "notice.group_decrease.leave":
                        user_info = await get_user_info(bot, event, event.get_user_id())
                        await handle_notice.finish(f"再见，{user_info.user_name} ({user_info.user_id})")
