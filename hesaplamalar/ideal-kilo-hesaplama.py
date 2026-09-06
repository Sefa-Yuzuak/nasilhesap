# -*- coding: utf-8 -*-
HESAP = {
    "slug": "ideal-kilo-hesaplama",
    "baslik": "İdeal Kilo Hesaplama",
    "h1": "İdeal Kilo Hesaplama — Boya Göre İdeal Ağırlık (Devine, Robinson, Miller, Hamwi)",
    "kategori": "saglik",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "İdeal kilo hesaplama: boy ve cinsiyete göre Devine, Robinson, Miller ve Hamwi formülleriyle ideal ağırlık, VKİ 18,5–24,9 normal kilo aralığı ve mevcut kilonuzla fark.",
    "kisa_cevap": "İdeal kilo için en yaygın formül Devine'dır: erkek 50 kg + 152 cm üzerindeki her cm için 0,9 kg; kadın 45,5 kg + her cm için 0,9 kg. 175 cm erkek için ≈ 70,7 kg, 165 cm kadın için ≈ 57,2 kg. Sağlıklı aralık ise VKİ 18,5–24,9'a karşılık gelir: 175 cm için 56,7–76,3 kg.",
    "girdiler": [
        {"id": "cins", "etiket": "Cinsiyet", "tip": "secim", "varsayilan": "e", "secenekler": [["e", "Erkek"], ["k", "Kadın"]]},
        {"id": "boy", "etiket": "Boy", "tip": "sayi", "varsayilan": "175", "birim": "cm"},
        {"id": "kilo", "etiket": "Mevcut kilo (isteğe bağlı)", "tip": "sayi", "varsayilan": "", "birim": "kg"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.boy > 100)) return {hata: 'Boyu cm olarak girin.'};
  var inc = g.boy / 2.54, e = g.cins === 'e', fazla = Math.max(0, inc - 60), m = g.boy / 100;
  var devine = (e ? 50 : 45.5) + 2.3 * fazla;
  var robinson = (e ? 52 : 49) + (e ? 1.9 : 1.7) * fazla;
  var miller = (e ? 56.2 : 53.1) + (e ? 1.41 : 1.36) * fazla;
  var hamwi = (e ? 48 : 45.5) + (e ? 2.7 : 2.2) * fazla;
  var ort = (devine + robinson + miller + hamwi) / 4;
  var alt = 18.5 * m * m, ust = 24.9 * m * m;
  var s = [
    {etiket: 'İdeal kilo (formüllerin ortalaması)', deger: ort, birim: 'kg', vurgu: true},
    {etiket: 'Sağlıklı aralık (VKİ 18,5–24,9)', deger: NH.fmt(alt) + ' – ' + NH.fmt(ust) + ' kg'},
    {etiket: 'Devine (1974)', deger: devine, birim: 'kg'},
    {etiket: 'Robinson (1983)', deger: robinson, birim: 'kg'},
    {etiket: 'Miller (1983)', deger: miller, birim: 'kg'},
    {etiket: 'Hamwi (1964)', deger: hamwi, birim: 'kg'}
  ];
  if (g.kilo > 0) {
    var d = g.kilo - ort, vki = g.kilo / (m * m);
    s.push({etiket: 'Mevcut kilo − ideal', deger: (d >= 0 ? '+' : '') + NH.fmt(d) + ' kg'});
    s.push({etiket: 'Mevcut VKİ', deger: Math.round(vki * 10) / 10});
  }
  return {sonuclar: s, notlar: ['Formüller 152 cm (60 inç) üzerindeki her inç için ekleme yapar; 152 cm altında sonuçlar güvenilir değildir. Kas kütlesi, yaş ve vücut tipi dikkate alınmaz; aralık olarak yorumlayın.']};
}
""",
    "nasil": [
        "İdeal kilo formülleri, ilaç dozu hesabı için geliştirilmiş ve sonradan genel sağlık ölçütü olarak yaygınlaşmış boya dayalı denklemlerdir. Hepsi aynı mantığı izler: 152 cm (5 fit) için bir taban kilo, üzerindeki her inç (2,54 cm) için sabit bir ekleme. En yaygın kullanılanı Devine (1974); Robinson ve Miller (1983) daha ılımlı, Hamwi (1964) daha yüksek değer verir.",
        "Tek bir 'ideal' sayı yerine aralık düşünmek daha doğrudur. Dünya Sağlık Örgütü'nün normal VKİ bandı (18,5–24,9), boyunuza göre sağlıklı kilo aralığını verir; formüllerin ortalaması genellikle bu bandın ortasına düşer. Sporcularda kas kütlesi nedeniyle ideal kilo formül değerinin üstünde olabilir.",
        "Bu değerler yetişkinler içindir; 18 yaş altı, gebelik ve ileri yaşta farklı ölçütler geçerlidir. Sağlık açısından kilo tek başına yeterli gösterge değildir: bel çevresi, vücut yağ oranı ve kan değerleriyle birlikte değerlendirilmelidir.",
    ],
    "formul": [
        "Devine: erkek 50 + 2,3 × (boy_inç − 60) · kadın 45,5 + 2,3 × (boy_inç − 60)",
        "Robinson: erkek 52 + 1,9 × (inç − 60) · kadın 49 + 1,7 × (inç − 60)",
        "Miller: erkek 56,2 + 1,41 × (inç − 60) · kadın 53,1 + 1,36 × (inç − 60)",
        "Hamwi: erkek 48 + 2,7 × (inç − 60) · kadın 45,5 + 2,2 × (inç − 60) · boy_inç = boy_cm ÷ 2,54",
        "Sağlıklı aralık = 18,5 × boy² … 24,9 × boy² (boy metre)",
    ],
    "ornekler": [
        {"baslik": "Erkek, 175 cm", "adimlar": ["175 ÷ 2,54 = 68,9 inç → fazla 8,9 inç", "Devine: 50 + 2,3 × 8,9 = 70,5 kg · Robinson 68,9 · Miller 68,7 · Hamwi 72,0", "Ortalama ≈ 70 kg; sağlıklı aralık 56,7–76,3 kg"]},
        {"baslik": "Kadın, 165 cm", "adimlar": ["165 ÷ 2,54 = 65 inç → fazla 5 inç", "Devine: 45,5 + 11,5 = 57 kg · Robinson 57,5 · Miller 59,9 · Hamwi 56,5", "Ortalama ≈ 57,7 kg; sağlıklı aralık 50,4–67,8 kg"]},
    ],
    "tablo": {
        "baslik": "Boya göre ideal kilo (Devine, yaklaşık)",
        "basliklar": ["Boy", "Erkek", "Kadın", "Sağlıklı aralık (VKİ)"],
        "satirlar": [["160 cm", "57,3 kg", "52,8 kg", "47,4 – 63,7 kg"], ["165 cm", "61,8 kg", "57,3 kg", "50,4 – 67,8 kg"], ["170 cm", "66,3 kg", "61,8 kg", "53,5 – 72,0 kg"], ["175 cm", "70,8 kg", "66,3 kg", "56,7 – 76,3 kg"], ["180 cm", "75,4 kg", "70,9 kg", "59,9 – 80,7 kg"], ["185 cm", "79,9 kg", "75,4 kg", "63,3 – 85,2 kg"]],
        "not": "Devine formülü; sağlıklı aralık DSÖ normal VKİ bandı.",
    },
    "sss": [
        {"soru": "İdeal kilom kaç olmalı?", "cevap": "Boyunuza göre Devine formülü tek bir değer verir (175 cm erkek ≈ 71 kg); daha gerçekçi olan VKİ 18,5–24,9 aralığıdır (175 cm için 57–76 kg). Aracımız ikisini de gösterir."},
        {"soru": "Hangi ideal kilo formülü en doğru?", "cevap": "Hiçbiri bireysel vücut yapısını ölçmez. Devine en yaygın olandır; ortalamalarını almak ve VKİ aralığıyla birlikte değerlendirmek en dengeli yaklaşımdır."},
        {"soru": "Boy − 100 formülü doğru mu?", "cevap": "Broca'nın eski formülü (boy − 100, kadınlarda %10 az) kabaca fikir verir ama uzun boylularda fazla, kısa boylularda düşük çıkar; modern formüller tercih edilir."},
        {"soru": "Kaslıysam ideal kilomun üstünde olmam sorun mu?", "cevap": "Hayır. Formüller kas kütlesini ayırt etmez; vücut yağ oranı normal aralıktaysa (erkek %10-20, kadın %20-30) formül değerinin üstünde olmak sağlıksız değildir."},
    ],
    "kaynaklar": [
        {"ad": "Pai MP, Paloucek FP. The origin of the 'ideal' body weight equations. Ann Pharmacother 2000", "url": "https://pubmed.ncbi.nlm.nih.gov/10981254/"},
        {"ad": "Dünya Sağlık Örgütü — BMI sınıflandırması", "url": "https://www.who.int/"},
    ],
    "ilgili": ["vki-hesaplama", "kalori-hesaplama"],
}
