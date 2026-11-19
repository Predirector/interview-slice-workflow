from common import *
from timeline import build
from fonts import audit,measured
import math,re
PUNCT=re.compile(r'[，。！？；：、…“”‘’!?;:,]')
def integer(v):return isinstance(v,int) and not isinstance(v,bool)
def intersect(a,b):return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
def validate(d,check_media=True):
 if d.get('fps')!=30 or d.get('width')!=1080 or d.get('height')!=1920:raise ValueError('Starter supports 1080x1920 at 30 fps; adapt code before other formats')
 if not d.get('title') or any(c in d['title'] for c in '/\\') or d['title'] in ['.','..']:raise ValueError('Final title must be a filename, not a path')
 if d.get('coverFrames')!=3:raise ValueError('Cover must be exactly three frames')
 if d['style'] not in ['studio-amber','editorial-teal']:raise ValueError('Unknown visual layout')
 if not d.get('demo') and (not d['interview']['verified'] or not d['interview']['context'] or not d.get('stages')):raise ValueError('Production requires verified interview context and semantic stage decisions')
 if not d.get('demo') and not d.get('music'):raise ValueError('Production music missing; resolve actual licensed selection or explicit override before export')
 rows,n=build(d['edits'],d['speed'],d['fps']);caps=d['captions']
 if not caps or caps[0]['start']!=0 or caps[-1]['end']!=n:raise ValueError('Captions must cover the whole body')
 for i,c in enumerate(caps):
  if not integer(c['start']) or not integer(c['end']) or not 0<=c['start']<c['end']<=n:raise ValueError('Invalid caption frames')
  if i and caps[i-1]['end']!=c['start']:raise ValueError('Caption gap or overlap')
  if not c['zh'].strip() or not c['en'].strip() or PUNCT.search(c['zh']+c['en']) or re.search(r'(?<!\d)\.|\.(?!\d)',c['zh']+c['en']):raise ValueError('Bilingual captions required without pause punctuation')
  if '\n' in c['zh']+c['en']:raise ValueError('Prefer single-line captions; split semantic time intervals')
 warnings=[];last=0
 ids=[b['id'] for b in d.get('branches',[])]
 if not ids or len(ids)!=len(set(ids)) or any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*',i) for i in ids):raise ValueError('Retained branches need unique safe composition IDs')
 for b in sorted(d.get('broll',[]),key=lambda b:b['start']):
  a,z=b['start'],b['end']
  if not integer(a) or not integer(z) or not last<=a<z<=n:raise ValueError('Invalid/overlapping B-roll frames')
  if last and 0<a-last<30:warnings.append({'kind':'short-person-return','frames':[last,a]})
  if z-a<120:warnings.append({'kind':'short-broll','frames':[a,z]})
  if not b.get('purpose') or not b.get('sourceIdentity'):raise ValueError('B-roll needs semantic purpose and actual identity')
  if check_media:
   dur=float(probe(asset(b['file']))['format']['duration']);rate=b.get('rate',1)
   if rate<=0 or b['sourceStart']<0 or b['sourceStart']+(z-a)/30*rate>dur+1/30:raise ValueError('B-roll source not long enough; no freeze/loop allowed')
  if b.get('internalCuts') is None:warnings.append({'kind':'source-cuts-not-reviewed','asset':b['file']})
  last=z
 box=d['mediaBox']
 if len(box)!=4 or min(box[2:])<=0 or min(box[:2])<0 or box[0]+box[2]>1080 or box[1]+box[3]>1920:raise ValueError('Invalid media box')
 if d.get('frameMode')!='full' and not .95<=box[2]/box[3]<=1.38:raise ValueError('Media area too narrow; target 1:1 or 4:3')
 for seq in d.get('semantic',[])+d.get('pip',[]):
  if not integer(seq['start']) or not integer(seq['end']) or not 0<=seq['start']<seq['end']<=n:raise ValueError('Invalid semantic/PiP interval')
 for x in d.get('danmaku',[]):
  if not integer(x['start']) or not integer(x['duration']) or x['start']<0 or x['duration']<2 or not x.get('text'):raise ValueError('Invalid danmaku timing/text')
 for s in d.get('semantic',[]):
  for item in s['items']:
   if not item.get('text') or not item.get('size'):raise ValueError('Empty semantic group')
 if check_media:
  fa=audit(d);caption_spec=d['fonts']['caption']
  for c in caps:
   for key,size in [('zh',d['captionSize']),('en',d['translationSize'])]:
    if measured(caption_spec,size).getlength(c[key])>900:raise ValueError('Caption too wide; split by full meaning instead of shrinking')
  for lines,size in [(d['titleLines'],d['titleSize']),(d['cover']['titleLines'],d['cover']['titleSize'])]:
   if any(measured(d['fonts']['title'],size).getlength(t)>900 for t in lines):raise ValueError('Title too wide; recompose actual wording')
  for s in d.get('semantic',[]):
   for item in s['items']:
    width=measured(d['fonts']['semantic'],item['size']).getlength(item['text']);rect=[item['x'],item['y'],width,item['size']*1.2]
    for shot in d.get('faces',[]):
     if shot['start']<s['end'] and shot['end']>s['start'] and intersect(rect,shot['box']):warnings.append({'kind':'semantic-face-overlap','text':item['text'],'frames':[s['start'],s['end']]})
  for x in d.get('danmaku',[]):
   x['measuredWidth']=math.ceil(measured(caption_spec,x.get('size',36)).getlength(x['text']))+8
  for f in [d['source']]+[x['file'] for x in d.get('broll',[])]+([d['music']['file']] if d.get('music') else [])+([d['foreground']] if d.get('foreground') else []):
   if not asset(f).is_file():raise ValueError('Missing media '+f)
 else:fa={}
 return {**d,'timeline':rows,'bodyFrames':n,'durationInFrames':n+3,'fontAudit':fa,'warnings':warnings}
