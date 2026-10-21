# Builds all app icons from the chosen 1024 storybook icon (_content/icon-source.jpg).
from PIL import Image
src=Image.open('_content/icon-source.jpg').convert('RGB')
from PIL import ImageDraw,ImageFilter
# inner art square is ~50..974 with ~184px rounded corners: crop just inside the corner curves
I=100; art=src.crop((I,I,1024-I,1024-I))
def sq(n):return art.resize((n,n),Image.LANCZOS)
sq(512).save('branding/icon-512-v2.png',optimize=True)
sq(512).convert('RGBA').save('branding/play-icon-512.png',optimize=True)  # Play Store: 512x512 32-bit PNG
sq(192).save('branding/icon-192-v2.png',optimize=True)
sq(180).save('branding/apple-touch-icon-v2.png',optimize=True)
sq(32).save('branding/favicon-32-v2.png',optimize=True)
sq(16).save('branding/favicon-16-v2.png',optimize=True)
sq(256).save('branding/story-icon-v2.png',optimize=True); sq(256).save('branding/story-icon-v2.webp',quality=88)
sq(64).save('branding/favicon-v2.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
# maskable: art inside the 80% safe zone on navy
from PIL import ImageStat; top=art.crop((0,0,art.width,40)); col=tuple(int(v) for v in ImageStat.Stat(top).mean); m=Image.new('RGB',(512,512),col); a=art.resize((372,372),Image.LANCZOS); fm=Image.new("L",(372,372),0); ImageDraw.Draw(fm).rounded_rectangle((0,0,371,371),radius=90,fill=255); m.paste(a,(70,70),fm.filter(ImageFilter.GaussianBlur(10))); m.save('branding/icon-maskable-512-v2.png',optimize=True)
