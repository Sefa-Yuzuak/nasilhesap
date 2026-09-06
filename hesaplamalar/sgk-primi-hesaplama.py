# -*- coding: utf-8 -*-
HESAP = {
    "slug": "sgk-primi-hesaplama",
    "baslik": "SGK Primi Hesaplama",
    "h1": "SGK Primi Hesaplama 2026 — İşçi ve İşveren Payı, Teşvikli Maliyet",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 SGK primi hesaplama: brüt ücrete göre işçi payı (%14 + %1 işsizlik), işveren payı (%20,5 + %2), 5 puanlık teşvik, prime esas kazanç taban-tavanı (33.030 – 297.270 ₺) ve toplam prim.",
    "kisa_cevap": "SGK primi brüt ücretin %37,5'idir: işçi %14 + işsizlik %1 (bordrodan kesilir), işveren %20,5 + işsizlik %2 (işveren ek öder). 50.000 ₺ brüt için işçi 7.500 ₺, işveren 11.250 ₺, toplam 18.750 ₺ prim ödenir. Prime esas kazanç 2026'da en az 33.030, en çok 297.270 ₺'dir; 5 puanlık teşvikte işveren payı %15,5'e iner.",
    "girdiler": [
        {"id": "brut", "etiket": "Aylık brüt ücret", "tip": "sayi", "varsayilan": "50000", "birim": "₺"},
        {"id": "tesvik", "etiket": "İşveren teşviki", "tip": "secim", "varsayilan": "yok", "secenekler": [["yok", "Teşvik yok (%20,5)"], ["5", "5 puanlık hazine teşviki (%15,5)"]]},
        {"id": "gun", "etiket": "Prim günü", "tip": "tamsayi", "varsayilan": "30", "birim": "gün"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.brut > 0)) return {hata: 'Brüt ücreti girin.'};
  var S = O.sgk, gun = (g.gun > 0 && g.gun <= 30) ? g.gun : 30;
  var taban = S.taban * gun / 30, tavan = S.tavan * gun / 30;
  var pek = Math.min(Math.max(g.brut, taban), tavan);
  var isci = pek * S.isci_orani, isciIss = pek * S.issizlik_isci_orani;
  var isvOran = S.isveren_orani - (g.tesvik === '5' ? 0.05 : 0);
  var isv = pek * isvOran, isvIss = pek * S.issizlik_isveren_orani;
  var n = ['Prime esas kazanç (PEK) alt sınır ' + NH.fmt(taban) + ' ₺, üst sınır ' + NH.fmt(tavan) + ' ₺ (' + gun + ' gün).'];
  if (g.brut > tavan) n.push('Brüt tavanı aştığı için prim tavan üzerinden hesaplandı; aşan kısımdan prim kesilmez.');
  if (g.brut < taban) n.push('Brüt tabanın altında; prim en az asgari ücret üzerinden ödenir.');
  n.push('İşveren payı: malullük-yaşlılık-ölüm %11 + genel sağlık %7,5 + kısa vadeli sigorta kolları %2 = %20,5. Teşvik şartları: borç yok, bildirge zamanında, kayıt dışı yok.');
  return {
    sonuclar: [
      {etiket: 'Toplam SGK primi (işçi + işveren)', deger: isci + isciIss + isv + isvIss, birim: '₺', vurgu: true},
      {etiket: 'Prime esas kazanç', deger: pek, birim: '₺'},
      {etiket: 'İşçi payı SGK (%14)', deger: isci, birim: '₺'},
      {etiket: 'İşçi payı işsizlik (%1)', deger: isciIss, birim: '₺'},
      {etiket: 'İşveren payı SGK (%' + (isvOran*100).toFixed(1).replace('.', ',') + ')', deger: isv, birim: '₺'},
      {etiket: 'İşveren payı işsizlik (%2)', deger: isvIss, birim: '₺'},
      {etiket: 'Bordrodan kesilen (işçi toplam)', deger: isci + isciIss, birim: '₺'},
      {etiket: 'İşverene toplam maliyet (brüt + işveren payı)', deger: g.brut + isv + isvIss, birim: '₺'}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "4/a (SSK) kapsamındaki bir çalışan için SGK primi, prime esas kazanç (PEK) üzerinden hesaplanır. PEK, brüt ücrettir ancak alt sınırı asgari ücret (2026'da 33.030 ₺), üst sınırı asgari ücretin 9 katıdır (297.270 ₺). Prim oranları 5510 sayılı Kanun'da belirlenmiştir: işçi payı %14 SGK + %1 işsizlik sigortası; işveren payı %20,5 SGK + %2 işsizlik.",
        "İşveren payının %20,5'i üç koldan oluşur: malullük, yaşlılık ve ölüm sigortası %11, genel sağlık sigortası %7,5, kısa vadeli sigorta kolları (iş kazası, meslek hastalığı, analık) %2. Prim borcu olmayan, bildirgelerini zamanında veren ve kayıt dışı işçi çalıştırmayan işverenler 5 puanlık hazine desteğinden yararlanır; bu durumda işveren payı %15,5'e iner.",
        "İşçi payı bordrodan kesilir ve gelir vergisi matrahını düşürür; işveren payı ise brüt ücretin üzerine eklenen bir maliyettir. Toplam prim, brüt ücretin %37,5'idir (teşvikli %32,5). Primler izleyen ayın sonuna kadar SGK'ya ödenir; gecikmede aylık gecikme zammı işler.",
    ],
    "formul": [
        "PEK = min(max(brüt, taban), tavan) · taban 33.030 ₺ · tavan 297.270 ₺ (2026)",
        "İşçi payı = PEK × (%14 + %1)",
        "İşveren payı = PEK × (%20,5 + %2) · 5 puan teşvikli: PEK × (%15,5 + %2)",
        "Toplam prim = PEK × %37,5 (teşvikli %32,5)",
    ],
    "ornekler": [
        {"baslik": "50.000 ₺ brüt, teşviksiz", "adimlar": ["İşçi: 50.000 × 0,15 = 7.500 ₺", "İşveren: 50.000 × 0,225 = 11.250 ₺", "Toplam 18.750 ₺; işverene maliyet 61.250 ₺"]},
        {"baslik": "350.000 ₺ brüt (tavan üstü)", "adimlar": ["PEK = 297.270 ₺", "İşçi: 44.590,50 ₺ · işveren: 66.885,75 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 SGK prim oranları (4/a)",
        "basliklar": ["Sigorta kolu", "İşçi", "İşveren", "Toplam"],
        "satirlar": [["Malullük, yaşlılık, ölüm", "%9", "%11", "%20"], ["Genel sağlık sigortası", "%5", "%7,5", "%12,5"], ["Kısa vadeli sigorta kolları", "—", "%2", "%2"], ["İşsizlik sigortası", "%1", "%2", "%3"], ["Toplam", "%15", "%22,5", "%37,5"]],
        "not": "5510 sayılı Kanun m.81 ve 4447 sayılı Kanun m.49. 5 puanlık hazine desteği işveren malullük-yaşlılık payından düşülür.",
    },
    "sss": [
        {"soru": "SGK primi yüzde kaç?", "cevap": "Toplam %37,5: işçi %15 (14 + 1 işsizlik), işveren %22,5 (20,5 + 2 işsizlik). Teşvikli işverende %32,5."},
        {"soru": "SGK tavanı ne demek?", "cevap": "Prime esas kazanç üst sınırı; 2026'da 297.270 ₺ (asgari ücretin 9 katı). Bunun üzerindeki ücretten prim kesilmez, ancak emeklilik hesabına da yansımaz."},
        {"soru": "Prim günü 30 mu 31 mi?", "cevap": "SGK'da her ay 30 gün sayılır; tam çalışılan Şubat da 30 gündür. Eksik günlerde prim gün sayısıyla orantılanır."},
        {"soru": "Emekli çalışanın primi farklı mı?", "cevap": "Evet. Emekli olup çalışanlardan sosyal güvenlik destek primi (SGDP) alınır: işçi %7,5, işveren %22,5 (toplam %30); işsizlik primi kesilmez."},
        {"soru": "Bağ-Kur (4/b) primi ne kadar?", "cevap": "Beyan edilen kazancın %34,5'i (5 puan indirimle %31); 2026'da asgari ücret üzerinden aylık yaklaşık 10.239 ₺ (indirimli)."},
    ],
    "kaynaklar": [
        {"ad": "5510 sayılı Sosyal Sigortalar ve Genel Sağlık Sigortası Kanunu m.81, m.82", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=5510&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "SGK — 2026 prime esas kazanç alt ve üst sınırları", "url": "https://www.sgk.gov.tr/"},
    ],
    "ilgili": ["brut-net-maas-hesaplama", "asgari-ucret-hesaplama", "kidem-tazminati-hesaplama"],
}
