# Meme-caption-over-screen-recording scene with fog/blur middle part (first used: "I bought a Claude subscription once / everything after is a blur").
# Input: frames from record_site.py. Output JPEG frames -> ffmpeg (see bottom of file docs in TEAM.md).
import json, math, random, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='/tmp/claude_blur'; F=D+'/frames'
times=json.load(open(F+'/times.json'))
W,H=1080,1920; FPS=30; TOTAL=16.6
BOLD='/usr/share/fonts/opentype/inter/Inter-Bold.otf'
if not os.path.exists(BOLD):
    import glob; BOLD=[f for f in glob.glob('/usr/share/fonts/**/Inter*Bold*',recursive=True)][0]
EXB=BOLD.replace('Bold','ExtraBold') if os.path.exists(BOLD.replace('Bold','ExtraBold')) else BOLD
def font(s,f=BOLD): return ImageFont.truetype(f,s)
def src(t):
    i=min(range(len(times)),key=lambda k:abs(times[k]-t)) if t<times[-1] else len(times)-1
    return Image.open(f'{F}/f{i:05d}.jpg').convert('RGB').resize((W,H))
random.seed(7)
# fog layer: big soft blobs
fog=Image.new('L',(W*2,H*2),0); d=ImageDraw.Draw(fog)
for _ in range(38):
    x,y=random.randint(0,W*2),random.randint(0,H*2); r=random.randint(180,520)
    d.ellipse([x-r,y-r,x+r,y+r],fill=random.randint(60,150))
fog=fog.filter(ImageFilter.GaussianBlur(120))
def caption(img,text,y,size=66,alpha=1.0):
    f=font(size); lines=text.split('\n'); dd=ImageDraw.Draw(img)
    lh=size*1.22; boxes=[]
    for k,l in enumerate(lines):
        w=dd.textlength(l,font=f); boxes.append((l,w,y+k*lh))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    for l,w,yy in boxes:
        x=(W-w)/2; od.rounded_rectangle([x-30,yy-14,x+w+30,yy+lh-4],22,fill=(255,255,255,int(255*alpha)))
    for l,w,yy in boxes:
        od.text(((W-w)/2,yy),l,font=f,fill=(10,12,20,int(255*alpha)))
    img.paste(ov,(0,0),ov)
def smooth(a,b,t): x=max(0,min(1,(t-a)/(b-a))); return x*x*(3-2*x)
def endcard(t):
    img=Image.new('RGB',(W,H),(7,11,24)); dd=ImageDraw.Draw(img)
    g=Image.new('L',(W,H),0); gd=ImageDraw.Draw(g); gd.ellipse([140,500,940,1300],fill=90); g=g.filter(ImageFilter.GaussianBlur(160))
    img.paste(Image.new('RGB',(W,H),(34,211,238)),(0,0),g)
    def c(txt,y,s,col,f=EXB):
        ff=font(s,f); w=dd.textlength(txt,font=ff); dd.text(((W-w)/2,y),txt,font=ff,fill=col)
    c('Watch them work',620,84,(255,255,255))
    c('live at Mission Control',730,56,(167,139,250),BOLD)
    dd.rounded_rectangle([170,930,910,1070],36,fill=(34,211,238))
    c('Free Starter 10  →  link in bio',968,50,(7,11,24))
    c('@aiedge.prompts',1180,54,(255,255,255),BOLD)
    return img
os.makedirs(D+'/out',exist_ok=True)
n=int(TOTAL*FPS)
for i in range(n):
    t=i/FPS
    if t<14.6:
        img=src(t)
        fogamt=smooth(2.3,3.1,t)*(1-smooth(9.4,10.4,t))
        if fogamt>0:
            r=fogamt*(5.5+2.5*math.sin(t*2.1))
            img=img.filter(ImageFilter.GaussianBlur(r))
            img=ImageEnhance.Color(img).enhance(1-0.3*fogamt)
            z=1+0.05*fogamt*math.sin(t*0.9)
            if z>1.001:
                cw,ch=int(W/z),int(H/z); img=img.crop(((W-cw)//2,(H-ch)//2,(W-cw)//2+cw,(H-ch)//2+ch)).resize((W,H))
            ox=int(300+220*math.sin(t*0.35)); oy=int(400+300*math.cos(t*0.27))
            fl=fog.crop((ox,oy,ox+W,oy+H)).point(lambda v:int(v*fogamt*0.75))
            img.paste(Image.new('RGB',(W,H),(225,230,240)),(0,0),fl)
        if t<3.1: caption(img,'I bought a Claude\nsubscription once',330,alpha=1-smooth(2.8,3.1,t))
        elif t<9.6: caption(img,'and everything after\nthat is a blur',860,alpha=smooth(3.1,3.5,t)*(1-smooth(9.3,9.6,t)))
        elif t>=10.2: caption(img,'now 7 AI agents\nrun my Instagram',1470,alpha=smooth(10.2,10.5,t)*(1-smooth(14.3,14.6,t)))
        if t>14.2:  # crossfade to end
            img=Image.blend(img,endcard(t),smooth(14.2,14.6,t))
    else:
        img=endcard(t)
    img.save(f'{D}/out/o{i:05d}.jpg',quality=93)
print('frames',n)
