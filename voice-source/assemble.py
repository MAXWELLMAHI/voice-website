from pathlib import Path
import base64,re,json
ROOT=Path(__file__).resolve().parent
SITE=ROOT.parent/'sleep-well-replica'
DIST=SITE/'dist'
def data(name,mime):return 'data:'+mime+';base64,'+base64.b64encode((ROOT/name).read_bytes()).decode()
s=(ROOT/'hero-simple.template.html').read_text(encoding='utf-8')
for key,name,mime in [('__VIDEO_DATA__','hero-7508.mp4','video/mp4'),('__POSTER_DATA__','hero-7508-poster.jpg','image/jpeg')]:s=s.replace(key,data(name,mime))
raw=(ROOT/'original-index.html').read_text(encoding='utf-8')
moon=re.search(r'<div class="preloader__svg w-embed">(.*?)</div>',raw,re.S).group(1)
legacy='<div class="loader" role="dialog" aria-label="Enter Site" aria-modal="true"><div class="loader-inner"><div class="loader-moon">'+moon+'</div><div class="legacy-loading">Loading<span> · · ·</span></div><button class="enter" disabled>Enter Site</button><div class="track" role="progressbar" aria-label="Loading video" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="bar"></div></div><span id="percent" hidden>0%</span></div></div>'
s=re.sub(r'<div class="loader" role="dialog".*?(?=<main)',legacy+'\n',s,count=1,flags=re.S)
extra='''<style>
.loader{--color:#2451b5;background:#fef1d0;color:#2451b5;background-image:url('__GRAIN_DATA__');background-size:220px}.loader-moon{width:42px;height:59px;margin:auto}.legacy-loading{font:22px 'Cormorant SC',Georgia,serif;margin-top:14px}.loader .enter{border:0;color:#2451b5;font:22px 'Cormorant SC',Georgia,serif;text-transform:none;letter-spacing:-.04em;padding:0;margin:14px auto 0;min-width:0}.loader .enter:hover{background:none}.loader .track{display:none}.loader:not(.is-ready) .enter,.loader.is-ready .legacy-loading{display:none}.embedded .loader{display:none!important}.sound-toggle{position:fixed;right:28px;top:50%;transform:translateY(-50%);z-index:12;border:1px solid #ffffff45;border-radius:40px;padding:12px 14px;display:flex;align-items:center;gap:9px;background:#060a1288;backdrop-filter:blur(10px);color:#efeae0;font:8px 'ABeeZee',Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;cursor:pointer}.sound-toggle svg{width:18px;height:18px}.sound-toggle .sound-cross{display:none}.sound-toggle.is-muted .sound-cross{display:block}.sound-toggle.is-muted .sound-waves{display:none}@media(max-width:600px){.sound-toggle{right:22px;top:auto;bottom:100px;transform:none;padding:10px 12px;font-size:7px}}
</style>'''
grain=DIST/'assets/96f2ec2618-690cdf5ffff2032d5eb4a260_pattern.webp'
extra=extra.replace('__GRAIN_DATA__','data:image/webp;base64,'+base64.b64encode(grain.read_bytes()).decode())
s=s.replace('</head>',extra+'</head>')
s=s.replace("const grain=document.createElement('canvas');", "const loaderMoon=document.querySelector('.loader .rect-solid');if(loaderMoon&&!EMBED){const length=loaderMoon.getTotalLength();gsap.fromTo(loaderMoon,{strokeDasharray:length,strokeDashoffset:length},{strokeDashoffset:0,repeat:-1,yoyo:true,duration:1.8,ease:'power3.inOut'});}const grain=document.createElement('canvas');")
faces=(ROOT/'font-faces.css').read_text(encoding='utf-8')
def embed_font(m):
 path=DIST/m.group(1).lstrip('/')
 return 'url(data:font/woff2;base64,'+base64.b64encode(path.read_bytes()).decode()+')'
