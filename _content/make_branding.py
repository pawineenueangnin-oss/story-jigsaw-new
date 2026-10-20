# Builds icons + link-preview image from our own story art. Title comes from config.js.
import re
from PIL import Image, ImageDraw, ImageFilter, ImageFont
title=re.search(r"title:\s*'([^']+)'",open('config.js').read()).group(1)
FS=['lantern-art','moon-turtle-art','rice-pot-art','kite-art','seasons-art','snow-fox-art']
def rounded(im,r):
    m=Image.new('L',im.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,im.size[0]-1,im.size[1]-1),r,fill=255)
    o=Image.new('RGBA',im.size,(0,0,0,0));o.paste(im,(0,0),m);return o
src=Image.open('lantern-art/chapter-1.webp').convert('RGB')
sq=src.crop((0,430,540,970)).resize((1024,1024),Image.LANCZOS)
# full-bleed (maskable / apple) and rounded with gold frame (favicon)
sq.resize((512,512),Image.LANCZOS).save('branding/icon-512.png')
sq.resize((192,192),Image.LANCZOS).save('branding/icon-192.png')
sq.resize((180,180),Image.LANCZOS).save('branding/apple-touch-icon.png')
fr=Image.new('RGBA',(1024,1024),(0,0,0,0));d=ImageDraw.Draw(fr)
d.rounded_rectangle((0,0,1023,1023),220,fill=(240,199,94,255))
fr.alpha_composite(rounded(sq.resize((944,944),Image.LANCZOS),180),(40,40))
fr.resize((256,256),Image.LANCZOS).save('branding/story-icon.png')
fr.resize((256,256),Image.LANCZOS).save('branding/story-icon.webp',quality=90)
fr.resize((64,64),Image.LANCZOS).save('branding/favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
fr.resize((32,32),Image.LANCZOS).save('branding/favicon-32.png')
# og 1200x630: six covers fanned on a warm background + title
W,H=1200,630
bg=Image.open('lantern-art/chapter-1.webp').convert('RGB').resize((1200,1600)).crop((0,300,1200,930)).filter(ImageFilter.GaussianBlur(18))
bg=Image.blend(bg,Image.new('RGB',(W,H),(30,20,10)),0.45).convert('RGBA')
cw,ch=176,235
for i,f in enumerate(FS):
    c=rounded(Image.open(f+'/chapter-1.webp').convert('RGB').resize((cw,ch),Image.LANCZOS),18)
    sh=Image.new('RGBA',(cw+40,ch+40),(0,0,0,0));ImageDraw.Draw(sh).rounded_rectangle((20,24,cw+20,ch+24),18,fill=(0,0,0,140));sh=sh.filter(ImageFilter.GaussianBlur(9))
    x=48+i*(cw+14);y=330
    bg.alpha_composite(sh,(x-20,y-20));bg.alpha_composite(c,(x,y))
d=ImageDraw.Draw(bg)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',84)
sub=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',34)
tw=d.textlength(title,font=font);d.text(((W-tw)/2+3,78),title,font=font,fill=(0,0,0,170));d.text(((W-tw)/2,74),title,font=font,fill=(255,226,150))
s='Picture stories to piece together · 21 languages';sw=d.textlength(s,font=sub);d.text(((W-sw)/2,190),s,font=sub,fill=(255,244,220))
bg.convert('RGB').save('branding/og.jpg',quality=88)
# loader slideshow frames (smaller webp)
for i,f in enumerate(FS):
    Image.open(f+'/chapter-1.webp').convert('RGB').resize((648,864),Image.LANCZOS).save(f'branding/loader-{i+1}.webp',quality=78)
print('ok',title)
