# -*- coding: utf-8 -*-
HESAP = {
    "slug": "asgari-ucret-hesaplama",
    "baslik": "Asgari Ücret 2026 Hesaplama",
    "h1": "2026 Asgari Ücret Ne Kadar? Brüt, Net, Günlük, Saatlik ve İşveren Maliyeti",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 asgari ücret: brüt 33.030 ₺, net 28.075,50 ₺. Kesintiler (SGK %14, işsizlik %1), günlük ve saatlik asgari ücret, işverene maliyet, eksik gün ve asgari ücret katı hesaplama.",
    "kisa_cevap": "2026 yılında asgari ücret aylık brüt 33.030 ₺, net 28.075,50 ₺'dir (günlük brüt 1.101 ₺). Brütten yalnızca %14 SGK işçi payı (4.624,20 ₺) ve %1 işsizlik sigortası (330,30 ₺) kesilir; gelir ve damga vergisi istisna kapsamındadır. İşverene teşviksiz maliyeti 40.461,75 ₺'dir.",
    "girdiler": [
        {"id": "kat", "etiket": "Asgari ücret katı", "tip": "sayi", "varsayilan": "1", "ipucu": "ör. 1,5 = asgari ücretin 1,5 katı"},
        {"id": "gun", "etiket": "Çalışılan gün", "tip": "tamsayi", "varsayilan": "30", "birim": "gün", "ipucu": "eksik gün için 30'dan az girin"},
    ],
    "js": r"""
function hesapla(g, O){
  var kat = g.kat > 0 ? g.kat : 1, gun = (g.gun > 0 && g.gun <= 31) ? g.gun : 30;
  var A = O.asgari_ucret, S = O.sgk;
  var brut = A.brut * kat * gun / 30;
  var sgk = brut * S.isci_orani, iss = brut * S.issizlik_isci_orani;
  var gvM = brut - sgk - iss, asgM = A.brut * gun / 30 * (1 - S.isci_orani - S.issizlik_isci_orani);
  var gv = Math.max(0, gvM * 0.15 - asgM * 0.15);           // Ocak ayı, ilk dilim
  var dv = Math.max(0, brut * O.damga_vergisi.ucret_oran - A.brut * gun / 30 * O.damga_vergisi.ucret_oran);
  var net = brut - sgk - iss - gv - dv;
  var isveren = brut + brut * (S.isveren_orani + S.issizlik_isveren_orani);
  return {
    sonuclar: [
      {etiket: 'Net ücret (Ocak)', deger: net, birim: '₺', vurgu: true},
      {etiket: 'Brüt ücret', deger: brut, birim: '₺'},
      {etiket: 'SGK işçi payı (%14)', deger: sgk, birim: '₺'},
      {etiket: 'İşsizlik sigortası (%1)', deger: iss, birim: '₺'},
      {etiket: 'Gelir vergisi (istisna sonrası)', deger: gv, birim: '₺'},
      {etiket: 'Damga vergisi (istisna sonrası)', deger: dv, birim: '₺'},
      {etiket: 'Günlük brüt', deger: A.brut * kat / 30, birim: '₺'},
      {etiket: 'Saatlik brüt (225 saat/ay)', deger: A.brut * kat / 225, birim: '₺'},
      {etiket: 'İşverene maliyet (teşviksiz %22,5)', deger: isveren, birim: '₺'}
    ],
    notlar: [kat !== 1 ? 'Asgari ücretin ' + kat + ' katı için Ocak ayı hesabıdır; yıl içinde kümülatif vergiyle net düşer (ayrıntı: Brüt-Net Maaş).' : 'Asgari ücretin tamamı gelir ve damga vergisinden istisna olduğu için net tutar yıl boyunca değişmez.',
             'İşveren 5 puanlık SGK teşvikinden yararlanıyorsa maliyet ' + NH.fmt(brut + brut * (S.isveren_orani - 0.05 + S.issizlik_isveren_orani)) + ' ₺ olur.']
  };
}
""",
    "nasil": [
        "Asgari ücret, Asgari Ücret Tespit Komisyonu tarafından belirlenir ve Resmî Gazete'de yayımlanır. 2026 için aylık brüt 33.030 ₺ olarak açıklandı; günlük brüt 1.101 ₺'dir (aylık 30 gün üzerinden). Net tutar, brütten SGK işçi payı (%14) ve işsizlik sigortası işçi payı (%1) düşülerek bulunur: 33.030 − 4.624,20 − 330,30 = 28.075,50 ₺.",
        "2022'den beri asgari ücret gelir vergisi ve damga vergisinden istisnadır; bu istisna asgari ücretin üzerindeki maaşlarda da asgari ücrete denk gelen kısım için uygulanır. Bu yüzden asgari ücretli için gelir vergisi ve damga vergisi kesintisi sıfırdır ve net ücret yılın her ayında aynıdır.",
        "İşverene maliyet, brüt ücrete SGK işveren payı (%20,5) ve işsizlik sigortası işveren payı (%2) eklenerek bulunur: 33.030 × 1,225 = 40.461,75 ₺. Prim borcu olmayan işverenler 5 puanlık hazine teşvikinden yararlanırsa maliyet 38.810,25 ₺'ye iner. Eksik günlü çalışmada brüt, gün sayısına oranlanır.",
    ],
    "formul": [
        "Net = brüt − brüt × %14 (SGK) − brüt × %1 (işsizlik)   [GV ve damga = 0, istisna]",
        "Günlük brüt = aylık brüt ÷ 30 · Saatlik brüt = aylık brüt ÷ 225",
        "İşveren maliyeti = brüt × (1 + %20,5 + %2) · teşvikli: brüt × (1 + %15,5 + %2)",
        "Eksik gün: brüt = 33.030 × çalışılan gün ÷ 30",
    ],
    "ornekler": [
        {"baslik": "Tam ay asgari ücret", "adimlar": ["SGK: 33.030 × 0,14 = 4.624,20 ₺", "İşsizlik: 33.030 × 0,01 = 330,30 ₺", "Net: 33.030 − 4.954,50 = 28.075,50 ₺"]},
        {"baslik": "20 gün çalışma", "adimlar": ["Brüt: 33.030 × 20/30 = 22.020 ₺", "Net: 22.020 × 0,85 = 18.717 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 asgari ücret özet tablosu",
        "basliklar": ["Kalem", "Tutar"],
        "satirlar": [["Aylık brüt", "33.030,00 ₺"], ["Günlük brüt", "1.101,00 ₺"], ["SGK işçi payı (%14)", "4.624,20 ₺"], ["İşsizlik işçi payı (%1)", "330,30 ₺"], ["Gelir vergisi", "0 ₺ (istisna)"], ["Damga vergisi", "0 ₺ (istisna)"], ["Aylık net", "28.075,50 ₺"], ["İşverene maliyet (teşviksiz)", "40.461,75 ₺"], ["İşverene maliyet (5 puan teşvikli)", "38.810,25 ₺"], ["SGK prim tavanı (9 kat)", "297.270,00 ₺"]],
        "not": "Asgari Ücret Tespit Komisyonu kararı, Resmî Gazete (Aralık 2025); SGK 2026 parametreleri.",
    },
    "sss": [
        {"soru": "2026 asgari ücret net kaç TL?", "cevap": "28.075,50 ₺. Brüt 33.030 ₺'den %14 SGK ve %1 işsizlik primi düşülür; vergi kesilmez."},
        {"soru": "Asgari ücret yıl ortasında artacak mı?", "cevap": "Komisyon kararına bağlıdır; 2026 için tek belirleme yapıldı. Ara zam olursa bu sayfa ve oran dosyası aynı gün güncellenir."},
        {"soru": "Asgari ücretli gelir vergisi öder mi?", "cevap": "Hayır. 2022'den itibaren asgari ücrete isabet eden kazanç gelir ve damga vergisinden istisnadır."},
        {"soru": "Saatlik asgari ücret ne kadar?", "cevap": "Aylık 225 saat esasıyla 33.030 ÷ 225 = 146,80 ₺ brüt. Fazla mesai bu saatlik ücretin 1,5 katı (220,20 ₺) üzerinden ödenir."},
        {"soru": "İşverene asgari ücretli maliyeti nedir?", "cevap": "Teşviksiz 40.461,75 ₺ (brüt + %22,5 işveren primi); 5 puanlık teşvikle 38.810,25 ₺."},
        {"soru": "Asgari ücretten AGİ kesintisi/ödemesi var mı?", "cevap": "AGİ 2022'de kaldırıldı; yerine asgari ücret vergi istisnası getirildi. Bordroda AGİ satırı artık yer almaz."},
    ],
    "kaynaklar": [
        {"ad": "ÇSGB — Asgari Ücret Tespit Komisyonu 2026 kararı", "url": "https://www.csgb.gov.tr/"},
        {"ad": "SGK — 2026 prime esas kazanç sınırları", "url": "https://www.sgk.gov.tr/"},
    ],
    "ilgili": ["brut-net-maas-hesaplama", "kidem-tazminati-hesaplama", "gelir-vergisi-hesaplama"],
}
