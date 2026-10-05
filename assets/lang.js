// PLESION: language switcher in the footer, and a one-time line when the browser prefers another language we have.
// Shared by every page; loaded with defer.
(function () {
  var PAGES = { en: '/', fr: '/fr/', it: '/it/' };
  var HINT = { en: ['View this page in English', 'Close'], fr: ['Voir cette page en français', 'Fermer'], it: ['Visualizza questa pagina in italiano', 'Chiudi'] };
  var cur = document.documentElement.lang;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  document.querySelectorAll('a[data-lang]').forEach(function (a) { a.addEventListener('click', function () { put('plesion-lang', a.getAttribute('data-lang')); }); });

  var btn = document.querySelector('.lang-btn');
  if (btn) {
    var panel = document.getElementById('lang-panel'), veil = document.querySelector('.lang-veil');
    var set = function (open) { btn.setAttribute('aria-expanded', open); panel.hidden = !open; veil.hidden = !open; if (open) panel.focus(); };
    btn.addEventListener('click', function () { set(panel.hidden); });
    panel.querySelector('.lang-close').addEventListener('click', function () { set(false); btn.focus(); });
    veil.addEventListener('click', function () { set(false); });
    document.addEventListener('click', function (e) { if (!panel.hidden && !e.target.closest('.lang')) set(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { set(false); btn.focus(); } });
  }

  var bar = document.querySelector('.lang-hint');
  if (!bar || get('plesion-lang') || get('plesion-lang-hint')) return;
  var pref = null;
  (navigator.languages || [navigator.language]).some(function (l) { var p = String(l || '').slice(0, 2).toLowerCase(); if (PAGES[p]) { pref = p; return true; } return false; });
  if (!pref || pref === cur) return;
  bar.innerHTML = '<a href="' + PAGES[pref] + '" lang="' + pref + '" hreflang="' + pref + '" data-lang="' + pref + '">' + HINT[pref][0] + ' →</a>' +
    '<button type="button" aria-label="' + HINT[pref][1] + '" lang="' + pref + '">×</button>';
  bar.querySelector('a').addEventListener('click', function () { put('plesion-lang', pref); });
  bar.querySelector('button').addEventListener('click', function () { put('plesion-lang-hint', '1'); bar.hidden = true; });
  bar.hidden = false;
})();
