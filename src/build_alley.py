from pathlib import Path
import shutil


def build_alley(site):
    site=Path(site)
    source=site/'src'
    dist=site/'dist'
    artwork=source/'media'/'teal-urban-canyon.png'
    asset=dist/'assets'/'mumbai'/'teal-urban-canyon.png'
    asset.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(artwork,asset)
    (dist/'mumbai-alley.html').write_text((source/'mumbai-alley.template.html').read_text(encoding='utf-8'),encoding='utf-8')

    index=dist/'index.html'
    html=index.read_text(encoding='utf-8')
    html=html.replace('<div class="spacer-fs scene-tunnel">','<div class="spacer-fs scene-tunnel" id="mumbai-alley"><div class="mumbai-alley-viewport"><iframe id="mumbai-alley-frame" src="/mumbai-alley.html?embed=1" title="Life in Mumbai — immersive alley illustration" loading="eager"></iframe></div>',1)
    style='''<style id="mumbai-alley-integration">
    .spacer-fs.scene-tunnel{position:relative!important;height:680svh!important;min-height:680svh!important;overflow:visible!important;z-index:30!important;background:#071c22!important}
    .scene-tunnel__hold{display:none!important}
    .mumbai-alley-viewport{position:sticky;top:0;height:100svh;width:100%;overflow:clip}
    .mumbai-alley-viewport iframe{display:block;width:100%;height:100%;border:0;background:#071c22}
    body.mumbai-alley-active .main-logo,body.mumbai-alley-active .trg-note,body.mumbai-alley-active .insigh-pannel,body.mumbai-alley-active .cursor-insight{visibility:hidden!important;pointer-events:none!important}
    body.mumbai-alley-active canvas.webgl{visibility:hidden!important}
    @media(prefers-reduced-motion:reduce){.spacer-fs.scene-tunnel{height:180svh!important;min-height:180svh!important}}
    </style>'''
    html=html.replace('</head>',style+'</head>')
    bridge='''<script id="mumbai-alley-bridge">
    (()=>{const section=document.getElementById('mumbai-alley'),frame=document.getElementById('mumbai-alley-frame');let scheduled=false;
    function update(){scheduled=false;const r=section.getBoundingClientRect();const active=r.top<innerHeight*.5&&r.bottom>innerHeight*.5;window.__mumbaiAlleyActive=active;document.body.classList.toggle('mumbai-alley-active',active);const progress=Math.max(0,Math.min(1,-r.top/Math.max(1,r.height-innerHeight)));frame.contentWindow.postMessage({mumbaiAlleyParent:true,active,progress},location.origin);}
    function schedule(){if(!scheduled){scheduled=true;requestAnimationFrame(update);}}
    frame.addEventListener('load',update);addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
    addEventListener('message',e=>{if(e.source!==frame.contentWindow||e.origin!==location.origin||!e.data?.mumbaiAlley)return;if(e.data.ready)update();if(Number.isFinite(e.data.wheel)){const delta=Math.max(-900,Math.min(900,e.data.wheel)),lenis=window.__voiceLenis;if(lenis)lenis.scrollTo(lenis.targetScroll+delta,{duration:.45,programmatic:false});else window.scrollBy(0,delta);}});update();})();
    </script>'''
    html=html.replace('</body>',bridge+'</body>')
    index.write_text(html,encoding='utf-8')

    runtime=dist/'assets'/'f7502c028f-index-8YjIcPvu.js'
    js=runtime.read_text(encoding='utf-8')
    # Feed iframe wheel deltas to the site's existing smooth-scroll controller.
    # Native scrollBy competes with Lenis' pending target on desktop.
    js=js.replace('this.lenis=new _3({})','this.lenis=window.__voiceLenis=new _3({})',1)
    js=js.replace('if(window.__voiceHeroActive)return;','if(window.__voiceHeroActive||window.__mumbaiAlleyActive)return;')
    # Keep the legacy timeline/labels available, but detach its old spiral and
    # pills from the renderer. The replacement fully owns this one scene.
    old='class iR{constructor(e){this.webgl_app=e,this.scene=this.webgl_app.scene,this.group=new gt,this.scene.add(this.group),this.objs='
    new='class iR{constructor(e){this.webgl_app=e,this.scene=this.webgl_app.scene,this.group=new gt,this.objs='
    js=js.replace(old,new,1)
    runtime.write_text(js,encoding='utf-8')


if __name__=='__main__':
    build_alley(Path(__file__).resolve().parent.parent)
