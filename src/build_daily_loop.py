from pathlib import Path
import html,json,math,re


def display_time(minutes):
    hour,minute=divmod(minutes%1440,60)
    return f'{hour%12 or 12}:{minute:02d} {"AM" if hour<12 else "PM"}'


def build_daily_loop(site):
    site=Path(site)
    source,dist=site/'src',site/'dist'
    stops=json.loads((source/'daily-loop.data.json').read_text(encoding='utf-8'))
    assert len(stops)==17 and stops[0]['start']==540 and stops[-1]['end']==1980
    assert all(stop['end']>stop['start'] for stop in stops)
    assert all(a['end']==b['start'] for a,b in zip(stops,stops[1:]))
    index=dist/'index.html'
    page=index.read_text(encoding='utf-8')
    match=re.search(r'<section class="stats section-reboot section-blue">(.*?)</section>',page,re.S)
    if not match:raise ValueError('Original clock section was not found')
    content=match.group(1)
    hold=content.index('<div class="stats__hold">')
    decoration=content[:hold]
    background=re.search(r'<div class="onclock__spiral stats__spiral">.*?(?=<div class="stats__lines-decor">)',content,re.S).group(0)
    legacy=content[hold:].replace(background,'',1).replace('id="clockwork-runner"','id="clockwork-runner-static"')
    template=(source/'daily-loop.template.html').read_text(encoding='utf-8')
    marks=[]
    for i in range(60):
        major=i%5==0
        marks.append(f'<path d="M0 -{215 if major else 225}V-233" transform="rotate({i*6})" stroke="#bd8946" stroke-width="{5 if major else 1.3}" stroke-linecap="round" opacity="{1 if major else .55}"/>')
    numbers=[]
    for hour in range(1,13):
        angle=hour*math.pi/6
        x,y=190*math.sin(angle),-190*math.cos(angle)
        numbers.append(f'<text x="{x:.3f}" y="{y:.3f}" data-dial-number="{hour}">{hour}</text>')
    markers,props,buttons,transcript=[],[],[],[]
    for i,stop in enumerate(stops):
        angle=i/len(stops)*math.tau
        x,y=279*math.sin(angle),-279*math.cos(angle)
        px,py=200*math.sin(angle),-200*math.cos(angle)
        markers.append(f'<circle data-route-stop="{i}" cx="{x:.3f}" cy="{y:.3f}" r="3.3"/>')
        props.append(f'<g class="loop-scene-prop" data-scene-stop="{i}" transform="translate({px:.3f},{py:.3f})"><use href="#loop-icon-{stop["icon"]}" x="-40" y="-29" width="80" height="58"/></g>')
        label=f'{display_time(stop["start"])} — {stop["label"]}'
        buttons.append(f'<button type="button" class="loop-stop-button" data-loop-stop="{i}" aria-label="{html.escape(label)}" aria-current="{str(i==0).lower()}" title="{html.escape(label)}"><span></span></button>')
        transcript.append(f'<li><time>{display_time(stop["start"])} – {display_time(stop["end"])}</time><strong>{html.escape(stop["label"])}</strong><p>{html.escape(stop["caption"])}</p></li>')
    for key,value in {
        '__ORIGINAL_BACKGROUND__':background,'__CLOCK_MARKS__':''.join(marks),'__CLOCK_NUMBERS__':''.join(numbers),
        '__ROUTE_MARKERS__':''.join(markers),'__SCENE_PROPS__':''.join(props),'__STOP_BUTTONS__':''.join(buttons),
        '__TRANSCRIPT__':''.join(transcript),'__DAILY_DATA__':json.dumps(stops,ensure_ascii=False).replace('</','<\\/'),
    }.items():template=template.replace(key,value)
    replacement='<section class="stats section-reboot section-blue daily-loop-section" id="daily-loop">'+decoration+template+'<div class="daily-loop-legacy" hidden aria-hidden="true">'+legacy+'</div></section>'
    page=page[:match.start()]+replacement+page[match.end():]
    page=page.replace('</head>','<link rel="stylesheet" href="/assets/daily-loop.css"></head>')
    page=page.replace('</body>','<script src="/assets/daily-loop.js" defer></script></body>')
    index.write_text(page,encoding='utf-8')
    for name in ('daily-loop.css','daily-loop.js'):(dist/'assets'/name).write_bytes((source/name).read_bytes())
    # The same scene is available directly, without the full site's existing
    # video entrance, so the interaction is easy to review and share.
    standalone='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>VOICE — The Daily Loop</title><link rel="stylesheet" href="/assets/site-typography.css"><link rel="stylesheet" href="/assets/daily-loop.css"><style>
    *{box-sizing:border-box}html,body{margin:0;--dark-blue:#101984;--color-soft:#fff0ce;--color:#fff0ce;color:#fff0ce;background:#101984}body{background-image:url('/assets/96f2ec2618-690cdf5ffff2032d5eb4a260_pattern.webp');background-size:220px}svg{overflow:visible}.loop-original-background .stats__spiral__center__pattern{position:absolute;overflow:hidden;border-radius:50%}.daily-loop-section{background:transparent}.loop-route-markers circle{stroke:#131d72}.loop-preview-outro{height:50svh;display:grid;place-items:center;text-align:center;padding:30px}.loop-preview-outro p{font:400 38px/1.2 var(--font-display)}.loop-preview-outro a{display:block;font:400 11px/1.5 var(--font-ui);margin-top:20px;color:#e2c698}.loop-original-background .stats__solid{stroke-dasharray:800 1400;animation:loop-lines 7s linear infinite}.loop-original-background .stats__solid:nth-child(2n){animation-delay:-2s}@keyframes loop-lines{to{stroke-dashoffset:-2200}}@media(prefers-reduced-motion:reduce){.loop-original-background .stats__solid{animation:none}}
    </style></head><body><section class="stats section-reboot section-blue daily-loop-section" id="daily-loop">'''+template+'''</section><div class="loop-preview-outro" id="mumbai-alley"><p>Tomorrow, we do it all again.<a href="/#daily-loop">Back to the full VOICE website ↗</a></p></div><script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script><script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script><script>if(window.gsap&&window.ScrollTrigger){gsap.registerPlugin(ScrollTrigger);window.__voiceAnimation={gsap,ScrollTrigger};}</script><script src="/assets/daily-loop.js"></script></body></html>'''
    standalone=standalone.replace('<body>','<body class="loop-standalone">',1)
    (dist/'daily-loop.html').write_text(standalone,encoding='utf-8')
    runtime=dist/'assets/f7502c028f-index-8YjIcPvu.js'
    js=runtime.read_text(encoding='utf-8')
    if 'window.__voiceAnimation=' not in js:
        needle='Z.registerPlugin(de,Zi,$s);class S3{'
        if needle not in js:raise ValueError('Existing animation library hook was not found')
        js=js.replace(needle,'window.__voiceAnimation={gsap:Z,ScrollTrigger:de};'+needle,1)
    runtime.write_text(js,encoding='utf-8')


if __name__=='__main__':build_daily_loop(Path(__file__).resolve().parent.parent)
