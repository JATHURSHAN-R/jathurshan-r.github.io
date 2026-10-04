'use strict';
const menuButton=document.querySelector('#menu-button'),nav=document.querySelector('#navigation');
menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}));
const dialog=document.querySelector('#evidence-dialog');let lastTrigger;
document.querySelectorAll('[data-evidence]').forEach(button=>button.addEventListener('click',()=>{lastTrigger=button;const image=document.querySelector('#evidence-image');image.src='assets/'+button.dataset.evidence;image.alt=button.dataset.title;document.querySelector('#evidence-title').textContent=button.dataset.title;dialog.showModal();}));
document.querySelector('#close-dialog').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
dialog.addEventListener('close',()=>lastTrigger?.focus());
// Abstract network geometry, independent of visitor data or lab activity.
const canvas=document.querySelector('#network'),ctx=canvas.getContext('2d'),motion=matchMedia('(prefers-reduced-motion: reduce)');
let width=0,height=0,angle=.55,raf,last=0;
const vertices=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]];
const edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
function resize(){const r=canvas.getBoundingClientRect();width=r.width;height=r.height;const d=Math.min(devicePixelRatio||1,2);canvas.width=width*d;canvas.height=height*d;ctx.setTransform(d,0,0,d,0,0);draw();}
function project(v,scale){const x=v[0]*Math.cos(angle)-v[2]*Math.sin(angle),z=v[0]*Math.sin(angle)+v[2]*Math.cos(angle),y=v[1]*.87-z*.48;return[width*.58+x*scale,height*.48+y*scale];}
function draw(){ctx.clearRect(0,0,width,height);ctx.lineWidth=.6;ctx.strokeStyle='#254a3455';for(let x=0;x<width;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,height);ctx.stroke();}for(let y=0;y<height;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(width,y);ctx.stroke();}const scale=Math.min(width*.17,height*.29);[1,.67,.34].forEach((ratio,index)=>{const pts=vertices.map(v=>project(v,scale*ratio));ctx.strokeStyle=index?'#4ca27166':'#64f4a5cc';ctx.lineWidth=index?.65:1;edges.forEach(([a,b])=>{ctx.beginPath();ctx.moveTo(...pts[a]);ctx.lineTo(...pts[b]);ctx.stroke();});pts.forEach(([x,y])=>{ctx.shadowBlur=9;ctx.shadowColor='#66f5a9';ctx.fillStyle='#8dffbc';ctx.fillRect(x-1.5,y-1.5,3,3);ctx.shadowBlur=0;});});}
function animate(now){if(now-last>40){angle+=.002;draw();last=now;}raf=requestAnimationFrame(animate);}
function start(){cancelAnimationFrame(raf);draw();if(!motion.matches&&!document.hidden)raf=requestAnimationFrame(animate);}
new ResizeObserver(resize).observe(canvas);motion.addEventListener('change',start);document.addEventListener('visibilitychange',start);start();
