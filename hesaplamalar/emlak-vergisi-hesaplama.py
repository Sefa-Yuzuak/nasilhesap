# -*- coding: utf-8 -*-
HESAP = {
    "slug": "emlak-vergisi-hesaplama",
    "baslik": "Emlak Vergisi Hesaplama",
    "h1": "Emlak Vergisi Hesaplama 2026 — Konut, İş Yeri, Arsa ve Arazi Oranları",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 emlak vergisi hesaplama: vergi değeri ve taşınmaz türüne göre yıllık emlak vergisi, büyükşehir farkı (konut ‰1/‰2, iş yeri ‰2/‰4, arsa ‰3/‰6, arazi ‰1/‰2), Mayıs ve Kasım taksitleri, muafiyetler.",
    "kisa_cevap": "Emlak vergisi = vergi değeri × oran. 2026'da konut ‰1, iş yeri ‰2, arsa ‰3, arazi ‰1; büyükşehir belediyesi sınırlarında bu oranlar iki katıdır. 3.000.000 ₺ vergi değerli bir konut için büyükşehirde yıllık 6.000 ₺ (Mayıs ve Kasım'da 3.000 ₺'lik iki taksit) ödenir.",
    "girdiler": [
        {"id": "deger", "etiket": "Emlak vergisi değeri", "tip": "sayi", "varsayilan": "3000000", "birim": "₺", "ipucu": "belediyenin bildirdiği değer"},
        {"id": "tur", "etiket": "Taşınmaz türü", "tip": "secim", "varsayilan": "konut", "secenekler": [["konut", "Konut (mesken)"], ["isyeri", "İş yeri"], ["arsa", "Arsa"], ["arazi", "Arazi"]]},
        {"id": "bs", "etiket": "Konum", "tip": "secim", "varsayilan": "buyuksehir", "secenekler": [["buyuksehir", "Büyükşehir sınırları içinde"], ["normal", "Diğer belediyeler"]]},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.deger > 0)) return {hata: 'Vergi değerini girin.'};
  var binde = O.emlak_vergisi[g.bs][g.tur], vergi = g.deger * binde / 1000;
  return {
    sonuclar: [
      {etiket: 'Yıllık emlak vergisi', deger: vergi, birim: '₺', vurgu: true},
      {etiket: 'Uygulanan oran', deger: '‰' + binde},
      {etiket: '1. taksit (Mayıs sonuna kadar)', deger: vergi / 2, birim: '₺'},
      {etiket: '2. taksit (Kasım sonuna kadar)', deger: vergi / 2, birim: '₺'},
      {etiket: 'Aylık karşılığı', deger: vergi / 12, birim: '₺'}
    ],
    notlar: ['Vergi değeri, belediyece takdir edilen arsa m² değeri ve bina inşaat maliyetine göre belirlenir; alım-satım bedeliyle aynı değildir ve her yıl yeniden değerleme oranının yarısı kadar artar.',
             'Tek meskeni olan emekli, engelli, gazi, şehit yakını ve geliri olmayanlar (200 m²’yi aşmayan konut) için oran sıfıra indirilmiştir; belediyeye başvuru gerekir.']
  };
}
""",
    "nasil": [
        "Emlak vergisi, Türkiye'de bina, arsa ve arazi sahiplerinin her yıl belediyeye ödediği servet vergisidir. Vergi, taşınmazın belediyece belirlenen 'emlak vergisi değeri' üzerinden sabit binde oranlarla hesaplanır: konut ‰1, iş yeri ve diğer binalar ‰2, arsa ‰3, arazi ‰1. Büyükşehir belediyesi sınırları ve mücavir alanlarında bu oranlar yüzde yüz artırımlı (iki katı) uygulanır.",
        "Vergi değeri, satış fiyatından farklıdır: arsa payı için takdir komisyonlarının belirlediği m² birim değeri, bina için ise Hazine ve Maliye Bakanlığı'nın yayımladığı inşaat maliyet bedelleri esas alınır; bu değer takdir yıllarının arasında her yıl yeniden değerleme oranının yarısı kadar artırılır. Değerinizi belediyeden veya e-Devlet'ten öğrenebilirsiniz.",
        "Vergi, Mayıs ve Kasım aylarının sonuna kadar iki eşit taksitte ödenir. Taşınmaz alındığında bildirim aynı yıl içinde (yılın son gününe kadar) belediyeye yapılır; vergi mükellefiyeti alım yılını izleyen yıl başlar. Tek meskene sahip emekli, engelli, gazi, şehit yakını ve hiç geliri olmayanlar için belirli şartlarla sıfır oran uygulanır.",
    ],
    "formul": [
        "Yıllık emlak vergisi = emlak vergisi değeri × oran ÷ 1.000",
        "Normal belediye: konut ‰1 · iş yeri ‰2 · arsa ‰3 · arazi ‰1",
        "Büyükşehir: konut ‰2 · iş yeri ‰4 · arsa ‰6 · arazi ‰2",
        "Taksit = yıllık vergi ÷ 2 (Mayıs ve Kasım)",
    ],
    "ornekler": [
        {"baslik": "3.000.000 ₺ vergi değerli konut, İstanbul", "adimlar": ["Büyükşehir konut oranı ‰2", "3.000.000 × 2 ÷ 1.000 = 6.000 ₺/yıl", "Taksitler: Mayıs 3.000 ₺, Kasım 3.000 ₺"]},
        {"baslik": "1.500.000 ₺ vergi değerli arsa, ilçe belediyesi (büyükşehir dışı)", "adimlar": ["Arsa oranı ‰3", "1.500.000 × 3 ÷ 1.000 = 4.500 ₺/yıl"]},
    ],
    "tablo": {
        "baslik": "2026 emlak vergisi oranları",
        "basliklar": ["Taşınmaz", "Normal belediye", "Büyükşehir"],
        "satirlar": [["Konut (mesken)", "‰1", "‰2"], ["İş yeri ve diğer binalar", "‰2", "‰4"], ["Arsa", "‰3", "‰6"], ["Arazi", "‰1", "‰2"]],
        "not": "1319 sayılı Emlak Vergisi Kanunu m.8 ve m.18. Değerli konut vergisi (2026 eşiğini aşan konutlar) ayrıca ve GİB'e ödenir.",
    },
    "sss": [
        {"soru": "Emlak vergisi ne zaman ödenir?", "cevap": "İki taksitte: birinci taksit Mart-Mayıs döneminde (en geç 31 Mayıs), ikinci taksit Kasım ayında (en geç 30 Kasım). İsteyen tamamını birinci taksitte ödeyebilir."},
        {"soru": "Vergi değeri ile satış fiyatı aynı mı?", "cevap": "Hayır. Vergi değeri belediyenin takdir ettiği arsa m² değeri ve bina maliyet bedeliyle hesaplanır; genellikle piyasa fiyatının altındadır. Tapu harcı ise en az bu değer üzerinden ödenir."},
        {"soru": "Kimler emlak vergisinden muaf?", "cevap": "Türkiye'de tek meskeni olan (200 m²'yi geçmeyen) emekliler, engelliler, gaziler, şehit dul ve yetimleri ile hiçbir geliri olmayanlar için oran sıfırdır. Belediyeye taahhütname ile başvurulur."},
        {"soru": "Yeni aldığım ev için ne zaman vergi öderim?", "cevap": "Alım yılı içinde belediyeye bildirim yaparsınız; mükellefiyet izleyen yıl başlar. Alım yılının vergisinden satıcı sorumludur."},
        {"soru": "Emlak vergisini ödemezsem ne olur?", "cevap": "Aylık gecikme zammı işler ve belediye 6183 sayılı Kanun kapsamında haciz dahil takip yapabilir. Ayrıca taşınmaz satışında borç bulunmadığına dair belge istenebilir."},
    ],
    "kaynaklar": [
        {"ad": "1319 sayılı Emlak Vergisi Kanunu", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=1319&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "TÜRMOB — 2026 yılında emlak vergisi uygulaması özeti", "url": "https://www.turmob.org.tr/"},
    ],
    "ilgili": ["tapu-harci-hesaplama", "kira-geliri-vergisi-hesaplama", "konut-kredisi-hesaplama"],
}
