# -*- coding: utf-8 -*-
# 직접 만든 '상황 카드' 이미지 생성 (이모지 + 짧은 설명). 방송 캡처/타인 이미지는 쓰지 않아요.
# 사용: python3 tools/make_cards.py   → img/cards/*.png
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "cards"); os.makedirs(OUT, exist_ok=True)
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
TXT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
INK = (43, 29, 110)
W, H = 640, 360
def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    bb = im.getbbox(); im = im.crop(bb) if bb else im
    r = size / max(im.size); return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
def _segments(caption):
    segs, buf, blank = [], "", False
    for ch in caption:
        if ch == "{": 
            if buf: segs.append((buf, False))
            buf, blank = "", True
        elif ch == "}":
            segs.append((buf, True)); buf, blank = "", False
        else: buf += ch
    if buf: segs.append((buf, False))
    return segs
def _width(d, segs, f):
    w = 0
    for t, b in segs: w += max(84, int(len(t) * 22 + 28)) if b else d.textlength(t, font=f)
    return w
def _draw_line(d, segs, f, y):
    x = (W - _width(d, segs, f)) / 2
    for t, b in segs:
        if b:
            bw = max(84, int(len(t) * 22 + 28))
            d.rounded_rectangle([x+2, y+2, x+bw-2, y+44], radius=8, fill=INK)
            qf = ImageFont.truetype(TXT, 28); q = "?" * max(2, min(5, len(t)))
            d.text((x + (bw - d.textlength(q, font=qf)) / 2, y+4), q, font=qf, fill=(255, 210, 63))
            x += bw
        else:
            d.text((x, y), t, font=f, fill=INK); x += d.textlength(t, font=f)
def _split2(caption):
    if "\n" in caption: return caption.split("\n")
    # 너무 길면 공백 기준으로 두 줄 (마스크 안에서는 자르지 않음)
    plain = caption.replace("{", "").replace("}", "")
    if len(plain) <= 20: return [caption]
    best, depth, cuts = None, 0, []
    for i, ch in enumerate(caption):
        if ch == "{": depth += 1
        elif ch == "}": depth -= 1
        elif ch == " " and depth == 0: cuts.append(i)
    if not cuts: return [caption]
    mid = len(caption) / 2; i = min(cuts, key=lambda c: abs(c - mid))
    return [caption[:i], caption[i+1:]]
def card(slug, emojis, caption, bg):
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im)
    for x in range(0, W, 40):                      # 은은한 도트 무늬
        for y in range(0, H, 40):
            d.ellipse([x+18, y+18, x+22, y+22], fill=tuple(min(255, c+14) for c in bg))
    lines = _split2(caption); n3 = len(lines) >= 3
    n = len(emojis); size = (95 if n3 else 120) if n <= 3 else 100; gap = 22
    imgs = [emoji_img(e, size) for e in emojis]
    total = sum(i.width for i in imgs) + gap * (n - 1); x = (W - total) // 2
    for i in imgs:
        im.paste(i, (x, (30 if n3 else 50) + (size - i.height) // 2), i); x += i.width + gap
    f = ImageFont.truetype(TXT, 32 if len(lines) == 1 else (28 if len(lines) == 2 else 24))
    bx0, bx1, by0, by1 = 24, W - 24, (150 if n3 else 215), (340 if n3 else 335)
    d.rounded_rectangle([bx0+5, by0+5, bx1+5, by1+5], radius=14, fill=INK)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=14, fill=(255, 255, 255), outline=INK, width=5)
    segs_lines = [_segments(l) for l in lines]
    if len(lines) == 1: _draw_line(d, segs_lines[0], f, by0 + 36)
    else:
        step = 50 if len(lines) == 2 else 52
        for k, sg in enumerate(segs_lines): _draw_line(d, sg, f, by0 + (16 if len(lines) == 2 else 18) + k * step)
    im.save(os.path.join(OUT, slug + ".png"), optimize=True)
CARDS = [
 ("godsaeng", ["🌅", "⏰", "📚", "💪"], "새벽 기상 · 독서 · 운동 완료!", (255, 233, 163)),
 ("ounwan",   ["🏋️", "😤", "📸"],        "운동 끝! 인증샷 찰칵", (190, 232, 255)),
 ("sohwakhaeng", ["☕", "🍰", "🌤️"],     "퇴근길 케이크 한 조각", (255, 214, 224)),
 ("godseongbi", ["🛒", "💰", "⭐"],       "5천 원인데 품질 최고!", (206, 240, 205)),
 ("eokkka",   ["😡", "👆", "💢"],         "잘했는데도 억지로 트집 잡기", (226, 214, 255)),
]
CARDS += [
 ("m107", ["😎","💸"], "저도 {재벌가}에서 태어났으면 이런 거 안 해요", (255,233,163)),
 ("m108", ["🤪","🎉"], "{엉망으로} 살아야 해! 인생은 한 번이야!", (190,232,255)),
 ("m109", ["😩","🥱"], "그렇지 않아도 {피곤한데}", (255,214,224)),
 ("m110", ["🙃","💦"], "열심히는 하지만 {노력}은 안 한다", (206,240,205)),
 ("m111", ["😴","💤"], "잠을 자도 {피로}가 안 풀리냐", (226,214,255)),
 ("m112", ["🧗","⛰️"], "인생이 어려운 {난관}이 이것만 있겠어?", (255,233,163)),
 ("m113", ["⏰","😅"], "늦었다고 생각할 때가 {진짜} 너무 늦었다", (190,232,255)),
 ("m114", ["💍","🕊️"], "죽음과 {결혼}은 뒤로 미룰수록 좋다", (255,214,224)),
 ("m115", ["🎮","🛋️"], "꿈은 없고요 그냥 {놀고} 싶습니다", (206,240,205)),
 ("m116", ["😵","💤"], "잠을 자도 피로가 안 풀리냐", (226,214,255)),
 ("m117", ["👨","👧"], "민서 아빠", (255,233,163)),
 ("m118", ["⏰","🙄"], "늦었다고 생각할 때가 진짜 너무 늦었다", (190,232,255)),
 ("m119", ["🍦","🎤"], "박성웅의 {바밤바} 삼행시", (255,214,224)),
 ("m120", ["🍦","✨"], "바(밤바)\n밤({맛이 나는})\n바(밤바)", (206,240,205)),
 ("m121", ["😳","👀"], "형이 왜 {거기서} 나와…?", (226,214,255)),
 ("m122", ["😳","❗"], "형이 왜 거기서 나와…?", (255,233,163)),
 ("m123", ["🎤","🔥"], "그리고 그의 손에 쥐어지는 {합격 목걸이}", (190,232,255)),
 ("m124", ["😮","👏"], "무대를 {뒤집어} 놓으셨다", (255,214,224)),
 ("m125", ["😖","🙈"], "아 안돼!", (206,240,205)),
 ("m126", ["😖","🙅"], "아 {안돼}!", (226,214,255)),
]
if __name__ == "__main__":
    for c in CARDS: card(*c)
    print("OK", len(CARDS))
