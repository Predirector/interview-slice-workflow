from common import *

def texts(d):
 roles={'title':''.join(d['titleLines'])+''.join(d['cover']['titleLines'])+d['interview']['context'],
 'semantic':''.join(x['text'] for s in d.get('semantic',[]) for x in s['items']),
 'caption':''.join(c['zh']+c['en'] for c in d['captions'])+d['interview']['name']+d['interview']['role']+''.join(x['text'] for x in d.get('danmaku',[]))}
 return roles

def measured(spec,size):
 from PIL import ImageFont
 f=ImageFont.truetype(str(asset(spec['file'])),size)
 try:f.set_variation_by_axes([spec['weight'] if a['name']==b'Weight' else a['default'] for a in f.get_variation_axes()])
 except OSError:pass
 return f

def audit(d):
 from fontTools.ttLib import TTFont
 out={}
 for role,text in texts(d).items():
  spec=d['fonts'][role];p=asset(spec['file']);h=sha(p)
  if h!=spec['sha256']:raise ValueError('Font SHA changed for '+role)
  font=TTFont(p);cmap=font.getBestCmap() or {};missing=sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
  if missing:raise ValueError('Missing '+role+' glyphs: '+''.join(missing))
  weight=spec['weight'];axis=next((x for x in font['fvar'].axes if x.axisTag=='wght'),None) if 'fvar' in font else None
  if axis and not axis.minValue<=weight<=axis.maxValue:raise ValueError('Font weight outside variable axis')
  if not axis and abs(weight-font['OS/2'].usWeightClass)>150:raise ValueError('Static font weight mismatch; do not synthesize bold')
  out[role]={'file':spec['file'],'sha256':h,'family':font['name'].getDebugName(1),'style':font['name'].getDebugName(2),'weight':weight,'glyphCoverage':True};font.close()
 return out

def import_font(role,path,weight):
 from fontTools.ttLib import TTFont
 src=Path(path).expanduser().resolve();f=TTFont(src);f.close();h=sha(src);rel='fonts/'+h[:16]+src.suffix.lower();dst=asset(rel);dst.parent.mkdir(parents=True,exist_ok=True)
 if src!=dst and not dst.exists():shutil.copyfile(src,dst)
 if sha(dst)!=h:raise ValueError('Font copy differs')
 d=episode();d['fonts'][role]={'file':rel,'weight':weight,'sha256':h};save(ROOT/'episode.json',d)
 return d['fonts'][role]
