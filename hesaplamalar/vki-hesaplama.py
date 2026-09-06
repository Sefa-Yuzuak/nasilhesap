# -*- coding: utf-8 -*-
HESAP = {
    "slug": "vki-hesaplama",
    "baslik": "Vücut Kitle İndeksi (VKİ) Hesaplama",
    "h1": "Vücut Kitle İndeksi (VKİ / BMI) Hesaplama — İdeal Kilo Aralığı",
    "kategori": "saglik",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "VKİ (BMI) hesaplama: boy ve kilonuza göre vücut kitle indeksi, Dünya Sağlık Örgütü sınıflandırması (zayıf, normal, fazla kilolu, obez) ve ideal kilo aralığınız. Formül, örnek ve sık sorulan sorular.",
    "kisa_cevap": "VKİ = kilo (kg) ÷ boy² (m²). 170 cm ve 70 kg için VKİ = 70 ÷ 1,7² = 24,2 → normal. DSÖ'ye göre 18,5 altı zayıf, 18,5–24,9 normal, 25–29,9 fazla kilolu, 30 ve üzeri obezdir; 170 cm için normal kilo aralığı 53,5–72 kg'dır.",
    "girdiler": [
        {"id": "boy", "etiket": "Boy", "tip": "sayi", "varsayilan": "170", "birim": "cm"},
        {"id": "kilo", "etiket": "Kilo", "tip": "sayi", "varsayilan": "70", "birim": "kg"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.boy > 50) || !(g.kilo > 10)) return {hata: 'Boy (cm) ve kilo (kg) girin.'};
  var m = g.boy / 100, vki = g.kilo / (m * m);
  var sinif = vki < 16 ? 'Ağır zayıf' : vki < 17 ? 'Orta zayıf' : vki < 18.5 ? 'Hafif zayıf' : vki < 25 ? 'Normal' : vki < 30 ? 'Fazla kilolu' : vki < 35 ? 'Obez (I. derece)' : vki < 40 ? 'Obez (II. derece)' : 'Morbid obez (III. derece)';
  var alt = 18.5 * m * m, ust = 24.9 * m * m;
  var fark = g.kilo < alt ? alt - g.kilo : g.kilo > ust ? g.kilo - ust : 0;
  return {
    sonuclar: [
      {etiket: 'Vücut kitle indeksi', deger: Math.round(vki * 10) / 10, vurgu: true},
      {etiket: 'Sınıf (DSÖ)', deger: sinif},
      {etiket: 'Normal kilo aralığı (VKİ 18,5–24,9)', deger: NH.fmt(alt) + ' – ' + NH.fmt(ust) + ' kg'},
      {etiket: fark ? (g.kilo < alt ? 'Normal aralığa ulaşmak için alınması gereken' : 'Normal aralığa inmek için verilmesi gereken') : 'Durum', deger: fark ? NH.fmt(fark) + ' kg' : 'Normal aralıktasınız'}
    ],
    notlar: ['VKİ kas kütlesi, yaş, cinsiyet ve yağ dağılımını dikkate almaz; sporcular ve yaşlılarda yanıltıcı olabilir. Bel çevresi ve vücut yağ oranı ile birlikte değerlendirin.', '18 yaş altı için yaşa göre persentil eğrileri kullanılır; bu araç yetişkinler içindir.']
  };
}
""",
    "nasil": [
        "Vücut kitle indeksi (VKİ, İngilizce BMI), kilonun boyun karesine bölünmesiyle bulunan ve vücut ağırlığının boya göre uygunluğunu gösteren basit bir ölçüttür. Kilogram ve metre cinsinden hesaplanır; boy santimetre olarak biliniyorsa önce 100'e bölünür.",
        "Dünya Sağlık Örgütü yetişkinler için VKİ'yi 18,5'in altı zayıf, 18,5–24,9 normal, 25–29,9 fazla kilolu ve 30 üzeri obez olarak sınıflandırır; obezite kendi içinde 30–34,9 (I), 35–39,9 (II) ve 40 üzeri (III, morbid) olarak derecelenir. İdeal kilo aralığı bu sınıflandırmanın 'normal' bandının boyunuza göre kilograma çevrilmesidir.",
        "VKİ bir tarama aracıdır, tanı aracı değildir: kas ağırlığı yüksek sporcularda yüksek çıkabilir, kas kaybı olan yaşlılarda ise normal görünmesine rağmen yağ oranı yüksek olabilir. Bel çevresi (erkek >102 cm, kadın >88 cm risk) ve vücut yağ yüzdesiyle birlikte yorumlanmalıdır.",
    ],
    "formul": [
        "VKİ = kilo (kg) ÷ [boy (m)]²",
        "Normal kilo alt sınırı = 18,5 × boy² · üst sınırı = 24,9 × boy²",
        "Sınıflar: <18,5 zayıf · 18,5–24,9 normal · 25–29,9 fazla kilolu · ≥30 obez",
    ],
    "ornekler": [
        {"baslik": "170 cm, 70 kg", "adimlar": ["Boy: 1,70 m → boy² = 2,89", "VKİ = 70 ÷ 2,89 = 24,2 → normal", "Normal aralık: 18,5 × 2,89 = 53,5 kg ile 24,9 × 2,89 = 72 kg"]},
        {"baslik": "180 cm, 95 kg", "adimlar": ["boy² = 3,24 → VKİ = 95 ÷ 3,24 = 29,3 → fazla kilolu", "Normal üst sınır 80,7 kg → 14,3 kg fazla"]},
    ],
    "tablo": {
        "baslik": "DSÖ VKİ sınıflandırması (yetişkin)",
        "basliklar": ["VKİ", "Sınıf"],
        "satirlar": [["< 18,5", "Zayıf"], ["18,5 – 24,9", "Normal"], ["25,0 – 29,9", "Fazla kilolu"], ["30,0 – 34,9", "Obez, I. derece"], ["35,0 – 39,9", "Obez, II. derece"], ["≥ 40", "Obez, III. derece (morbid)"]],
        "not": "Kaynak: Dünya Sağlık Örgütü; T.C. Sağlık Bakanlığı Türkiye Sağlıklı Beslenme ve Hareketli Hayat Programı.",
    },
    "sss": [
        {"soru": "VKİ nasıl hesaplanır?", "cevap": "Kilonuzu (kg) boyunuzun metre cinsinden karesine bölün. 65 kg ve 1,65 m için 65 ÷ 2,72 = 23,9."},
        {"soru": "İdeal VKİ kaç olmalı?", "cevap": "Yetişkinlerde 18,5–24,9 aralığı normal kabul edilir; birçok çalışma 21–23 bandını en düşük sağlık riskiyle ilişkilendirir."},
        {"soru": "VKİ kadın ve erkekte farklı mı?", "cevap": "Formül ve DSÖ sınırları aynıdır. Ancak kadınlarda doğal yağ oranı daha yüksek olduğundan aynı VKİ farklı vücut kompozisyonuna karşılık gelebilir."},
        {"soru": "Çocuklarda VKİ nasıl değerlendirilir?", "cevap": "2-18 yaş için yaşa ve cinsiyete göre persentil eğrileri kullanılır; 85. persentil üzeri fazla kilolu, 95. persentil üzeri obez sayılır. Yetişkin sınırları çocuklara uygulanmaz."},
        {"soru": "VKİ yüksek ama kaslıyım, obez miyim?", "cevap": "Muhtemelen hayır. VKİ kas ile yağı ayırt etmez; vücut yağ oranı ölçümü (biyoempedans, DEXA) ve bel çevresi daha doğru fikir verir."},
    ],
    "kaynaklar": [
        {"ad": "Dünya Sağlık Örgütü — Body mass index (BMI)", "url": "https://www.who.int/"},
        {"ad": "T.C. Sağlık Bakanlığı — Türkiye Sağlıklı Beslenme ve Hareketli Hayat Programı", "url": "https://hsgm.saglik.gov.tr/"},
    ],
    "ilgili": ["yas-hesaplama", "yuzde-hesaplama"],
}