faces=re.sub(r'url\((/assets/fonts/[^)]+)\)',embed_font,faces)
s=s.replace('</head>','<style>'+faces+'</style></head>')
(DIST/'voice-hero.html').write_text(s,encoding='utf-8')
index=DIST/'index.html'
baseline=ROOT/'original-index.html'
if not baseline.exists():baseline.write_bytes(index.read_bytes())
h=baseline.read_text(encoding='utf-8')
h=h.replace('<title>Sleep Well Creatives</title>','<title>VOICE — Built in the Noise.</title>')
h=h.replace('content="Sleep Well Creatives" property="og:title"','content="VOICE — Built in the Noise." property="og:title"')
h=re.sub(r'<meta[^>]*name="description"[^>]*>','<meta name="description" content="VOICE — Built in the Noise. Mumbai Chawl Edition.">',h,count=1)
h=h.replace('<div class="hero">','<div class="hero"><div class="voice-viewport"><iframe id="voice-hero" src="/voice-hero.html?embed=1" title="Mumbai Chawl Edition" allow="autoplay" loading="eager"></iframe></div>',1)
style='''<style id="voice-integration">
.hero{height:160svh!important;min-height:100svh!important;position:relative!important;overflow:visible!important;z-index:30!important;background:#080e19!important}.hero__hold{display:none!important}.voice-viewport{position:sticky;top:0;height:100svh;width:100%;overflow:clip}.voice-viewport iframe{border:0;display:block;width:100%;height:100%;background:#080e19}.preloader{pointer-events:none;z-index:2147483000!important}body.voice-video-ready.webgl-ready .preloader{pointer-events:auto}body:not(.voice-video-ready) .preloader__enter{display:none!important}body:not(.voice-video-ready) .preloader__span{display:block!important}.trg-sound{display:none!important}body.voice-active .main-logo,body.voice-active .trg-note,body.voice-active .insigh-pannel,body.voice-active .cursor-insight{visibility:hidden!important;pointer-events:none!important}body.voice-active canvas.webgl{visibility:hidden!important}
</style>'''
h=h.replace('</head>','<link rel="stylesheet" href="/assets/site-typography.css">'+style+'</head>')
h=h.replace('I hope you find it helpful. Thank you 😊','<span class="handwritten-note">I hope you find it helpful. Thank you 😊</span>')
h=h.replace('<body ', '<body ',1)
bridge='''<script id="voice-bridge">
(()=>{const frame=document.getElementById('voice-hero'),hero=document.querySelector('.hero');let ticking=false,lastActive=null,entered=false;window.__voiceHeroActive=true;document.body.classList.add('voice-active');document.querySelectorAll('audio').forEach(a=>a.muted=true);
function update(){ticking=false;const r=hero.getBoundingClientRect(),active=r.bottom>0&&r.top<innerHeight;window.__voiceHeroActive=active;document.body.classList.toggle('voice-active',active);const p=Math.max(0,Math.min(1,(-r.top)/(r.height-innerHeight)));frame.contentWindow.postMessage({voiceParent:true,progress:p,active},location.origin);lastActive=active;}
function schedule(){if(!ticking){ticking=true;requestAnimationFrame(update);}}
frame.addEventListener('load',()=>{if(frame.contentDocument?.querySelector('#stage')?.dataset.ready==='true')document.body.classList.add('voice-video-ready');update();});addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
document.querySelector('.preloader').addEventListener('click',()=>{if(entered)return;entered=true;const v=frame.contentDocument?.querySelector('#city-video');if(v){v.muted=false;v.volume=1;v.play().catch(()=>{});}frame.contentWindow.postMessage({voiceParent:true,enter:true},location.origin);},{capture:true,once:true});
addEventListener('message',e=>{if(e.source!==frame.contentWindow||e.origin!==location.origin||!e.data?.voice)return;const d=e.data;if(d.ready)document.body.classList.add('voice-video-ready');if(Number.isFinite(d.wheel))window.scrollBy(0,Math.max(-900,Math.min(900,d.wheel)));if(Number.isFinite(d.scrollTo))window.scrollTo({top:hero.offsetTop+Math.max(0,Math.min(1,d.scrollTo))*(hero.offsetHeight-innerHeight),behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});});update();})();
</script>'''
h=h.replace('</body>',bridge+'</body>')
index.write_text(h,encoding='utf-8')
runtime=DIST/'assets/f7502c028f-index-8YjIcPvu.js'
js=runtime.read_text(encoding='utf-8')
if 'if(window.__voiceHeroActive)return;' not in js:
 js=js.replace('update(){this.world.update(this.time.elapsed,this.time.delta)', 'update(){if(window.__voiceHeroActive)return;this.world.update(this.time.elapsed,this.time.delta)',1)
js=js.replace('const e=document.title,t="Did you fall asleep?";','const e=document.title,t=e;')
runtime.write_text(js,encoding='utf-8')
for name in ['hero-simple.template.html','assemble.py','prepare_fonts.py','font-faces.css']:
 p=SITE/'voice-source'/name;p.parent.mkdir(exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
print(json.dumps({'hero_bytes':(DIST/'voice-hero.html').stat().st_size,'video_bytes':(ROOT/'hero-7508.mp4').stat().st_size}))
