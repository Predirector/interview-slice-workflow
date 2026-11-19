from pathlib import Path
import os,json,hashlib,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
def config():
 p=ROOT/'runtime.local.json'
 return json.loads(p.read_text()) if p.exists() else {}
def save(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(d,ensure_ascii=False,indent=2));t.replace(p)
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def media():
 value=os.environ.get('SLICE_MEDIA_ROOT') or config().get('mediaRoot')
 if not value:raise RuntimeError('Set an existing mediaRoot in runtime.local.json; no implicit internal-disk fallback')
 p=Path(value).expanduser().resolve()
 if not p.is_dir() or not os.access(p,os.W_OK):raise RuntimeError('Configured media root absent or not writable; reconnect it before writing')
 return p
def public():return media()/'public'
def asset(rel):
 if not isinstance(rel,str) or Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('Asset must be relative to media public')
 p=(public()/rel).resolve()
 if not p.is_relative_to(public().resolve()):raise ValueError('Asset escapes public media')
 return p
def tool(name):
 p=os.environ.get('SLICE_'+name.upper()) or config().get(name) or shutil.which(name)
 if not p or not Path(p).is_file():raise RuntimeError('Missing '+name+': configure an existing compatible tool or install it')
 return str(Path(p).resolve())
def ffmpeg():return tool('ffmpeg')
def tool_env(exe=None):return os.environ.copy()
def run(args,**kw):return subprocess.run([str(x) for x in args],check=True,**kw)
def probe(path):return json.loads(subprocess.check_output([tool('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
def episode():return json.loads((ROOT/'episode.json').read_text())
def report(name,d):save(ROOT/'reports'/name,d)
