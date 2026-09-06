/* nasilhesap.com — istemci tarafı hesaplayıcı çalışma zamanı + arama. Veri gönderilmez. */
(function () {
  'use strict';
  var TL = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var SAYI = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 2 });

  function parseNum(s) {
    if (typeof s === 'number') return s;
    s = String(s || '').trim();
    if (!s) return NaN;
    s = s.replace(/\s|₺|%/g, '');
    if (s.indexOf(',') > -1 && s.indexOf('.') > -1) s = s.replace(/\./g, '').replace(',', '.');
    else if (s.indexOf(',') > -1) s = s.replace(',', '.');
    return parseFloat(s);
  }
  function fmt(n, dec) {
    if (n === null || n === undefined || isNaN(n)) return '—';
    if (typeof n === 'string') return n;
    if (dec === 0) return SAYI.format(Math.round(n));
    return TL.format(n);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  window.NH = { parseNum: parseNum, fmt: fmt, TL: TL };

  /* ---------- hesaplayıcı ---------- */
  var form = document.getElementById('hesap-form');
  var sonuc = document.getElementById('sonuc');
  if (form && sonuc && typeof window.hesapla === 'function') {
    var alanlar = Array.prototype.slice.call(form.querySelectorAll('[name]'));
    var varsayilan = {};
    alanlar.forEach(function (el) { varsayilan[el.name] = el.type === 'checkbox' ? el.checked : el.value; });

    function oku() {
      var g = {};
      alanlar.forEach(function (el) {
        var tip = el.getAttribute('data-tip');
        if (tip === 'onay') g[el.name] = el.checked;
        else if (tip === 'secim' || tip === 'tarih' || tip === 'metin') g[el.name] = el.value;
        else if (tip === 'tamsayi') g[el.name] = parseInt(el.value, 10);
        else g[el.name] = parseNum(el.value);
      });
      return g;
    }
    function gizliUygula(g) {
      form.querySelectorAll('[data-gizli]').forEach(function (kutu) {
        // data-gizli="alan=deger" -> yalnızca eşleşince göster
        var kural = kutu.getAttribute('data-gizli').split('=');
        var goster = String(g[kural[0]]) === kural[1];
        kutu.hidden = !goster;
      });
    }
    function ciz(r) {
      if (!r) { sonuc.innerHTML = ''; return; }
      if (r.hata) { sonuc.innerHTML = '<p class="sonuc-hata">' + esc(r.hata) + '</p>'; return; }
      var h = '';
      (r.sonuclar || []).forEach(function (s) {
        var d = (typeof s.deger === 'number') ? fmt(s.deger, s.ondalik) : esc(s.deger);
        var b = s.birim ? ' ' + esc(s.birim) : '';
        if (s.vurgu) h += '<div class="sonuc-ana"><div class="etk">' + esc(s.etiket) + '</div><div class="deg">' + d + b + '</div></div>';
        else h += '<div class="sonuc-satir"><span>' + esc(s.etiket) + '</span><b>' + d + b + '</b></div>';
      });
      if (r.tablo) {
        h += '<table><thead><tr>' + r.tablo.basliklar.map(function (x) { return '<th>' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>';
        r.tablo.satirlar.forEach(function (row) { h += '<tr>' + row.map(function (c) { return '<td>' + (typeof c === 'number' ? fmt(c) : esc(c)) + '</td>'; }).join('') + '</tr>'; });
        h += '</tbody></table>';
      }
      if (r.notlar && r.notlar.length) h += '<ul class="sonuc-not">' + r.notlar.map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('') + '</ul>';
      sonuc.innerHTML = h;
    }
    function calistir() {
      var g = oku();
      gizliUygula(g);
      try { ciz(window.hesapla(g, window.ORAN || {})); }
      catch (e) { sonuc.innerHTML = '<p class="sonuc-hata">Hesaplanamadı: ' + esc(e.message) + '</p>'; }
    }
    form.addEventListener('input', calistir);
    form.addEventListener('change', calistir);
    document.getElementById('hesapla-btn').addEventListener('click', calistir);
    document.getElementById('sifirla-btn').addEventListener('click', function () {
      alanlar.forEach(function (el) { if (el.type === 'checkbox') el.checked = !!varsayilan[el.name]; else el.value = varsayilan[el.name]; });
      calistir();
    });
    calistir();
  }

  /* ---------- arama ---------- */
  var dizin = null;
  function dizinYukle(cb) {
    if (dizin) return cb(dizin);
    fetch('/static/araclar.json').then(function (r) { return r.json(); }).then(function (d) { dizin = d; cb(d); }).catch(function () { cb([]); });
  }
  function norm(s) { return String(s).toLocaleLowerCase('tr-TR').replace(/[İı]/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c'); }
  function aramaBagla(inputId, kutuId) {
    var inp = document.getElementById(inputId), kutu = document.getElementById(kutuId);
    if (!inp || !kutu) return;
    inp.addEventListener('input', function () {
      var q = norm(inp.value.trim());
      if (q.length < 2) { kutu.hidden = true; return; }
      dizinYukle(function (d) {
        var hits = d.filter(function (a) { return norm(a.b + ' ' + a.k + ' ' + a.a).indexOf(q) > -1; }).slice(0, 8);
        if (!hits.length) { kutu.innerHTML = '<a href="/"><span>Sonuç yok</span></a>'; kutu.hidden = false; return; }
        kutu.innerHTML = hits.map(function (a) { return '<a href="/' + a.s + '/"><span>' + a.i + ' ' + esc(a.b) + '</span><small>' + esc(a.k) + '</small></a>'; }).join('');
        kutu.hidden = false;
      });
    });
    document.addEventListener('click', function (e) { if (!kutu.contains(e.target) && e.target !== inp) kutu.hidden = true; });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { var ilk = kutu.querySelector('a'); if (ilk) { e.preventDefault(); location.href = ilk.getAttribute('href'); } } });
  }
  aramaBagla('q', 'ara-sonuc');
  aramaBagla('q2', 'ara-sonuc2');
  var qs = new URLSearchParams(location.search).get('q');
  if (qs) { var i2 = document.getElementById('q2') || document.getElementById('q'); if (i2) { i2.value = qs; i2.dispatchEvent(new Event('input')); i2.focus(); } }
})();
