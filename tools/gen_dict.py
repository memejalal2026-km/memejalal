# -*- coding: utf-8 -*-
# 밈 사전 페이지 생성: python3 tools/gen_dict.py  (index.html의 문제 + tools/question_db.csv의 해설 사용)
import csv, re, json, html, os
from urllib.parse import urlparse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.reader(open(os.path.join(ROOT,"tools","question_db.csv"),encoding="utf-8-sig")))[1:]
E = html.escape
FOOT = '''<footer class="site-foot">
  <a href="/about.html">소개</a>·<a href="/dict/">밈 사전</a>·<a href="/privacy.html">개인정보처리방침</a>·<a href="/contact.html">문의</a><br>
  문의: memejalal2026@gmail.com · ⓒ 2026 밈잘알?
</footer>'''
CATS = [
 ("신조어","sinjoeo","신조어 모음","요즘 온라인에서 쓰이는 줄임말, 합성어, 감탄사를 모았어요. 뜻만 알면 대화나 댓글을 이해하기 쉬워져요. 예전부터 쓰던 말과 최근에 생긴 말이 섞여 있어서, 처음 보는 말이라도 어떻게 만들어졌는지 함께 설명해 두었어요."),
 ("유래","yurae","밈 유래 모음","밈은 어디서 시작됐느냐에 따라 뜻이 달라지기도 해요. 방송, 유튜브, 커뮤니티, 노래 등 밈이 처음 퍼진 곳과 사건을 정리했어요."),
 ("고전밈","gojeonme","고전 밈 모음","시간이 지나도 계속 쓰이는 인터넷 고전 밈을 모았어요. 지금 보면 낯설 수 있지만 여전히 댓글과 짤에서 자주 만나게 되는 표현들이에요."),
 ("이미지밈","imageme","이미지·짤 밈 모음","짤과 이미지에서 시작되어 하나의 표현 방식이 된 밈을 글로 설명했어요. 어떤 상황에 쓰는지, 어떤 형식으로 만드는지 알면 따라 만들기도 쉬워요."),
 ("챌린지","challenge","챌린지 모음","짧은 영상 플랫폼에서 유행한 챌린지와 따라 하기 문화를 정리했어요. 누가 어떤 영상에서 시작했는지, 어떻게 퍼졌는지 살펴보세요."),
]
data = {c[0]:[] for c in CATS}
for r in rows:
    id_,lv,cat,q,o1,o2,o3,o4,a,ex,src,conf,img,status,memo = (r+[""]*15)[:15]
    if img or cat not in data or not ex: continue
    ans = [o1,o2,o3,o4][int(a)-1]
    data[cat].append((id_,q,ans,ex,src))

def page(title, desc, body, canon):
    return f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} | 밈잘알?</title>
<meta name="description" content="{E(desc)}">
<link rel="icon" type="image/png" href="/icon-192.png">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/galmuri@latest/dist/galmuri.css">
<link rel="stylesheet" href="/site.css">
</head><body><div class="page">
<div class="top"><a class="brand" href="/">밈잘알?</a><a class="play" href="/">게임하기 ▶</a></div>
{body}
</div>{FOOT}</body></html>'''

def nav(cur):
    s = '<div class="nav"><a href="/dict/"%s>전체</a>' % (' class="on"' if cur=="" else "")
    for c in CATS: s += '<a href="/dict/%s.html"%s>%s</a>' % (c[1], ' class="on"' if cur==c[1] else "", c[0])
    return s + "</div>"

total = sum(len(v) for v in data.values())
idx = f'''<div class="box"><h1>밈잘알? 밈 사전</h1>
<p>밈잘알? 게임에 나오는 밈과 신조어의 뜻, 유래, 쓰임을 한곳에 정리한 사전이에요. 현재 {total}개의 항목이 있고, 새 문제가 추가될 때마다 함께 늘어나요.</p>
<p class="sub">설명은 공개된 기사, 블로그, 커뮤니티 글을 참고해 직접 다시 쓴 것이며, 항목마다 참고한 곳을 적어 두었어요. 밈은 빠르게 변하므로 뜻이 달라지거나 틀린 부분이 있으면 <a href="/contact.html">문의</a>로 알려 주세요.</p>
{nav("")}</div>'''
for c in CATS:
    idx += f'<div class="box"><h2><a href="/dict/{c[1]}.html">{E(c[2])}</a> <span class="sub">({len(data[c[0]])}개)</span></h2><p>{E(c[3])}</p></div>'
os.makedirs(os.path.join(ROOT,"dict"),exist_ok=True)
open(os.path.join(ROOT,"dict","index.html"),"w",encoding="utf-8").write(page("밈 사전 - 밈과 신조어 뜻 모음", f"밈과 신조어 {total}개의 뜻과 유래를 정리한 밈잘알? 밈 사전", idx, ""))
for cat,slug,title,intro in CATS:
    b = f'<div class="box"><h1>{E(title)}</h1><p>{E(intro)}</p><p class="sub">총 {len(data[cat])}개 항목 · 아래 문제의 정답은 <b>정답</b> 칸에 있어요. 게임에서 먼저 풀어 보고 싶다면 <a href="/">게임하기</a>를 눌러 주세요.</p>{nav(slug)}'
    for id_,q,ans,ex,src in data[cat]:
        s = ""
        if src.startswith("http"):
            s = f'<p class="src">참고: <a href="{E(src)}" target="_blank" rel="noopener nofollow">{E(urlparse(src).netloc)}</a></p>'
        b += f'<div class="entry"><h3>{E(q)}</h3><div class="ans"><b>정답</b> {E(ans)}</div><p>{E(ex)}</p>{s}</div>'
    b += "</div>"
    open(os.path.join(ROOT,"dict",slug+".html"),"w",encoding="utf-8").write(page(title, intro[:90], b, slug))
print("OK", {c[0]:len(data[c[0]]) for c in CATS}, total)
