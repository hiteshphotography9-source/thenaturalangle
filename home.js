(function(){
  var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hd=document.getElementById('hd');
  function onScroll(){hd.classList.toggle('sc',scrollY>40);}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  var io=('IntersectionObserver' in window)&&!RM?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -10% 0px'}):null;
  document.querySelectorAll('.rv,mark').forEach(function(el){ if(io) io.observe(el); else el.classList.add('in'); });
  // stagger grid children
  document.querySelectorAll('.tr,.gdg,.rlg,.bdg,.stats').forEach(function(g){[].forEach.call(g.children,function(c,i){c.style.transitionDelay=(i%3)*90+'ms';});});
  // parallax hero + hotel band
  if(!RM){var hb=document.querySelector('.hotel>img'),hc=document.querySelector('.hc');
    addEventListener('scroll',function(){var y=scrollY;if(hc&&y<innerHeight)hc.style.transform='translateY('+y*.25+'px)';if(hc)hc.style.opacity=Math.max(0,1-y/(innerHeight*.8));
      if(hb){var r=hb.parentElement.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)hb.style.transform='scale(1.1) translateY('+(r.top*-.08)+'px)';}},{passive:true});}
  // active section in nav
  var links=[].slice.call(document.querySelectorAll('.tn a[href^="#"],.bn a[href^="#"]'));
  if('IntersectionObserver' in window){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var id='#'+e.target.id;links.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')===id||(id==='#top'&&a.getAttribute('href')==='#top'));});}});},{rootMargin:'-45% 0px -50% 0px'});
    ['tours','watch','learn','ebooks'].forEach(function(i){var s=document.getElementById(i);if(s)so.observe(s);});}
})();
/* Live feed: YouTube + Instagram from data/feed.json (refreshed every 3 hours by GitHub Actions) */
(function(){
  function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function dt(s){try{return new Date(s).toLocaleDateString('en-IN',{day:'numeric',month:'short'});}catch(e){return '';}}
  function th(id,q){return 'https://i.ytimg.com/vi/'+id+'/'+(q||'hqdefault')+'.jpg';}
  function seen(root){ if(!('IntersectionObserver' in window)){root.querySelectorAll('.rv,mark').forEach(function(e){e.classList.add('in');});return;}
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});});root.querySelectorAll('.rv').forEach(function(e){io.observe(e);}); }
  fetch('data/feed.json?t='+Math.floor(Date.now()/600000)).then(function(r){return r.json();}).then(function(d){
    var y=d.youtube||{},L=y.long||[],S=y.shorts||[],wg=document.querySelector('.wg'),sh=document.querySelector('.shorts'),rl=document.querySelector('.rlg');
    if(wg&&L.length){var f=L[0];
      wg.innerHTML='<a class="feat" href="https://www.youtube.com/watch?v='+f.id+'"><img src="'+th(f.id,'maxresdefault')+'" onerror="this.src=\''+th(f.id)+'\'" alt="'+esc(f.title)+'"><span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span><div class="fcap"><span class="chip">New · '+dt(f.published)+'</span><h3>'+esc(f.title)+'</h3></div></a><div class="vlist">'+
      L.slice(1,4).map(function(v){return '<a class="vrow rv" href="https://www.youtube.com/watch?v='+v.id+'"><img loading="lazy" src="'+th(v.id,'mqdefault')+'" alt=""><span><b>'+esc(v.title)+'</b><small>Video · '+dt(v.published)+'</small></span></a>';}).join('')+'</div>';seen(wg);}
    if(sh&&S.length){sh.innerHTML=S.slice(0,8).map(function(v){return '<a class="short rv" href="https://www.youtube.com/shorts/'+v.id+'"><img loading="lazy" src="'+th(v.id)+'" alt=""><span>'+esc(v.title)+'</span></a>';}).join('');seen(sh);}
    var I=d.instagram||[];
    if(rl&&I.length){rl.innerHTML=I.slice(0,6).map(function(p){return '<a class="rl rv'+(p.thumb?' hasimg':'')+'" href="'+esc(p.permalink)+'">'+(p.thumb?'<img loading="lazy" src="'+esc(p.thumb)+'" alt="">':'')+'<span class="kick">'+(p.type==='VIDEO'?'Reel':'Post')+'</span><b>'+esc(p.caption)+'</b><span class="go">Open on Instagram ↗</span></a>';}).join('');seen(rl);}
  }).catch(function(){});
})();
(function(){
  var pr=document.querySelector('.prog');
  if(pr)addEventListener('scroll',function(){var h=document.documentElement;pr.style.transform='scaleX('+(h.scrollTop/(h.scrollHeight-h.clientHeight||1))+')';},{passive:true});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -15% 0px'});
    document.querySelectorAll('.pugs,.planner').forEach(function(el){io.observe(el);});}
  else document.querySelectorAll('.pugs,.planner').forEach(function(el){el.classList.add('in');});
})();
/* Watch page: live grids from data/feed.json */
(function(){
  var lg=document.querySelector('[data-feed="long"]'),sg=document.querySelector('[data-feed="shorts"]'); if(!lg&&!sg)return;
  function esc(s){return String(s||'').replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function dt(s){try{return new Date(s).toLocaleDateString('en-IN',{day:'numeric',month:'short'});}catch(e){return '';}}
  fetch('data/feed.json?t='+Math.floor(Date.now()/600000)).then(function(r){return r.json();}).then(function(d){
    var y=d.youtube||{};
    if(lg&&(y.long||[]).length) lg.innerHTML=y.long.map(function(v){return '<a class="vc in" href="https://www.youtube.com/watch?v='+v.id+'"><div class="vt"><img loading="lazy" src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt=""><span class="pl2"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></div><b>'+esc(v.title)+'</b><small>'+dt(v.published)+'</small></a>';}).join('');
    if(sg&&(y.shorts||[]).length) sg.innerHTML=y.shorts.map(function(v){return '<a class="short" href="https://www.youtube.com/shorts/'+v.id+'"><img loading="lazy" src="https://i.ytimg.com/vi/'+v.id+'/hqdefault.jpg" alt=""><span>'+esc(v.title)+'</span></a>';}).join('');
  }).catch(function(){});
})();
