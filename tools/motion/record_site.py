# Records the Mission Control site (served locally: python3 -m http.server 8765 from repo root) as a 1080x1920 screencast.
# Edit the `seg` list = scroll timeline [start_ms,end_ms,y_from,y_to]. Frames + times.json go to /tmp/rec_frames.
import base64, time, json
from playwright.sync_api import sync_playwright
out='/tmp/rec_frames'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome')
    pg=b.new_page(viewport={'width':540,'height':960},device_scale_factor=2)
    pg.goto('http://localhost:8765/hq/'); pg.wait_for_timeout(2500)
    team=pg.evaluate("(()=>{const h=[...document.querySelectorAll('h2,h3,div')].find(e=>e.innerText&&e.innerText.trim()==='THE TEAM');return h?h.getBoundingClientRect().top+scrollY-30:900})()")
    cdp=pg.context.new_cdp_session(pg)
    frames=[]
    def onf(e):
        frames.append((time.time(),e['data'])); cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':1080,'maxHeight':1920,'everyNthFrame':1})
    t0=time.time()
    # keep page repainting so idle frames still arrive
    pg.evaluate("""(team)=>{window._t0=performance.now();
      const seg=[[0,2500,0,0],[2500,9000,0,3300],[9000,10000,3300,team],[10000,14500,team,team]];
      const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
      function f(now){const t=now-window._t0;let y=team;
        for(const [a,b,y0,y1] of seg){if(t>=a&&t<b){y=y0+(y1-y0)*ease((t-a)/(b-a));break}}
        scrollTo(0,y); document.body.style.outline=(Math.floor(t/33)%2?'0':'0.01px')+' solid transparent';
        if(t<14600)requestAnimationFrame(f)} requestAnimationFrame(f)}""",team)
    pg.wait_for_timeout(14800)
    cdp.send('Page.stopScreencast')
    b.close()
for i,(t,d) in enumerate(frames):
    open(f'{out}/f{i:05d}.jpg','wb').write(base64.b64decode(d))
json.dump([t-frames[0][0] for t,_ in frames],open(f'{out}/times.json','w'))
print(len(frames), 'frames', frames[-1][0]-frames[0][0],'s; team y',team)
