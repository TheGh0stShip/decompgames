// Independent CC0 block glyphs drawn by an authored MIT renderer. No system game font or image input.
window.drawSurveyTerminal=function(cells,rows,cols){
 const canvas=document.querySelector('#board');if(!canvas)return;
 const context=canvas.getContext('2d');context.imageSmoothingEnabled=false;
 context.fillStyle='#0c151d';context.fillRect(0,0,canvas.width,canvas.height);
 for(let y=0;y<rows;y++)for(let x=0;x<cols;x++){
  const code=cells[y*80+x],char=String.fromCharCode(code&255),bits=SurveyGlyphs[char];
  if(!bits)throw Error('Unsupported game glyph '+(code&255));
  let ink=y===0||y===23?'#d5e5e3':char==='@'?'#88e2d2':/[A-Z]/.test(char)?'#f4ad6e':'|+-'.includes(char)?'#668c9c':'#b1c2c7';
  if(code&256){context.fillStyle='#315763';context.fillRect(x*10,y*14,10,14);ink='#fff1c7';}
  context.fillStyle=ink;
  for(let row=0;row<5;row++)for(let col=0;col<3;col++)if(bits[row*3+col]==='1')context.fillRect(x*10+2+col*2,y*14+2+row*2,2,2);
 }
};
