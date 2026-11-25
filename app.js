/* The Natural Angle app shell: offline, onboarding, share, save. */
(function () {
  var page = (location.pathname.split('/').pop() || 'Home.html'); if (page === 'index.html') page = 'Home.html';
  var LS = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }
  if (page === 'Home.html' || page === 'Interests.html') LS.set('tna_onboarded', true);
  if (page === 'Splash.html') {
    setTimeout(function () { location.replace(LS.get('tna_onboarded', false) ? 'Home.html' : 'Onboard1.html'); }, 1600);
  }


  // Guides are for people using the app. Outside the app, a PDF link shows an install prompt.
  var GATE = false, PLAY_URL = "", GMAP = {"g-2956a871146857.pdf": "reading-the-signal-guide.pdf", "g-3403fca6140789.pdf": "safari_signs_guide.pdf", "g-1e30d638648068.pdf": "safari-timing-guide.pdf", "g-59e71667d49b29.pdf": "beldanda-family-guide.pdf", "g-68694d28ae5001.pdf": "focus-through-it-guide.pdf", "g-c790eebc25eb38.pdf": "sunbird_settings_guide.pdf", "g-14a5ebc39b934b.pdf": "darter_fish_theft_guide.pdf", "g-7f135cb5e9890d.pdf": "rimlight_exposure_guide.pdf", "g-29f2620fab8b0f.pdf": "reading_light_guide.pdf", "g-541c57cb337b33.pdf": "negative-space-guide.pdf", "g-f4d6c0ea6048e5.pdf": "reach-restraint-guide.pdf", "g-b3ddd5fe9ae996.pdf": "decisions_not_gear_guide.pdf", "g-b75187d4aa4f72.pdf": "lens_switch_guide.pdf", "g-5dde2ae7868bc8.pdf": "start_your_local_species_list.pdf"};
  function inApp() {
    try {
      if (window.matchMedia && (matchMedia('(display-mode: standalone)').matches || matchMedia('(display-mode: fullscreen)').matches)) return true;
      if (navigator.standalone) return true;
      if (/^android-app:\/\//.test(document.referrer)) { sessionStorage.setItem('tna_app_session', '1'); return true; }
      return sessionStorage.getItem('tna_app_session') === '1';
    } catch (e) { return false; }
  }
  function showGate() {
    if (document.getElementById('tnaGate')) return;
    var d = document.createElement('div'); d.id = 'tnaGate';
    d.style.cssText = 'position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.72);display:flex;align-items:flex-end;justify-content:center;font-family:Barlow,system-ui,sans-serif';
    d.innerHTML = '<div style="width:100%;max-width:480px;background:#161815;border-radius:20px 20px 0 0;padding:26px 22px 34px;display:flex;flex-direction:column;gap:14px;box-shadow:0 -10px 40px rgba(0,0,0,.5)">'
      + '<span style="font-family:Barlow Condensed,sans-serif;font-weight:600;font-size:12px;letter-spacing:.16em;color:#C9A45C">APP USERS ONLY</span>'
      + '<span style="font-family:Newsreader,Georgia,serif;font-size:26px;line-height:1.15;color:#EDE8DF">The field guides are inside the app.</span>'
      + '<span style="font-size:14px;line-height:1.5;color:#A9A498">Install The Natural Angle from Google Play to download all 14 guides and read them offline in the park.</span>'
      + (PLAY_URL ? '<a href="' + PLAY_URL + '" style="display:flex;align-items:center;justify-content:center;min-height:52px;border-radius:12px;background:#C9A45C;color:#15120B;font-family:Barlow Condensed,sans-serif;font-weight:600;letter-spacing:.14em;text-transform:uppercase;text-decoration:none">Get it on Google Play</a>' : '<span style="font-size:13px;color:#C9A45C">Coming soon on Google Play.</span>')
      + '<button type="button" id="tnaGateClose" style="min-height:44px;border:0;border-radius:12px;background:transparent;color:#EDE8DF;box-shadow:inset 0 0 0 1px #3C4039;font-family:Barlow Condensed,sans-serif;font-weight:600;letter-spacing:.14em;text-transform:uppercase;cursor:pointer">Close</button></div>';
    document.body.appendChild(d);
    d.addEventListener('click', function (e) { if (e.target === d || e.target.id === 'tnaGateClose') d.remove(); });
  }


  window.__tna = { toast: function (m) { toast(m); }, inApp: inApp, gate: function () { if (GATE && !inApp()) { showGate(); return true; } return false; } };

  // ---- Fixed bottom menu on every main screen -------------------------------------------------
  var base = page.replace(/\.html$/, '');
  var NOCHROME = { Splash: 1, Onboard1: 1, Onboard2: 1, Onboard3: 1, Interests: 1, index: 1, privacy: 1 };
  var TABOF = { Home: 'Home', Saved: 'Home', Profile: 'Home', About: 'Home', Watch: 'Watch', VideoDetail: 'Watch',
    Learn: 'Learn', ShotBreakdown: 'Learn', ShotBreakdownTigress: 'Learn', ShotBreakdownCover: 'Learn', ShotBreakdownJackal: 'Learn',
    ShotBreakdownKingfisher: 'Learn', HowIShotThis: 'Learn', Resources: 'Learn', ResourceDetail: 'Learn', SafariToolkit: 'Learn', CameraSettings: 'Learn',
    Tours: 'Tours', TourDetail: 'Tours', TalChhaparTour: 'Tours', DestinationDetail: 'Tours', Shop: 'Shop', Books: 'Shop', BookDetail: 'Shop', ProductDetail: 'Shop' };
  var NAV_HTML = "<a href=\"/\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><path d=\"M3.5 10.5 12 3.5l8.5 7V20.5h-5.5v-6h-6v6H3.5z\"/></svg>HOME</a>\n<a href=\"Watch.html\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><rect x=\"3\" y=\"5\" width=\"18\" height=\"14\" rx=\"3\"/><path d=\"M10.5 9.5v5l4-2.5z\"/></svg>WATCH</a>\n<a href=\"Learn.html\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"M12 8.2l3.3 1.9v3.8L12 15.8l-3.3-1.9v-3.8z\"/></svg>LEARN</a>\n<a href=\"Tours.html\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"8.5\"/><path d=\"m15.5 8.5-2 5-5 2 2-5z\"/></svg>TOURS</a>\n<a href=\"Shop.html\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><path d=\"M5 8h14l-1.2 12.5H6.2z\"/><path d=\"M9 8V6.5a3 3 0 0 1 6 0V8\"/></svg>SHOP</a>\n<a href=\"/interiors/\"><svg class=\"ic\" viewBox=\"0 0 24 24\"><path d=\"M4 20V9l8-5 8 5v11\"/><path d=\"M9 20v-6h6v6\"/><path d=\"M3 20h18\"/></svg>HOTELS</a>";
  var NAV_CSS = '.nav{display:none !important}'
    + '#tnaNav{position:fixed;left:0;right:0;bottom:0;z-index:50;background:rgba(11,12,10,.98);border-top:1px solid #20231E;padding-bottom:env(safe-area-inset-bottom)}'
    + '#tnaNav .in{max-width:480px;margin:0 auto;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));padding:6px 6px 8px}'
    + '#tnaNav a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;min-height:54px;color:#85817A;font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:11px;letter-spacing:.16em;text-decoration:none}'
    + '#tnaNav a.on{color:#EDE8DF}#tnaNav a.on .ic{stroke:#C9A45C}'
    + 'body{padding-bottom:calc(72px + env(safe-area-inset-bottom)) !important}'
    + 'body.tna-cta{padding-bottom:calc(150px + env(safe-area-inset-bottom)) !important}'
    + '.cta{position:fixed !important;left:0;right:0;bottom:calc(66px + env(safe-area-inset-bottom)) !important;margin:0 auto !important;max-width:480px;padding-bottom:14px !important;z-index:49}';
  function injectNav() {
    if (NOCHROME[base] || document.getElementById('tnaNav')) return;
    var st = document.createElement('style'); st.textContent = NAV_CSS; document.head.appendChild(st);
    var n = document.createElement('nav'); n.id = 'tnaNav'; n.setAttribute('aria-label', 'Main');
    n.innerHTML = '<div class="in">' + NAV_HTML + '</div>';
    var tab = TABOF[base] || 'Home';
    Array.prototype.forEach.call(n.querySelectorAll('a'), function (x) {
      var on = x.getAttribute('href') === tab + '.html';
      x.className = on ? 'on' : ''; if (on) x.setAttribute('aria-current', 'page'); else x.removeAttribute('aria-current');
    });
    document.body.appendChild(n);
    if (document.querySelector('.cta')) document.body.classList.add('tna-cta');
  }

  // ---- Small message at the bottom of the screen --------------------------------------------
  function toast(msg) {
    var t = document.getElementById('tnaToast');
    if (!t) {
      t = document.createElement('div'); t.id = 'tnaToast';
      t.style.cssText = 'position:fixed;left:50%;transform:translateX(-50%);bottom:calc(150px + env(safe-area-inset-bottom));z-index:120;max-width:88%;padding:12px 18px;border-radius:12px;background:#EDE8DF;color:#15120B;font:600 14px Barlow,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.5);transition:opacity .2s;opacity:0;pointer-events:none;text-align:center';
      document.body.appendChild(t);
    }
    t.textContent = msg; t.style.opacity = '1';
    clearTimeout(t.__h); t.__h = setTimeout(function () { t.style.opacity = '0'; }, 2600);
  }

  // Inside the preview frame, outside links are handed to the page around it.
  if (window.top !== window) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || a.host === location.host || !/^https?:/.test(a.href)) return;
      e.preventDefault();
      try { parent.postMessage({ tnaOpen: a.href }, '*'); } catch (err) {}
    }, true);
  }

  // Back arrows go to the previous screen when there is one.
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('a[aria-label="Back"]');
    if (!b) return;
    var same = document.referrer && document.referrer.indexOf(location.origin) === 0 && !/preview\.html/.test(document.referrer);
    if (same && history.length > 1) { e.preventDefault(); history.back(); }
  });

  function shareLink() {
    var h = document.querySelector('h1');
    var title = (h ? h.textContent.trim() + ' · ' : '') + 'The Natural Angle';
    var url = PLAY_URL || (location.origin + location.pathname);
    var data = { title: title, text: 'The Natural Angle: wildlife photography lessons, breakdowns and field guides by Hitesh Chawla.', url: url };
    var copy = function () {
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(url).then(function () { toast('Link copied'); }, function () { toast('Copy this link: ' + url); }); return; }
      } catch (err) {}
      toast('Copy this link: ' + url);
    };
    if (navigator.share && window.top === window) navigator.share(data).catch(function (err) { if (err && err.name !== 'AbortError') copy(); });
    else copy();
  }


  function injectFoot() {
    if (NOCHROME[base] || document.getElementById('tnaFoot')) return;
    var host = document.querySelector('.s'); if (!host) return;
    var f = document.createElement('footer'); f.id = 'tnaFoot';
    f.innerHTML = '<a class="wa" href="https://wa.me/919899114998?text=' + encodeURIComponent('Hi Hitesh') + '"><svg class="ic" viewBox="0 0 24 24"><path d="M4 20l1.3-3.9A8 8 0 1 1 8 18.8z"/></svg>WhatsApp +91 98991 14998</a>'
      + '<div class="ln"><a href="https://www.instagram.com/thenaturalangle/">Instagram</a><a href="https://www.youtube.com/@thenaturalangle/videos">YouTube</a><a href="/interiors/">Hotel photography</a><a href="privacy.html">Privacy</a></div>'
      + '<p>© Hitesh Chawla · The Natural Angle</p>';
    var nav = host.querySelector('.nav'); if (nav) host.insertBefore(f, nav); else host.appendChild(f);
  }
  function enhance() {
    injectNav(); injectFoot();
    // External links open outside the app shell.
    document.querySelectorAll('a[href^="http"]').forEach(function (a) {
      if (a.host !== location.host) { a.target = '_blank'; a.rel = 'noopener'; }
    });
    // WhatsApp enquiries are tagged so Hitesh can see which ones came from the app.
    document.querySelectorAll('a[href*="wa.me/"]').forEach(function (a) {
      if (a.__wa) return; a.__wa = 1;
      var h = a.getAttribute('href');
      a.setAttribute('href', h.indexOf('?text=') > -1 ? h + '%20(via%20website)' : h.replace(/\?.*$/, '') + '?text=' + encodeURIComponent('Hi Hitesh (via website)'));
    });
    // Guides download as files in the installed app.
    document.querySelectorAll('a[href$=".pdf"]').forEach(function (a) {
      if (a.__tna) return; a.__tna = 1;
      var base = (a.getAttribute('href') || '').split('/').pop();
      a.setAttribute('download', GMAP[base] || '');
      a.addEventListener('click', function (e) {
        if (GATE && !inApp()) { e.preventDefault(); showGate(); return; }
        if (window.__tnaLive && window.__tnaLive.lock) { e.preventDefault(); window.__tnaLive.guide(GMAP[base] || base, GMAP[base] || base); return; }
        if (window.top !== window) {
          e.preventDefault();
          try { parent.postMessage({ tnaDownload: a.href, name: GMAP[base] || base }, '*'); } catch (err) {}
        }
      });
    });
    // Share
    document.querySelectorAll('button[aria-label="Share"]').forEach(function (b) {
      if (b.__tna) return; b.__tna = 1;
      b.addEventListener('click', shareLink);
    });
    // Save (bookmark) buttons
    document.querySelectorAll('button[aria-label^="Save"]').forEach(function (b) {
      if (b.__tna) return; b.__tna = 1;
      var kind = b.getAttribute('aria-label').replace(/^Save\s*/, '') || 'item';
      var paint = function () {
        var on = LS.get('tna_saved', []).some(function (x) { return x.href === page; });
        var p = b.querySelector('path'); if (p) p.style.fill = on ? 'currentColor' : 'none';
        b.style.color = on ? '#C9A45C' : '';
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      };
      b.addEventListener('click', function () {
        var list = LS.get('tna_saved', []);
        var i = list.findIndex(function (x) { return x.href === page; });
        if (i > -1) list.splice(i, 1);
        else {
          var h = document.querySelector('h1');
          var img = document.querySelector('img.pi');
          list.unshift({ href: page, kind: kind.charAt(0).toUpperCase() + kind.slice(1), title: h ? h.textContent.trim() : document.title, img: img ? img.getAttribute('src') : '', pos: img ? img.style.objectPosition : '' });
        }
        LS.set('tna_saved', list); paint();
      });
      paint();
    });
    // Saved screen
    var host = document.getElementById('savedList');
    if (host) {
      var list = LS.get('tna_saved', []);
      var cnt = document.getElementById('savedCount'); if (cnt) cnt.textContent = list.length + (list.length === 1 ? ' item' : ' items');
      host.innerHTML = list.length ? list.map(function (x) {
        var th = x.img ? '<div class="ph t3" style="width: 64px; height: 64px; border-radius: 10px"><img class="pi" src="' + x.img + '" alt="" style="object-position: ' + (x.pos || '50% 50%') + '"></div>'
          : '<div style="width: 64px; height: 64px; border-radius: 10px; background: #13201A; flex: none"></div>';
        return '<a class="it" href="' + x.href + '">' + th + '<div style="display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1"><span class="k kg" style="font-size: 10px">' + x.kind + '</span><span class="h4">' + x.title.replace(/</g, '&lt;') + '</span></div></a>';
      }).join('') : '<div style="padding: 28px 20px; border-radius: 16px; background: #141613; box-shadow: inset 0 0 0 1px #23261F; display: flex; flex-direction: column; gap: 8px"><span class="h4">Nothing saved yet</span><span class="sm mut">Tap the bookmark on any breakdown, field guide or tour and it lands here.</span></div>';
    }
    var sc = document.getElementById('savedCountRow');
    if (sc) sc.textContent = LS.get('tna_saved', []).length + ' →';
  }

  // Swipe rows: touch works natively; on desktop mouse, drag to scroll and show a thin scrollbar.
  (function () {
    var st = document.createElement('style');
    st.textContent = '@media (hover:hover) and (pointer:fine){.hs,[style*="overflow-x: auto"]{scrollbar-width:thin!important;scrollbar-color:#4A4F45 transparent;cursor:grab}.tna-drag,.tna-drag *{cursor:grabbing!important;user-select:none!important}}img{-webkit-user-drag:none}';
    (document.head || document.documentElement).appendChild(st);
    var row = null, sx = 0, sl = 0, moved = false;
    function scroller(el) {
      while (el && el !== document.body) {
        var o = getComputedStyle(el).overflowX;
        if ((o === 'auto' || o === 'scroll') && el.scrollWidth > el.clientWidth + 4) return el;
        el = el.parentElement;
      }
      return null;
    }
    document.addEventListener('dragstart', function (e) { if (scroller(e.target)) e.preventDefault(); });
    document.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse' || e.button !== 0) return;
      row = scroller(e.target); if (!row) return;
      sx = e.clientX; sl = row.scrollLeft; moved = false;
    });
    document.addEventListener('pointermove', function (e) {
      if (!row) return;
      var dx = e.clientX - sx;
      if (!moved && Math.abs(dx) > 6) { moved = true; row.classList.add('tna-drag'); }
      if (moved) row.scrollLeft = sl - dx;
    });
    function end() { if (row) { row.classList.remove('tna-drag'); row = null; } }
    document.addEventListener('pointerup', end); document.addEventListener('pointercancel', end);
    document.addEventListener('click', function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; } }, true);
  })();
  document.addEventListener('dc:render', enhance);
  if (document.readyState !== 'loading') enhance(); else document.addEventListener('DOMContentLoaded', enhance);
})();

