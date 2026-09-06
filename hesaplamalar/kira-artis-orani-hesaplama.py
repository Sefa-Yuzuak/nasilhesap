# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kira-artis-orani-hesaplama",
    "baslik": "Kira Artış Oranı Hesaplama",
    "h1": "Kira Artış Oranı Hesaplama — Eylül 2026 TÜFE Oranı %31,79",
    "kategori": "kredi-finans",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Eylül 2026 kira artış oranı %31,79 (TÜFE 12 aylık ortalama). Mevcut kiranıza yasal azami zammı ve yeni kira tutarını anında hesaplayın. Konut ve iş yeri kira artışı, TBK m.344, son ayların oranları.",
    "kisa_cevap": "Yeni kira = mevcut kira × (1 + TÜFE 12 aylık ortalama oranı ÷ 100). Eylül 2026'da yenilenen konut ve çatılı iş yeri sözleşmelerinde uygulanabilecek azami artış oranı %31,79'dur (TÜİK, 3 Eylül 2026). 20.000 ₺ kira en fazla 26.358 ₺ olur.",
    "senaryolar": [
        {"ad": "10.000 ₺ kira", "degerler": {"kira": "10000", "oran": "31.79", "tur": "konut"}},
        {"ad": "20.000 ₺ kira", "degerler": {"kira": "20000", "oran": "31.79", "tur": "konut"}},
        {"ad": "35.000 ₺ kira", "degerler": {"kira": "35000", "oran": "31.79", "tur": "konut"}},
        {"ad": "İş yeri 50.000 ₺", "degerler": {"kira": "50000", "oran": "31.79", "tur": "isyeri"}},
    ],
    "girdiler": [
        {"id": "kira", "etiket": "Mevcut aylık kira", "tip": "sayi", "varsayilan": "20000", "birim": "₺"},
        {"id": "oran", "etiket": "Artış oranı (TÜFE 12 aylık ort.)", "tip": "sayi", "varsayilan": "31.79", "birim": "%", "ipucu": "Eylül 2026 için %31,79"},
        {"id": "tur", "etiket": "Taşınmaz türü", "tip": "secim", "varsayilan": "konut", "secenekler": [["konut", "Konut"], ["isyeri", "Çatılı iş yeri"]]},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.kira > 0)) return {hata: 'Mevcut kirayı girin.'};
  if (!(g.oran >= 0)) return {hata: 'Artış oranını girin.'};
  var artis = g.kira * g.oran / 100, yeni = g.kira + artis;
  var tbl = [[O.kira_artis.ay_ad, O.kira_artis.oran + '%', NH.fmt(g.kira * (1 + O.kira_artis.oran/100)) + ' ₺']];
  (O.kira_artis.onceki || []).forEach(function(x){ tbl.push([x[0], x[1] + '%', NH.fmt(g.kira * (1 + x[1]/100)) + ' ₺']); });
  return {
    sonuclar: [
      {etiket: 'Yeni aylık kira (azami)', deger: yeni, birim: '₺', vurgu: true},
      {etiket: 'Aylık artış tutarı', deger: artis, birim: '₺'},
      {etiket: 'Yıllık ek ödeme', deger: artis * 12, birim: '₺'},
      {etiket: 'Yeni yıllık kira', deger: yeni * 12, birim: '₺'}
    ],
    tablo: {basliklar: ['Yenileme ayı', 'Oran', 'Bu kira için yeni tutar'], satirlar: tbl},
    notlar: ['Oran, TÜİK\'in açıkladığı TÜFE 12 aylık ortalamalara göre değişim oranıdır (' + O.kira_artis.aciklama_tarihi + ' verisi). Bu bir üst sınırdır; taraflar daha düşük artışta anlaşabilir.',
             g.tur === 'isyeri' ? 'Çatılı iş yerleri için de aynı üst sınır (TBK m.344) uygulanır.' : 'Konut kiralarında geçici %25 sınırı 1 Temmuz 2024\'te sona erdi; artık TÜFE 12 aylık ortalama uygulanır.']
  };
}
""",
    "nasil": [
        "Türk Borçlar Kanunu m.344'e göre kira sözleşmesi yenilenirken uygulanacak artış, bir önceki kira yılında TÜFE'nin on iki aylık ortalamalara göre değişim oranını geçemez. Bu oran, yıllık enflasyon (bir önceki yılın aynı ayına göre değişim) değildir; TÜİK'in her ay enflasyon verisiyle birlikte açıkladığı '12 aylık ortalamalara göre değişim' değeridir.",
        "Kira artışı, sözleşmenin yenilendiği ayın oranıyla hesaplanır: sözleşmeniz Eylül'de yenileniyorsa Ağustos ayı enflasyonuyla açıklanan (3 Eylül 2026 tarihli) 12 aylık ortalama oran (%31,79) esas alınır. Mevcut kira bu oranla çarpılıp eklenerek yeni kira bulunur.",
        "Konut kiralarına 2022-2024 arasında uygulanan geçici %25 üst sınır 1 Temmuz 2024'te sona erdi. Bugün konut ve çatılı iş yeri sözleşmelerinin tamamında TÜFE 12 aylık ortalama oranı üst sınırdır; sözleşmede daha yüksek bir oran yazsa bile bu sınır uygulanır.",
    ],
    "formul": [
        "Azami artış tutarı = mevcut kira × TÜFE 12 aylık ortalama oranı ÷ 100",
        "Yeni kira = mevcut kira × (1 + oran ÷ 100)",
        "Eylül 2026 oranı: %31,79 (TÜİK, 3 Eylül 2026)",
    ],
    "ornekler": [
        {"baslik": "20.000 ₺ konut kirası, Eylül 2026 yenileme", "adimlar": ["Artış: 20.000 × 31,79 ÷ 100 = 6.358 ₺", "Yeni kira: 26.358 ₺ (azami)"]},
        {"baslik": "45.000 ₺ iş yeri kirası, Ağustos 2026 (%31,90)", "adimlar": ["Artış: 45.000 × 0,319 = 14.355 ₺", "Yeni kira: 59.355 ₺"]},
    ],
    "tablo": {
        "baslik": "Son ayların kira artış oranları (TÜFE 12 aylık ortalama)",
        "basliklar": ["Yenileme ayı", "Azami oran"],
        "satirlar": [["Eylül 2026", "%31,79"], ["Ağustos 2026", "%31,90"]],
        "not": "Her ayın oranı, bir önceki ayın enflasyon verisiyle (ayın 3'ü civarı) TÜİK tarafından açıklanır. Tablo yeni veri geldikçe güncellenir.",
    },
    "sss": [
        {"soru": "Eylül 2026 kira artış oranı yüzde kaç?", "cevap": "%31,79. TÜİK'in 3 Eylül 2026'da açıkladığı Ağustos verisine göre TÜFE'nin 12 aylık ortalamalara göre değişimi bu oranda gerçekleşti; Eylül'de yenilenen sözleşmelerde azami artış budur."},
        {"soru": "Kira artışında yıllık enflasyon mu, 12 aylık ortalama mı kullanılır?", "cevap": "12 aylık ortalamalara göre değişim oranı kullanılır (TBK m.344). Yıllık enflasyon farklı ve genellikle daha yüksek/düşük bir değerdir; kira için geçerli değildir."},
        {"soru": "Ev sahibi TÜFE oranından fazla zam yapabilir mi?", "cevap": "Hayır. Sözleşmede daha yüksek oran yazsa bile TÜFE 12 aylık ortalama üst sınırı aşan kısım geçersizdir. Kiracı fazla ödemeyi reddedebilir ve gerekirse sulh hukuk mahkemesinde tespit davası açabilir."},
        {"soru": "5 yılı dolan kiralarda durum ne?", "cevap": "5 yıllık kira süresinin sonunda taraflar anlaşamazsa hâkim, TÜFE oranı, taşınmazın durumu ve emsal kiraları dikkate alarak yeni kirayı belirleyebilir (kira tespit davası); bu durumda TÜFE üst sınırı bağlayıcı değildir."},
        {"soru": "Konut kirasındaki %25 sınırı hâlâ geçerli mi?", "cevap": "Hayır. Geçici %25 sınırı 1 Temmuz 2024'te sona erdi. O tarihten itibaren yenilenen tüm konut sözleşmelerinde TÜFE 12 aylık ortalama oranı uygulanır."},
    ],
    "kaynaklar": [
        {"ad": "TÜİK — Tüketici Fiyat Endeksi (aylık bülten, 12 aylık ortalamalara göre değişim)", "url": "https://data.tuik.gov.tr/"},
        {"ad": "6098 sayılı Türk Borçlar Kanunu m.344", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6098&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["yuzde-hesaplama", "kira-geliri-vergisi-hesaplama", "konut-kredisi-hesaplama"],
}
