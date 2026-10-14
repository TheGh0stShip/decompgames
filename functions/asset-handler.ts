import type { PagesFunction, R2Bucket } from '@cloudflare/workers-types';
declare const Response: typeof import('@cloudflare/workers-types').Response;
declare const Headers: typeof import('@cloudflare/workers-types').Headers;
interface Env { GAME_ASSETS: R2Bucket }
const types:Record<string,string>={wasm:'application/wasm',html:'text/html; charset=utf-8',js:'text/javascript; charset=utf-8',json:'application/json',ini:'text/plain',txt:'text/plain',gz:'application/gzip',zip:'application/zip'};
export const serveAsset:PagesFunction<Env>=async ({request,env})=>{
 if(!['GET','HEAD','OPTIONS'].includes(request.method))return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD, OPTIONS'}});
 const origin=request.headers.get('Origin');const allowed=['https://decompgames.com','https://play.decompgames.com','https://decompgames.pages.dev'];
 const cors:Record<string,string>=origin&&allowed.includes(origin)?{'Access-Control-Allow-Origin':origin,'Vary':'Origin'}:{};
 if(request.method==='OPTIONS')return new Response(null,{status:204,headers:{...cors,'Access-Control-Allow-Methods':'GET, HEAD, OPTIONS','Access-Control-Allow-Headers':'Range'}});
 const key=decodeURIComponent(new URL(request.url).pathname.slice(1));if(!/^(runtime|data|sources)\//.test(key)||key.includes('..'))return new Response('Not found',{status:404});
 const object=await env.GAME_ASSETS.get(key,{range:request.headers,onlyIf:request.headers});
 if(!object)return new Response('Not found',{status:404});
 const headers=new Headers(cors);object.writeHttpMetadata(headers);headers.set('Content-Type',types[key.split('.').pop()!]||'application/octet-stream');headers.set('ETag',object.httpEtag);headers.set('Accept-Ranges','bytes');headers.set('X-Content-Type-Options','nosniff');headers.set('X-Robots-Tag','noindex');headers.set('Cache-Control',key.startsWith('runtime/')||key.startsWith('sources/')?'public, max-age=31536000, immutable':'public, max-age=3600');
 if(!('body' in object))return new Response(null,{status:304,headers});
 let status=200;if(object.range){const range=object.range as {offset:number;length:number};headers.set('Content-Range',`bytes ${range.offset}-${range.offset+range.length-1}/${object.size}`);headers.set('Content-Length',String(range.length));status=206;}else headers.set('Content-Length',String(object.size));
 return new Response(request.method==='HEAD'?null:object.body,{status,headers});
};
