import fs from 'node:fs';import path from 'node:path';import {createRequire}from'node:module';import{fileURLToPath}from'node:url';import{spawnSync}from'node:child_process';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));process.chdir(root);
const cfg=JSON.parse(fs.readFileSync('runtime.local.json')),d=JSON.parse(fs.readFileSync('src/episode.compiled.json')),args=process.argv.slice(2),branch=args.find(x=>!x.startsWith('-'))||'plain',cover=args.includes('--cover'),idx=args.indexOf('--frames'),frames=idx>=0?args[idx+1]:null,stillIdx=args.indexOf('--still'),still=stillIdx>=0?Number(args[stillIdx+1]):null;
const nm=path.resolve(cfg.nodeModules||'node_modules'),req=createRequire(path.join(nm,'@remotion/renderer/package.json'));
const{bundle}=req('@remotion/bundler'),{selectComposition,renderMedia,renderStill}=req('@remotion/renderer');
for(const [name,version]of Object.entries(JSON.parse(fs.readFileSync('package.json')).dependencies)){if(JSON.parse(fs.readFileSync(path.join(nm,name,'package.json'))).version!==version)throw Error('Incompatible runtime '+name)}
const media=process.env.SLICE_MEDIA_ROOT||cfg.mediaRoot;if(!media||!fs.existsSync(media))throw Error('Media root absent; no fallback');
const pub=path.join(media,'public'),qa=path.join(media,'qa'),out=path.join(media,'deliverables');fs.mkdirSync(qa,{recursive:true});fs.mkdirSync(out,{recursive:true});
const browserExecutable=cfg.browserExecutable||process.env.REMOTION_BROWSER_EXECUTABLE;
const serveUrl=await bundle({entryPoint:path.join(root,'src/Root.tsx'),publicDir:pub,webpackOverride:c=>({...c,resolve:{...c.resolve,modules:[nm,'node_modules']}})});
const composition=await selectComposition({serveUrl,id:cover?'cover':branch,browserExecutable});
if(still!==null){await renderStill({serveUrl,composition,output:path.join(qa,`still-${branch}-${still}.png`),frame:still,imageFormat:'png',browserExecutable});}
else if(cover){await renderStill({serveUrl,composition,output:path.join(out,d.title+'_封面.png'),imageFormat:'png',browserExecutable});}
else{const b=d.branches.find(b=>b.id===branch);if(!b)throw Error('Unknown retained branch');const target=frames?path.join(qa,'render-check-'+branch+'.mp4'):path.join(out,d.title+(b.danmaku?'（弹幕版）':'')+'.mp4');const range=frames?frames.split('-').map(Number):undefined;
 await renderMedia({serveUrl,composition,outputLocation:target,codec:'h264',audioCodec:'aac',crf:18,concurrency:1,browserExecutable,frameRange:range,logLevel:'error'});console.log(JSON.stringify({output:target,check:!!frames}));}
