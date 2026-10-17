(function(){
var K='nyc-days-v1',st={};try{st=JSON.parse(localStorage.getItem(K)||'{}');}catch(e){}
function save(){try{localStorage.setItem(K,JSON.stringify(st));}catch(e){}}
var tabs=[].slice.call(document.querySelectorAll('.dtabs [role=tab]')),cur=-1;
function sel(i,focus){if(i<0||i>=tabs.length)return;tabs.forEach(function(t,j){var on=j===i;t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!on;});if(focus)tabs[i].focus();try{tabs[i].scrollIntoView({block:'nearest',inline:'center'});}catch(e){}cur=i;}
tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(i);});t.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){sel(i+1,1);e.preventDefault();}if(e.key==='ArrowLeft'){sel(i-1,1);e.preventDefault();}});});
document.querySelectorAll('.pn').forEach(function(b){b.addEventListener('click',function(){sel(+b.dataset.go);window.scrollTo(0,0);});});
document.querySelectorAll('input[data-k]').forEach(function(c){c.checked=!!st[c.dataset.k];c.addEventListener('change',function(){st[c.dataset.k]=c.checked;document.querySelectorAll('input[data-k="'+c.dataset.k+'"]').forEach(function(o){o.checked=c.checked;});save();});});
function paintDone(p){p.querySelectorAll('.stop').forEach(function(li){var b=li.querySelector('.done'),on=!!st[b.dataset.k];b.setAttribute('aria-pressed',on);li.classList.toggle('is-done',on);p.querySelectorAll('.dpin[data-n="'+li.dataset.n+'"]').forEach(function(g){g.classList.toggle('is-done',on);});});}
document.querySelectorAll('.dpanel').forEach(function(p){
 p.querySelectorAll('.done').forEach(function(b){b.addEventListener('click',function(){st[b.dataset.k]=!st[b.dataset.k];save();paintDone(p);live();});});
 paintDone(p);
 function go(n){var li=p.querySelector('.stop[data-n="'+n+'"]');if(!li)return;p.querySelectorAll('.stop.hl').forEach(function(x){x.classList.remove('hl');});li.classList.add('hl');li.scrollIntoView({behavior:'smooth',block:'center'});}
 p.querySelectorAll('.dpin').forEach(function(g){g.addEventListener('click',function(){go(g.dataset.n);});g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go(g.dataset.n);}});});
 var x0=null,y0=null;p.addEventListener('touchstart',function(e){if(e.target.closest('svg,a,button,input,label'))return;x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
 p.addEventListener('touchend',function(e){if(x0==null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;x0=null;if(Math.abs(dx)>70&&Math.abs(dx)>2*Math.abs(dy)){sel(cur+(dx<0?1:-1));}},{passive:true});
});
function nyNow(){var q=(location.search.match(/[?&]now=([^&]+)/)||[])[1];if(q){q=decodeURIComponent(q);return {d:q.slice(0,10),m:+q.slice(11,13)*60+ +q.slice(14,16)};}
 try{var f={};new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date()).forEach(function(x){f[x.type]=x.value;});return {d:f.year+'-'+f.month+'-'+f.day,m:+f.hour*60+ +f.minute};}catch(e){return null;}}
var days=[].slice.call(document.querySelectorAll('.dpanel[data-date]'));
function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function live(){var n=nyNow(),tm=document.getElementById('tripmode');days.forEach(function(p){p.querySelector('.live').hidden=true;p.querySelectorAll('.is-now').forEach(function(x){x.classList.remove('is-now');});});
 if(!n)return -1;var di=-1,m=n.m;days.forEach(function(p,i){if(p.dataset.date===n.d)di=i;});
 if(di>0&&m<240){di-=1;m+=1440;}
 if(di<0){tm.textContent=n.d<'2026-12-31'?'Trip mode turns on Dec 31: this page will open on that day and show what\u2019s next.':'';return -1;}
 tm.textContent='';var p=days[di],stops=[].slice.call(p.querySelectorAll('.stop')),now=null,next=null;
 stops.forEach(function(li){if(+li.dataset.min<=m)now=li;});
 for(var i=0;i<stops.length;i++){var li=stops[i];if(+li.dataset.min>m&&!st[li.querySelector('.done').dataset.k]){next=li;break;}}
 var box=p.querySelector('.live'),h='<div class="lrow">';
 if(now){now.classList.add('is-now');p.querySelectorAll('.dpin[data-n="'+now.dataset.n+'"]').forEach(function(g){g.classList.add('is-now');});h+='<div><div class="lk">Now</div><div class="lv">'+esc(now.dataset.time)+' · '+esc(now.dataset.name)+'</div></div>';}
 if(next){h+='<div><div class="lk">Up next</div><div class="lv">'+esc(next.dataset.time)+' · '+esc(next.dataset.name)+'</div><div>'+esc(next.dataset.how)+(next.dataset.g?' · <a href="'+esc(next.dataset.g)+'" target="_blank" rel="noopener">Directions</a>':'')+'</div></div>';}
 else h+='<div><div class="lk">Up next</div><div class="lv">That\u2019s the day. Sweet dreams.</div></div>';
 h+='</div><button type="button" class="jump">Jump to now</button>';box.innerHTML=h;box.hidden=false;
 box.querySelector('.jump').addEventListener('click',function(){var t=p.querySelector('.stop.is-now')||next;if(t)t.scrollIntoView({behavior:'smooth',block:'center'});});
 return di;}
var di=live();sel(di>=0?di+1:1);setInterval(live,60000);
})();
