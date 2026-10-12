# -*- coding: utf-8 -*-
"""국기 그림(SVG) 3차 추가:  python3 tools/make_flags_extra2.py"""
import math, pathlib, importlib.util
spec=importlib.util.spec_from_file_location("f1", pathlib.Path(__file__).parent/"make_flags_extra.py")
W,H=300,200
OUT=pathlib.Path(__file__).resolve().parent.parent/"img"/"flags"
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{b}</svg>'
def hstr(*c,hs=None):
  hs=hs or [H/len(c)]*len(c); y=0; o=''
  for col,h in zip(c,hs): o+=f'<rect y="{y:.2f}" width="{W}" height="{h+0.5:.2f}" fill="{col}"/>'; y+=h
  return o
def vstr(*c):
  n=len(c); return ''.join(f'<rect x="{W*i/n:.2f}" width="{W/n+0.5:.2f}" height="{H}" fill="{x}"/>' for i,x in enumerate(c))
def star(cx,cy,r,col,rot=-90,outline=None):
  pts=[]
  for i in range(10):
    rr=r if i%2==0 else r*0.382; a=math.radians(rot+i*36); pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
  if outline: return f'<polygon points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{outline}"/>'
  return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'
def crescent(cx,cy,r,col,bg,dx):
  return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}"/><circle cx="{cx+dx}" cy="{cy}" r="{r*0.82:.1f}" fill="{bg}"/>'
F={}
F['ml']=vstr('#14B53A','#FCD116','#CE1126')
F['ye']=hstr('#CE1126','#fff','#000')
F['sl']=hstr('#1EB53A','#fff','#0072C6')
F['gm']=hstr('#CE1126','#fff','#0C1C8C','#fff','#3A7728',hs=[66,8,52,8,66])
F['mu']=hstr('#EA2839','#1A206D','#FFD500','#00A551')
F['bo']=hstr('#D52B1E','#F9E300','#007934')
F['am']=hstr('#D90012','#0033A0','#F2A800')
F['kw']=hstr('#007A3D','#fff','#CE1126')+'<polygon points="0,0 75,66.7 75,133.3 0,200" fill="#000"/>'
F['sg']=hstr('#EF3340','#fff')+crescent(55,50,30,'#fff','#EF3340',11)+''.join(star(85+18*math.cos(math.radians(a)),50+18*math.sin(math.radians(a)),6,'#fff') for a in (-90,-18,54,126,198))
F['tw']=f'<rect width="{W}" height="{H}" fill="#FE0000"/><rect width="150" height="100" fill="#000095"/>'+ \
  ''.join(f'<polygon points="{75+40*math.cos(math.radians(a)):.1f},{50+40*math.sin(math.radians(a)):.1f} {75+18*math.cos(math.radians(a+15)):.1f},{50+18*math.sin(math.radians(a+15)):.1f} {75+18*math.cos(math.radians(a-15)):.1f},{50+18*math.sin(math.radians(a-15)):.1f}" fill="#fff"/>' for a in range(0,360,30))+ \
  '<circle cx="75" cy="50" r="20" fill="#fff"/><circle cx="75" cy="50" r="17" fill="#000095"/><circle cx="75" cy="50" r="15" fill="#fff"/>'
F['cu']=''.join(f'<rect y="{H*i/5:.1f}" width="{W}" height="{H/5+0.4:.1f}" fill="{"#002A8F" if i%2==0 else "#fff"}"/>' for i in range(5))+'<polygon points="0,0 173,100 0,200" fill="#CF142B"/>'+star(58,100,26,'#fff')
F['pa']=(f'<rect width="{W}" height="{H}" fill="#fff"/><rect x="150" width="150" height="100" fill="#DA121A"/><rect y="100" width="150" height="100" fill="#072357"/>'
  +star(75,50,22,'#072357')+star(225,150,22,'#DA121A'))
F['bj']=f'<rect width="{W}" height="100" fill="#FCD116"/><rect y="100" width="{W}" height="100" fill="#E8112D"/><rect width="120" height="200" fill="#008751"/>'
F['mg']=f'<rect width="{W}" height="100" fill="#FC3D32"/><rect y="100" width="{W}" height="100" fill="#007E3A"/><rect width="100" height="200" fill="#fff"/>'
F['bf']=hstr('#EF2B2D','#009E49')+star(150,100,28,'#FCD116')
F['bs']=hstr('#00778B','#FFC72C','#00778B')+'<polygon points="0,0 130,100 0,200" fill="#000"/>'
F['sr']=hstr('#377E3F','#fff','#B40A2D','#fff','#377E3F',hs=[40,20,80,20,40])+star(150,100,32,'#ECC81D')
F['pk']=f'<rect width="{W}" height="{H}" fill="#01411C"/><rect width="75" height="200" fill="#fff"/>'+crescent(195,100,52,'#fff','#01411C',14)+star(222,78,16,'#fff',rot=-50)
F['dz']=f'<rect width="150" height="200" fill="#006233"/><rect x="150" width="150" height="200" fill="#fff"/>'+crescent(150,100,50,'#D21034','#fff',13)+star(170,100,22,'#D21034',rot=0)
F['tn']=f'<rect width="{W}" height="{H}" fill="#E70013"/><circle cx="150" cy="100" r="50" fill="#fff"/>'+crescent(150,100,38,'#E70013','#fff',10)+star(160,100,18,'#E70013',rot=0)
F['ma']=f'<rect width="{W}" height="{H}" fill="#C1272D"/>'+star(150,100,45,'#006233',outline=6)
for k,b in F.items(): (OUT/f"{k}.svg").write_text(svg(b),encoding="utf-8")
print(len(F))
