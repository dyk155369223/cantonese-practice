import asyncio, edge_tts, os

OUT = "audio"
os.makedirs(OUT, exist_ok=True)

# 纯文本生成（不要 SSML，避免标点被读出来、各句雷同）
texts = {
    "001": "早晨！",
    "002": "請問辦咩業務？",
    "003": "請坐低，",
    "004": "慢慢講。",
}

VOICE = "zh-HK-HiuGaaiNeural"
RATE = "-10%"  # 略放慢，更贴近日常聊天

async def gen(num, text):
    comm = edge_tts.Communicate(text, VOICE, rate=RATE)
    path = os.path.join(OUT, f"{num}.mp3")
    await comm.save(path)
    sz = os.path.getsize(path)
    print(f"{num}: {text} -> {path} ({sz} bytes)")

async def main():
    for num, text in texts.items():
        await gen(num, text)

if __name__ == "__main__":
    asyncio.run(main())
    print("DONE")
