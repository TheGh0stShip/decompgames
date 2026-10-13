function validDemoSave(bytes){
 if(!Array.isArray(bytes)||bytes.length<514||bytes.length>1048576||!bytes.every(x=>Number.isInteger(x)&&x>=0&&x<=255))return false;
 const u=new Uint8Array(bytes),v=new DataView(u.buffer);if(v.getInt16(0,true)!==-1)return false;
 const count=v.getInt16(2,true),current=v.getInt16(17,true);if(count<0||count>15||current<0||current>count||u[264]!==1)return false;
 for(let offset=29;offset<=239;offset+=21)if(u[offset]>20)return false;
 let pos=512;for(let n=0;n<=count;n++){if(pos+2>u.length)return false;const len=v.getUint16(pos,true);pos+=2;if(len<51||pos+len>u.length)return false;pos+=len;}return pos===u.length;
}
if(typeof module!=="undefined")module.exports={validDemoSave};
