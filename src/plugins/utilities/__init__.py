from time import time

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="utilities",
    description="查看管理员专用工具菜单（需要有管理员权限）",
    usage="/utilities",
    config=Config,
)

config = get_plugin_config(Config)

utilities = on_command("utilities", permission=GROUP_OWNER | GROUP_ADMIN)


@utilities.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    menus = [["ban", "封禁（禁言）一个群成员", "/ban <@user_name or user_id> <duration>"],
             ["unban", "解除封禁（禁言）一个群成员", "/unban <@user_name or user_id>"],
             ["kick", "踢出一个群成员", "/kick <@user_name or user_id> [true | false]"],
             ["set_group_name", "设置群名称", "/set_group_name <name>"],
             ["set_group_mute", "设置群禁言状态", "/set_group_mute <true | false>"],
             ["set_group_admin", "设置群管理员（需要机器人为群主）",
              "/set_group_admin <@user_name or user_id> <true | false>"]]
    messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人管理员工具菜单 ---")
    for menu in menus:
        name = menu[0] or "无"
        description = menu[1] or "无"
        usage = menu[2] or "无"
        messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                               f"命令：/{name}\n介绍：{description}\n用法：{usage}")
    messages += MessageSegment.node_custom(event.self_id, "小源机器人", "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
    await bot.send(event, messages)


ban = on_command("ban", permission=GROUP_OWNER | GROUP_ADMIN)


@ban.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        print("args", args)
        user_id = 0
        duration = 0
        if event.get_message().get("at") and args:
            user_id = int(event.get_message().get("at").pop(0).data.get("qq"))
            duration = int(args[0])
        else:
            if args and len(args) == 2:
                user_id = int(args[0])
                duration = int(args[1])
        if not user_id or not duration or duration == "0":
            await ban.finish("参数错误！请使用：/ban <@user_name or user_id> <duration>")
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id, duration=duration)
        await ban.finish(f"已成功封禁用户 {user_id}，禁言时长：{duration} 秒")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await ban.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


unban = on_command("unban", permission=GROUP_OWNER | GROUP_ADMIN)


@unban.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        user_id = 0
        if event.get_message().get("at"):
            user_id = int(event.get_message().get("at").pop(0).data.get("qq"))
        else:
            if args:
                user_id = int(args[0])
        if not user_id:
            await unban.finish("参数错误！请使用：/unban <@user_name or user_id>")
        await bot.set_group_ban(group_id=event.group_id, user_id=user_id, duration=0)
        await unban.finish(f"已成功解除封禁用户 {user_id}")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await unban.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


kick = on_command("kick", permission=GROUP_OWNER | GROUP_ADMIN)


@kick.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        user_id = 0
        reject_add_request = False
        if event.get_message().get("at"):
            user_id = int(event.get_message().get("at").pop(0).data.get("qq"))
            if args and len(args) == 1:
                reject_add_request = args[0] == "true"
        else:
            if args and len(args) == 2:
                user_id = int(args[0])
                reject_add_request = args[1] == "true"
            elif args and len(args) == 1:
                user_id = int(args[0])
        if not user_id:
            await kick.finish("参数错误！请使用：/kick <@user_name or user_id> [true | false]")
        await bot.set_group_kick(group_id=event.group_id, user_id=user_id, reject_add_request=reject_add_request)
        if reject_add_request:
            await kick.finish(f"已成功踢出用户 {user_id} 并拒绝其加群请求")
        else:
            await kick.finish(f"已成功踢出用户 {user_id}")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await kick.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


set_group_name = on_command("set_group_name", permission=GROUP_OWNER | GROUP_ADMIN)


@set_group_name.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args or not len(args) == 1:
            await set_group_name.finish("参数错误！请使用：/set_group_name <name>")
        await bot.set_group_name(group_id=event.group_id, group_name=args[0])
        await set_group_name.finish(f"已成功设置群名称为 {args[0]}")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await set_group_name.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


set_group_mute = on_command("set_group_mute", permission=GROUP_OWNER | GROUP_ADMIN)


@set_group_mute.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        if not args or not len(args) == 1 or args[0] not in ["true", "false"]:
            await set_group_mute.finish("参数错误！请使用：/set_group_mute <true | false>")
        await bot.set_group_whole_ban(group_id=event.group_id, enable=args[0] == "true")
        await set_group_mute.finish(f"已成功设置群禁言状态为 {args[0]}")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await set_group_mute.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


set_group_admin = on_command("set_group_admin", permission=GROUP_OWNER)


@set_group_admin.handle()
async def handle_function(bot: Bot, event: GroupMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        user_id = 0
        status = None
        if event.get_message().get("at"):
            user_id = int(event.get_message().get("at").pop(0).data.get("qq"))
            if args and len(args) == 1:
                status = args[0] == "true"
        else:
            if args and len(args) == 2:
                user_id = int(args[0])
                status = args[1] == "true"
        if not user_id or status == None:
            await set_group_admin.finish("参数错误！请使用：/set_group_admin <@user_name or user_id> <true | false>")
        await bot.set_group_admin(group_id=event.group_id, user_id=user_id, status=status)
        await set_group_admin.finish(f"已成功设置用户 {user_id} 的管理员状态为 {status}")
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await set_group_admin.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")
