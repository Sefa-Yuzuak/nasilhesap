# -*- coding: utf-8 -*-
HESAP = {
    "slug": "damga-vergisi-hesaplama",
    "baslik": "Damga Vergisi Hesaplama",
    "h1": "Damga Vergisi Hesaplama 2026 — Sözleşme, Kira, İhale ve Maaş Oranları",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 damga vergisi hesaplama: sözleşmelerde binde 9,48, kira sözleşmelerinde binde 1,89, ihale kararlarında binde 5,69, ücretlerde binde 7,59. Azami tutar 29.115.961,10 ₺. Kira sözleşmesi ve maaş damga vergisi örnekleri.",
    "kisa_cevap": "Damga vergisi = kâğıtta yazılı tutar × oran. 2026'da sözleşmeler binde 9,48, kira sözleşmeleri binde 1,89, ihale kararları binde 5,69, ücret ve avanslar binde 7,59 oranındadır; bir kâğıttan alınacak vergi 29.115.961,10 ₺'yi aşamaz. 1.000.000 ₺'lik sözleşmenin damga vergisi 9.480 ₺, yıllık 240.000 ₺'lik kira sözleşmesininki 453,60 ₺'dir.",
    "girdiler": [
        {"id": "tur", "etiket": "Kâğıt türü", "tip": "secim", "varsayilan": "sozlesme", "genis": True,
         "secenekler": [["sozlesme", "Sözleşme, taahhütname, mukavele (‰9,48)"], ["kira", "Kira sözleşmesi (‰1,89)"], ["ihale", "İhale kararı (‰5,69)"], ["ucret", "Ücret / maaş ödemesi (‰7,59)"], ["avans", "Avans makbuzu (‰7,59)"], ["ozel", "Özel oran"]]},
        {"id": "tutar", "etiket": "Kâğıtta yazılı tutar", "tip": "sayi", "varsayilan": "1000000", "birim": "₺", "ipucu": "kira için: aylık kira × ay sayısı"},
        {"id": "ozel_oran", "etiket": "Özel oran (binde)", "tip": "sayi", "varsayilan": "9.48", "birim": "‰", "gizli": "tur=ozel"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.tutar >= 0)) return {hata: 'Tutarı girin.'};
  var D = O.damga_vergisi, oran;
  if (g.tur === 'ozel') oran = (g.ozel_oran || 0) / 1000;
  else oran = {sozlesme: D.sozlesme, kira: D.kira, ihale: D.ihale, ucret: D.ucret_oran, avans: D.avans}[g.tur];
  var vergi = g.tutar * oran, sinir = false;
  if (vergi > D.azami) { vergi = D.azami; sinir = true; }
  var n = ['Bir kâğıttan alınacak damga vergisi 2026 için en fazla ' + NH.fmt(D.azami) + ' ₺ olabilir.'];
  if (g.tur === 'ucret') n.push('Ücretlerde asgari ücrete isabet eden kısım (2026: ' + NH.fmt(O.asgari_ucret.brut * D.ucret_oran) + ' ₺) damga vergisinden istisnadır; bordroda bu tutar düşülür.');
  if (g.tur === 'kira') n.push('Kira sözleşmesinde matrah, sözleşme süresince ödenecek toplam kiradır (aylık kira × ay). Yalnızca konut kirası için kiracı gerçek kişiyse ve iş yeri değilse istisna uygulanır (DVK ek 2 sayılı tablo IV/31); iş yeri kiraları vergiye tabidir.');
  return {
    sonuclar: [
      {etiket: 'Damga vergisi', deger: vergi, birim: '₺', vurgu: true},
      {etiket: 'Uygulanan oran', deger: '‰' + (oran * 1000).toFixed(2).replace('.', ',')},
      {etiket: 'Matrah', deger: g.tutar, birim: '₺'},
      {etiket: 'Azami sınır uygulandı mı?', deger: sinir ? 'Evet — üst sınırda' : 'Hayır'}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "Damga vergisi, 488 sayılı Kanun'a ekli (1) sayılı tabloda sayılan kâğıtlar (sözleşme, taahhütname, kira sözleşmesi, ihale kararı, ücret bordrosu, makbuz vb.) üzerinden alınır. Nispi vergide kâğıtta yazılı para tutarı ilgili oranla çarpılır; maktu vergide ise kâğıt başına sabit tutar ödenir. 2026'da en yaygın oranlar sözleşmelerde binde 9,48, kira sözleşmelerinde binde 1,89, ihale kararlarında binde 5,69, ücretlerde binde 7,59'dur.",
        "Bir kâğıttan alınacak damga vergisinin üst sınırı her yıl yeniden değerleme oranıyla güncellenir; 2026 için bu sınır 29.115.961,10 ₺'dir (2025 tutarının %18,95 artırılmasıyla). Sözleşmenin birden fazla nüshası düzenlense bile 2016'dan beri yalnızca bir nüsha vergilendirilir; aynı kâğıtta birden fazla akit varsa en yüksek vergiyi gerektiren üzerinden hesaplanır.",
        "Vergiyi, kâğıdı imzalayanlar müteselsilen öder; uygulamada sözleşmede belirlenen taraf beyan eder. Sürekli damga vergisi mükellefiyeti olanlar (anonim ve limited şirketler vb.) aylık beyanname verir; diğerleri kâğıdın düzenlendiği ayı izleyen ayın 26'sına kadar vergi dairesine beyan edip öder. Konut kira sözleşmeleri (gerçek kişiler arası, iktisadi işletmeye dahil olmayan) 2016'dan itibaren damga vergisinden istisnadır.",
    ],
    "formul": [
        "Damga vergisi = kâğıtta yazılı tutar × oran (‰)",
        "Sözleşme: tutar × 9,48 ÷ 1.000 · Kira: (aylık kira × ay) × 1,89 ÷ 1.000",
        "İhale kararı: bedel × 5,69 ÷ 1.000 · Ücret: brüt × 7,59 ÷ 1.000 − asgari ücret istisnası",
        "Üst sınır (2026): 29.115.961,10 ₺ / kâğıt",
    ],
    "ornekler": [
        {"baslik": "1.000.000 ₺ bedelli hizmet sözleşmesi", "adimlar": ["1.000.000 × 9,48 ÷ 1.000 = 9.480 ₺"]},
        {"baslik": "İş yeri kira sözleşmesi: aylık 20.000 ₺, 12 ay", "adimlar": ["Matrah: 20.000 × 12 = 240.000 ₺", "Vergi: 240.000 × 1,89 ÷ 1.000 = 453,60 ₺"]},
        {"baslik": "50.000 ₺ brüt maaş", "adimlar": ["50.000 × 7,59 ÷ 1.000 = 379,50 ₺", "Asgari ücret istisnası 250,70 ₺ → kesilen 128,80 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 damga vergisi oranları (nispi)",
        "basliklar": ["Kâğıt", "Oran"],
        "satirlar": [["Mukavelename, taahhütname, temliknameler", "‰9,48"], ["Kira sözleşmeleri (bedel üzerinden)", "‰1,89"], ["Kefalet, teminat, rehin senetleri", "‰9,48"], ["İhale kararları", "‰5,69"], ["Ücret, maaş, harcırah, ikramiye vb.", "‰7,59"], ["Avans makbuzları", "‰7,59"], ["Bilanço (maktu)", "sabit tutar"], ["Azami vergi (kâğıt başına)", "29.115.961,10 ₺"]],
        "not": "488 sayılı Damga Vergisi Kanunu (1) sayılı tablo; 2026 maktu tutarlar ve azami sınır Cumhurbaşkanı Kararı ile %18,95 artırıldı.",
    },
    "sss": [
        {"soru": "Kira sözleşmesi damga vergisi nasıl hesaplanır?", "cevap": "Sözleşme süresince ödenecek toplam kira (aylık kira × ay sayısı) binde 1,89 ile çarpılır. Gerçek kişiler arasındaki konut kiraları istisnadır; iş yeri kiraları vergiye tabidir ve kefil varsa kefalet için ayrıca ‰9,48 hesaplanır."},
        {"soru": "Sözleşmede damga vergisini kim öder?", "cevap": "Kanunen imzalayanlar müteselsil sorumludur; taraflar sözleşmede kimin ödeyeceğini kararlaştırabilir. Resmî dairelerle yapılan sözleşmelerde kişi öder."},
        {"soru": "Sözleşmenin iki nüshası varsa iki kat vergi mi ödenir?", "cevap": "Hayır. 2016'dan (6728 sayılı Kanun) beri nüsha sayısına bakılmaksızın tek nüsha üzerinden vergi alınır."},
        {"soru": "Maaştan damga vergisi kesilir mi?", "cevap": "Evet, brüt ücret üzerinden binde 7,59. Asgari ücrete isabet eden kısım (2026'da aylık 250,70 ₺) istisnadır; asgari ücretliden kesilmez."},
        {"soru": "Damga vergisi ne zaman ödenir?", "cevap": "Sürekli mükellefler her ay 26'sına kadar beyan eder; diğerleri kâğıdın düzenlendiği tarihi izleyen 15 gün içinde (uygulamada izleyen ayın 26'sı) beyan edip öder."},
    ],
    "kaynaklar": [
        {"ad": "488 sayılı Damga Vergisi Kanunu ve (1) sayılı tablo", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=488&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "GİB — Damga Vergisi Kanunu Genel Tebliğleri (2026 tutarları)", "url": "https://www.gib.gov.tr/"},
    ],
    "ilgili": ["kdv-hesaplama", "brut-net-maas-hesaplama", "kira-artis-orani-hesaplama"],
}
