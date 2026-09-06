# -*- coding: utf-8 -*-
HESAP = {
    "slug": "yuzde-hesaplama",
    "baslik": "Yüzde Hesaplama",
    "h1": "Yüzde Hesaplama — Bir Sayının Yüzdesi, Yüzde Değişim ve Oran",
    "kategori": "gunluk",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Yüzde hesaplama aracı: bir sayının yüzde kaçı, bir sayı diğerinin yüzde kaçı, yüzde artış-azalış (değişim) ve bir sayıya yüzde ekleme-çıkarma. Formüller ve örneklerle anında hesaplayın.",
    "kisa_cevap": "Bir sayının yüzdesi = sayı × yüzde ÷ 100 (200'ün %15'i = 30). Bir sayının diğerine oranı = (parça ÷ bütün) × 100 (30, 200'ün %15'idir). Yüzde değişim = (yeni − eski) ÷ eski × 100 (200'den 250'ye çıkış %25 artıştır).",
    "girdiler": [
        {"id": "mod", "etiket": "Hesaplama türü", "tip": "secim", "varsayilan": "yuzdesi", "genis": True,
         "secenekler": [["yuzdesi", "A sayısının %B'si kaçtır?"], ["orani", "A sayısı, B'nin yüzde kaçıdır?"],
                        ["degisim", "A'dan B'ye yüzde değişim"], ["ekle", "A sayısına %B ekle"], ["cikar", "A sayısından %B çıkar"]]},
        {"id": "a", "etiket": "A", "tip": "sayi", "varsayilan": "200"},
        {"id": "b", "etiket": "B", "tip": "sayi", "varsayilan": "15"},
    ],
    "js": r"""
function hesapla(g){
  var a = g.a, b = g.b;
  if (isNaN(a) || isNaN(b)) return {hata: 'A ve B değerlerini girin.'};
  var s = [], n = [];
  if (g.mod === 'yuzdesi') {
    s.push({etiket: a + ' sayısının %' + b + '\'si', deger: a * b / 100, vurgu: true});
    n.push('Formül: ' + a + ' × ' + b + ' ÷ 100');
  } else if (g.mod === 'orani') {
    if (b === 0) return {hata: 'B sıfır olamaz.'};
    s.push({etiket: a + ', ' + b + ' sayısının yüzde kaçı?', deger: a / b * 100, birim: '%', vurgu: true});
    n.push('Formül: (' + a + ' ÷ ' + b + ') × 100');
  } else if (g.mod === 'degisim') {
    if (a === 0) return {hata: 'Başlangıç değeri (A) sıfır olamaz.'};
    var d = (b - a) / a * 100;
    s.push({etiket: d >= 0 ? 'Yüzde artış' : 'Yüzde azalış', deger: Math.abs(d), birim: '%', vurgu: true});
    s.push({etiket: 'Fark', deger: b - a});
    n.push('Formül: (' + b + ' − ' + a + ') ÷ ' + a + ' × 100');
  } else if (g.mod === 'ekle') {
    s.push({etiket: a + ' + %' + b, deger: a * (1 + b / 100), vurgu: true});
    s.push({etiket: 'Eklenen tutar', deger: a * b / 100});
    n.push('Formül: ' + a + ' × (1 + ' + b + '/100)');
  } else {
    s.push({etiket: a + ' − %' + b, deger: a * (1 - b / 100), vurgu: true});
    s.push({etiket: 'Çıkarılan tutar', deger: a * b / 100});
    n.push('Formül: ' + a + ' × (1 − ' + b + '/100)');
  }
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Yüzde, bir bütünün 100 eşit parçasından kaçını aldığınızı gösterir; %15 demek 100'de 15 demektir. Bu yüzden bir sayının yüzdesini bulmak için sayıyı yüzde değeriyle çarpıp 100'e bölersiniz.",
        "Tersine, bir parçanın bütüne oranını yüzde olarak bulmak için parçayı bütüne bölüp 100 ile çarparsınız. Yüzde değişim ise yeni değerle eski değer arasındaki farkın eski değere oranıdır — artış ve azalışta payda her zaman başlangıç değeridir.",
        "İndirim, zam, faiz, KDV ve enflasyon hesaplarının tamamı bu üç temel işlemin türevidir. Bir sayıya yüzde eklemek için (1 + yüzde/100), çıkarmak için (1 − yüzde/100) ile çarpmak en pratik yoldur.",
    ],
    "formul": [
        "A'nın %B'si = A × B ÷ 100",
        "A, B'nin yüzde kaçı = (A ÷ B) × 100",
        "Yüzde değişim = (Yeni − Eski) ÷ Eski × 100",
        "A'ya %B ekle = A × (1 + B ÷ 100) · A'dan %B çıkar = A × (1 − B ÷ 100)",
    ],
    "ornekler": [
        {"baslik": "1.250 ₺'lik ürüne %30 indirim", "adimlar": ["İndirim tutarı: 1.250 × 30 ÷ 100 = 375 ₺", "İndirimli fiyat: 1.250 − 375 = 875 ₺"]},
        {"baslik": "Maaş 30.000 ₺'den 36.000 ₺'ye çıktı; zam yüzde kaç?", "adimlar": ["Fark: 36.000 − 30.000 = 6.000", "Değişim: 6.000 ÷ 30.000 × 100 = %20"]},
        {"baslik": "40 sorunun 34'ü doğru; başarı yüzdesi", "adimlar": ["(34 ÷ 40) × 100 = %85"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Bir sayının yüzdesi nasıl hesaplanır?", "cevap": "Sayıyı yüzde değeriyle çarpıp 100'e bölün. 800'ün %25'i: 800 × 25 ÷ 100 = 200."},
        {"soru": "Yüzde artış nasıl hesaplanır?", "cevap": "(Yeni − Eski) ÷ Eski × 100. 50'den 65'e çıkış: (65 − 50) ÷ 50 × 100 = %30 artış."},
        {"soru": "Yüzde azalış hesaplaması artıştan farklı mı?", "cevap": "Formül aynıdır; sonuç negatif çıkar ve azalış olarak okunur. 65'ten 50'ye düşüş: (50 − 65) ÷ 65 × 100 = −%23,08."},
        {"soru": "%20 zam sonra %20 indirim başa döndürür mü?", "cevap": "Hayır. 100 → %20 zam → 120 → %20 indirim → 96. Çünkü indirim daha büyük bir tabana uygulanır; bu yüzden ardışık yüzdeler toplanmaz, çarpılır."},
        {"soru": "Yüzde puanı ile yüzde farkı nedir?", "cevap": "Oranlar arasındaki mutlak fark 'puan'dır: %10'dan %15'e çıkış 5 puan artıştır ama yüzde olarak %50 artıştır."},
    ],
    "kaynaklar": [],
    "ilgili": ["kdv-hesaplama", "indirim-hesaplama", "kira-artis-orani-hesaplama"],
}
