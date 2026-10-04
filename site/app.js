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
function draw(){ctx.clearRect(0,0,width,height);ctx.lineWidth=.6;ctx.strokeStyle='#254a3455';for(let x=0;x<width;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,height);ctx.stroke();}for(let y=0;y<height;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(width,y);ctx.stroke();}// Moving wireframe ground, decorative rather than a live activity feed.
const time=angle*3;
ctx.lineWidth=.6;ctx.strokeStyle='#45d38b35';
for(let row=0;row<14;row++){ctx.beginPath();for(let col=0;col<=40;col++){const x=col*width/40,y=height*.73+row*7+Math.sin(col*.25+row*.21+time)*13+Math.cos(col*.4-time)*6;col?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
for(let col=0;col<=40;col+=2){ctx.beginPath();for(let row=0;row<14;row++){const x=col*width/40,y=height*.73+row*7+Math.sin(col*.25+row*.21+time)*13+Math.cos(col*.4-time)*6;row?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.stroke();}
for(let n=0;n<28;n++){const x=(n*97.7)%width,y=(n*43.3+Math.sin(time+n)*9)%height;ctx.fillStyle=n%4?'#65f7ac55':'#94ffcb';ctx.fillRect(x,y,n%4?1:2,n%4?1:2);}
const scale=Math.min(width*.23,height*.27);[1,.8,.6,.4].forEach((ratio,index)=>{const pts=vertices.map(v=>project(v,scale*ratio));ctx.strokeStyle=index?'#4ca27166':'#64f4a5cc';ctx.lineWidth=index?.65:1;edges.forEach(([a,b])=>{ctx.beginPath();ctx.moveTo(...pts[a]);ctx.lineTo(...pts[b]);ctx.stroke();});pts.forEach(([x,y])=>{ctx.shadowBlur=9;ctx.shadowColor='#66f5a9';ctx.fillStyle='#8dffbc';ctx.fillRect(x-1.5,y-1.5,3,3);ctx.shadowBlur=0;});});}
function animate(now){if(now-last>40){angle+=.002;draw();last=now;}raf=requestAnimationFrame(animate);}
function start(){cancelAnimationFrame(raf);draw();if(!motion.matches&&!document.hidden)raf=requestAnimationFrame(animate);}
new ResizeObserver(resize).observe(canvas);motion.addEventListener('change',start);document.addEventListener('visibilitychange',start);start();

// Content remains visible even when JavaScript or animation is unavailable.
const revealObserver=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){if(!motion.matches)entry.target.classList.add('reveal-in');revealObserver.unobserve(entry.target);}}},{threshold:.12});
document.querySelectorAll('.platform-card,.project-card,.credentials article,.writeup-card,.badge-grid article').forEach(el=>revealObserver.observe(el));
const progress=document.querySelector('.scroll-progress');let scrollPending=false;
function updateScroll(){const length=document.documentElement.scrollHeight-innerHeight;progress.style.transform=`scaleX(${length>0?scrollY/length:0})`;scrollPending=false;}
addEventListener('scroll',()=>{if(!scrollPending){scrollPending=true;requestAnimationFrame(updateScroll);}},{passive:true});addEventListener('resize',updateScroll);updateScroll();
const sections=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){nav.querySelectorAll('a').forEach(a=>{if(a.hash==='#'+entry.target.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}}},{rootMargin:'-15% 0px -60% 0px'});
document.querySelectorAll('section[id]').forEach(el=>sections.observe(el));
