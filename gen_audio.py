import re, os, asyncio, edge_tts
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, 'index.html')
AUDIO = os.path.join(BASE, 'audio')
VOICE = 'zh-HK-HiuGaaiNeural'

# 停顿时长（毫秒）：逗号/顿号短，分号/冒号中，句号/问号/感叹号长
PUNCT = {'，': 320, '、': 300, '；': 430, '：': 430,
         '。': 620, '！': 620, '？': 620, '…': 500}

def to_ssml(text):
    # 按标点切分成“气群”，相邻气群用轻微交替的语速制造自然轻重起伏
    parts = re.split(r'([，、；：。！？…])', text)
    out = []
    k = 0
    for i in range(0, len(parts), 2):
        chunk = parts[i]
        punct = parts[i + 1] if i + 1 < len(parts) else ''
        if not chunk and not punct:
            continue
        rate = '-5%' if (k % 2 == 0) else '-12%'  # 轻微起伏，避免字字匀速
        k += 1
        seg = escape(chunk)
        if punct:
            seg += punct + '<break time="%dms"/>' % PUNCT.get(punct, 350)
        out.append('<prosody rate="%s">%s</prosody>' % (rate, seg))
    return ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-HK">'
            + ''.join(out) + '</speak>')

def extract():
    html = open(HTML, encoding='utf-8').read()
    # 仅 dialogue 数据里含 yue:'...' 字段
    return re.findall(r"yue:'([^']*)'", html)

async def gen_one(text, out):
    ssml = to_ssml(text)
    c = edge_tts.Communicate(ssml, VOICE)
    await c.save(out)

async def main():
    texts = extract()
    print('found', len(texts), 'phrases')
    os.makedirs(AUDIO, exist_ok=True)
    for i, t in enumerate(texts, 1):
        out = os.path.join(AUDIO, '%03d.mp3' % i)
        await gen_one(t, out)
        print('saved', out, '|', t[:20])
    print('ALL DONE')

asyncio.run(main())
