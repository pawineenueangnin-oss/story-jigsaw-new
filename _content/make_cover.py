# Builds branding/og.jpg (1200x630) from branding/cover.jpg with the title over the sky.
from PIL import Image,ImageDraw,ImageFont,ImageFilter
im=Image.open('branding/cover.jpg').convert('RGB')
W,H=1200,630
s=im.resize((W,round(im.height*W/im.width)),Image.LANCZOS)
y0=630;og=s.crop((0,y0,W,y0+H)).convert('RGBA')
sh=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(sh)
for y in range(230):g.line([(0,y),(W,y)],fill=(30,15,40,int(150*(1-y/230))))
og=Image.alpha_composite(og,sh);d=ImageDraw.Draw(og)
title='Moonpiece Tales'
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',78)
sub=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',32)
tw=d.textlength(title,font=f)
glow=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(glow).text(((W-tw)/2,18),title,font=f,fill=(0,0,0,220))
og=Image.alpha_composite(og,glow.filter(ImageFilter.GaussianBlur(6)));d=ImageDraw.Draw(og)
d.text(((W-tw)/2,18),title,font=f,fill=(255,226,150),stroke_width=2,stroke_fill=(80,40,10))
t2='Picture stories to piece together · 21 languages';sw=d.textlength(t2,font=sub)
d.text(((W-sw)/2,114),t2,font=sub,fill=(255,246,226),stroke_width=2,stroke_fill=(40,20,30))
og.convert('RGB').save('branding/og.jpg',quality=88,optimize=True)
