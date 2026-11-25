/* Website layer: scroll reveals, counters, map links, forest ambience. */
(function(){
  var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function ready(f){document.readyState!=='loading'?f():document.addEventListener('DOMContentLoaded',f);}
  ready(function(){
    // reveal
    var els=document.querySelectorAll('.s section, .s .card:not(.tc), .tc, .stats>div');
    if('IntersectionObserver' in window && !RM){
      var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});
      els.forEach(function(el,i){ if(el.getBoundingClientRect().top<innerHeight) return; el.classList.add('rv-i'); el.style.transitionDelay=(i%4)*60+'ms'; io.observe(el);});
    }
    // counters
    document.querySelectorAll('[data-count]').forEach(function(el){
      var n=+el.getAttribute('data-count'),suf=el.getAttribute('data-suf')||'';
      if(RM||!('IntersectionObserver' in window))return;
      var o=new IntersectionObserver(function(es){ if(!es[0].isIntersecting)return; o.disconnect(); var t0=performance.now();
        (function step(t){var p=Math.min(1,(t-t0)/1200),v=Math.round(n*(1-Math.pow(1-p,3)));el.textContent=v+(p===1?suf:'');if(p<1)requestAnimationFrame(step);})(t0);});
      o.observe(el);
    });
    // map pins -> tour cards
    document.querySelectorAll('.map .pin').forEach(function(p){
      p.addEventListener('click',function(e){
        var c=document.getElementById('t-'+p.getAttribute('data-t'));
        if(!c){ e.preventDefault(); location.href='Tours.html'; return; }
        e.preventDefault();
        document.querySelectorAll('.tc.on,.pin.on').forEach(function(x){x.classList.remove('on');});
        c.classList.add('on'); p.classList.add('on');
        var row=c.parentElement; row.scrollTo({left:c.offsetLeft-20,behavior:RM?'auto':'smooth'});
        c.scrollIntoView({block:'nearest',behavior:RM?'auto':'smooth'});
      });
    });
    // ambience
    if(/Splash|Onboard/.test(location.pathname))return;
    var b=document.createElement('button'); b.id='amb'; b.type='button';
    b.innerHTML='<span class="eq"><i></i><i></i><i></i></span><span class="lb">FOREST SOUNDS</span>';
    b.setAttribute('aria-pressed','false'); b.setAttribute('aria-label','Play forest ambience');
    document.body.appendChild(b);
    var a=new Audio('assets/audio/forest.mp3'); a.loop=true; a.volume=0; a.preload='none';
    var fade; function to(v,done){clearInterval(fade);fade=setInterval(function(){var d=v-a.volume;if(Math.abs(d)<.02){a.volume=v;clearInterval(fade);done&&done();}else a.volume=Math.max(0,Math.min(1,a.volume+d*.15));},60);}
    function set(on){b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);try{localStorage.setItem('tna_amb',on?'1':'0');}catch(e){}}
    function play(){ try{var t=+sessionStorage.getItem('tna_amb_t'); if(t) a.currentTime=t;}catch(e){} a.play().then(function(){set(true);to(.35);}).catch(function(){}); }
    function stop(){ set(false); to(0,function(){a.pause();}); }
    b.addEventListener('click',function(){ b.classList.contains('on')?stop():play(); });
    var want=false; try{want=localStorage.getItem('tna_amb')==='1';}catch(e){}
    if(want){ var go=function(){document.removeEventListener('pointerdown',go,true);if(!b.classList.contains('on'))play();}; document.addEventListener('pointerdown',go,true); b.classList.add('on'); }
    addEventListener('pagehide',function(){try{sessionStorage.setItem('tna_amb_t',a.currentTime||0);}catch(e){}});
  });
})();
