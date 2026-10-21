// Story Jigsaw Tales — add-on features: gentle hint, storybook mode, stickers,
// text size, ad placement hooks (no SDK on web) and offline service worker.
(function(){
'use strict';
const FT=en=>{if(gameLang==='en')return en;const v=TR(en,1);return v==null?en:v;};
const $=id=>document.getElementById(id);
const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;};
const menuVisible=()=>!document.getElementById('menu').classList.contains('hide');

/* ---------- 1. Gentle hint: wiggle a misplaced piece, glow its home ---------- */
let wiggleAt=0;
function gentleHint(){
 if(!playing||boardIntroActive)return;
 const kids=document.getElementById('board').children,wrong=[];
 for(let i=0;i<tiles.length;i++)if(!locked[i]&&tiles[i]!==i)wrong.push(i);
 if(!wrong.length)return;
 const from=wrong[Math.floor(Math.random()*wrong.length)],home=tiles[from];
 const a=kids[from],b=kids[home];if(!a||!b)return;
 wiggleAt=Date.now();
 a.classList.remove('sj-wiggle');b.classList.remove('sj-home');void a.offsetWidth;
 a.classList.add('sj-wiggle');b.classList.add('sj-home');
 storyToast(FT('Look! This piece belongs in the glowing spot'));
 setTimeout(()=>{a.classList.remove('sj-wiggle');b.classList.remove('sj-home');},2600);
}
window.gentleHint=gentleHint;
const wiggleBtn=el('button',null,'👀');wiggleBtn.id='helpWiggle';
const helpPlace=$('helpPlace');helpPlace.before(wiggleBtn);
wiggleBtn.onclick=()=>{helpers.close();gentleHint();};
const baseHelpers=openStoryHelpers;
openStoryHelpers=function(){
 baseHelpers();if(!helpers.open)return;
 wiggleBtn.textContent=FT('👀 Show me a piece');
 // (a) Rewarded placement: opt-in only, clearly labelled, never automatic.
 if(window.AndroidAds&&AndroidAds.showRewarded)helpers.querySelector('p').textContent=FT('Optional: watch a short ad for one extra hint');
};
$('hintBtn').onclick=()=>openStoryHelpers();

/* ---------- 2. Stickers for finishing a story on Hard ---------- */
const STICKERS={lantern16:'🏮',moonturtle16:'🐢',ricepot16:'🍚',kite16:'🪁',seasons16:'🌳',snowfox16:'🦊'};
function hasSticker(id){const b=STORY_CATALOG[id];if(!b)return false;const n=b.images.length;const d=new Set(readProgress('lsj-story-'+id+'-done-hard').split(',').map(Number).filter(x=>x>=1&&x<=n));return d.size===n;}
function stickerNode(id){
 const b=STORY_CATALOG[id],got=hasSticker(id),s=el('div','sj-sticker'+(got?' got':''));
 const face=el('span','sj-sticker-face',got?STICKERS[id]:'?');if(got)face.style.backgroundImage='url("'+b.images[b.images.length-1]+'")';
 s.append(face,el('small',null,(b.titles&&b.titles[gameLang])||b.title||''));
 const name=(b.titles&&b.titles[gameLang])||b.title||'';s.title=got?name:name+' · '+FT('Finish a story on Hard to earn its sticker');s.setAttribute('role','img');s.setAttribute('aria-label',s.title);return s;
}
function stickerShelf(){
 const sec=el('section');sec.id='stickerShelf';sec.append(el('h3',null,'⭐ '+FT('Stickers')));
 const row=el('div','sj-sticker-row');for(const id of Object.keys(STICKERS))if(STORY_CATALOG[id])row.append(stickerNode(id));
 sec.append(row);const got=Object.keys(STICKERS).filter(hasSticker).length;
 sec.append(el('p','sj-sticker-tip',got+' / '+Object.keys(STICKERS).length+' · '+FT('Finish a story on Hard to earn its sticker')));return sec;
}

/* ---------- 3. Storybook: read the whole story ---------- */
const book=el('dialog','story-dialog');book.id='storyBook';document.body.append(book);
let bookPage=0,bookAuto=false,bookTimer=null;
function bookText(n){const c=STORY_DATA.chapters[n];return c[2]+' '+c[3];}
function stopBook(){bookAuto=false;clearTimeout(bookTimer);stopNarration();}
function renderBook(){
 const n=bookPage,count=storyCount(),c=STORY_DATA.chapters[n];
 book.innerHTML='';
 const top=el('div','album-top');top.append(el('small',null,STORY_DATA.title),el('button',null,TR('Close ✕')));top.lastChild.id='bookClose';
 const img=el('img','sb-img');img.src=STORY_DATA.images[n];img.alt=c[0];
 const body=el('div','sb-body');body.append(el('h2',null,(n+1)+'. '+c[0]),el('p','sb-text',bookText(n)));
 if(n===count-1)body.append(el('p','sb-end','✨ '+FT('The End')+' ✨'));
 const nav=el('div','album-actions sb-nav');
 const prev=el('button',null,TR('‹ Previous')),pg=el('span',null,(n+1)+' / '+count),next=el('button',null,TR('Next ›'));
 prev.disabled=n===0;next.disabled=n>=count-1;nav.append(prev,pg,next);
 const tools=el('div','sb-tools');const listen=el('button',null,TR('🔊 Listen')),auto=el('button',null,bookAuto?FT('⏸ Pause'):FT('▶ Read to me'));listen.id='bookListen';auto.id='bookAuto';tools.append(listen,auto);
 book.append(top,img,body,tools,nav);
 top.lastChild.onclick=()=>book.close();
 prev.onclick=()=>{const a=bookAuto;stopBook();bookPage--;renderBook();if(a)startAuto();};
 next.onclick=()=>{const a=bookAuto;stopBook();bookPage++;renderBook();if(a)startAuto();};
 listen.onclick=()=>{stopBook();renderBook();narrateStory(bookText(bookPage),true);};
 auto.onclick=()=>{if(bookAuto){stopBook();renderBook();}else startAuto();};
}
function startAuto(){
 bookAuto=true;renderBook();const page=bookPage;
 narrateStory(bookText(page),true,spoke=>{
  if(!bookAuto||bookPage!==page||!book.open)return;
  const wait=spoke?900:Math.max(3500,Math.min(11000,bookText(page).length*70));
  bookTimer=setTimeout(()=>{if(!bookAuto||!book.open)return;if(bookPage<storyCount()-1){bookPage++;startAuto();}else{bookAuto=false;renderBook();}},wait);
 });
}
function openStoryBook(){
 stopNarration();if(album.open)album.close();if($('settingsDialog'))$('settingsDialog').close();
 bookPage=0;bookAuto=false;renderBook();book.showModal();lastBanner=null;syncBanner();
}
book.addEventListener('close',()=>{stopBook();syncBanner();});
window.openStoryBook=openStoryBook;
const baseRead=readCollectedStory;
readCollectedStory=function(){if(collectedStory().size===storyCount())openStoryBook();else baseRead();};

/* Album: storybook button, stickers; (c) banner allowed on album */
const baseAlbum=openStoryAlbum;
openStoryAlbum=function(){
 baseAlbum();
 if(collectedStory().size===storyCount()){const r=album.querySelector('.story-collection');if(r)r.textContent=FT('✨ Read the whole story');}
 const badges=$('albumBadges');if(badges&&!$('stickerShelf'))badges.after(stickerShelf());
 syncBanner();
};
$('openStoryAlbum').onclick=()=>openStoryAlbum();

/* Result screen after the ending: storybook + sticker reward */
const baseSummary=renderStorySummary;
renderStorySummary=function(){
 baseSummary();const sec=$('storySummary');if(!sec||!storyMode)return;
 if(storyDoneFor(level).size!==storyCount())return;
 const read=el('button','story-collection sj-read-all',FT('✨ Read the whole story'));read.onclick=()=>{$('win').classList.remove('show');play.classList.remove('win-open');openStoryBook();};
 sec.querySelector('h3').after(read);
 if(level==='hard'&&hasSticker(STORY_DATA.id)){
  const s=stickerNode(STORY_DATA.id);s.classList.add('sj-new');read.after(s);
  const key='lsj-sticker-seen-'+STORY_DATA.id;if(!readProgress(key)){writeProgress(key,'1');storyToast(FT('New sticker! 🎉'));}
 }
};

/* ---------- 4. Text size (persists) ---------- */
function applyTextSize(v){if(!['s','m','l'].includes(v))v='m';document.documentElement.dataset.text=v;}
applyTextSize(readProgress('lsj-text-size')||'m');
const baseSettings=openGameSettings;
openGameSettings=function(){
 baseSettings();const d=$('settingsDialog');if(!d||$('textSizeRow'))return;
 const row=el('div','sj-textsize');row.id='textSizeRow';row.append(el('span',null,FT('Text size')));
 const group=el('div','sj-textsize-btns');group.setAttribute('role','radiogroup');group.setAttribute('aria-label',FT('Text size'));
 for(const v of ['s','m','l']){const b=el('button','sj-ts-'+v,'A');b.type='button';b.setAttribute('role','radio');b.setAttribute('aria-label',FT('Text size')+' '+({s:1,m:2,l:3})[v]+'/3');
  const sync=()=>group.querySelectorAll('button').forEach(x=>x.setAttribute('aria-checked',String(x===group.querySelector('.sj-ts-'+document.documentElement.dataset.text))));
  b.onclick=()=>{applyTextSize(v);writeProgress('lsj-text-size',v);sync();};group.append(b);}
 row.append(group);const p=d.querySelector(':scope>p');(p||d.querySelector('button')).before(row);
 group.querySelectorAll('button').forEach(x=>x.setAttribute('aria-checked',String(x.classList.contains('sj-ts-'+document.documentElement.dataset.text))));
};
document.querySelectorAll('button').forEach(b=>{if(b.onclick===baseSettings)b.onclick=()=>openGameSettings();});


/* ---------- 6. Banner placement: menu, album and puzzle board ----------
   Shown on menu/album and on the gameplay board in its own reserved strip
   (screens shrink via --ad-space; a 16px gap + separator sits above it).
   Hidden on results, story scenes and the storybook. Made non-interactive
   while a piece is touched and for 500ms after release. */
const playEl=document.getElementById('play'),winEl=document.getElementById('win'),cinemaEl=document.getElementById('storyCinema');
function playVisible(){return !playEl.classList.contains('hide')&&!playEl.hidden;}
function wantBanner(){
 if(book.open||(cinemaEl&&!cinemaEl.hidden)||document.getElementById('inter')?.classList.contains('show'))return false;
 if(menuVisible())return true;
 return playVisible()&&!playEl.classList.contains('win-open')&&!winEl.classList.contains('show');
}
let lastBanner=null;
function syncBanner(){
 const v=wantBanner(),onPlay=v&&playVisible();
 document.documentElement.classList.toggle('sj-play-banner',onPlay);
 if(v!==lastBanner){lastBanner=v;nativeBanner(v);}
}
window.syncBanner=syncBanner;
const baseShow2=show;show=function(el){baseShow2(el);lastBanner=null;syncBanner();};
const mo=new MutationObserver(()=>syncBanner());
for(const n of [playEl,winEl,cinemaEl,document.getElementById('inter'),document.getElementById('menu')])if(n)mo.observe(n,{attributes:true,attributeFilter:['class','hidden']});
let touchTimer=null,bannerLocked=false;
function setBannerTouchable(on){
 if(bannerLocked===!on)return;bannerLocked=!on;
 try{if(window.AndroidAds&&AndroidAds.setBannerTouchable)AndroidAds.setBannerTouchable(on);}catch(e){}
 document.documentElement.classList.toggle('sj-banner-locked',!on);
}
window.sjBannerTouchable=()=>!bannerLocked;
playEl.addEventListener('pointerdown',()=>{clearTimeout(touchTimer);setBannerTouchable(false);},{capture:true,passive:true});
const release=()=>{clearTimeout(touchTimer);touchTimer=setTimeout(()=>setBannerTouchable(true),500);};
for(const t of ['pointerup','pointercancel','lostpointercapture'])document.addEventListener(t,release,{capture:true,passive:true});
syncBanner();

/* ---------- 5. Offline play: service worker with versioned cache ---------- */
if('serviceWorker' in navigator&&(location.protocol==='https:'||location.hostname==='localhost'||location.hostname==='127.0.0.1')&&!/[?&]nosw=1/.test(location.search)){
 window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').then(r=>{r.update&&r.update();}).catch(()=>{});});
}
})();