/* The Natural Angle live layer: tour dates from Google Calendar, new guides and carousels from a feed,
   and a real sign-in lock on the field guides. Every part is off until its keys are set in config.json.
   Any network failure falls back to the built-in content, so the app never breaks. */
(function () {
  var C = {"supabaseUrl": "", "supabaseKey": "", "calendarId": "", "googleKey": ""}, T = window.__tna || {}, GMAP = {"g-2956a871146857.pdf": "reading-the-signal-guide.pdf", "g-3403fca6140789.pdf": "safari_signs_guide.pdf", "g-1e30d638648068.pdf": "safari-timing-guide.pdf", "g-59e71667d49b29.pdf": "beldanda-family-guide.pdf", "g-68694d28ae5001.pdf": "focus-through-it-guide.pdf", "g-c790eebc25eb38.pdf": "sunbird_settings_guide.pdf", "g-14a5ebc39b934b.pdf": "darter_fish_theft_guide.pdf", "g-7f135cb5e9890d.pdf": "rimlight_exposure_guide.pdf", "g-29f2620fab8b0f.pdf": "reading_light_guide.pdf", "g-541c57cb337b33.pdf": "negative-space-guide.pdf", "g-f4d6c0ea6048e5.pdf": "reach-restraint-guide.pdf", "g-b3ddd5fe9ae996.pdf": "decisions_not_gear_guide.pdf", "g-b75187d4aa4f72.pdf": "lens_switch_guide.pdf", "g-5dde2ae7868bc8.pdf": "start_your_local_species_list.pdf"};
  var SB = !!(C.supabaseUrl && C.supabaseKey), CAL = !!(C.calendarId && C.googleKey);
  var LOCK = SB && false;
  function ls(k, d) { try { var v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } }
  function lsset(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function toast(m) { if (T.toast) T.toast(m); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function onReady(fn) { if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  // ---------------- Tour dates from Google Calendar ----------------
  var KEYS = {
    panna: /panna/i, talchhapar: /tal\s*chhapar|chhapar|bikaner/i, bharatpur: /bharatpur|keoladeo/i,
    pilibhit: /pilibhit/i, rajaji: /rajaji/i, dudhwa: /dudhwa|kishanpur/i, ranthambore: /ranthambore/i
  };
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function parseDay(o) {
    if (!o) return null;
    if (o.date) { var p = o.date.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
    if (o.dateTime) { var d = new Date(o.dateTime); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
    return null;
  }
  function range(a, b) {
    // all-day events end on the day after the last day
    var last = new Date(b.getTime() - 86400000); if (last < a) last = a;
    if (a.getTime() === last.getTime()) return a.getDate() + ' ' + MON[a.getMonth()];
    if (a.getMonth() === last.getMonth()) return a.getDate() + ' to ' + last.getDate() + ' ' + MON[a.getMonth()];
    return a.getDate() + ' ' + MON[a.getMonth()] + ' to ' + last.getDate() + ' ' + MON[last.getMonth()];
  }
  function batches(items) {
    var out = {}, today = new Date(); today.setHours(0, 0, 0, 0);
    (items || []).forEach(function (ev) {
      if (!ev || ev.status === 'cancelled') return;
      var a = parseDay(ev.start), b = parseDay(ev.end) || a;
      if (!a || b < today) return;
      var txt = (ev.summary || '') + ' ' + (ev.description || '');
      Object.keys(KEYS).forEach(function (k) {
        if (!KEYS[k].test(ev.summary || '')) return;
        (out[k] = out[k] || []).push({ at: a.getTime(), label: range(a, b), full: /\b(full|sold\s*out)\b/i.test(txt) });
      });
    });
    Object.keys(out).forEach(function (k) { out[k].sort(function (x, y) { return x.at - y.at; }); });
    return out;
  }
  function paintDates(map) {
    document.querySelectorAll('[data-nb]').forEach(function (el) {
      if (el.__orig === undefined) el.__orig = el.textContent;
      var list = map[el.getAttribute('data-nb')];
      if (!list || !list.length) { el.textContent = el.__orig; return; }
      var detail = /^(TourDetail|TalChhaparTour)\.html$/.test(location.pathname.split('/').pop());
      var shown = list.slice(0, detail ? 3 : 1).map(function (b) { return b.label + (b.full ? ' (full)' : ''); });
      var more = '';
      var pre = el.getAttribute('data-pre') || '';
      el.textContent = pre + shown.join(', ') + more;
    });
  }
  function loadCalendar() {
    if (!CAL || !document.querySelector('[data-nb]')) return;
    var cached = ls('tna_cal', null);
    if (cached && cached.map) paintDates(batches(cached.items));
    if (cached && Date.now() - cached.t < 10 * 60 * 1000) return;
    var u = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(C.calendarId) + '/events?singleEvents=true&orderBy=startTime&maxResults=100&timeMin=' +
      encodeURIComponent(new Date().toISOString()) + '&key=' + encodeURIComponent(C.googleKey);
    fetch(u).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var items = (j.items || []).map(function (e) { return { summary: e.summary, description: e.description, status: e.status, start: e.start, end: e.end }; });
      lsset('tna_cal', { t: Date.now(), items: items, map: 1 });
      paintDates(batches(items));
    }).catch(function () {});
  }

  // ---------------- Supabase: sign-in, guides, feed ----------------
  function api(path, o) {
    o = o || {};
    var h = { apikey: C.supabaseKey };
    if (o.body) h['Content-Type'] = 'application/json';
    if (o.bearer) h.Authorization = 'Bearer ' + o.bearer;
    return fetch(C.supabaseUrl + path, { method: o.method || 'GET', headers: h, body: o.body ? JSON.stringify(o.body) : undefined }).then(function (r) {
      if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { throw { status: r.status, msg: j.msg || j.error_description || j.message || j.error || ('Error ' + r.status) }; });
      return o.blob ? r.blob() : r.json().catch(function () { return {}; });
    }, function () { throw { status: 0, msg: 'No connection. Check your internet and try again.' }; });
  }
  function sess() { return ls('tna_sess', null); }
  function saveSess(r) {
    if (!r || !r.access_token) return null;
    var old = sess();
    var s = { a: r.access_token, r: r.refresh_token, exp: Date.now() + ((r.expires_in || 3600) - 60) * 1000, email: (r.user && r.user.email) || (old && old.email) || '' };
    lsset('tna_sess', s); return s;
  }
  function token() {
    var s = sess(); if (!s) return Promise.resolve(null);
    if (Date.now() < s.exp) return Promise.resolve(s.a);
    return api('/auth/v1/token?grant_type=refresh_token', { method: 'POST', body: { refresh_token: s.r } }).then(function (r) { var n = saveSess(r); return n ? n.a : null; }, function (e) {
      if (e && e.status >= 400 && e.status < 500) lsset('tna_sess', null);
      return null;
    });
  }
  function signOut() {
    lsset('tna_sess', null);
    try { if (window.caches) caches.delete('tna-guides'); } catch (e) {}
  }

  var sheetEl = null;
  function closeSheet() { if (sheetEl) { sheetEl.remove(); sheetEl = null; } }
  function signInSheet() {
    return new Promise(function (resolve, reject) {
      closeSheet();
      var mode = 'in';
      var d = sheetEl = document.createElement('div'); d.id = 'tnaAuth';
      d.style.cssText = 'position:fixed;inset:0;z-index:130;background:rgba(0,0,0,.74);display:flex;align-items:flex-end;justify-content:center;font-family:Barlow,system-ui,sans-serif';
      var FONT = 'Barlow Condensed,sans-serif', IN = 'width:100%;box-sizing:border-box;min-height:50px;border-radius:12px;border:0;background:#0E0F0D;color:#EDE8DF;box-shadow:inset 0 0 0 1px #3C4039;padding:0 14px;font-size:16px;font-family:Barlow,sans-serif';
      function draw(msg, good) {
        var t = mode === 'up' ? 'Create your free account' : mode === 'reset' ? 'Reset your password' : 'Sign in to open the guides';
        var sub = mode === 'up' ? 'One account unlocks all 14 field guides and every new one I add.' : mode === 'reset' ? 'We will email you a link to set a new password.' : 'Use the email you signed up with.';
        d.innerHTML = '<form id="tnaAuthForm" style="width:100%;max-width:480px;background:#161815;border-radius:20px 20px 0 0;padding:26px 22px 30px;display:flex;flex-direction:column;gap:12px;box-shadow:0 -10px 40px rgba(0,0,0,.5);max-height:92vh;overflow:auto">'
          + '<span style="font-family:' + FONT + ';font-weight:600;font-size:12px;letter-spacing:.16em;color:#C9A45C">FIELD GUIDES</span>'
          + '<span style="font-family:Newsreader,Georgia,serif;font-size:26px;line-height:1.15;color:#EDE8DF">' + t + '</span>'
          + '<span style="font-size:14px;line-height:1.5;color:#A9A498">' + sub + '</span>'
          + '<input id="tnaEm" type="email" autocomplete="email" inputmode="email" placeholder="Email" required style="' + IN + '">'
          + (mode === 'reset' ? '' : '<input id="tnaPw" type="password" autocomplete="' + (mode === 'up' ? 'new-password' : 'current-password') + '" placeholder="Password' + (mode === 'up' ? ' (8 or more characters)' : '') + '" required minlength="' + (mode === 'up' ? 8 : 1) + '" style="' + IN + '">')
          + '<span id="tnaAuthMsg" role="status" style="font-size:13px;line-height:1.4;min-height:18px;color:' + (good ? '#8FD19E' : '#E58C7B') + '">' + esc(msg || '') + '</span>'
          + '<button type="submit" id="tnaGo" style="min-height:52px;border:0;border-radius:12px;background:#C9A45C;color:#15120B;font-family:' + FONT + ';font-weight:600;letter-spacing:.14em;text-transform:uppercase;cursor:pointer">' + (mode === 'up' ? 'Create account' : mode === 'reset' ? 'Send reset link' : 'Sign in') + '</button>'
          + '<div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap">'
          + (mode === 'in' ? '<button type="button" data-m="up" style="' + LINK + '">New here? Create account</button><button type="button" data-m="reset" style="' + LINK + '">Forgot password</button>' : '<button type="button" data-m="in" style="' + LINK + '">Back to sign in</button>')
          + '<button type="button" id="tnaAuthX" style="' + LINK + '">Close</button></div></form>';
        var f = d.querySelector('form');
        f.addEventListener('submit', function (e) { e.preventDefault(); submit(); });
        Array.prototype.forEach.call(d.querySelectorAll('[data-m]'), function (b) { b.addEventListener('click', function () { var em = d.querySelector('#tnaEm').value; mode = b.getAttribute('data-m'); draw(''); d.querySelector('#tnaEm').value = em; }); });
        d.querySelector('#tnaAuthX').addEventListener('click', function () { closeSheet(); reject({ cancelled: true }); });
      }
      var LINK = 'background:transparent;border:0;color:#C9A45C;font-family:Barlow,sans-serif;font-size:14px;min-height:44px;padding:0;cursor:pointer;text-align:left';
      function submit() {
        var em = d.querySelector('#tnaEm').value.trim(), pwEl = d.querySelector('#tnaPw'), pw = pwEl ? pwEl.value : '';
        var go = d.querySelector('#tnaGo'); go.disabled = true; go.style.opacity = '.6';
        var p;
        if (mode === 'reset') {
          p = api('/auth/v1/recover', { method: 'POST', body: { email: em } }).then(function () { draw('Check your email for the reset link.', true); d.querySelector('#tnaEm').value = em; });
        } else if (mode === 'up') {
          p = api('/auth/v1/signup', { method: 'POST', body: { email: em, password: pw } }).then(function (r) {
            var s = saveSess(r);
            if (s) { closeSheet(); resolve(s); } else { mode = 'in'; draw('Account created. Confirm the email we sent you, then sign in.', true); d.querySelector('#tnaEm').value = em; }
          });
        } else {
          p = api('/auth/v1/token?grant_type=password', { method: 'POST', body: { email: em, password: pw } }).then(function (r) { var s = saveSess(r); if (!s) throw { msg: 'Sign in failed.' }; closeSheet(); resolve(s); });
        }
        p.catch(function (e) {
          var m = (e && e.msg) || 'Something went wrong.';
          if (/invalid login/i.test(m)) m = 'Wrong email or password.';
          if (/already registered|already been registered/i.test(m)) m = 'That email already has an account. Sign in instead.';
          if (/not confirmed/i.test(m)) m = 'Confirm your email first. Check your inbox.';
          if (/rate limit|too many/i.test(m)) m = 'Too many tries. Wait a few minutes and try again.';
          draw(m, false); d.querySelector('#tnaEm').value = em;
        });
      }
      draw('');
      document.body.appendChild(d);
    });
  }
  function ensureSignedIn() {
    return token().then(function (t) { return t || signInSheet().then(function () { return token(); }); });
  }

  function saveBlob(blob, name) {
    var u = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = u; a.download = name; a.style.display = 'none'; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(u); a.remove(); }, 4000);
  }
  function cachedGuide(file) {
    if (!window.caches) return Promise.resolve(null);
    return caches.open('tna-guides').then(function (c) { return c.match('guide/' + file); }).then(function (r) { return r ? r.blob() : null; }).catch(function () { return null; });
  }
  function putGuide(file, blob) {
    if (!window.caches) return;
    caches.open('tna-guides').then(function (c) { return c.put('guide/' + file, new Response(blob, { headers: { 'Content-Type': 'application/pdf' } })); }).catch(function () {});
  }
  function guide(file, nice) {
    nice = nice || file;
    cachedGuide(file).then(function (b) {
      if (b) { saveBlob(b, nice); toast('Saved ' + nice); return; }
      return ensureSignedIn().then(function (t) {
        if (!t) { toast('Could not sign you in. Try again.'); return; }
        toast('Downloading...');
        return api('/storage/v1/object/authenticated/guides/' + encodeURIComponent(file), { bearer: t, blob: true }).then(function (blob) {
          putGuide(file, blob); saveBlob(blob, nice); toast('Saved ' + nice);
        }, function (e) {
          if (e && e.status === 404) toast('That guide is not uploaded yet.');
          else if (e && (e.status === 401 || e.status === 403)) { lsset('tna_sess', null); toast('Please sign in again.'); }
          else toast((e && e.msg) || 'Download failed.');
        });
      }, function (e) { if (!e || !e.cancelled) toast('Sign in cancelled.'); });
    });
  }

  // ---------------- Feed: new guides and carousels ----------------
  var DL = '<svg class="ic" style="color: #C9A45C" viewBox="0 0 24 24"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>';
  function paintFeed(rows) {
    var g = document.getElementById('tnaFeedGuides'), c = document.getElementById('tnaFeedCarousels');
    rows = rows || [];
    if (g) {
      Array.prototype.forEach.call(g.querySelectorAll('[data-feed]'), function (n) { n.remove(); });
      rows.filter(function (r) { return r.kind === 'guide' && r.file; }).slice().reverse().forEach(function (r) {
        var a = document.createElement('a'); a.className = 'card ri'; a.setAttribute('data-feed', '1'); a.href = '#';
        a.innerHTML = '<div style="display: flex; flex-direction: column; gap: 4px; min-width: 0; flex: 1; padding: 4px 0"><span class="k kg" style="font-size: 10px">NEW</span><span class="h4">' + esc(r.title) + '</span>' + (r.description ? '<span class="sm mut">' + esc(r.description) + '</span>' : '') + '</div>' + DL;
        a.addEventListener('click', function (e) { e.preventDefault(); if (T.gate && T.gate()) return; guide(r.file, r.file); });
        g.insertBefore(a, g.firstChild);
      });
    }
    if (c) {
      Array.prototype.forEach.call(c.querySelectorAll('[data-feed]'), function (n) { n.remove(); });
      rows.filter(function (r) { return r.kind === 'carousel' && r.image; }).slice().reverse().forEach(function (r) {
        var a = document.createElement('a'); a.className = 'card'; a.setAttribute('data-feed', '1'); a.style.cssText = 'width: 210px; flex: none';
        a.href = r.link || 'https://www.instagram.com/thenaturalangle/';
        a.innerHTML = '<div class="ph" style="height: 210px"><img class="pi" src="' + esc(r.image) + '" alt="' + esc(r.title) + '"></div><div style="padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 3px"><span class="k kg" style="font-size: 11px">NEW</span><span class="h4">' + esc(r.title) + '</span><span class="sm mut">Read on Instagram ↗</span></div>';
        c.insertBefore(a, c.firstChild);
      });
    }
  }
  function loadFeed() {
    if (!SB || !(document.getElementById('tnaFeedGuides') || document.getElementById('tnaFeedCarousels'))) return;
    var cached = ls('tna_feed', null); if (cached) paintFeed(cached);
    if (loadFeed.done) return; loadFeed.done = true;
    api('/rest/v1/feed?select=kind,title,description,file,image,link,created_at&order=created_at.desc&limit=60').then(function (rows) {
      if (Array.isArray(rows)) { lsset('tna_feed', rows); paintFeed(rows); }
    }).catch(function () {});
  }

  // ---------------- Profile account rows ----------------
  function wireAccount() {
    var row = document.getElementById('tnaAcct'); if (!row || !LOCK || row.__w) return; row.__w = 1;
    var label = row.querySelector('.t'), sub = row.querySelector('.m');
    function paint() { var s = sess(); label.textContent = s ? 'Sign out' : 'Sign in for field guides'; sub.textContent = s ? (s.email || '') : '→'; var del = document.getElementById('tnaDel'); if (del) del.style.display = s ? '' : 'none'; }
    row.addEventListener('click', function (e) {
      e.preventDefault();
      if (sess()) { signOut(); paint(); toast('Signed out. Downloaded guides were cleared from this phone.'); }
      else signInSheet().then(paint, function () {});
    });
    paint();
  }

  window.__tnaLive = { guide: guide, lock: LOCK, signOut: signOut };
  onReady(function () { loadCalendar(); loadFeed(); wireAccount(); });
  document.addEventListener('dc:render', function () { loadCalendar(); loadFeed(); wireAccount(); });
})();
