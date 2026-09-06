# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kalori-hesaplama",
    "baslik": "Günlük Kalori İhtiyacı Hesaplama",
    "h1": "Günlük Kalori İhtiyacı Hesaplama — Bazal Metabolizma (BMR) ve Kilo Verme Kalorisi",
    "kategori": "saglik",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Günlük kalori ihtiyacı hesaplama: yaş, cinsiyet, boy, kilo ve aktivite düzeyine göre bazal metabolizma hızı (BMR, Mifflin-St Jeor), günlük toplam enerji harcaması ve kilo verme / koruma / alma için hedef kalori.",
    "kisa_cevap": "Bazal metabolizma (BMR) Mifflin-St Jeor formülüyle bulunur: erkek 10×kilo + 6,25×boy − 5×yaş + 5; kadın aynı formül − 161. Günlük ihtiyaç = BMR × aktivite katsayısı (1,2 hareketsiz … 1,9 çok aktif). 30 yaş, 175 cm, 75 kg, az hareketli bir erkeğin BMR'si 1.699 kcal, günlük ihtiyacı ≈ 2.336 kcal; haftada ~0,5 kg vermek için ≈ 1.836 kcal.",
    "girdiler": [
        {"id": "cins", "etiket": "Cinsiyet", "tip": "secim", "varsayilan": "e", "secenekler": [["e", "Erkek"], ["k", "Kadın"]]},
        {"id": "yas", "etiket": "Yaş", "tip": "tamsayi", "varsayilan": "30", "birim": "yıl"},
        {"id": "boy", "etiket": "Boy", "tip": "sayi", "varsayilan": "175", "birim": "cm"},
        {"id": "kilo", "etiket": "Kilo", "tip": "sayi", "varsayilan": "75", "birim": "kg"},
        {"id": "akt", "etiket": "Aktivite düzeyi", "tip": "secim", "varsayilan": "1.375", "genis": True,
         "secenekler": [["1.2", "Hareketsiz (masa başı, spor yok)"], ["1.375", "Az hareketli (haftada 1-3 gün hafif egzersiz)"], ["1.55", "Orta (haftada 3-5 gün egzersiz)"], ["1.725", "Aktif (haftada 6-7 gün yoğun egzersiz)"], ["1.9", "Çok aktif (ağır iş / günde 2 antrenman)"]]},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.yas > 0) || !(g.boy > 50) || !(g.kilo > 10)) return {hata: 'Yaş, boy ve kiloyu girin.'};
  var bmr = 10 * g.kilo + 6.25 * g.boy - 5 * g.yas + (g.cins === 'e' ? 5 : -161);
  var akt = parseFloat(g.akt) || 1.2, tdee = bmr * akt;
  return {
    sonuclar: [
      {etiket: 'Günlük kalori ihtiyacı (kilo koruma)', deger: Math.round(tdee), birim: 'kcal', ondalik: 0, vurgu: true},
      {etiket: 'Bazal metabolizma hızı (BMR)', deger: Math.round(bmr), birim: 'kcal', ondalik: 0},
      {etiket: 'Hafif kilo verme (−0,25 kg/hafta)', deger: Math.round(tdee - 250), birim: 'kcal', ondalik: 0},
      {etiket: 'Kilo verme (−0,5 kg/hafta)', deger: Math.round(tdee - 500), birim: 'kcal', ondalik: 0},
      {etiket: 'Hızlı kilo verme (−1 kg/hafta)', deger: Math.round(Math.max(bmr, tdee - 1000)), birim: 'kcal', ondalik: 0},
      {etiket: 'Kilo alma (+0,25 kg/hafta)', deger: Math.round(tdee + 250), birim: 'kcal', ondalik: 0},
      {etiket: 'Kilo alma (+0,5 kg/hafta)', deger: Math.round(tdee + 500), birim: 'kcal', ondalik: 0}
    ],
    notlar: ['Mifflin-St Jeor denklemi; aktivite katsayısı ' + akt + '. Günlük alım uzun süre BMR\'nin altına inmemelidir (kadın ≥1.200, erkek ≥1.500 kcal genel alt sınır).', 'Gebelik, emzirme, tiroid hastalıkları ve 18 yaş altı için diyetisyen/hekim görüşü alın.']
  };
}
""",
    "nasil": [
        "Günlük kalori ihtiyacı iki adımda bulunur: önce vücudun dinlenirken harcadığı enerji olan bazal metabolizma hızı (BMR), sonra bunun aktivite düzeyiyle çarpılmasıyla günlük toplam enerji harcaması (TDEE). Bu sayfa, 1990'da yayımlanan ve Amerikan Diyetisyenler Derneği'nce en isabetli kabul edilen Mifflin-St Jeor denklemini kullanır.",
        "Aktivite katsayısı, egzersiz ve iş temposuna göre 1,2 (hareketsiz) ile 1,9 (çok aktif) arasında seçilir. Çoğu masa başı çalışan 'az hareketli' (1,375) sınıfındadır; katsayıyı olduğundan yüksek seçmek, kalori ihtiyacını abartmanın en yaygın nedenidir.",
        "Kilo vermek için günlük alım, ihtiyacın altında tutulur: 0,5 kg yağ yaklaşık 3.500 kcal'ye denk geldiğinden haftada 0,5 kg için günde ~500 kcal açık gerekir. Açık, BMR'nin altına inmemeli; sürdürülebilir hedef haftada 0,25-0,5 kg'dır. Kilo almak için ise ihtiyacın 250-500 kcal üzerine çıkılır.",
    ],
    "formul": [
        "BMR (erkek) = 10 × kilo + 6,25 × boy − 5 × yaş + 5",
        "BMR (kadın) = 10 × kilo + 6,25 × boy − 5 × yaş − 161",
        "Günlük ihtiyaç (TDEE) = BMR × aktivite katsayısı (1,2 / 1,375 / 1,55 / 1,725 / 1,9)",
        "Kilo verme kalorisi = TDEE − 500 (≈ 0,5 kg/hafta) · kilo alma = TDEE + 250–500",
    ],
    "ornekler": [
        {"baslik": "Erkek, 30 yaş, 175 cm, 75 kg, az hareketli", "adimlar": ["BMR = 10×75 + 6,25×175 − 5×30 + 5 = 750 + 1.093,75 − 150 + 5 = 1.698,75 kcal", "TDEE = 1.698,75 × 1,375 ≈ 2.336 kcal", "0,5 kg/hafta vermek için ≈ 1.836 kcal"]},
        {"baslik": "Kadın, 28 yaş, 165 cm, 60 kg, orta aktif", "adimlar": ["BMR = 600 + 1.031,25 − 140 − 161 = 1.330,25 kcal", "TDEE = 1.330,25 × 1,55 ≈ 2.062 kcal"]},
    ],
    "tablo": {
        "baslik": "Aktivite katsayıları",
        "basliklar": ["Düzey", "Katsayı", "Tanım"],
        "satirlar": [["Hareketsiz", "1,2", "Masa başı, düzenli egzersiz yok"], ["Az hareketli", "1,375", "Haftada 1-3 gün hafif egzersiz"], ["Orta", "1,55", "Haftada 3-5 gün orta egzersiz"], ["Aktif", "1,725", "Haftada 6-7 gün yoğun egzersiz"], ["Çok aktif", "1,9", "Fiziksel iş veya günde iki antrenman"]],
        "not": "Katsayılar Harris-Benedict/Mifflin-St Jeor literatüründen; bireysel farklar ±%10-15 olabilir.",
    },
    "sss": [
        {"soru": "Günde kaç kalori almalıyım?", "cevap": "Kilonuzu korumak için BMR × aktivite katsayısı kadar; vermek için bunun 250-500 kcal altı, almak için 250-500 kcal üstü. Aracımız yaş, boy, kilo ve aktivitenize göre hesaplar."},
        {"soru": "BMR nedir?", "cevap": "Bazal metabolizma hızı: vücudun tam dinlenirken (nefes, dolaşım, hücre yenilenmesi) harcadığı günlük enerji. Toplam harcamanın %60-70'ini oluşturur."},
        {"soru": "1 kilo vermek için kaç kalori yakmalıyım?", "cevap": "Yaklaşık 7.000 kcal açık gerekir (0,5 kg ≈ 3.500 kcal). Günde 500 kcal açıkla haftada ~0,5 kg, 1.000 kcal açıkla ~1 kg verilir."},
        {"soru": "Kalori hesaplamada hangi formül en doğru?", "cevap": "Mifflin-St Jeor (1990), Harris-Benedict'e göre daha isabetli bulunmuştur ve bu sayfada kullanılır. Kas oranı bilinen kişiler için Katch-McArdle da kullanılabilir."},
        {"soru": "Çok düşük kalori almak kilo vermeyi hızlandırır mı?", "cevap": "Kısa vadede evet ama kas kaybı, metabolizma yavaşlaması ve besin eksikliği riski taşır. Günlük alım BMR'nin altına uzun süre inmemelidir."},
    ],
    "kaynaklar": [
        {"ad": "Mifflin MD ve ark., A new predictive equation for resting energy expenditure, Am J Clin Nutr 1990", "url": "https://pubmed.ncbi.nlm.nih.gov/2305711/"},
        {"ad": "T.C. Sağlık Bakanlığı — Türkiye Beslenme Rehberi", "url": "https://hsgm.saglik.gov.tr/"},
    ],
    "ilgili": ["vki-hesaplama", "ideal-kilo-hesaplama", "yas-hesaplama"],
}
