from pathlib import Path
import unittest,sys,copy,tempfile,json,os,subprocess
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/interview-slice-workflow';S=SKILL/'assets/starter/scripts';sys.path.insert(0,str(S));sys.path.insert(0,str(SKILL/'scripts'))
from timeline import build,source_to_body,body_to_source
from contract import validate,intersect
from intake import starts_item,select_doc
from materials import safe_url
BASE=json.loads((SKILL/'assets/starter/episode.json').read_text())
class Workflow(unittest.TestCase):
 def test_multi_cut_map(self):
  rows,n=build([{'sourceStart':10,'sourceEnd':12.2},{'sourceStart':15,'sourceEnd':18.3}]);self.assertEqual(n,150);self.assertEqual(source_to_body(15,rows,1.1,30),60);self.assertAlmostEqual(body_to_source(90,rows,1.1,30),16.1)
 def test_removed_time(self):
  rows,n=build([{'sourceStart':10,'sourceEnd':11}]);self.assertRaises(ValueError,source_to_body,12,rows,1.1,30)
 def test_one_point_two_override(self):
  rows,n=build([{'sourceStart':0,'sourceEnd':12}],1.2);self.assertEqual(n,300)
 def test_invalid_speed(self):
  for s in [0,float('nan'),float('inf'),3]:self.assertRaises(ValueError,build,BASE['edits'],s)
 def test_caption_full_coverage(self):self.assertEqual(validate(copy.deepcopy(BASE),False)['durationInFrames'],243)
 def test_caption_gap(self):
  d=copy.deepcopy(BASE);d['captions'][1]['start']=121;self.assertRaises(ValueError,validate,d,False)
 def test_caption_overlap(self):
  d=copy.deepcopy(BASE);d['captions'][0]['end']=121;self.assertRaises(ValueError,validate,d,False)
 def test_caption_end(self):
  d=copy.deepcopy(BASE);d['captions'][-1]['end']=239;self.assertRaises(ValueError,validate,d,False)
 def test_bilingual_required(self):
  d=copy.deepcopy(BASE);d['captions'][0]['en']='';self.assertRaises(ValueError,validate,d,False)
 def test_caption_pause_punctuation(self):
  d=copy.deepcopy(BASE);d['captions'][0]['zh']+='，';self.assertRaises(ValueError,validate,d,False)
 def test_caption_english_fullstop(self):
  d=copy.deepcopy(BASE);d['captions'][0]['en']+='.';self.assertRaises(ValueError,validate,d,False)
 def test_caption_singleline(self):
  d=copy.deepcopy(BASE);d['captions'][0]['en']+='\nextra';self.assertRaises(ValueError,validate,d,False)
 def test_decimal_preserved(self):
  d=copy.deepcopy(BASE);d['captions'][0]['zh']='达到1.2倍';self.assertEqual(validate(d,False)['bodyFrames'],240)
 def test_cover_exactly_three(self):
  for n in [90,150,2,4]:
   d=copy.deepcopy(BASE);d['coverFrames']=n;self.assertRaises(ValueError,validate,d,False)
 def test_broll_frame_integer(self):
  d=copy.deepcopy(BASE);d['broll'][0]['start']=90.2;self.assertRaises(ValueError,validate,d,False)
 def test_broll_overlap(self):
  d=copy.deepcopy(BASE);d['broll'].append(copy.deepcopy(d['broll'][0]));self.assertRaises(ValueError,validate,d,False)
 def test_broll_identity(self):
  d=copy.deepcopy(BASE);d['broll'][0]['sourceIdentity']='';self.assertRaises(ValueError,validate,d,False)
 def test_short_person_return(self):
  d=copy.deepcopy(BASE);b=copy.deepcopy(d['broll'][0]);d['broll'][0]['end']=110;b.update(start=120,end=225);d['broll'].append(b);self.assertTrue(any(w['kind']=='short-person-return' for w in validate(d,False)['warnings']))
 def test_production_requires_context(self):
  d=copy.deepcopy(BASE);d['demo']=False;self.assertRaises(ValueError,validate,d,False)
 def test_not_skinny_picture(self):
  d=copy.deepcopy(BASE);d['mediaBox']=[90,530,900,506];self.assertRaises(ValueError,validate,d,False)
 def test_explicit_fullscreen_mode(self):
  d=copy.deepcopy(BASE);d['frameMode']='full';d['mediaBox']=[0,0,1080,1920];self.assertEqual(validate(d,False)['bodyFrames'],240)
 def test_number_not_substring(self):self.assertTrue(starts_item('2.1 内容','2.1'));self.assertFalse(starts_item('2.10 内容','2.1'))
 def test_duplicate_items_not_silently_first(self):
  blocks=[{'block_id':'p','block_type':1,'children':['a','b']},{'block_id':'a','block_type':3,'heading1':{'elements':[{'text_run':{'content':'01 第一条'}}]}},{'block_id':'b','block_type':3,'heading1':{'elements':[{'text_run':{'content':'01 第二条'}}]}}];self.assertEqual(len(select_doc(blocks,'01')),2)
 def test_credential_url_redaction(self):
  u=safe_url('https://example.org/path?access_token=secret&id=3&signature=hidden');self.assertNotIn('secret',u);self.assertNotIn('hidden',u);self.assertIn('id=3',u)
 def test_face_rectangle_candidate(self):self.assertTrue(intersect([0,0,20,20],[10,10,20,20]));self.assertFalse(intersect([0,0,20,20],[21,10,20,20]))
 def test_independent_init_and_links(self):
  with tempfile.TemporaryDirectory() as t:
   media=Path(t)/'media';media.mkdir();dst=Path(t)/'code'
   subprocess.run([sys.executable,str(SKILL/'scripts/init_project.py'),str(dst),'--media-root',str(media)],check=True,capture_output=True)
   self.assertTrue((dst/'PRODUCTION_RULES.md').is_file());self.assertTrue((dst/'references/defaults-and-overrides.md').is_file())
   p=subprocess.run([sys.executable,str(SKILL/'scripts/init_project.py'),str(dst),'--media-root',str(media)],capture_output=True);self.assertNotEqual(p.returncode,0)
 def test_missing_media_no_fallback(self):
  with tempfile.TemporaryDirectory() as t:
   dst=Path(t)/'code';p=subprocess.run([sys.executable,str(SKILL/'scripts/init_project.py'),str(dst),'--media-root',str(Path(t)/'absent')],capture_output=True);self.assertNotEqual(p.returncode,0);self.assertFalse(dst.exists())
