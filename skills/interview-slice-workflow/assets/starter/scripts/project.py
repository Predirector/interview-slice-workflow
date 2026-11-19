#!/usr/bin/env python3
"""Portable slice project lifecycle. No account secrets or author-specific paths."""
from common import *
from timeline import build
from contract import validate
from fonts import import_font
import argparse,sys,venv,urllib.request,tempfile,re,math

def doctor():
 cfg=config();result={'project':str(ROOT),'python':sys.version.split()[0],'configuredTools':{},'mediaAvailable':False}
 for key in ['ffmpeg','ffprobe','node']:
  try:result['configuredTools'][key]=tool(key)
  except RuntimeError as e:result['configuredTools'][key]={'missing':str(e)}
 try:result['mediaRoot']=str(media());result['mediaAvailable']=True
 except RuntimeError as e:result['mediaError']=str(e)
 nm=Path(cfg.get('nodeModules',str(ROOT/'node_modules')))
 expected=json.loads((ROOT/'package.json').read_text())['dependencies'];result['nodePackages']={}
 for name,version in expected.items():
  p=nm/name/'package.json';actual=json.loads(p.read_text()).get('version') if p.exists() else None
  result['nodePackages'][name]={'expected':version,'actual':actual,'matches':actual==version}
 result['browserConfigured']=bool(cfg.get('browserExecutable'))
 report('doctor.json',result);return result

def setup(install=False):
 media();d=doctor();cfg=config()
 if not all(v['matches'] for v in d['nodePackages'].values()):
  if not install:raise RuntimeError('Missing compatible runtime; review doctor and run setup --install if needed')
  if cfg.get('nodeModules') or (ROOT/'node_modules').is_symlink():raise RuntimeError('Do not overwrite configured/shared runtime; choose a compatible one or independent project')
  run([tool('npm'),'ci','--ignore-scripts','--no-audit','--no-fund'],cwd=ROOT)
 try:import PIL,fontTools
 except ImportError:
  if not install:raise RuntimeError('FontTools/Pillow missing in selected Python')
  p=ROOT/'.venv';venv.EnvBuilder(with_pip=True).create(p);exe=p/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
  run([exe,'-m','pip','install','-r',ROOT/'requirements.txt']);cfg['python']=str(exe);save(ROOT/'runtime.local.json',cfg)
 for folder in ['public','deliverables','qa']: (media()/folder).mkdir(exist_ok=True)
 catalog=json.loads((ROOT/'font-catalog.json').read_text())
 for spec in episode()['fonts'].values():
  dst=asset(spec['file']);entry=catalog.get(spec['file'])
  if dst.exists():
   if sha(dst)!=spec['sha256']:raise RuntimeError('Existing font hash differs; no automatic replacement')
   continue
  if not entry:raise RuntimeError('Custom font missing; import the actual licensed file')
  if not install:raise RuntimeError('Default font missing; setup --install downloads official pinned font')
  dst.parent.mkdir(parents=True,exist_ok=True);tmp=dst.with_suffix('.part')
  try:
   with urllib.request.urlopen(entry['url'],timeout=60) as r,tmp.open('wb') as f:shutil.copyfileobj(r,f)
   if sha(tmp)!=entry['sha256']:raise RuntimeError('Official font bytes changed; review catalog')
   tmp.replace(dst)
  finally:
   if tmp.exists():tmp.unlink()
  if entry.get('licenseUrl'):
   with urllib.request.urlopen(entry['licenseUrl'],timeout=30) as r:dst.with_suffix('.OFL.txt').write_bytes(r.read())
 return doctor()

def demo():
 if not episode().get('demo'):raise ValueError('Refuse demo generation in a production episode')
 (public()/'demo').mkdir(parents=True,exist_ok=True)
 for name,filter_ in [('source','testsrc2=size=1200x900:rate=30:duration=9'),('broll','smptebars=size=1200x900:rate=30:duration=5')]:
  cmd=[ffmpeg(),'-y','-v','error','-f','lavfi','-i',filter_]
  if name=='source':cmd+=['-f','lavfi','-i','sine=frequency=220:sample_rate=48000:duration=9','-map','0:v','-map','1:a','-c:a','aac']
  cmd+=['-c:v','libx264','-preset','fast','-pix_fmt','yuv420p',str(asset('demo/'+name+'.mp4'))];run(cmd)
 return {'note':'Synthetic moving charts and test tone only; not interview, speech or music quality evidence'}

