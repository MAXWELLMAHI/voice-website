from pathlib import Path
from urllib.request import Request,urlopen
import re,hashlib,json
ROOT=Path(__file__).resolve().parent
DIST=ROOT.parent/'sleep-well-replica'/'dist'
fonts=DIST/'assets'/'fonts';fonts.mkdir(parents=True,exist_ok=True)
url='https://fonts.googleapis.com/css2?family=ABeeZee:ital@0;1&family=Borel&family=Cormorant+SC:wght@400;600&display=swap'
ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
css=urlopen(Request(url,headers={'User-Agent':ua})).read().decode()
blocks=re.findall(r'/\* latin \*/\s*(@font-face\s*\{[^}]+\})',css)
assert blocks,'Google Fonts returned no Latin font faces'
local=[]
for block in blocks:
 remote=re.search(r'url\((https[^)]+)\)',block).group(1)
 family=re.search(r"font-family:\s*'([^']+)'",block).group(1)
 weight=re.search(r'font-weight:\s*(\d+)',block).group(1)
 name=family.lower().replace(' ','-')+'-'+weight+'-'+hashlib.sha1(remote.encode()).hexdigest()[:8]+'.woff2'
 p=fonts/name
 if not p.exists():p.write_bytes(urlopen(remote).read())
 local.append(block.replace(remote,'/assets/fonts/'+name))
for slug in ['abeezee','borel','cormorantsc']:
 p=fonts/(slug+'-OFL.txt')
 if not p.exists():p.write_bytes(urlopen('https://raw.githubusercontent.com/google/fonts/main/ofl/'+slug+'/OFL.txt').read())
faces='\n'.join(local)
(ROOT/'font-faces.css').write_text(faces,encoding='utf-8')
rules='''
:root{--font-display:"Cormorant SC",Georgia,serif;--font-ui:"ABeeZee",Arial,sans-serif;--font-note:"Borel",cursive}
html,body,button,input,textarea,select,p,a,li{font-family:var(--font-ui)}
h1,h2,h3,h4,h5,h6,.title_serif,.title_sans,.typog__word__text,.insights__insight__text,.note__title{font-family:var(--font-display)!important}
.parag,.small-parag,.description,.note__parag__serif,.subtitle__text,.note__parag,.note__parag__bold,.footer__parag,.trg-note__text,.insights__text{font-family:var(--font-ui)!important}
.handwritten-note,.small-parag.minimum,.cursor-insight__text{font-family:var(--font-note)!important;font-weight:400;letter-spacing:0;text-transform:none;line-height:1.8}
.handwritten-note{display:inline-block;font-size:1.05em;padding-top:.15em}
.small-parag.minimum{font-size:max(12px,1.7rem);line-height:1.9}
'''
(DIST/'assets'/'site-typography.css').write_text(faces+'\n'+rules,encoding='utf-8')
# Keep icon fonts intact and retain the legacy declarations for source fidelity.
# Replace the actual typography rules, excluding old @font-face declarations.
p=DIST/'assets/e2cea6f2ea-play-sleepwell-creatives.webflow.shared.eb1e20856.css'
s=p.read_text(encoding='utf-8')
def rewrite(m):
 selector,body=m.group(1),m.group(2)
 if '@font-face' in selector:return m.group(0)
 body=re.sub(r'font-family:\s*Editorial[^;}]*;', 'font-family: "Cormorant SC", Georgia, serif;',body)
 body=re.sub(r'font-family:\s*NM_(?:Light|Medium|Regular)[^;}]*;', 'font-family: "ABeeZee", Arial, sans-serif;',body)
 body=re.sub(r'font-family:\s*(?:Arial[^;}]*|Helvetica Neue[^;}]*|sans-serif|serif);', 'font-family: "ABeeZee", Arial, sans-serif;',body)
 return selector+'{'+body+'}'
s=re.sub(r'([^{}]+)\{([^{}]*)\}',rewrite,s)
p.write_text(s,encoding='utf-8')
print(json.dumps({'font_faces':len(blocks),'families':sorted(set(re.findall(r"font-family:\s*'([^']+)'",faces))),'font_bytes':sum(p.stat().st_size for p in fonts.glob('*.woff2'))}))
