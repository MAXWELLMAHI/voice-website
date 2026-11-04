from pathlib import Path
import html,json,re,shutil,math


def esc(value):return html.escape(str(value),quote=True)


def sound_wave_svg():
    paths=[]
    for layer in range(5):
        points=[]
        for x in range(0,1601,4):
            phase=2*math.pi*x/1600
            envelope=.2+.8*(.5+.5*math.sin(2*phase-.8))**2
            oscillation=math.sin(10*phase)+.22*math.sin(20*phase)
            y=300+(layer-2)*22+(135-layer*12)*envelope*oscillation
            points.append(f'{x},{y:.2f}')
        paths.append(f'<path d="M'+ ' L'.join(points)+f'" opacity="{.62-layer*.08:.2f}"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 720" fill="none"><g stroke="#194ca9" stroke-width="1.5" stroke-linecap="round">'+''.join(paths)+'</g></svg>'


def image_slot(project,index,source,dist):
    images=project['images']
    image=images[index] if index<len(images) else None
    if image:
        relative=Path(image)
        if relative.is_absolute() or '..' in relative.parts:raise ValueError('Timeline images must stay inside src/media')
        file=source/'media'/relative
        target=dist/'assets'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists() or file.stat().st_mtime > target.stat().st_mtime:
            try: shutil.copyfile(file,target)
            except Exception: pass
        captions=project.get('imageCaptions',[])
        alt=captions[index] if index<len(captions) else f'{project["title"]} — image {index+1}'
        return f'<img src="/assets/{relative.as_posix()}" alt="{esc(alt)}" loading="lazy" decoding="async">'
    return f'<div class="wave-card-placeholder"><div class="wave-card-badge"><span>SLOT {index+1:02d}</span></div><div class="wave-card-center-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="wave-card-kicker">{esc(project["title"])}</div></div>'


def page_shell(title,body):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' — VOICE</title><link rel="stylesheet" href="/assets/site-typography.css"><link rel="stylesheet" href="/assets/project-wave.css"><style>*{box-sizing:border-box}html,body{margin:0;background:#f9eed7;--color:#194ca9}body{overflow-x:clip}</style></head><body id="top">'+body+'</body></html>'


def build_project_wave(site):
    site=Path(site);source,dist=site/'src',site/'dist'
    wave=sound_wave_svg()
    (source/'media/project-soundwave.svg').write_text(wave,encoding='utf-8')
    (dist/'assets/project-soundwave.svg').write_text(wave,encoding='utf-8')
    projects=json.loads((source/'project-wave.data.json').read_text(encoding='utf-8'))
    assert projects and len({project['id'] for project in projects})==len(projects)
    rows=[];project_dir=dist/'projects';project_dir.mkdir(parents=True,exist_ok=True)
    media_dir=source/'media'/'wave-projects';dist_media_dir=dist/'assets'/'wave-projects'
    if media_dir.exists():
        dist_media_dir.mkdir(parents=True,exist_ok=True)
        for f in media_dir.glob('*'):
            if f.is_file():
                dest_f = dist_media_dir / f.name
                if not dest_f.exists() or f.stat().st_mtime > dest_f.stat().st_mtime:
                    try: shutil.copyfile(f, dest_f)
                    except Exception: pass

    annotations = {
        "jaggernaut": "heritage, reimagined for the web",
        "college-finale": "the black book & presentation",
        "create": "marketing campaigns for OpenAI",
        "gallygood": "building my own startup",
        "blinksquare": "six months of campaigns",
        "industry-events": "learning by showing up",
        "agency-ai": "data, models & momentum",
        "solo-travel": "finding perspective on my own",
        "bali-mun": "voice on the world stage · Bali",
        "pause-ngo": "first steps outside the classroom",
        "engineering": "where the spark started"
    }

    for i,project in enumerate(projects):
        assert len(project.get('images',[]))>=3, 'Every milestone needs at least three image slots'
        slots=[image_slot(project,j,source,dist) for j in range(len(project['images']))]
        scribble = annotations.get(project['id'], "movement in key")
        station_num = project.get('num', len(projects) - i)

        pile_cards = ''.join([
            f'<div class="wave-pile-card card-{j}{" is-full-page" if j in project.get("fullWidthImages",[]) else ""}" data-card-index="{j}">{slots[j]}</div>'
            for j in range(3)
        ])

        station_html = (
            f'<li class="wave-project-station" id="station-{esc(project["id"])}" data-project-index="{i}" data-project-id="{esc(project["id"])}">'
            f'<div class="station-anchor" data-anchor-index="{i}">'
            f'  <div class="station-note-head"><span class="note-num">{station_num:02d}</span></div>'
            f'  <div class="station-note-meta">'
            f'    <span class="station-year">{esc(project["subheading"])}</span>'
            f'    <h4 class="station-title">{esc(project["title"])}</h4>'
            f'  </div>'
            f'</div>'
            f'<div class="station-scribble">{esc(scribble)}</div>'
            f'<div class="station-card-pile" data-pile-index="{i}" role="button" tabindex="0" aria-label="Explore {esc(project["title"])}">'
            f'  {pile_cards}'
            f'</div>'
            f'</li>'
        )
        rows.append(station_html)

        page_slots=[]
        for j,image in enumerate(project['images']):
            full=' is-full-page' if j in project.get('fullWidthImages',[]) else ''
            natural=' preserves-aspect' if project.get('preserveImageAspect') else ''
            captions=project.get('imageCaptions',[])
            caption=f'<figcaption class="project-image-caption">{esc(captions[j])}</figcaption>' if j<len(captions) else ''
            page_slots.append(f'<figure class="project-detail-item{full}{natural}"><div class="project-detail-slot {"is-empty" if not image else ""}">{slots[j]}</div>{caption}</figure>')
        page_slots=''.join(page_slots)
        next_story='' if project.get('complete') else '<h2>The full story, next.</h2>'
        next_images='' if project.get('complete') else '<p>More images and project details will be added here.</p>'
        detail=f'<main class="project-detail"><a class="project-detail-back" href="/project-wave.html#station-{esc(project["id"])}">← Back to the score</a><div class="project-detail-kicker">{station_num:02d} / {esc(project["subheading"])}</div><h1>{esc(project["title"])}</h1><p class="project-detail-intro">{esc(project["summary"])}</p><div class="project-detail-slots">{page_slots}</div><div class="project-detail-pending">{next_story}<p>{esc(project["work"])}</p>{next_images}</div><a class="project-detail-back" href="/contact.html">Keep the conversation going ↗</a></main>'
        (project_dir/(project['id']+'.html')).write_text(page_shell(project['title'],detail),encoding='utf-8')

    template=(source/'project-wave.template.html').read_text(encoding='utf-8')
    template=template.replace('__WAVE_PROJECT_ROWS__',''.join(rows)).replace('__PROJECT_COUNT__',f'{len(projects):02d}').replace('__WAVE_DATA__',json.dumps(projects,ensure_ascii=False).replace('</','<\\/'))
    contact=(source/'contact.template.html').read_text(encoding='utf-8')
    index=dist/'index.html';page=index.read_text(encoding='utf-8')
    match=re.search(r'<section class="importance section-blue">(.*?)</section>',page,re.S)
    if not match:raise ValueError('The right Beat section was not found')
    replacement='<section class="importance section-blue voice-project-wave" id="project-wave">'+template+'<div class="wave-legacy" hidden aria-hidden="true">'+match.group(1)+'</div></section>'
    # Retain hidden runtime hooks while ending the visible portfolio at contact.
    tail=page[match.end():]
    footer_end=tail.find('</footer>')
    if footer_end<0:raise ValueError('The legacy footer was not found')
    footer_end+=len('</footer>')
    tail='<div class="voice-retired-chapters" hidden aria-hidden="true">'+tail[:footer_end]+'</div>'+tail[footer_end:]
    page=page[:match.start()]+replacement+contact+tail
    page=page.replace('<body ','<body id="top" ',1)
    page=page.replace('</head>','<link rel="stylesheet" href="/assets/project-wave.css"></head>')
    page=page.replace('</body>','<script src="/assets/project-wave.js" defer></script></body>')
    index.write_text(page,encoding='utf-8')
    for name in ('project-wave.css','project-wave.js'):(dist/'assets'/name).write_bytes((source/name).read_bytes())
    runtime=dist/'assets/f7502c028f-index-8YjIcPvu.js'
    if runtime.exists():
        js=runtime.read_text(encoding='utf-8')
        target_str='if(window.__voiceHeroActive||window.__mumbaiAlleyActive)return;'
        if target_str in js:
            runtime.write_text(js.replace(target_str,'if(window.__voiceHeroActive||window.__mumbaiAlleyActive||window.__voiceProjectWaveActive)return;'),encoding='utf-8')
    standalone='<section class="importance section-blue voice-project-wave" id="project-wave">'+template+'</section>'+contact+'<script src="/assets/project-wave.js"></script>'
    (dist/'project-wave.html').write_text(page_shell('The project score',standalone),encoding='utf-8')
    contact_page='<a class="contact-page-back" href="/project-wave.html">← Back to the score</a>'+contact.replace('Contact page ↗','Project timeline ↗').replace('href="/contact.html"','href="/project-wave.html"')
    (dist/'contact.html').write_text(page_shell('Contact',contact_page),encoding='utf-8')


if __name__=='__main__':build_project_wave(Path(__file__).resolve().parent.parent)
