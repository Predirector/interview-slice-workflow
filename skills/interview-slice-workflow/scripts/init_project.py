#!/usr/bin/env python3
from pathlib import Path
import argparse,shutil,json,os
p=argparse.ArgumentParser(description="Create a new editable slice project without overwriting")
p.add_argument('destination');p.add_argument('--media-root',required=True);a=p.parse_args()
dst=Path(a.destination).expanduser().resolve();media=Path(a.media_root).expanduser().resolve()
if dst.exists():p.error('Destination exists; migration requires an explicit plan, not overwrite')
if not media.is_dir() or not os.access(media,os.W_OK):p.error('Media root must already exist and be writable')
if dst==media or dst.is_relative_to(media):p.error('Keep code separate from the media root')
skill=Path(__file__).resolve().parents[1];shutil.copytree(skill/'assets/starter',dst)
shutil.copytree(skill/'references',dst/'references')
for source,target in [('production-rules.md','PRODUCTION_RULES.md'),('implementation-matrix.md','IMPLEMENTATION_MATRIX.md')]:
 text=(skill/'references'/source).read_text().replace('同目录 implementation-matrix.md','IMPLEMENTATION_MATRIX.md')
 (dst/target).write_text(text)
(dst/'runtime.local.json').write_text(json.dumps({'mediaRoot':str(media)},ensure_ascii=False,indent=2))
print(json.dumps({'project':str(dst),'mediaRoot':str(media),'next':'Run scripts/project.py doctor, then review and reuse tools before setup'},ensure_ascii=False))
