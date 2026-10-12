# -*- coding: utf-8 -*-
"""국기 그림(SVG) 추가분 만들기:  python3 tools/make_flags_extra.py  → img/flags/*.svg"""
import math, pathlib
W,H=300,200
OUT=pathlib.Path(__file__).resolve().parent.parent/"img"/"flags"
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{b}</svg>'
def hstr(*c,hs=None):
  hs=hs or [H/len(c)]*len(c); y=0; o=''
  for col,h in zip(c,hs): o+=f'<rect y="{y:.2f}" width="{W}" height="{h+0.5:.2f}" fill="{col}"/>'; y+=h
  return o
def vstr(*c):
  n=len(c); return ''.join(f'<rect x="{W*i/n:.2f}" width="{W/n+0.5:.2f}" height="{H}" fill="{x}"/>' for i,x in enumerate(c))
def star(cx,cy,r,col,rot=-90):
  pts=[]
  for i in range(10):
    rr=r if i%2==0 else r*0.382; a=math.radians(rot+i*36); pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
  return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
def trigram(cx,cy,pattern):
  ang=math.degrees(math.atan2(cy-100,cx-150))+90; o=f'<g transform="rotate({ang:.2f} {cx} {cy})">'
  for i,solid in enumerate(pattern):
    y=cy-16+i*12
    if solid: o+=f'<rect x="{cx-24}" y="{y}" width="48" height="8" fill="#000"/>'
    else: o+=f'<rect x="{cx-24}" y="{y}" width="21" height="8" fill="#000"/><rect x="{cx+3}" y="{y}" width="21" height="8" fill="#000"/>'
  return o+'</g>'
F={}
F['kr']=(f'<rect width="{W}" height="{H}" fill="#fff"/><g transform="rotate(33.69 150 100)">'
  '<path d="M100,100 A50,50 0 0 1 200,100 Z" fill="#CD2E3A"/><path d="M100,100 A50,50 0 0 0 200,100 Z" fill="#0047A0"/>'
  '<circle cx="125" cy="100" r="25" fill="#CD2E3A"/><circle cx="175" cy="100" r="25" fill="#0047A0"/></g>'
  +trigram(62,41,[1,1,1])+trigram(238,159,[0,0,0])+trigram(238,41,[0,1,0])+trigram(62,159,[1,0,1]))
F['us']=''.join(f'<rect y="{H*i/13:.2f}" width="{W}" height="{H/13+0.4:.2f}" fill="{"#B22234" if i%2==0 else "#fff"}"/>' for i in range(13))+ \
  f'<rect width="120" height="{H*7/13:.2f}" fill="#3C3B6E"/>'+''.join(f'<circle cx="{10+j*20+(10 if i%2 else 0)}" cy="{9+i*11.5:.1f}" r="2.6" fill="#fff"/>' for i in range(9) for j in range(6 if i%2==0 else 5))
F['gb']=(f'<rect width="{W}" height="{H}" fill="#012169"/><path d="M0,0L300,200M300,0L0,200" stroke="#fff" stroke-width="40"/>'
  '<path d="M0,0L300,200M300,0L0,200" stroke="#C8102E" stroke-width="13"/>'
  '<rect x="125" width="50" height="200" fill="#fff"/><rect y="75" width="300" height="50" fill="#fff"/>'
  '<rect x="135" width="30" height="200" fill="#C8102E"/><rect y="85" width="300" height="30" fill="#C8102E"/>')
F['cn']=f'<rect width="{W}" height="{H}" fill="#EE1C25"/>'+star(50,50,30,'#FFFF00')+''.join(star(x,y,10,'#FFFF00',rot=r) for x,y,r in [(100,20,-60),(120,40,-80),(120,70,-100),(100,90,-120)])
F['br']=(f'<rect width="{W}" height="{H}" fill="#009C3B"/><polygon points="150,22 278,100 150,178 22,100" fill="#FFDF00"/>'
  '<circle cx="150" cy="100" r="46" fill="#002776"/><path d="M106,90 Q150,78 194,108" stroke="#fff" stroke-width="7" fill="none"/>')
F['ar']=hstr('#74ACDF','#fff','#74ACDF')+'<circle cx="150" cy="100" r="17" fill="#F6B40E"/>'
F['cz']=hstr('#fff','#D7141A')+'<polygon points="0,0 150,100 0,200" fill="#11457E"/>'
F['ph']=hstr('#0038A8','#CE1126')+'<polygon points="0,0 173,100 0,200" fill="#fff"/><circle cx="58" cy="100" r="18" fill="#FCD116"/>'+''.join(star(x,y,7,'#FCD116') for x,y in [(14,18),(14,182),(150,100)][:2])+star(148,100,7,'#FCD116')
F['il']=(f'<rect width="{W}" height="{H}" fill="#fff"/><rect y="20" width="300" height="30" fill="#0038B8"/><rect y="150" width="300" height="30" fill="#0038B8"/>'
  '<polygon points="150,62 183,119 117,119" fill="none" stroke="#0038B8" stroke-width="6"/><polygon points="150,138 183,81 117,81" fill="none" stroke="#0038B8" stroke-width="6"/>')
F['pe']=vstr('#D91023','#fff','#D91023')
F['ci']=vstr('#F77F00','#fff','#009E60')
F['gh']=hstr('#CE1126','#FCD116','#006B3F')+star(150,102,30,'#000')
F['cm']=vstr('#007A5E','#CE1126','#FCD116')+star(150,102,22,'#FCD116')
F['sn']=vstr('#00853F','#FDEF42','#E31B23')+star(150,102,24,'#00853F')
F['so']=f'<rect width="{W}" height="{H}" fill="#4189DD"/>'+star(150,103,44,'#fff')
F['cl']=hstr('#fff','#D52B1E')+'<rect width="100" height="100" fill="#0039A6"/>'+star(50,52,24,'#fff')
F['lv']=hstr('#9E3039','#fff','#9E3039',hs=[80,40,80])
F['bg']=hstr('#fff','#00966E','#D62612')
F['la']=hstr('#CE1126','#002868','#CE1126',hs=[50,100,50])+'<circle cx="150" cy="100" r="40" fill="#fff"/>'
F['pw']=f'<rect width="{W}" height="{H}" fill="#4AADD6"/><circle cx="135" cy="100" r="50" fill="#FFDE00"/>'
F['is']=(f'<rect width="{W}" height="{H}" fill="#02529C"/><rect x="81" width="37.5" height="200" fill="#fff"/><rect y="80" width="300" height="40" fill="#fff"/>'
  '<rect x="88.5" width="22.5" height="200" fill="#DC1E35"/><rect y="87.5" width="300" height="25" fill="#DC1E35"/>')
F['ae']=hstr('#00732F','#fff','#000')+'<rect width="75" height="200" fill="#FF0000"/>'
F['bw']=f'<rect width="{W}" height="{H}" fill="#75AADB"/><rect y="74" width="300" height="52" fill="#fff"/><rect y="81" width="300" height="38" fill="#000"/>'
F['ga']=hstr('#009E60','#FCD116','#3A75C4')
F['jm']=(f'<rect width="{W}" height="{H}" fill="#000"/><polygon points="0,0 300,0 150,100" fill="#009B3A"/><polygon points="0,200 300,200 150,100" fill="#009B3A"/>'
  '<path d="M0,0L300,200M300,0L0,200" stroke="#FED100" stroke-width="28"/>')
F['mm']=hstr('#FECB00','#34B233','#EA2839')+star(150,108,58,'#fff')
for k,b in F.items(): (OUT/f"{k}.svg").write_text(svg(b),encoding="utf-8")
print(len(F))
