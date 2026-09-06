/* nasilhesap.com — istemci tarafı hesaplayıcı çalışma zamanı, grafik, senaryo,
   paylaşılabilir link, son araçlar ve arama. Hesaplama tarayıcıda yapılır, veri gönderilmez. */
(function () {
  'use strict';
  var TL = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var SAYI = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 2 });
  var KISA = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 });

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
    if (n === null || n === undefined || (typeof n === 'number' && isNaN(n))) return '—';
    if (typeof n === 'string') return n;
    if (dec === 0) return KISA.format(Math.round(n));
    return TL.format(n);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function kisaSayi(n) {
    var a = Math.abs(n);
    if (a >= 1e9) return SAYI.format(n / 1e9) + ' mr';
    if (a >= 1e6) return SAYI.format(Math.round(n / 1e5) / 10) + ' M';
    if (a >= 1e4) return KISA.format(Math.round(n / 1e3)) + ' B';
    return KISA.format(Math.round(n));
  }
  window.NH = { parseNum: parseNum, fmt: fmt, TL: TL };

  /* ---------- mobil menü ---------- */
  var mBtn = document.getElementById('menu-btn'), mMenu = document.getElementById('ana-menu');
  if (mBtn && mMenu) {
    mBtn.addEventListener('click', function () {
      var acik = mMenu.classList.toggle('acik');
      mBtn.setAttribute('aria-expanded', acik ? 'true' : 'false');
      mBtn.setAttribute('aria-label', acik ? 'Menüyü kapat' : 'Menüyü aç');
    });
    document.addEventListener('click', function (e) {
      if (mMenu.classList.contains('acik') && !mMenu.contains(e.target) && !mBtn.contains(e.target)) {
        mMenu.classList.remove('acik'); mBtn.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mMenu.classList.contains('acik')) { mMenu.classList.remove('acik'); mBtn.setAttribute('aria-expanded', 'false'); mBtn.focus(); }
    });
  }

  /* ---------- son kullanılan araçlar (localStorage) ---------- */
  var SON_ANAHTAR = 'nh_son_araclar';
  function sonOku() { try { return JSON.parse(localStorage.getItem(SON_ANAHTAR) || '[]'); } catch (e) { return []; } }
  function sonEkle(slug, baslik) {
    try {
      var l = sonOku().filter(function (x) { return x.s !== slug; });
      l.unshift({ s: slug, b: baslik });
      localStorage.setItem(SON_ANAHTAR, JSON.stringify(l.slice(0, 6)));
    } catch (e) { /* gizli mod */ }
  }
  function sonCiz() {
    var kutu = document.getElementById('son-araclar');
    if (!kutu) return;
    var simdi = kutu.getAttribute('data-slug') || '';
    var l = sonOku().filter(function (x) { return x.s !== simdi; });
    if (l.length < 2) return;
    kutu.innerHTML = '<span class="soluk kucuk">Son kullandıkların:</span> ' +
      l.map(function (x) { return '<a class="etiket" href="/' + esc(x.s) + '/">' + esc(x.b) + '</a>'; }).join('');
    kutu.hidden = false;
  }

  /* ---------- basit SVG grafik ---------- */
  function grafikCiz(g) {
    if (!g || !g.seriler || !g.seriler.length) return '';
    var W = 640, H = 240, P = { l: 56, r: 14, t: 18, b: 30 };
    var n = g.etiketler.length, iw = W - P.l - P.r, ih = H - P.t - P.b;
    var tumu = [];
    g.seriler.forEach(function (s) { s.veri.forEach(function (v) { if (typeof v === 'number' && isFinite(v)) tumu.push(v); }); });
    if (!tumu.length) return '';
    var mx = Math.max.apply(null, tumu), mn = Math.min.apply(null, tumu.concat([0]));
    if (mx === mn) mx = mn + 1;
    var x = function (i) { return P.l + (n === 1 ? iw / 2 : iw * i / (n - 1)); };
    var y = function (v) { return P.t + ih - ih * (v - mn) / (mx - mn); };
    var renkler = ['#4f46e5', '#059669', '#dc2626', '#d97706'];
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="grafik" role="img" aria-label="' + esc(g.baslik || 'grafik') + '">';
    for (var k = 0; k <= 4; k++) {
      var vv = mn + (mx - mn) * k / 4, yy = y(vv);
      s += '<line x1="' + P.l + '" y1="' + yy + '" x2="' + (W - P.r) + '" y2="' + yy + '" stroke="#e5e7eb"/>';
      s += '<text x="' + (P.l - 8) + '" y="' + (yy + 4) + '" text-anchor="end" class="gx">' + kisaSayi(vv) + '</text>';
    }
    var adim = Math.max(1, Math.ceil(n / 7));
    g.etiketler.forEach(function (e, i) {
      if (i % adim === 0 || i === n - 1) s += '<text x="' + x(i) + '" y="' + (H - 8) + '" text-anchor="middle" class="gx">' + esc(e) + '</text>';
    });
    g.seriler.forEach(function (ser, si) {
      var renk = ser.renk || renkler[si % renkler.length];
      if (g.tur === 'sutun') {
        var bw = Math.max(2, iw / n / g.seriler.length - 2);
        ser.veri.forEach(function (v, i) {
          if (typeof v !== 'number' || !isFinite(v)) return;
          var bx = x(i) - (g.seriler.length * bw) / 2 + si * bw;
          s += '<rect x="' + bx + '" y="' + y(Math.max(v, 0)) + '" width="' + bw + '" height="' + Math.abs(y(v) - y(0)) + '" fill="' + renk + '" opacity=".85"/>';
        });
      } else {
        var d = '';
        ser.veri.forEach(function (v, i) { if (typeof v === 'number' && isFinite(v)) d += (d ? 'L' : 'M') + x(i) + ' ' + y(v) + ' '; });
        s += '<path d="' + d + '" fill="none" stroke="' + renk + '" stroke-width="2.5" stroke-linejoin="round"/>';
      }
    });
    s += '</svg>';
    var lej = g.seriler.map(function (ser, si) {
      return '<span class="lej"><i style="background:' + (ser.renk || renkler[si % renkler.length]) + '"></i>' + esc(ser.ad) + '</span>';
    }).join('');
    return '<figure class="grafik-kap">' + (g.baslik ? '<figcaption>' + esc(g.baslik) + '</figcaption>' : '') + s + '<div class="lejant">' + lej + '</div></figure>';
  }

  /* ---------- hesaplayıcı ---------- */
  var form = document.getElementById('hesap-form');
  var sonuc = document.getElementById('sonuc');
  var sonSonuc = null;

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
        else if (tip === 'tamsayi') g[el.name] = parseInt(String(el.value).replace(/\./g, ''), 10);
        else g[el.name] = parseNum(el.value);
      });
      return g;
    }
    function yaz(degerler) {
      alanlar.forEach(function (el) {
        if (!(el.name in degerler)) return;
        var v = degerler[el.name];
        if (el.type === 'checkbox') el.checked = (v === true || v === '1' || v === 'true');
        else el.value = v;
      });
    }
    function gizliUygula(g) {
      form.querySelectorAll('[data-gizli]').forEach(function (kutu) {
        var kural = kutu.getAttribute('data-gizli').split('=');
        var kabul = kural[1].split(',');
        kutu.hidden = kabul.indexOf(String(g[kural[0]])) === -1;
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
      if (r.grafik) h += grafikCiz(r.grafik);
      if (r.tablo) {
        h += '<div class="tablo-kap"><table><thead><tr>' + r.tablo.basliklar.map(function (x) { return '<th>' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>';
        r.tablo.satirlar.forEach(function (row) { h += '<tr>' + row.map(function (c) { return '<td>' + (typeof c === 'number' ? fmt(c) : esc(c)) + '</td>'; }).join('') + '</tr>'; });
        h += '</tbody></table></div>';
      }
      if (r.notlar && r.notlar.length) h += '<ul class="sonuc-not">' + r.notlar.map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('') + '</ul>';
      h += '<div class="sonuc-eylem"><button type="button" class="mini" id="kopyala-btn">Sonucu kopyala</button>' +
           '<button type="button" class="mini" id="paylas-btn">Bağlantıyı kopyala</button>' +
           '<span id="eylem-not" class="soluk kucuk"></span></div>';
      sonuc.innerHTML = h;
      var kb = document.getElementById('kopyala-btn'), pb = document.getElementById('paylas-btn');
      if (kb) kb.addEventListener('click', function () { panoya(metinOzet(r), 'Sonuç kopyalandı'); });
      if (pb) pb.addEventListener('click', function () { panoya(paylasLink(), 'Bağlantı kopyalandı'); });
      miniGuncelle(r);
    }

    /* mobil yapışkan sonuç çubuğu */
    var mini = document.getElementById('mini-sonuc'), miniGorunur = false;
    function miniGuncelle(r) {
      if (!mini) return;
      var ana = (r && !r.hata && (r.sonuclar || []).filter(function (x) { return x.vurgu; })[0]) || null;
      if (!ana) { mini.hidden = true; mini.classList.remove('gorunur'); document.body.classList.remove('mini-acik'); miniGorunur = false; return; }
      var d = (typeof ana.deger === 'number') ? fmt(ana.deger, ana.ondalik) : ana.deger;
      mini.querySelector('.me').textContent = ana.etiket;
      mini.querySelector('.md').textContent = d + (ana.birim ? ' ' + ana.birim : '');
      mini.hidden = false;
      miniKontrol();
    }
    function miniKontrol() {
      if (!mini || mini.hidden) return;
      var k = document.querySelector('.hesaplayici');
      if (!k) return;
      var kutu = k.getBoundingClientRect();
      var anaKutu = sonuc.querySelector('.sonuc-ana');
      var sonucGorunur = anaKutu && anaKutu.getBoundingClientRect().bottom > 0 && anaKutu.getBoundingClientRect().top < window.innerHeight;
      // hesaplayıcı ekranda ama ana sonuç görünmüyorsa (ya da form altında kaldıysa) çubuğu göster
      var goster = !sonucGorunur && kutu.bottom > 0 && kutu.top < window.innerHeight * 1.6;
      if (goster !== miniGorunur) {
        miniGorunur = goster;
        mini.classList.toggle('gorunur', goster);
        document.body.classList.toggle('mini-acik', goster);
      }
    }
    if (mini) {
      mini.addEventListener('click', function () {
        var a = sonuc.querySelector('.sonuc-ana') || sonuc;
        a.scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
      window.addEventListener('scroll', miniKontrol, { passive: true });
      window.addEventListener('resize', miniKontrol);
    }
    function metinOzet(r) {
      var l = [document.title.split('|')[0].trim()];
      (r.sonuclar || []).forEach(function (s) {
        var d = (typeof s.deger === 'number') ? fmt(s.deger, s.ondalik) : s.deger;
        l.push(s.etiket + ': ' + d + (s.birim ? ' ' + s.birim : ''));
      });
      l.push(location.origin + location.pathname);
      return l.join('\n');
    }
    function paylasLink() {
      var g = oku(), p = [];
      alanlar.forEach(function (el) {
        var v = el.type === 'checkbox' ? (el.checked ? '1' : '0') : el.value;
        if (v !== '' && v !== null && v !== undefined) p.push(encodeURIComponent(el.name) + '=' + encodeURIComponent(v));
      });
      return location.origin + location.pathname + (p.length ? '?' + p.join('&') : '');
    }
    function panoya(metin, mesaj) {
      var not = document.getElementById('eylem-not');
      var bitir = function (ok) { if (not) { not.textContent = ok ? '✓ ' + mesaj : 'Kopyalanamadı'; setTimeout(function () { not.textContent = ''; }, 2500); } };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(metin).then(function () { bitir(true); }, function () { bitir(false); });
      else {
        var ta = document.createElement('textarea'); ta.value = metin; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); bitir(true); } catch (e) { bitir(false); }
        document.body.removeChild(ta);
      }
    }
    function calistir() {
      var g = oku();
      gizliUygula(g);
      try { sonSonuc = window.hesapla(g, window.ORAN || {}); ciz(sonSonuc); }
      catch (e) { sonuc.innerHTML = '<p class="sonuc-hata">Hesaplanamadı: ' + esc(e.message) + '</p>'; }
    }
    form.addEventListener('input', calistir);
    form.addEventListener('change', calistir);
    var hb = document.getElementById('hesapla-btn'); if (hb) hb.addEventListener('click', calistir);
    var sb = document.getElementById('sifirla-btn');
    if (sb) sb.addEventListener('click', function () {
      alanlar.forEach(function (el) { if (el.type === 'checkbox') el.checked = !!varsayilan[el.name]; else el.value = varsayilan[el.name]; });
      calistir();
    });

    /* hazır senaryolar */
    document.querySelectorAll('[data-senaryo]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var d;
        try { d = JSON.parse(btn.getAttribute('data-senaryo')); } catch (e) { return; }
        yaz(d);
        calistir();
        document.querySelectorAll('[data-senaryo]').forEach(function (b) { b.classList.remove('secili'); });
        btn.classList.add('secili');
        var k = document.querySelector('.hesaplayici');
        if (k) k.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    /* URL parametrelerinden doldur (paylaşılan sonuç) */
    var qp = new URLSearchParams(location.search), dolu = {};
    alanlar.forEach(function (el) { if (qp.has(el.name)) dolu[el.name] = qp.get(el.name); });
    if (Object.keys(dolu).length) yaz(dolu);

    calistir();

    var kutu = document.getElementById('son-araclar');
    if (kutu) sonEkle(kutu.getAttribute('data-slug'), kutu.getAttribute('data-baslik'));
  }
  sonCiz();

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
