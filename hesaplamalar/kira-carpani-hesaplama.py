# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kira-carpani-hesaplama",
    "baslik": "Kira Çarpanı ve Amortisman Hesaplama",
    "h1": "Kira Çarpanı Hesaplama — Ev Kaç Yılda Kendini Amorti Eder, Kira Getirisi Yüzde Kaç?",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Kira çarpanı (amortisman süresi) ve brüt/net kira getirisi hesaplama: ev fiyatı, aylık kira, aidat, emlak vergisi ve boş kalma payıyla yatırım verimliliği; m² fiyatı ve mevduatla karşılaştırma.",
    "kisa_cevap": "Kira çarpanı = ev fiyatı ÷ yıllık kira; evin kirayla kendini kaç yılda amorti ettiğini gösterir. 5.000.000 ₺'lik ev aylık 20.000 ₺ kira getiriyorsa çarpan 5.000.000 ÷ 240.000 = 20,8 yıl, brüt kira getirisi %4,8'dir. Türkiye'de tarihsel ortalama 15-20 yıl; 25 yılı aşan çarpan pahalı, 12 yılın altı ucuz kabul edilir.",
    "girdiler": [
        {"id": "fiyat", "etiket": "Ev fiyatı", "tip": "sayi", "varsayilan": "5000000", "birim": "₺"},
        {"id": "kira", "etiket": "Aylık kira", "tip": "sayi", "varsayilan": "20000", "birim": "₺"},
        {"id": "m2", "etiket": "Net alan (isteğe bağlı)", "tip": "sayi", "varsayilan": "", "birim": "m²"},
        {"id": "gider", "etiket": "Yıllık giderler (emlak vergisi, sigorta, bakım; aidat kiracıda)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "bos", "etiket": "Yılda boş kalma", "tip": "sayi", "varsayilan": "0", "birim": "ay"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.fiyat > 0) || !(g.kira > 0)) return {hata: 'Fiyat ve kirayı girin.'};
  var yillik = g.kira * 12, bos = (g.bos > 0 ? Math.min(g.bos, 12) : 0);
  var netYillik = g.kira * (12 - bos) - (g.gider > 0 ? g.gider : 0);
  var carpan = g.fiyat / yillik, brut = yillik / g.fiyat * 100, net = netYillik / g.fiyat * 100;
  var yorum = carpan < 12 ? 'Ucuz / yüksek getirili' : carpan <= 20 ? 'Makul (tarihsel ortalama)' : carpan <= 25 ? 'Pahalı' : 'Çok pahalı (getiri düşük)';
  var s = [
    {etiket: 'Kira çarpanı (amortisman)', deger: carpan.toFixed(1) + ' yıl — ' + yorum, vurgu: true},
    {etiket: 'Brüt kira getirisi (yıllık)', deger: brut, birim: '%'},
    {etiket: 'Net kira getirisi (gider ve boşluk sonrası)', deger: net, birim: '%'},
    {etiket: 'Net amortisman süresi', deger: netYillik > 0 ? (g.fiyat / netYillik).toFixed(1) + ' yıl' : '—'},
    {etiket: 'Yıllık brüt kira', deger: yillik, birim: '₺'},
    {etiket: 'Yıllık net kira', deger: netYillik, birim: '₺'}
  ];
  if (g.m2 > 0) { s.push({etiket: 'm² satış fiyatı', deger: g.fiyat / g.m2, birim: '₺'}); s.push({etiket: 'm² kira', deger: g.kira / g.m2, birim: '₺'}); }
  return {sonuclar: s, notlar: ['Değer artışı (sermaye kazancı) ve kira artışları hesaba dahil değildir; bu araç yalnızca kira akışını ölçer.', 'Kira geliri vergisi (istisna 58.000 ₺ sonrası) net getiriyi ayrıca düşürür.']};
}
""",
    "nasil": [
        "Kira çarpanı (fiyat/kira oranı), bir konutun fiyatının yıllık kira gelirine bölünmesiyle bulunur ve evin kirayla kaç yılda kendini ödediğini gösterir; tersi brüt kira getirisidir. Türkiye'de konut piyasasında tarihsel ortalama 15-20 yıl civarındadır; 12 yılın altı yatırımcı için cazip, 25 yılın üstü pahalı sayılır. Aynı mahalledeki farklı evleri ve şehirleri karşılaştırmak için en pratik göstergedir.",
        "Brüt getiri gerçek kazancı abartır: emlak vergisi, DASK, bakım-onarım, boş kalan aylar ve kira geliri vergisi düşüldükten sonra net getiri genellikle brütün %70-85'ine iner. Aidat kiracı tarafından ödendiğinden mal sahibinin giderine girmez; ancak boş dönemlerde aidat da sahibine kalır.",
        "Kira getirisi mevduat veya tahvil getirisiyle karşılaştırılırken konutun değer artışı potansiyeli ve likidite düşüklüğü de hesaba katılmalıdır. Düşük kira çarpanı genellikle değer artışı beklentisinin düşük olduğu bölgelerde, yüksek çarpan ise değerlenme beklentisinin yüksek olduğu merkezlerde görülür.",
    ],
    "formul": [
        "Kira çarpanı (yıl) = ev fiyatı ÷ (aylık kira × 12)",
        "Brüt kira getirisi (%) = yıllık kira ÷ ev fiyatı × 100",
        "Net getiri (%) = (kira × dolu ay − yıllık giderler) ÷ ev fiyatı × 100",
        "m² fiyatı = fiyat ÷ net alan",
    ],
    "ornekler": [
        {"baslik": "5.000.000 ₺ ev, 20.000 ₺ kira", "adimlar": ["Yıllık kira 240.000 ₺ → çarpan 20,8 yıl", "Brüt getiri %4,8"]},
        {"baslik": "Aynı ev, yılda 1 ay boş, 12.000 ₺ gider", "adimlar": ["Net yıllık: 220.000 − 12.000 = 208.000 ₺", "Net getiri %4,16; net amortisman 24 yıl"]},
    ],
    "tablo": {
        "baslik": "Kira çarpanı yorumu",
        "basliklar": ["Çarpan", "Brüt getiri", "Yorum"],
        "satirlar": [["< 12 yıl", "> %8,3", "Ucuz — yüksek kira getirisi"], ["12 – 20 yıl", "%5 – 8,3", "Makul, tarihsel ortalama"], ["20 – 25 yıl", "%4 – 5", "Pahalı"], ["> 25 yıl", "< %4", "Çok pahalı — değer artışı beklentisine dayalı"]],
        "not": "Eşikler yaygın yatırımcı pratiğidir; bölge ve dönem koşullarına göre yorumlanmalıdır.",
    },
    "sss": [
        {"soru": "Kira çarpanı nasıl hesaplanır?", "cevap": "Ev fiyatını yıllık kiraya bölün. 3.000.000 ₺ ev, 15.000 ₺ kira → 3.000.000 ÷ 180.000 = 16,7 yıl."},
        {"soru": "İyi kira getirisi yüzde kaç?", "cevap": "Türkiye'de brüt %5-8 makul, %8 üzeri yüksek kabul edilir. Net getiri giderler ve vergi sonrası genellikle 1-2 puan düşüktür."},
        {"soru": "Amortisman süresi neden önemli?", "cevap": "Kira yatırımının geri dönüş hızını gösterir ve farklı bölge/evleri kıyaslamayı sağlar; kısa süre daha iyi nakit getirisi demektir."},
        {"soru": "Kira çarpanı tek başına yeterli mi?", "cevap": "Hayır. Değer artışı, likidite, boş kalma riski, bina yaşı ve vergi de yatırım kararını etkiler."},
    ],
    "kaynaklar": [
        {"ad": "TCMB — Konut Fiyat Endeksi ve kira istatistikleri", "url": "https://www.tcmb.gov.tr/"},
        {"ad": "TÜİK — Konut satış ve kira endeksleri", "url": "https://data.tuik.gov.tr/"},
    ],
    "ilgili": ["kira-artis-orani-hesaplama", "kira-geliri-vergisi-hesaplama", "konut-kredisi-hesaplama", "ev-alma-maliyeti-hesaplama"],
}
