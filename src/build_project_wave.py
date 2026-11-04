from pathlib import Path
import html,json,re,shutil


def esc(value):return html.escape(str(value),quote=True)


def image_slot(project,index,source,dist):
    images=project['images']
    image=images[index] if index<len(images) else None
    if image:
        relative=Path(image)
        if relative.is_absolute() or '..' in relative.parts:raise ValueError('Timeline images must stay inside src/media')
        file=source/'media'/relative
        target=dist/'assets'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(file,target)
        return f'<img src="/assets/{relative.as_posix()}" alt="{esc(project["title"])} — image {index+1}" loading="lazy" decoding="async">'
    return f'<div class="wave-card-placeholder"><div class="wave-card-badge"><span>SLOT {index+1:02d}</span></div><div class="wave-card-center-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="wave-card-kicker">{esc(project["title"])}</div></div>'


def page_shell(title,body):
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' — VOICE</title><link rel="stylesheet" href="/assets/site-typography.css"><link rel="stylesheet" href="/assets/project-wave.css"><style>*{box-sizing:border-box}html,body{margin:0;background:#f9eed7;--color:#194ca9}body{overflow-x:clip}</style></head><body id="top">'+body+'</body></html>'


def build_project_wave(site):
    site=Path(site);source,dist=site/'src',site/'dist'
    projects=json.loads((source/'project-wave.data.json').read_text(encoding='utf-8'))
    assert projects and len({project['id'] for project in projects})==len(projects)
    rows=[];project_dir=dist/'projects';project_dir.mkdir(parents=True,exist_ok=True)

    annotations = [
        "where the spark started",
        "first steps outside the classroom",
        "voice on the world stage · Bali",
        "finding perspective on my own",
        "data, models & momentum",
        "learning by showing up",
        "six months of campaigns",
        "building my own startup",
        "marketing campaigns for OpenAI",
        "the black book & presentation"
    ]

    for i,project in enumerate(projects):
        assert len(project.get('images',[]))>=3, 'Every milestone needs at least three image slots'
        slots=[image_slot(project,j,source,dist) for j in range(len(project['images']))]
        scribble = annotations[i] if i < len(annotations) else "movement in key"

        pile_cards = ''.join([
            f'<div class="wave-pile-card card-{j}" data-card-index="{j}">{slots[j]}</div>'
            for j in range(3)
        ])

        station_html = (
            f'<li class="wave-project-station" id="station-{esc(project["id"])}" data-project-index="{i}" data-project-id="{esc(project["id"])}">'
            f'<div class="station-anchor" data-anchor-index="{i}">'
            f'  <div class="station-note-head"><span class="note-num">{i+1:02d}</span></div>'
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

        page_slots=''.join(f'<div class="project-detail-slot {"is-empty" if not image else ""}">{slots[j]}</div>' for j,image in enumerate(project['images']))
        detail=f'<main class="project-detail"><a class="project-detail-back" href="/project-wave.html#station-{esc(project["id"])}">← Back to the score</a><div class="project-detail-kicker">{i+1:02d} / {esc(project["subheading"])}</div><h1>{esc(project["title"])}</h1><p class="project-detail-intro">{esc(project["summary"])}</p><div class="project-detail-slots">{page_slots}</div><div class="project-detail-pending"><h2>The full story, next.</h2><p>{esc(project["work"])}</p><p>More images and project details will be added here.</p></div><a class="project-detail-back" href="/contact.html">Keep the conversation going ↗</a></main>'
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
    runtime=dist/'assets/f7502c028f-index-8YjIcPvu.js';js=runtime.read_text(encoding='utf-8')
    js=js.replace('if(window.__voiceHeroActive||window.__mumbaiAlleyActive)return;','if(window.__voiceHeroActive||window.__mumbaiAlleyActive||window.__voiceProjectWaveActive)return;')
    runtime.write_text(js,encoding='utf-8')
    standalone='<section class="importance section-blue voice-project-wave" id="project-wave">'+template+'</section>'+contact+'<script src="/assets/project-wave.js"></script>'
    (dist/'project-wave.html').write_text(page_shell('The project score',standalone),encoding='utf-8')
    contact_page='<a class="contact-page-back" href="/project-wave.html">← Back to the score</a>'+contact.replace('Contact page ↗','Project timeline ↗').replace('href="/contact.html"','href="/project-wave.html"')
    (dist/'contact.html').write_text(page_shell('Contact',contact_page),encoding='utf-8')


if __name__=='__main__':build_project_wave(Path(__file__).resolve().parent.parent)
