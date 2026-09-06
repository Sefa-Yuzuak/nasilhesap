# -*- coding: utf-8 -*-
HESAP = {
    "slug": "enflasyon-hesaplama",
    "baslik": "Enflasyon Hesaplama",
    "h1": "Enflasyon Hesaplama — Alım Gücü Kaybı, Reel Getiri ve Gelecekteki Fiyat",
    "kategori": "kredi-finans",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Enflasyon hesaplama: yıllık enflasyon oranıyla paranın alım gücü kaybı, bugünkü fiyatın X yıl sonraki karşılığı, faiz getirisinin enflasyondan arındırılmış reel değeri ve iki TÜFE endeksi arasındaki artış.",
    "kisa_cevap": "Enflasyon, paranın alım gücünü her yıl (1 + enflasyon) kadar aşındırır: gelecekteki fiyat = bugünkü fiyat × (1 + enflasyon)^yıl. %30 yıllık enflasyonda 100.000 ₺ 3 yıl sonra 219.700 ₺'lik fiyatlara denk gelir; başka deyişle bugünkü 100.000 ₺'nin alım gücü 3 yılda 45.517 ₺'ye iner. Reel getiri = (1 + faiz) ÷ (1 + enflasyon) − 1'dir.",
    "girdiler": [
        {"id": "mod", "etiket": "Hesaplama", "tip": "secim", "varsayilan": "gelecek", "genis": True,
         "secenekler": [["gelecek", "Bugünkü tutar gelecekte kaç ₺ eder? (alım gücü)"], ["reel", "Faiz getirimin reel (enflasyondan arındırılmış) değeri"], ["endeks", "İki TÜFE endeksi arasındaki enflasyon oranı"]]},
        {"id": "tutar", "etiket": "Tutar", "tip": "sayi", "varsayilan": "100000", "birim": "₺"},
        {"id": "enf", "etiket": "Yıllık enflasyon oranı", "tip": "sayi", "varsayilan": "30", "birim": "%"},
        {"id": "yil", "etiket": "Süre", "tip": "sayi", "varsayilan": "3", "birim": "yıl"},
        {"id": "faiz", "etiket": "Yıllık faiz / getiri (reel için)", "tip": "sayi", "varsayilan": "40", "birim": "%", "gizli": "mod=reel"},
        {"id": "e1", "etiket": "Başlangıç TÜFE endeksi", "tip": "sayi", "varsayilan": "", "gizli": "mod=endeks"},
        {"id": "e2", "etiket": "Bitiş TÜFE endeksi", "tip": "sayi", "varsayilan": "", "gizli": "mod=endeks"},
    ],
    "js": r"""
function hesapla(g){
  var s = [], n = [];
  if (g.mod === 'endeks') {
    if (!(g.e1 > 0) || !(g.e2 > 0)) return {hata: 'İki endeks değerini girin (TÜİK TÜFE, 2003=100).'};
    var art = (g.e2 / g.e1 - 1) * 100;
    s.push({etiket: 'Dönem enflasyonu', deger: art, birim: '%', vurgu: true});
    if (g.tutar > 0) s.push({etiket: NH.fmt(g.tutar) + ' ₺ başlangıçta = bitişte', deger: g.tutar * g.e2 / g.e1, birim: '₺'});
    n.push('Kira artışı için bu oran değil, TÜİK\'in "12 aylık ortalamalara göre değişim" oranı kullanılır.');
    return {sonuclar: s, notlar: n};
  }
  if (!(g.tutar > 0) || isNaN(g.enf) || !(g.yil > 0)) return {hata: 'Tutar, enflasyon ve süreyi girin.'};
  var carpan = Math.pow(1 + g.enf / 100, g.yil);
  if (g.mod === 'gelecek') {
    s.push({etiket: g.yil + ' yıl sonra aynı alım gücü için gereken', deger: g.tutar * carpan, birim: '₺', vurgu: true});
    s.push({etiket: 'Bugünkü ' + NH.fmt(g.tutar) + ' ₺\'nin ' + g.yil + ' yıl sonraki alım gücü', deger: g.tutar / carpan, birim: '₺'});
    s.push({etiket: 'Alım gücü kaybı', deger: (1 - 1 / carpan) * 100, birim: '%'});
    s.push({etiket: 'Kümülatif enflasyon', deger: (carpan - 1) * 100, birim: '%'});
    s.push({etiket: 'Fiyatların ikiye katlanma süresi', deger: g.enf > 0 ? (Math.log(2) / Math.log(1 + g.enf / 100)).toFixed(1) + ' yıl' : '—'});
  } else {
    if (isNaN(g.faiz)) return {hata: 'Faiz oranını girin.'};
    var reel = ((1 + g.faiz / 100) / (1 + g.enf / 100) - 1) * 100;
    var nominalSon = g.tutar * Math.pow(1 + g.faiz / 100, g.yil), reelSon = nominalSon / carpan;
    s.push({etiket: 'Reel yıllık getiri', deger: reel, birim: '%', vurgu: true});
    s.push({etiket: g.yil + ' yıl sonra nominal tutar', deger: nominalSon, birim: '₺'});
    s.push({etiket: 'Bugünkü fiyatlarla değeri', deger: reelSon, birim: '₺'});
    s.push({etiket: 'Reel kazanç / kayıp', deger: reelSon - g.tutar, birim: '₺'});
    n.push(reel < 0 ? 'Faiz enflasyonun altında: paranız nominal olarak artsa da alım gücü azalıyor.' : 'Faiz enflasyonun üzerinde: alım gücü artıyor.');
    n.push('Faiz üzerinden stopaj hesaba katılmamıştır; net faizi girmeniz daha doğru sonuç verir.');
  }
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Enflasyon, genel fiyat düzeyindeki yıllık artıştır; TÜİK her ayın 3'ünde Tüketici Fiyat Endeksi'ni (TÜFE) açıklar. Aynı para bir yıl sonra (1 + enflasyon) kat daha az mal alır; bu etki yıllar boyunca bileşik olarak birikir. %30 enflasyonda fiyatlar yaklaşık 2,6 yılda ikiye katlanır.",
        "Bir yatırımın gerçek kazancı nominal faiz değil, enflasyondan arındırılmış reel getiridir: (1 + faiz) ÷ (1 + enflasyon) − 1. Faiz %40, enflasyon %30 ise reel getiri %7,7'dir; faiz enflasyonun altında kalırsa reel getiri negatif olur ve para nominal büyürken alım gücü erir. Yaygın 'faiz − enflasyon' kısayolu yüksek oranlarda yanıltır.",
        "İki tarih arasındaki gerçekleşen enflasyon, TÜFE endeks değerlerinin oranından bulunur; TÜİK'in 2003=100 bazlı endeksleri kullanılır. Sözleşme, alacak ve maaş güncellemelerinde bu oran; kira artışında ise TÜFE'nin 12 aylık ortalamalara göre değişim oranı esas alınır.",
    ],
    "formul": [
        "Gelecekteki eşdeğer tutar = bugünkü tutar × (1 + enflasyon)^yıl",
        "Alım gücü = bugünkü tutar ÷ (1 + enflasyon)^yıl",
        "Reel getiri = (1 + nominal faiz) ÷ (1 + enflasyon) − 1",
        "Dönem enflasyonu = (bitiş endeksi ÷ başlangıç endeksi − 1) × 100",
    ],
    "ornekler": [
        {"baslik": "100.000 ₺, %30 enflasyon, 3 yıl", "adimlar": ["(1,30)³ = 2,197 → 3 yıl sonra 219.700 ₺ gerekir", "Bugünkü 100.000 ₺'nin alım gücü 45.517 ₺'ye iner (%54,5 kayıp)"]},
        {"baslik": "Faiz %40, enflasyon %30", "adimlar": ["Reel getiri: 1,40 ÷ 1,30 − 1 = %7,69", "Kısayol (40 − 30 = %10) yanıltır"]},
    ],
    "tablo": {
        "baslik": "Enflasyona göre alım gücü kaybı (bugünkü 100 ₺)",
        "basliklar": ["Yıllık enflasyon", "1 yıl", "3 yıl", "5 yıl", "10 yıl"],
        "satirlar": [["%10", "90,9 ₺", "75,1 ₺", "62,1 ₺", "38,6 ₺"], ["%20", "83,3 ₺", "57,9 ₺", "40,2 ₺", "16,2 ₺"], ["%30", "76,9 ₺", "45,5 ₺", "26,9 ₺", "7,3 ₺"], ["%50", "66,7 ₺", "29,6 ₺", "13,2 ₺", "1,7 ₺"]],
        "not": "100 ÷ (1 + enflasyon)^yıl formülüyle.",
    },
    "sss": [
        {"soru": "Enflasyon hesabı nasıl yapılır?", "cevap": "Yıllık oranı yıl sayısı kadar bileşik uygulayın: tutar × (1 + oran)^yıl. %25 ile 2 yıl: × 1,5625."},
        {"soru": "Reel getiri nasıl hesaplanır?", "cevap": "(1 + faiz) ÷ (1 + enflasyon) − 1. Faiz %35, enflasyon %35 ise reel getiri sıfırdır."},
        {"soru": "Yıllık enflasyon ile 12 aylık ortalama farkı nedir?", "cevap": "Yıllık enflasyon, endeksin bir önceki yılın aynı ayına göre değişimi; 12 aylık ortalama ise son 12 ayın endeks ortalamasının önceki 12 ayınkine oranıdır. Kira artışında ikincisi kullanılır."},
        {"soru": "TÜFE endeksi nereden bulunur?", "cevap": "TÜİK veri portalından (data.tuik.gov.tr), 2003=100 bazlı aylık endeks tablosundan."},
    ],
    "kaynaklar": [
        {"ad": "TÜİK — Tüketici Fiyat Endeksi (aylık bülten ve endeks tabloları)", "url": "https://data.tuik.gov.tr/"},
        {"ad": "TCMB — Enflasyon raporu ve beklentiler", "url": "https://www.tcmb.gov.tr/"},
    ],
    "ilgili": ["kira-artis-orani-hesaplama", "mevduat-faizi-hesaplama", "bilesik-faiz-hesaplama"],
}
