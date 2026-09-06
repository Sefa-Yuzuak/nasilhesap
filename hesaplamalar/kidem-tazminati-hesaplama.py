# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kidem-tazminati-hesaplama",
    "baslik": "Kıdem ve İhbar Tazminatı Hesaplama",
    "h1": "Kıdem Tazminatı Hesaplama 2026 — İhbar Tazminatı ve Tavan",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 kıdem tazminatı hesaplama: işe giriş-çıkış tarihi ve brüt ücretle kıdem tazminatı, tavan (Ocak-Haziran 64.948,77 ₺ / Temmuz-Aralık 73.729,84 ₺), damga vergisi kesintisi ve ihbar süresi-tazminatı. Formül ve örneklerle.",
    "kisa_cevap": "Kıdem tazminatı = her tam yıl için 30 günlük giydirilmiş brüt ücret (yıldan artan süreler oranlanır). Aylık brüt, tavanı (2026'nın ikinci yarısı için 73.729,84 ₺) aşamaz. Tazminattan yalnızca ‰7,59 damga vergisi kesilir; gelir vergisi ve SGK kesilmez. En az 1 yıl kıdem şarttır.",
    "girdiler": [
        {"id": "brut", "etiket": "Aylık giydirilmiş brüt ücret", "tip": "sayi", "varsayilan": "60000", "birim": "₺", "ipucu": "yol, yemek gibi düzenli ödemeler dahil"},
        {"id": "giris", "etiket": "İşe giriş tarihi", "tip": "tarih", "varsayilan": "2019-03-01"},
        {"id": "cikis", "etiket": "İşten çıkış tarihi", "tip": "tarih", "varsayilan": "2026-09-01"},
        {"id": "ihbar", "etiket": "İhbar tazminatı da hesaplansın", "tip": "onay", "varsayilan": True, "onay_metin": "İhbar süresi kullandırılmadı"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.brut > 0)) return {hata: 'Brüt ücreti girin.'};
  if (!g.giris || !g.cikis) return {hata: 'Giriş ve çıkış tarihlerini seçin.'};
  var gi = new Date(g.giris), ci = new Date(g.cikis);
  var gun = Math.round((ci - gi) / 86400000);
  if (gun <= 0) return {hata: 'Çıkış tarihi giriş tarihinden sonra olmalı.'};
  var yil = Math.floor(gun / 365), kalanGun = gun - yil * 365;
  var ayNo = ci.getMonth() + 1, ciYil = ci.getFullYear();
  var tavan = ayNo <= 6 ? O.kidem.tavan_ocak_haziran : O.kidem.tavan_temmuz_aralik;
  var esas = Math.min(g.brut, tavan);
  var s = [], n = [];
  if (gun < 365) {
    s.push({etiket: 'Kıdem tazminatı', deger: 'Hak yok (1 yıl dolmadı)', vurgu: true});
  } else {
    var kidemBrut = esas * yil + esas * (kalanGun / 365);
    var damga = kidemBrut * O.kidem.damga_oran;
    s.push({etiket: 'Net kıdem tazminatı', deger: kidemBrut - damga, birim: '₺', vurgu: true});
    s.push({etiket: 'Brüt kıdem tazminatı', deger: kidemBrut, birim: '₺'});
    s.push({etiket: 'Damga vergisi (‰7,59)', deger: damga, birim: '₺'});
    s.push({etiket: 'Hesaba esas aylık ücret', deger: esas, birim: '₺'});
    if (g.brut > tavan) n.push('Brüt ücret tavanı aştığı için hesap tavan (' + NH.fmt(tavan) + ' ₺) üzerinden yapıldı.');
  }
  s.push({etiket: 'Çalışma süresi', deger: yil + ' yıl ' + Math.floor(kalanGun / 30) + ' ay ' + (kalanGun % 30) + ' gün (' + gun + ' gün)'});
  if (g.ihbar) {
    var ay = gun / 30.4375, hafta = 8;
    for (var i = 0; i < O.ihbar.sureler_hafta.length; i++) { var ust = O.ihbar.sureler_hafta[i][0]; if (ust === null || ay < ust) { hafta = O.ihbar.sureler_hafta[i][1]; break; } }
    var ihbarBrut = (g.brut / 30) * 7 * hafta;
    s.push({etiket: 'İhbar süresi', deger: hafta + ' hafta'});
    s.push({etiket: 'İhbar tazminatı (brüt)', deger: ihbarBrut, birim: '₺'});
    n.push('İhbar tazminatı brüttür; gelir vergisi ve damga vergisine tabidir, SGK kesilmez. Net tutar yıl içindeki vergi dilimine göre değişir.');
  }
  if (ciYil !== O.yil) n.push('Tavan tutarları ' + O.yil + ' yılına aittir; farklı yıl için ilgili dönemin tavanını kullanın.');
  n.push('Kıdem tazminatı gelir vergisinden ve SGK priminden muaftır; yalnızca damga vergisi kesilir.');
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Kıdem tazminatı, en az bir yıl çalışmış işçiye, iş sözleşmesinin kanunda sayılan hallerde (işveren feshi, emeklilik, askerlik, evlilik nedeniyle kadın işçinin ayrılması, haklı nedenle işçi feshi vb.) sona ermesi durumunda ödenir. Her tam yıl için 30 günlük ücret tutarında hesaplanır; bir yıldan artan süreler için aynı oran üzerinden kıstelyevm (oranlama) yapılır.",
        "Hesaba esas ücret 'giydirilmiş brüt' ücrettir: çıplak brüt maaşa yol, yemek, ikramiye, prim gibi süreklilik arz eden ayni ve nakdi ödemelerin aylık karşılığı eklenir. Ancak bu ücret, devlet memurlarına ödenen en yüksek emekli ikramiyesine göre belirlenen kıdem tazminatı tavanını aşamaz; 2026 için tavan Ocak-Haziran'da 64.948,77 ₺, Temmuz-Aralık'ta 73.729,84 ₺'dir.",
        "İhbar tazminatı ise belirsiz süreli sözleşmeyi bildirim süresine uymadan fesheden tarafın ödediği tutardır. Bildirim süresi kıdeme göre 2, 4, 6 veya 8 haftadır ve ihbar tazminatı bu haftaların ücreti kadardır. Kıdem tazminatından farklı olarak ihbar tazminatı gelir vergisine tabidir.",
    ],
    "formul": [
        "Kıdem tazminatı (brüt) = min(giydirilmiş brüt, tavan) × yıl + min(giydirilmiş brüt, tavan) × (artan gün ÷ 365)",
        "Net kıdem = brüt kıdem − brüt kıdem × ‰7,59 (damga vergisi)",
        "İhbar süresi: 0-6 ay → 2 hafta · 6-18 ay → 4 hafta · 18-36 ay → 6 hafta · 36+ ay → 8 hafta",
        "İhbar tazminatı (brüt) = günlük brüt ücret × 7 × hafta",
    ],
    "ornekler": [
        {"baslik": "7 yıl 6 ay kıdem, 60.000 ₺ brüt, çıkış Eylül 2026",
         "adimlar": ["Tavan 73.729,84 ₺ > 60.000 ₺ → esas ücret 60.000 ₺", "Tam yıllar: 60.000 × 7 = 420.000 ₺", "Artan 6 ay (≈182 gün): 60.000 × 182/365 ≈ 29.918 ₺", "Brüt kıdem ≈ 449.918 ₺; damga ‰7,59 ≈ 3.415 ₺; net ≈ 446.503 ₺", "İhbar: 36+ ay → 8 hafta → 60.000/30 × 7 × 8 = 112.000 ₺ brüt"]},
        {"baslik": "Tavanı aşan ücret: 100.000 ₺ brüt, 3 yıl, çıkış Mart 2026",
         "adimlar": ["Tavan Ocak-Haziran 64.948,77 ₺ < 100.000 ₺ → esas ücret 64.948,77 ₺", "Brüt kıdem: 64.948,77 × 3 = 194.846,31 ₺", "Damga: 1.478,88 ₺ → net 193.367,43 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 kıdem tazminatı tavanı ve ihbar süreleri",
        "basliklar": ["Kalem", "Değer"],
        "satirlar": [["Tavan (01.01.2026 – 30.06.2026)", "64.948,77 ₺"], ["Tavan (01.07.2026 – 31.12.2026)", "73.729,84 ₺"],
                     ["İhbar: 6 aydan az", "2 hafta"], ["İhbar: 6 ay – 1,5 yıl", "4 hafta"], ["İhbar: 1,5 – 3 yıl", "6 hafta"], ["İhbar: 3 yıldan fazla", "8 hafta"]],
        "not": "Tavan, Hazine ve Maliye Bakanlığı'nın Ocak ve Temmuz aylarında yayımladığı memur maaş katsayısı genelgeleriyle güncellenir.",
    },
    "sss": [
        {"soru": "Kıdem tazminatı kimlere ödenir?", "cevap": "En az 1 yıl kıdemi olan ve iş sözleşmesi 1475 sayılı Kanun m.14'teki hallerde sona eren işçilere: işverenin haklı neden dışında feshi, işçinin haklı nedenle feshi, emeklilik, askerlik, kadın işçinin evlilik tarihinden itibaren 1 yıl içinde ayrılması, ölüm. İstifa eden işçi kural olarak alamaz."},
        {"soru": "Kıdem tazminatından hangi kesintiler yapılır?", "cevap": "Yalnızca ‰7,59 damga vergisi. Gelir vergisi ve SGK primi kesilmez (tavanı aşmayan tutar için)."},
        {"soru": "2026 kıdem tazminatı tavanı ne kadar?", "cevap": "1 Ocak–30 Haziran 2026 için 64.948,77 ₺; 1 Temmuz–31 Aralık 2026 için 73.729,84 ₺. Giydirilmiş brüt ücret bu tutarı aşarsa hesap tavan üzerinden yapılır."},
        {"soru": "Giydirilmiş ücret nedir?", "cevap": "Çıplak brüt ücrete ek olarak yol, yemek, yakacak, ikramiye, prim gibi düzenli ödemelerin aylık karşılığının eklenmesiyle bulunan ücrettir. Kıdem hesabında bu ücret kullanılır."},
        {"soru": "İhbar tazminatı ile kıdem tazminatı birlikte alınır mı?", "cevap": "Evet, şartları ayrı ayrı oluşmuşsa ikisi birden ödenir. İşveren ihbar süresini kullandırdıysa ihbar tazminatı doğmaz; kıdem tazminatı bundan etkilenmez."},
        {"soru": "İstifa eden işçi kıdem tazminatı alabilir mi?", "cevap": "Kural olarak hayır. Ancak haklı nedenle fesih (ücretin ödenmemesi, mobbing vb.), emeklilik yaşı/prim gününü doldurma, askerlik ve evlilik (kadın işçi) hallerinde işçi kendisi ayrılsa da kıdem tazminatına hak kazanır."},
    ],
    "kaynaklar": [
        {"ad": "1475 sayılı İş Kanunu m.14 (kıdem tazminatı) — mevzuat.gov.tr", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=1475&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "4857 sayılı İş Kanunu m.17 (ihbar süreleri)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=4857&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "Hazine ve Maliye Bakanlığı — kıdem tazminatı tavanı genelgeleri", "url": "https://www.hmb.gov.tr/"},
    ],
    "ilgili": ["brut-net-maas-hesaplama", "gelir-vergisi-hesaplama", "gun-hesaplama"],
}
