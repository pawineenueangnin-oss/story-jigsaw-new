# Builds Play Store graphics into store-assets/ (not deployed).
import os,glob,shutil
from PIL import Image,ImageDraw,ImageFilter,ImageFont
S='store-assets/';os.makedirs(S+'framed',exist_ok=True)
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-SemiBold.ttf'
KB='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-Bold.ttf' if os.path.exists('/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-Bold.ttf') else K
NAVY=(13,27,43);GOLD=(255,214,120);CREAM=(255,244,220)
CAP={'en':{'01-home':'Six picture stories to explore','02-story':'4 levels, from 2×2 up to 5×5','03-board-2x2':'Very easy 2×2 for little hands','04-hint-4x4':'Gentle hints show where a piece goes','05-result-sticker':'Earn stars and collect stickers','06-storybook':'Read the whole story aloud','07-album-stickers':'Your album of pictures & stickers','08-languages':'Play in 21 languages'},
'th':{'01-home':'นิทานภาพ 6 เรื่องให้ออกผจญภัย','02-story':'4 ระดับ ตั้งแต่ 2×2 ถึง 5×5','03-board-2x2':'ง่ายมาก 2×2 สำหรับเด็กเล็ก','04-hint-4x4':'ตัวช่วยใบ้ชิ้นที่ถูกอย่างนุ่มนวล','05-result-sticker':'สะสมดาวและสติกเกอร์','06-storybook':'อ่านนิทานทั้งเรื่องพร้อมเสียงเล่า','07-album-stickers':'สมุดภาพและสติกเกอร์ของฉัน','08-languages':'เล่นได้ 21 ภาษา'}}
def fit(d,text,font,maxw,size):
    while size>30:
        f=ImageFont.truetype(font,size)
        if d.textlength(text,font=f)<=maxw:return f
        size-=2
    return ImageFont.truetype(font,size)
def framed(src,dst,cap):
    shot=Image.open(src).convert('RGB');W,H=shot.size
    bg=Image.open('branding/cover.jpg').convert('RGB').resize((W,round(W*4/3)) if W/H<0.75 else (round(H*0.75),H)).resize((W,H)).filter(ImageFilter.GaussianBlur(28))
    bg=Image.blend(bg,Image.new('RGB',(W,H),NAVY),0.55)
    band=int(H*0.15);d=ImageDraw.Draw(bg)
    f=fit(d,cap,KB,W*0.86,int(W*0.075))
    tw=d.textlength(cap,font=f);bb=d.textbbox((0,0),cap,font=f);th=bb[3]-bb[1]
    d.text(((W-tw)/2,(band-th)/2-bb[1]+H*0.012),cap,font=f,fill=GOLD,stroke_width=max(2,W//360),stroke_fill=(60,30,10))
    d.line([(W*0.3,band-H*0.005),(W*0.7,band-H*0.005)],fill=GOLD+(255,),width=max(3,W//270))
    m=int(W*0.07);sw=W-2*m;sh=round(H*sw/W)
    if band+sh>H-m*0.6:sh=int(H-band-m*0.6);sw=round(W*sh/H)
    s=shot.resize((sw,sh),Image.LANCZOS);r=int(sw*0.05)
    mask=Image.new('L',(sw,sh),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,sw-1,sh-1),radius=r,fill=255)
    x=(W-sw)//2;y=band+int(m*0.25)
    sh_=Image.new('L',(W,H),0);ImageDraw.Draw(sh_).rounded_rectangle((x,y+12,x+sw,y+sh+12),radius=r,fill=170);bg.paste((0,0,0),(0,0),sh_.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(bg).rounded_rectangle((x-6,y-6,x+sw+5,y+sh+5),radius=r+6,fill=GOLD)
    bg.paste(s,(x,y),mask);bg.save(dst,optimize=True)
for f in ([] if os.environ.get('FG_ONLY') else sorted(glob.glob(S+'raw/*.png'))):
    n=os.path.basename(f);dev,lang,rest=n[:-4].split('-',2)
    framed(f,S+'framed/'+n,CAP[lang][rest])
# feature graphic 1024x500, 24-bit, content centered
c=Image.open('branding/cover.jpg').convert('RGB');W,H=1024,500
s=c.resize((W,round(c.height*W/c.width)),Image.LANCZOS);y0=round(s.height*0.43);fg=s.crop((0,y0,W,y0+H))
ov=Image.new('RGBA',(W,H),(0,0,0,0));o=ImageDraw.Draw(ov)
for y in range(200):o.line([(0,y),(W,y)],fill=(25,15,40,int(170*(1-y/200))))
fg=Image.alpha_composite(fg.convert('RGBA'),ov);d=ImageDraw.Draw(fg)
t='Moonpiece Tales';f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',62);tw=d.textlength(t,font=f)
d.text(((W-tw)/2,14),t,font=f,fill=GOLD,stroke_width=3,stroke_fill=(70,35,10))
t2='Picture-story jigsaw puzzles for kids';f2=ImageFont.truetype(KB,28);tw2=d.textlength(t2,font=f2)
d.text(((W-tw2)/2,86),t2,font=f2,fill=CREAM,stroke_width=2,stroke_fill=(40,20,30))
fg.convert('RGB').save(S+'feature-graphic-1024x500.png',optimize=True);fg.convert('RGB').save(S+'feature-graphic-1024x500.jpg',quality=92)
shutil.copy('branding/play-icon-512.png',S+'app-icon-512.png')