if __name__=='__main__':unittest.main()

class AssetsAndCleanup(unittest.TestCase):
 def test_danmaku_zero_duration(self):
  d=copy.deepcopy(BASE);d['danmaku'][0]['duration']=0;self.assertRaises(ValueError,validate,d,False)
 def test_cleanup_rejects_changed_file(self):
  import project
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as t:
   media=Path(t);qa=media/'qa';qa.mkdir();p=qa/'old.mp4';p.write_bytes(b'old');plan=media/'plan.json';plan.write_text(json.dumps({'scope':str(qa),'files':[{'file':str(p),'bytes':3,'sha256':project.sha(p),'reason':'obsolete'}]}));p.write_bytes(b'new')
   with patch.object(project,'media',return_value=media):self.assertRaises(ValueError,project.cleanup,plan,True)
   self.assertTrue(p.exists())
 def test_cleanup_rejects_deliverable(self):
  import project
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as t:
   m=Path(t);qa=m/'qa';qa.mkdir();p=m/'final.mp4';p.write_bytes(b'ok');plan=m/'plan.json';plan.write_text(json.dumps({'scope':str(qa),'files':[{'file':str(p),'bytes':2,'sha256':project.sha(p),'reason':'wrong'}]}))
   with patch.object(project,'media',return_value=m):self.assertRaises(ValueError,project.cleanup,plan,True)
   self.assertTrue(p.exists())
 def test_font_glyph_and_hash(self):
  try:
   from fontTools.fontBuilder import FontBuilder
   from fontTools.pens.ttGlyphPen import TTGlyphPen
  except ImportError:self.skipTest('FontTools absent in this interpreter');return
  import fonts
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'font.ttf';fb=FontBuilder(1000,isTTF=True);fb.setupGlyphOrder(['.notdef','A']);fb.setupCharacterMap({65:'A'});pen=TTGlyphPen(None);glyph=pen.glyph();fb.setupGlyf({'.notdef':glyph,'A':glyph});fb.setupHorizontalMetrics({'.notdef':(500,0),'A':(600,0)});fb.setupHorizontalHeader(ascent=800,descent=-200);fb.setupNameTable({'familyName':'SliceTest','styleName':'Bold','uniqueFontIdentifier':'SliceTest','fullName':'SliceTest Bold','psName':'SliceTest-Bold'});fb.setupOS2(usWeightClass=700,sTypoAscender=800,sTypoDescender=-200,usWinAscent=800,usWinDescent=200);fb.setupPost();fb.save(path)
   d=copy.deepcopy(BASE);d['fonts']={k:{'file':'font.ttf','weight':700,'sha256':fonts.sha(path)} for k in ['title','semantic','caption']}
   with patch.object(fonts,'asset',return_value=path),patch.object(fonts,'texts',return_value={'title':'A','semantic':'A','caption':'A'}):self.assertTrue(fonts.audit(d)['title']['glyphCoverage'])
   with patch.object(fonts,'asset',return_value=path),patch.object(fonts,'texts',return_value={'title':'中'}):self.assertRaises(ValueError,fonts.audit,d)
   d['fonts']['title']['sha256']='wrong'
   with patch.object(fonts,'asset',return_value=path),patch.object(fonts,'texts',return_value={'title':'A'}):self.assertRaises(ValueError,fonts.audit,d)

class TitlesAndBranches(unittest.TestCase):
 def test_title_cannot_escape_delivery(self):
  d=copy.deepcopy(BASE);d['title']='../outside';self.assertRaises(ValueError,validate,d,False)
 def test_duplicate_branches_rejected(self):
  d=copy.deepcopy(BASE);d['branches'].append(copy.deepcopy(d['branches'][0]));self.assertRaises(ValueError,validate,d,False)
