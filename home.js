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
