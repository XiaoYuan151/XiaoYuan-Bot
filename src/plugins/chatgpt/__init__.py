from os import getcwd, path, makedirs
from time import time

from nonebot import get_plugin_config, on_command, on_message
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, PrivateMessageEvent
from nonebot.exception import FinishedException
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="chatgpt",
    description="在 QQ 中使用 ChatGPT（仅限私信，且需要提供 OpenAI API Key）",
    usage="/chatgpt <option>",
    config=Config,
)

config = get_plugin_config(Config)
c_path = c_path = f"{getcwd()}/src/plugins/chatgpt/configs"
if not path.exists(c_path):
    makedirs(c_path)

chatgpt = on_command("chatgpt")


@chatgpt.handle()
async def handle_function(bot: Bot, event: PrivateMessageEvent):
    try:
        args = event.get_plaintext().split(" ")
        args.pop(0)
        args = list(filter(None, args))
        commands = [["on", "开启 ChatGPT", "/chatgpt on"],
                    ["off", "关闭 ChatGPT", "/chatgpt off"],
                    ["config", "配置 ChatGPT", "/chatgpt config [option]"],
                    ["menu", "显示此菜单", "/chatgpt menu or /chatgpt help"]]
        configs = [["key", "配置 OpenAI API Key", "/chatgpt config key <OpenAI API Key> <password>"],
                   ["del", "删除 OpenAI API Key", "/chatgpt config del <key_id>"],
                   ["select", "选择 ChatGPT 模型", "/chatgpt config select <model_name>"],
                   ["choose", "选择 ChatGPT 角色", "/chatgpt config choose <character_name>"],
                   ["reset", "重置 ChatGPT 配置（此命令将会从服务器删除你的配置文件）", "/chatgpt config reset"]]
        if not args or args[0] == "menu" or args[0] == "help":
            messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人 ChatGPT 工具菜单 ---")
            for command in commands:
                name = command[0] or "无"
                description = command[1] or "无"
                usage = command[2] or "无"
                messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                       f"命令：/chatgpt {name}\n介绍：{description}\n用法：{usage}")
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   "注：你的 OpenAI API Key 将会使用你的密码加密后存储在服务器中的独立配置文件内，仅在你与 ChatGPT 对话时会调用")
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
            await bot.send(event, messages)
        elif args[0] == "on":
            await bot.send(event, "ChatGPT 已开启，今后除命令外所有内容将被视为 ChatGPT 的输入")
        elif args[0] == "off":
            await bot.send(event, "ChatGPT 已关闭，今后除命令外所有内容将被视为普通消息")
        elif args[0] == "config" and len(args) == 1:
            messages = MessageSegment.node_custom(event.self_id, "小源机器人", "--- 小源机器人 ChatGPT 工具菜单 ---")
            for t_config in configs:
                name = t_config[0] or "无"
                description = t_config[1] or "无"
                usage = t_config[2] or "无"
                messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                       f"命令：/chatgpt config {name}\n介绍：{description}\n用法：{usage}")
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   "注：你的 OpenAI API Key 将会使用你的密码加密后存储在服务器中的独立配置文件内，仅在你与 ChatGPT 对话时会调用")
            messages += MessageSegment.node_custom(event.self_id, "小源机器人",
                                                   "版权所有 © 2025 XiaoYuan Studio 保留所有权利")
            await bot.send(event, messages)
    except FinishedException:
        pass
    except Exception as e:
        t_id = round(time())
        with open("tracker.txt", "a") as file:
            file.write(f"[{t_id}] Bug Tracker: {str(e)}")
        await chatgpt.finish(f"Someone tell XiaoYuan there is a problem with my plugin.\nTracker ID: {t_id}")


handle = on_message()


@handle.handle()
async def handle_function(bot: Bot, event: PrivateMessageEvent):
    print(f"发送到 ChatGPT: {event.get_plaintext()}")
