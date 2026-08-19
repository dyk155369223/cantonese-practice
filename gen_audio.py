import re, os, asyncio, edge_tts

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, 'index.html')
AUDIO = os.path.join(BASE, 'audio')
VOICE = 'zh-HK-HiuGaaiNeural'
RATE = '-10%'   # 略慢，更贴近日常聊天语速

def extract():
    html = open(HTML, encoding='utf-8').read()
    return re.findall(r"yue:'([^']*)'", html)

async def gen_one(text, out):
    # 纯文本：edge-tts 自动处理标点和自然停顿，避免 SSML 把中文标点当字符读出
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(out)

async def main():
    texts = extract()
    print('found', len(texts), 'phrases')
    os.makedirs(AUDIO, exist_ok=True)
    for i, t in enumerate(texts, 1):
        out = os.path.join(AUDIO, '%03d.mp3' % i)
        await gen_one(t, out)
        print('saved', out)

asyncio.run(main())
print('ALL DONE')
