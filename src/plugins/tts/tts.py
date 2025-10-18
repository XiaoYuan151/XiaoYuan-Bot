from urllib.parse import urlencode, urlparse

from requests import get


def gen_tts(text: str, output: str) -> list:
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
        "referer": "https://www.text-to-speech.cn"
    }
    data = {
        "language": "English+(United+States)",
        "voice": "en-US-AshleyNeural",
        "text": text,
        "role": 0,  # 模仿
        "style": "chat",  # 感情
        "styledegree": 2,  # 强度
        "volume": "x-loud",  # 音量
        "predict": 1,  # 预测
        "rate": -20,  # 语速
        "pitch": 25,  # 语调
        "kbitrate": "audio-16khz-32kbitrate-mono-mp3",  # 质量
        "silence": "150ms",  # 停顿
        "yzm": 202410170001
    }
    e_data = urlencode(data)
    p_url = urlparse("https://www.text-to-speech.cn/getSpeek.php")
    url = p_url._replace(query=e_data).geturl()
    req = get(url, headers=headers)
    js = req.json()
    if js["code"] == 200:
        down = get(js["download"], headers=headers)
        with open(output, "wb") as file:
            file.write(down.content)

    ret = [js["code"], js["msg"]]
    return ret

# "https://www.text-to-speech.cn/getSpeek.php?language=English+(United+States)&voice=en-US-AshleyNeural&text=hell&role=0&style=0&styledegree=2&volume=x-loud&predict=1&rate=-10&pitch=25&kbitrate=audio-16khz-32kbitrate-mono-mp3&silence=&user_id=&yzm=202410170001&token=70acf71f1069d63c3f0bfb6de8240152&token2=c2b8b11b9aac849a5d573ed6e80e33a1"
