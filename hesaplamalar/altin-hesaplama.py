# -*- coding: utf-8 -*-
HESAP = {
    "slug": "altin-hesaplama",
    "baslik": "Altın Hesaplama",
    "h1": "Altın Hesaplama — Gram, Çeyrek, Yarım, Tam ve Cumhuriyet Altını Çevirici",
    "kategori": "kredi-finans",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Altın hesaplama: gram altın fiyatını girin, çeyrek-yarım-tam-Cumhuriyet altınının TL değerini, has (saf) altın karşılığını ve elinizdeki altınların toplam değerini hesaplayın. 22 ayar milyem 916 esaslı.",
    "kisa_cevap": "Ziynet altınları 22 ayardır (916 milyem): çeyrek 1,75 gram, yarım 3,50 gram, tam 7,00 gram, Cumhuriyet (Ata) altını 7,216 gram gelir. Has (saf) altın karşılığı ağırlığın 22/24'üdür; çeyrek altında yaklaşık 1,60 gram saf altın bulunur. Gram (24 ayar) altın 5.000 ₺ ise bir çeyreğin saf altın değeri yaklaşık 8.020 ₺'dir; piyasa satış fiyatı işçilik ve talep nedeniyle bunun biraz üzerindedir.",
    "senaryolar": [
        {"ad": "Gram 5.000 ₺", "degerler": {"gram_fiyat": "5000", "ceyrek": "0", "yarim": "0", "tam": "0", "cumhuriyet": "0", "gram_adet": "0", "bilezik_gr": "0"}},
        {"ad": "10 çeyrek", "degerler": {"gram_fiyat": "5000", "ceyrek": "10", "yarim": "0", "tam": "0", "cumhuriyet": "0", "gram_adet": "0", "bilezik_gr": "0"}},
        {"ad": "Karışık portföy", "degerler": {"gram_fiyat": "5000", "ceyrek": "8", "yarim": "2", "tam": "1", "cumhuriyet": "1", "gram_adet": "20", "bilezik_gr": "0"}},
        {"ad": "22 ayar bilezik 50 gr", "degerler": {"gram_fiyat": "5000", "ceyrek": "0", "yarim": "0", "tam": "0", "cumhuriyet": "0", "gram_adet": "0", "bilezik_gr": "50"}},
    ],
    "girdiler": [
        {"id": "gram_fiyat", "etiket": "Gram altın (24 ayar) fiyatı", "tip": "sayi", "varsayilan": "5000", "birim": "₺", "genis": True, "ipucu": "güncel kapalıçarşı/banka fiyatı"},
        {"id": "ceyrek", "etiket": "Çeyrek altın adedi", "tip": "sayi", "varsayilan": "0", "birim": "adet"},
        {"id": "yarim", "etiket": "Yarım altın adedi", "tip": "sayi", "varsayilan": "0", "birim": "adet"},
        {"id": "tam", "etiket": "Tam altın adedi", "tip": "sayi", "varsayilan": "0", "birim": "adet"},
        {"id": "cumhuriyet", "etiket": "Cumhuriyet (Ata) altını adedi", "tip": "sayi", "varsayilan": "0", "birim": "adet"},
        {"id": "gram_adet", "etiket": "Gram altın (24 ayar)", "tip": "sayi", "varsayilan": "0", "birim": "gram"},
        {"id": "bilezik_gr", "etiket": "22 ayar takı / bilezik", "tip": "sayi", "varsayilan": "0", "birim": "gram"},
    ],
    "js": r"""
var Z = [['Çeyrek altın','ceyrek',1.75], ['Yarım altın','yarim',3.50], ['Tam altın','tam',7.00], ['Cumhuriyet (Ata)','cumhuriyet',7.216]];
var AYAR22 = 22/24; // 0,9166…
function hesapla(g){
  var gf = g.gram_fiyat;
  if (!(gf > 0)) return {hata: 'Güncel gram altın (24 ayar) fiyatını girin.'};
  var s = [], sat = [], hasToplam = 0, deger = 0, adetVar = false;
  for (var i = 0; i < Z.length; i++) {
    var ad = Z[i][0], k = Z[i][1], gr = Z[i][2];
    var adet = g[k] > 0 ? g[k] : 0;
    var has = gr * AYAR22, birim = has * gf;
    sat.push([ad, gr.toString().replace('.', ',') + ' gr', (Math.round(has * 1000) / 1000).toString().replace('.', ',') + ' gr', NH.fmt(birim) + ' ₺', adet, NH.fmt(birim * adet) + ' ₺']);
    if (adet > 0) { adetVar = true; hasToplam += has * adet; deger += birim * adet; }
  }
  var ga = g.gram_adet > 0 ? g.gram_adet : 0;
  if (ga > 0) { adetVar = true; hasToplam += ga; deger += ga * gf; sat.push(['Gram altın (24 ayar)', '1 gr', '1 gr', NH.fmt(gf) + ' ₺', ga, NH.fmt(ga * gf) + ' ₺']); }
  var bg = g.bilezik_gr > 0 ? g.bilezik_gr : 0;
  if (bg > 0) { adetVar = true; var bhas = bg * AYAR22; hasToplam += bhas; deger += bhas * gf; sat.push(['22 ayar takı', bg + ' gr', (Math.round(bhas*100)/100) + ' gr', NH.fmt(AYAR22 * gf) + ' ₺/gr', bg + ' gr', NH.fmt(bhas * gf) + ' ₺']); }
  if (adetVar) {
    s.push({etiket: 'Toplam altın değeri (has altın üzerinden)', deger: deger, birim: '₺', vurgu: true});
    s.push({etiket: 'Toplam has (saf) altın', deger: hasToplam, birim: 'gram'});
    s.push({etiket: 'Kaç çeyrek altına denk', deger: hasToplam / (1.75 * AYAR22), birim: 'çeyrek'});
  } else {
    s.push({etiket: 'Çeyrek altın (has değeri)', deger: 1.75 * AYAR22 * gf, birim: '₺', vurgu: true});
  }
  s.push({etiket: '1 çeyrek altın', deger: 1.75 * AYAR22 * gf, birim: '₺'});
  s.push({etiket: '1 yarım altın', deger: 3.50 * AYAR22 * gf, birim: '₺'});
  s.push({etiket: '1 tam altın', deger: 7.00 * AYAR22 * gf, birim: '₺'});
  s.push({etiket: '1 Cumhuriyet altını', deger: 7.216 * AYAR22 * gf, birim: '₺'});
  s.push({etiket: '22 ayar gram fiyatı', deger: AYAR22 * gf, birim: '₺'});
  s.push({etiket: '18 ayar gram fiyatı', deger: (18/24) * gf, birim: '₺'});
  s.push({etiket: '14 ayar gram fiyatı', deger: (14/24) * gf, birim: '₺'});
  return {sonuclar: s,
    tablo: {basliklar: ['Altın', 'Ağırlık', 'Has altın', 'Birim değer', 'Adet', 'Toplam'], satirlar: sat},
    notlar: ['Hesap, altının içindeki saf (has) altın miktarına dayanır: 22 ayar = 916 milyem, yani ağırlığın 22/24\'ü saf altındır.',
             'Piyasadaki alış-satış fiyatları işçilik, darphane primi, arz-talep ve makas (spread) nedeniyle bu teorik değerden farklı olur; ziynet altınları genelde has değerinin bir miktar üzerinde satılır, bilezikte işçilik ayrıca eklenir.',
             'Gram altın fiyatını bankanızın, Kapalıçarşı\'nın veya Darphane\'nin güncel verisinden alın; bu araç canlı fiyat çekmez, girdiğiniz fiyatla hesaplar.']};
}
""",
    "nasil": [
        "Türkiye'de ziynet (takı) altınları 22 ayardır; yani 1.000 birimde 916 birim saf altın içerir (milyem 916). Standart ağırlıklar şöyledir: çeyrek altın 1,75 gram, yarım altın 3,50 gram, tam altın 7,00 gram, Cumhuriyet (Ata) altını 7,216 gram. Bir altının gerçek (has) değeri, ağırlığının 22/24'ü kadar saf altın içermesiyle bulunur.",
        "Buna göre çeyrek altında 1,75 × 22/24 ≈ 1,604 gram saf altın vardır. Gram altın (24 ayar) fiyatı biliniyorsa, çeyreğin teorik değeri bu saf altın miktarı ile gram fiyatının çarpımıdır. Aynı mantık yarım (≈3,21 gr has), tam (≈6,42 gr has) ve Cumhuriyet altını (≈6,61 gr has) için de geçerlidir.",
        "Piyasa fiyatı bu teorik değerden farklıdır: darphane primi, işçilik, kuyumcu kâr marjı ve arz-talep nedeniyle ziynet altınları genellikle has değerinin bir miktar üzerinde satılır, alışta ise makas nedeniyle daha düşük fiyat verilir. Bilezik ve takıda ayrıca işçilik ücreti eklenir; bozdururken bu işçiliğin büyük kısmı geri alınamaz.",
    ],
    "formul": [
        "Has (saf) altın = ağırlık (gram) × ayar ÷ 24   → 22 ayar için × 0,91667",
        "Teorik değer = has altın (gram) × gram altın (24 ayar) fiyatı",
        "Çeyrek 1,75 gr · Yarım 3,50 gr · Tam 7,00 gr · Cumhuriyet 7,216 gr",
        "22 ayar gram fiyatı = 24 ayar gram fiyatı × 0,91667",
    ],
    "ornekler": [
        {"baslik": "Gram altın 5.000 ₺ iken çeyrek", "adimlar": ["Has altın: 1,75 × 22/24 = 1,604 gr", "Değer: 1,604 × 5.000 = 8.020 ₺ (teorik)"]},
        {"baslik": "10 çeyrek + 2 yarım", "adimlar": ["Has: 10 × 1,604 + 2 × 3,208 = 22,46 gr", "Değer: 22,46 × 5.000 = 112.300 ₺"]},
        {"baslik": "50 gram 22 ayar bilezik", "adimlar": ["Has: 50 × 0,91667 = 45,83 gr", "Değer: 45,83 × 5.000 = 229.165 ₺ (işçilik hariç)"]},
    ],
    "tablo": {
        "baslik": "Ziynet altınları: ağırlık ve saf altın karşılığı",
        "basliklar": ["Altın", "Ağırlık", "Ayar", "Has (saf) altın"],
        "satirlar": [["Çeyrek", "1,75 gr", "22 (916)", "≈ 1,604 gr"], ["Yarım", "3,50 gr", "22 (916)", "≈ 3,208 gr"], ["Tam", "7,00 gr", "22 (916)", "≈ 6,417 gr"], ["Cumhuriyet (Ata)", "7,216 gr", "22 (916)", "≈ 6,615 gr"], ["Gram altın", "1,00 gr", "24 (995-999)", "≈ 1,00 gr"], ["22 ayar takı", "1,00 gr", "22 (916)", "≈ 0,917 gr"], ["18 ayar takı", "1,00 gr", "18 (750)", "0,750 gr"], ["14 ayar takı", "1,00 gr", "14 (585)", "0,583 gr"]],
        "not": "Darphane basımı ziynet altınları için standart değerler. Eski tarihli veya farklı darphane basımlarında küçük sapmalar olabilir.",
    },
    "sss": [
        {"soru": "Çeyrek altın kaç gram?", "cevap": "1,75 gram ve 22 ayardır; içinde yaklaşık 1,604 gram saf altın bulunur."},
        {"soru": "Cumhuriyet altını kaç gram?", "cevap": "7,216 gram (22 ayar), yaklaşık 6,615 gram saf altın içerir. Tam altından (7,00 gr) biraz daha ağırdır."},
        {"soru": "22 ayar ne demek?", "cevap": "1.000 birimde 916 birim saf altın (milyem 916) demektir; kalan kısım dayanıklılık için eklenen alaşımdır. Gram altın ise 24 ayardır (995-999 milyem)."},
        {"soru": "Çeyrek altın mı gram altın mı almalı?", "cevap": "Gram altında makas (alış-satış farkı) genelde daha dardır; çeyrekte darphane primi ve işçilik nedeniyle prim ödersiniz. Küçük tasarruf ve hediye için çeyrek, yatırım için gram altın tercih edilir."},
        {"soru": "Bilezik bozdurunca neden az para veriyorlar?", "cevap": "Alışta ödediğiniz işçilik ücreti bozdurmada geri alınmaz; ayrıca kuyumcu alış fiyatı has altın değerinin biraz altındadır."},
        {"soru": "Bu araç canlı fiyat çekiyor mu?", "cevap": "Hayır. Güncel gram altın fiyatını siz girersiniz; hesaplama tarayıcınızda yapılır ve hiçbir veri gönderilmez."},
    ],
    "kaynaklar": [
        {"ad": "Darphane ve Damga Matbaası Genel Müdürlüğü — ziynet altınları", "url": "https://www.darphane.gov.tr/"},
        {"ad": "Borsa İstanbul — Kıymetli Madenler Piyasası", "url": "https://www.borsaistanbul.com/"},
    ],
    "ilgili": ["bilesik-faiz-hesaplama", "enflasyon-hesaplama", "zekat-hesaplama"],
}