def prepare():
 d=validate(episode());pub=public();pub.mkdir(exist_ok=True);(media()/'deliverables').mkdir(exist_ok=True);(pub/'prepared').mkdir(exist_ok=True)
 qa=media()/'qa';qa.mkdir(exist_ok=True);parts=[];source=asset(d['source']);source_probe=probe(source)
 source_duration=float(source_probe['format']['duration']);has_audio=any(s['codec_type']=='audio' for s in source_probe['streams'])
 if not has_audio:raise ValueError('Interview needs an original audio stream')
 for i,e in enumerate(d['timeline']):
  if e['sourceEnd']>source_duration+1/30:raise ValueError('Source edit exceeds actual source duration')
  out=qa/f'part-{i:03}.mp4';n=e['frames'];duration=n/30;vf=''
  if e.get('crop'):
   x,y,w,h=e['crop'];vf=f'crop={w}:{h}:{x}:{y},'
  vf+=f'setpts=(PTS-STARTPTS)/{d["speed"]},fps=30,scale=1200:900:force_original_aspect_ratio=decrease,pad=1200:900:(ow-iw)/2:(oh-ih)/2,tpad=stop_mode=clone:stop_duration=0.04,trim=end_frame={n},setpts=PTS-STARTPTS'
  af=f'asetpts=PTS-STARTPTS,atempo={d["speed"]},apad,atrim=duration={duration},aresample=48000'
  run([ffmpeg(),'-y','-v','error','-ss',e['sourceStart'],'-t',e['sourceEnd']-e['sourceStart'],'-i',source,'-vf',vf,'-af',af,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2',out]);parts.append(out)
 # Identical shape/codecs permit concat without introducing visual cuts between adjacent samples.
 concat=qa/'parts.txt';concat.write_text('\n'.join("file '"+p.as_posix().replace("'","'\\''")+"'" for p in parts))
 body=asset('prepared/interview.mp4');run([ffmpeg(),'-y','-v','error','-f','concat','-safe','0','-i',concat,'-c','copy',body])
 speech=qa/'speech.wav';run([ffmpeg(),'-y','-v','error','-i',body,'-vn','-af',f'apad,atrim=duration={d["bodyFrames"]/30}', '-ar','48000','-ac','2',speech])
 for i,b in enumerate(d.get('broll',[])):
  n=b['end']-b['start'];b['prepared']=f'prepared/broll-{i}.mp4'
  run([ffmpeg(),'-y','-v','error','-ss',b['sourceStart'],'-i',asset(b['file']),'-an','-vf',f'setpts=(PTS-STARTPTS)/{b.get("rate",1)},fps=30,scale=1200:900:force_original_aspect_ratio=decrease,pad=1200:900:(ow-iw)/2:(oh-ih)/2,trim=end_frame={n},setpts=PTS-STARTPTS','-frames:v',n,'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',asset(b['prepared'])])
 mix=asset('prepared/mix.wav');duration=d['bodyFrames']/30
 if d.get('music'):
  m=d['music'];mdur=float(probe(asset(m['file']))['format']['duration'])
  if m.get('sourceStart',0)+duration>mdur+.03:raise ValueError('Music too short; select a sufficient continuous section, no automatic loop')
  fg=f'[0:a]asplit=2[voice][side];[1:a]atrim=duration={duration},asetpts=PTS-STARTPTS,volume={m.get("gain",.12)},afade=t=in:d=0.6,afade=t=out:st={max(0,duration-.8)}:d=0.8[bed];[bed][side]sidechaincompress=threshold=0.025:ratio=5:attack=15:release=300[duck];[voice][duck]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:latency=1,adelay=100:all=1,apad,atrim=duration={duration+.1}[out]'
  run([ffmpeg(),'-y','-v','error','-i',speech,'-ss',m.get('sourceStart',0),'-i',asset(m['file']),'-filter_complex',fg,'-map','[out]','-ar','48000','-ac','2',mix])
 else:run([ffmpeg(),'-y','-v','error','-i',speech,'-af',f'adelay=100:all=1,apad,atrim=duration={duration+.1}','-ar','48000','-ac','2',mix])
 run([ffmpeg(),'-y','-v','error','-i',body,'-frames:v','1',asset('prepared/cover-source.png')])
 d['mix']='prepared/mix.wav';d['preparedInterview']='prepared/interview.mp4'
 d['mediaManifest']=[{'file':str(p.relative_to(pub)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in [source,body,mix]+[asset(b['prepared']) for b in d.get('broll',[])]]
 save(ROOT/'src/episode.compiled.json',d);report('prepare.json',{'timeline':d['timeline'],'bodyFrames':d['bodyFrames'],'durationInFrames':d['durationInFrames'],'media':d['mediaManifest'],'warnings':d['warnings']})
 for lang in ['zh','en','bilingual']:
  def ts(frame):
   ms=round((frame+3)/30*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
  text='\n\n'.join(f'{i+1}\n{ts(c["start"])} --> {ts(c["end"])}\n'+(c['zh']+'\n'+c['en'] if lang=='bilingual' else c[lang]) for i,c in enumerate(d['captions']))
  (media()/'deliverables'/f'{d["title"]}.{lang}.srt').write_text(text+'\n')
 return {'compiled':str(ROOT/'src/episode.compiled.json'),'frames':d['durationInFrames'],'warnings':d['warnings']}

def final_paths(d,b):
 suffix='（弹幕版）' if b.get('danmaku') else ''
 return media()/'deliverables'/(d['title']+suffix+'.mp4'),media()/'deliverables'/(d['title']+'_封面.png')

def audio_compare(actual,expected):
 from array import array
 def decode(p):
  raw=subprocess.check_output([ffmpeg(),'-v','error','-i',p,'-vn','-ar','8000','-ac','1','-f','s16le','-'])
  out=array('h');out.frombytes(raw);return out
 a,b=decode(actual),decode(expected);n=min(len(a),len(b));energy=sum(x*x for x in b[:n])
 if not energy:raise ValueError('Expected mix is silent; cannot verify audible content by correlation')
 error=sum((a[i]-b[i])**2 for i in range(n));den=math.sqrt(sum(x*x for x in a[:n])*energy)
 corr=sum(a[i]*b[i] for i in range(n))/den if den else 0;relative=math.sqrt(error/energy)
 if abs(len(a)-len(b))>1200 or corr<.98 or relative>.18:raise ValueError('Encoded audio differs from intended full mix')
 return {'correlation':corr,'relativeRmse':relative,'sampleDelta':len(a)-len(b),'note':'Encoding comparison only; does not prove music taste, license or dialogue quality'}

def verify(branch):
 d=json.loads((ROOT/'src/episode.compiled.json').read_text());b=next(x for x in d['branches'] if x['id']==branch);video,cover=final_paths(d,b);p=probe(video);v=next(s for s in p['streams'] if s['codec_type']=='video');a=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
 if (v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames',0)))!=(1080,1920,'30/1',d['durationInFrames']) or not a:raise ValueError('Encoded dimensions/frame rate/frame count/audio mismatch')
 run([ffmpeg(),'-v','error','-xerror','-i',video,'-f','null','-'],stdout=subprocess.DEVNULL)
 from PIL import Image
 import array
 ref=Image.open(cover).convert('RGB').resize((108,192));refvals=list(ref.tobytes());scores=[]
 for f in range(4):
  raw=subprocess.check_output([ffmpeg(),'-v','error','-i',video,'-vf',f'select=eq(n\\,{f}),scale=108:192','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
  err=sum(abs(x-y) for x,y in zip(raw,refvals))/len(refvals);scores.append(err)
 if max(scores[:3])>7 or scores[3]<3:raise ValueError('Cover is not exactly the first three frames')
 result={'file':str(video),'sha256':sha(video),'frames':int(v['nb_frames']),'fullDecode':True,'coverMeanAbsError':scores,'audioDuration':a.get('duration'),'mixSha256':sha(asset(d['mix'])),'encodedAudio':audio_compare(video,asset(d['mix'])),'humanReview':'not implied by technical checks'}
 report('verify-'+branch+'.json',result);return result

def cleanup_plan(files,reason):
 qa=(media()/'qa').resolve();rows=[]
 for raw in files:
  p=Path(raw).absolute()
  if p.name.startswith('._'):raise ValueError('AppleDouble metadata is managed with its ordinary file; do not plan it as an independent asset')
  if p.is_symlink() or not p.resolve().is_relative_to(qa) or not p.is_file():raise ValueError('Only regular qa files may be planned by this helper')
  rows.append({'file':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p),'reason':reason})
 out=ROOT/'cleanup-plan.json';save(out,{'scope':str(qa),'files':rows,'postRenderRequired':True});return {'plan':str(out),'files':rows}

def cleanup(path,execute):
 plan=json.loads(Path(path).read_text());qa=(media()/'qa').resolve();rows=plan['files'];seen=set()
 if Path(plan['scope']).resolve()!=qa:raise ValueError('Plan belongs to another media root')
 for row in rows:
  p=Path(row['file'])
  if str(p) in seen:raise ValueError('Duplicate cleanup target')
  seen.add(str(p))
  if p.name.startswith('._') or p.is_symlink() or not p.resolve().is_relative_to(qa) or not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:raise ValueError('Target changed or outside temporary scope')
  # Prepared/public/deliverables are outside qa; protect explicit retained references too.
  if str(p.resolve()) in episode().get('retainedFiles',[]):raise ValueError('Explicitly retained file')
  if not row.get('reason'):raise ValueError('Deletion reason required')
 # Exact configured references protect qa assets too; dependency analysis beyond JSON is still manual.
 def strings(v):
  if isinstance(v,str):return [v]
  if isinstance(v,list):return [s for x in v for s in strings(x)]
  if isinstance(v,dict):return [s for x in v.values() for s in strings(x)]
  return []
 for value in strings(episode()):
  for row in rows:
   p=Path(row['file']).resolve()
   if value==str(p) or (ROOT/value).resolve()==p or (public()/value).resolve()==p:raise ValueError('Target is referenced by active episode configuration')
 before=shutil.disk_usage(media()).free
 if execute:
  for row in rows:Path(row['file']).unlink()
 result={'executed':execute,'count':len(rows),'logicalBytes':sum(r['bytes'] for r in rows),'freeSpaceDelta':shutil.disk_usage(media()).free-before,'postRenderRequired':True,'files':rows}
 if execute:report('cleanup.json',result)
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True);sub.add_parser('doctor');s=sub.add_parser('setup');s.add_argument('--install',action='store_true');sub.add_parser('demo');sub.add_parser('validate');sub.add_parser('prepare');v=sub.add_parser('verify');v.add_argument('--branch',default='plain');f=sub.add_parser('font-import');f.add_argument('--role',choices=['title','semantic','caption'],required=True);f.add_argument('--file',required=True);f.add_argument('--weight',required=True,type=int);c=sub.add_parser('cleanup-plan');c.add_argument('--file',action='append',required=True);c.add_argument('--reason',required=True);c=sub.add_parser('cleanup');c.add_argument('--plan',required=True);c.add_argument('--execute',action='store_true');a=p.parse_args()
 if a.cmd=='doctor':r=doctor()
 elif a.cmd=='setup':r=setup(a.install)
 elif a.cmd=='demo':r=demo()
 elif a.cmd=='validate':r=validate(episode());report('contract.json',r);r={'frames':r['durationInFrames'],'warnings':r['warnings'],'fonts':r['fontAudit']}
 elif a.cmd=='prepare':r=prepare()
 elif a.cmd=='verify':r=verify(a.branch)
 elif a.cmd=='font-import':r=import_font(a.role,a.file,a.weight)
 elif a.cmd=='cleanup-plan':r=cleanup_plan(a.file,a.reason)
 else:r=cleanup(a.plan,a.execute)
 print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,RuntimeError,FileNotFoundError) as e:raise SystemExit(str(e))
