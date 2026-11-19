#!/usr/bin/env python3
"""Route project lifecycle and the shared MIT acquisition layer."""
from pathlib import Path
import argparse,json,subprocess,sys
import toolchain,materials,intake
p=argparse.ArgumentParser();p.add_argument('--project',required=True);sub=p.add_subparsers(dest='cmd',required=True)
for c in ['doctor','setup-acquisition','connect','status']:
 s=sub.add_parser(c)
 if c=='connect':s.add_argument('--configure',action='store_true');s.add_argument('--resume')
s=sub.add_parser('intake');s.add_argument('--url',required=True);s.add_argument('--item',required=True);s.add_argument('--section');s.add_argument('--sheet');s.add_argument('--range',default='A1:Z200');s.add_argument('--download',action='store_true')
s=sub.add_parser('search');s.add_argument('query');s.add_argument('--provider',choices=['commons','youtube','brave'],default='commons');s.add_argument('--limit',type=int,default=6)
s=sub.add_parser('import');s.add_argument('file')
s=sub.add_parser('fetch');s.add_argument('url');s.add_argument('--kind',choices=['file','page','video'],required=True);s.add_argument('--height',type=int,default=1080);s.add_argument('--browser');s.add_argument('--max-mb',type=int,default=500)
a=p.parse_args();root=Path(a.project).expanduser().resolve()
if not (root/'episode.json').is_file():p.error('Use init_project.py first; project absent or wrong type')
try:
 if a.cmd=='doctor':
  cfg=json.loads((root/'runtime.local.json').read_text());subprocess.run([cfg.get('python',sys.executable),str(root/'scripts/project.py'),'doctor'],check=True);raise SystemExit(0)
 elif a.cmd=='setup-acquisition':result=toolchain.setup(root)
 elif a.cmd=='connect':toolchain.connect(root,a.configure,a.resume);raise SystemExit(0)
 elif a.cmd=='status':subprocess.run(toolchain.lark(root)+['auth','status'],cwd=root,check=True);raise SystemExit(0)
 elif a.cmd=='intake':result=intake.intake(root,a.url,a.item,a.download,a.sheet,a.range,a.section)
 elif a.cmd=='search':result=materials.search(root,a.query,a.provider,a.limit)
 elif a.cmd=='import':result=materials.import_file(root,a.file)
 elif a.kind=='file':result=materials.direct(root,a.url,a.max_mb)
 elif a.kind=='page':result=materials.page(root,a.url)
 else:result=materials.video(root,a.url,a.height,a.browser,max_mb=a.max_mb)
 print(json.dumps(result,ensure_ascii=False,indent=2))
except (ValueError,RuntimeError) as e:raise SystemExit(str(e))
