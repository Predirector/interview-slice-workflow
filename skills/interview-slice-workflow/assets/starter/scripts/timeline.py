import math

def frames(seconds,fps):return math.floor(seconds*fps+.5)
def build(edits,speed=1.1,fps=30):
 if not math.isfinite(speed) or not .5<=speed<=2:raise ValueError('Unsupported speech speed')
 rows=[];cursor=0
 for e in edits:
  a,b=e['sourceStart'],e['sourceEnd']
  if not (math.isfinite(a) and math.isfinite(b) and 0<=a<b):raise ValueError('Invalid source edit')
  n=frames((b-a)/speed,fps)
  if n<1:raise ValueError('Edit shorter than a frame')
  rows.append({**e,'bodyStart':cursor,'bodyEnd':cursor+n,'frames':n});cursor+=n
 if not rows:raise ValueError('At least one verbatim edit required')
 return rows,cursor

def source_to_body(t,rows,speed,fps):
 for i,e in enumerate(rows):
  if e['sourceStart']<=t<e['sourceEnd'] or i==len(rows)-1 and t==e['sourceEnd']:
   return min(e['bodyEnd'],e['bodyStart']+frames((t-e['sourceStart'])/speed,fps))
 raise ValueError('Source time was removed; no body frame exists')

def body_to_source(f,rows,speed,fps):
 for e in rows:
  if e['bodyStart']<=f<e['bodyEnd']:return e['sourceStart']+(f-e['bodyStart'])/fps*speed
 raise ValueError('Body frame outside timeline')
