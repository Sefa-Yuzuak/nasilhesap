# -*- coding: utf-8 -*-
HESAP = {
    "slug": "obp-hesaplama",
    "baslik": "OBP Hesaplama",
    "h1": "OBP Hesaplama — Ortaöğretim Başarı Puanı ve YKS Puanına Katkısı",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "OBP hesaplama: diploma notunuzdan ortaöğretim başarı puanını (diploma × 5) ve YKS yerleştirme puanınıza katkısını (OBP × 0,12; önceki yıl yerleşenlerde 0,06) hesaplayın. 100'lük–5'lik not dönüşümü dahil.",
    "kisa_cevap": "OBP = diploma notu × 5 olarak hesaplanır ve 250–500 aralığında değer alır (diploma notu 50–100). YKS yerleştirme puanına katkısı OBP × 0,12'dir; yani en fazla 60 puan (100 × 5 × 0,12) ekler. Bir önceki yıl bir yükseköğretim programına yerleşmiş adaylarda katsayı 0,06'ya düşer ve katkı yarıya iner.",
    "senaryolar": [
        {"ad": "Diploma 70", "degerler": {"sistem": "100", "not": "70", "yerlesti": False}},
        {"ad": "Diploma 85", "degerler": {"sistem": "100", "not": "85", "yerlesti": False}},
        {"ad": "Diploma 100 (tam)", "degerler": {"sistem": "100", "not": "100", "yerlesti": False}},
        {"ad": "Diploma 85 · geçen yıl yerleşti", "degerler": {"sistem": "100", "not": "85", "yerlesti": True}},
        {"ad": "5'lik sistem: 4,20", "degerler": {"sistem": "5", "not": "4.20", "yerlesti": False}},
    ],
    "girdiler": [
        {"id": "sistem", "etiket": "Diploma notu sistemi", "tip": "secim", "varsayilan": "100",
         "secenekler": [["100", "100'lük sistem"], ["5", "5'lik sistem"]]},
        {"id": "not", "etiket": "Diploma notu", "tip": "sayi", "varsayilan": "85", "ipucu": "e-Okul / diploma"},
        {"id": "yerlesti", "etiket": "Durum", "tip": "onay", "varsayilan": False, "onay_metin": "Bir önceki yıl bir yükseköğretim programına yerleştim", "genis": True},
    ],
    "js": r"""
function hesapla(g){
  var d100;
  if (g.sistem === '5') {
    if (!(g.not >= 1 && g.not <= 5)) return {hata: "5'lik sistemde diploma notu 1 ile 5 arasında olmalı."};
    d100 = g.not * 20;
  } else {
    if (!(g.not >= 0 && g.not <= 100)) return {hata: "100'lük sistemde diploma notu 0 ile 100 arasında olmalı."};
    d100 = g.not;
  }
  if (d100 < 50) return {hata: 'Diploma notu 50\'nin altında olamaz (mezuniyet şartı).'};
  var obp = d100 * 5;
  var kat = g.yerlesti ? 0.06 : 0.12;
  var katki = obp * kat;
  var maks = 500 * kat;
  return {
    sonuclar: [
      {etiket: 'OBP (Ortaöğretim Başarı Puanı)', deger: obp, vurgu: true},
      {etiket: 'YKS puanına katkısı (× ' + kat.toFixed(2).replace('.', ',') + ')', deger: katki, birim: 'puan'},
      {etiket: 'Bu durumdaki en yüksek katkı', deger: maks, birim: 'puan'},
      {etiket: 'Kaçırılan puan (tam diplomaya göre)', deger: maks - katki, birim: 'puan'},
      {etiket: 'Diploma notu (100\'lük)', deger: d100},
      {etiket: 'Diploma notu (5\'lik)', deger: d100 / 20},
      {etiket: 'Uygulanan katsayı', deger: g.yerlesti ? '0,06 (önceki yıl yerleşen)' : '0,12 (standart)'}
    ],
    notlar: ['OBP 250–500 aralığındadır: mezuniyet için gereken en düşük diploma notu 50 olduğundan alt sınır 250\'dir.',
             g.yerlesti ? 'Önceki yıl bir programa yerleştiğiniz için katsayı yarıya (0,06) iner; kayıt sildirmek bu kuralı değiştirmez.' : 'Bir önceki yıl herhangi bir yükseköğretim programına yerleşirseniz sonraki yıl katsayınız 0,06\'ya düşer.',
             'OBP, TYT ve AYT puanlarına eklenir; ek puanlı yerleştirmelerde (meslek lisesi vb.) farklı hükümler uygulanabilir. Kesin bilgi için ÖSYM kılavuzuna bakın.']
  };
}
""",
    "nasil": [
        "Ortaöğretim Başarı Puanı (OBP), lise diploma notunuzun 5 ile çarpılmasıyla bulunur. Mezuniyet için gereken en düşük diploma notu 50 olduğu için OBP 250 ile 500 arasında değer alır. Diploma notunuz 5'lik sistemdeyse önce 20 ile çarpılarak 100'lük sisteme çevrilir (4,25 × 20 = 85).",
        "OBP doğrudan sıralamaya girmez; YKS puanınıza katkı olarak eklenir. Standart durumda katsayı 0,12'dir, yani 500 OBP en fazla 60 puan katkı sağlar. Bir önceki yıl herhangi bir yükseköğretim programına (açıköğretim dahil) yerleşmiş adaylarda bu katsayı 0,06'ya düşer ve katkı 30 puanla sınırlanır; kayıt sildirmek bu durumu değiştirmez.",
        "Bu 60 puanlık fark, yoğun rekabetin olduğu bölümlerde binlerce sıralamaya karşılık gelebilir. Diploma notu 70 olan bir aday 100 olan adaya göre 18 puan geride başlar — bu, TYT'de yaklaşık 3-4 net farkına denk düşen ciddi bir açıktır.",
    ],
    "formul": [
        "OBP = diploma notu (100'lük) × 5   → 250–500 aralığı",
        "5'lik sistemde: diploma notu × 20 = 100'lük not",
        "YKS puanına katkı = OBP × 0,12   (önceki yıl yerleşenler: OBP × 0,06)",
        "En yüksek katkı = 500 × 0,12 = 60 puan (yerleşenler için 30 puan)",
    ],
    "ornekler": [
        {"baslik": "Diploma notu 85", "adimlar": ["OBP = 85 × 5 = 425", "Katkı = 425 × 0,12 = 51 puan", "Tam diplomalı adaya göre 9 puan geride"]},
        {"baslik": "Diploma 4,25 (5'lik sistem)", "adimlar": ["100'lük: 4,25 × 20 = 85", "OBP 425, katkı 51 puan"]},
        {"baslik": "Diploma 92, geçen yıl yerleşmiş", "adimlar": ["OBP = 460", "Katsayı 0,06 → katkı 27,6 puan (yerleşmeseydi 55,2)"]},
    ],
    "tablo": {
        "baslik": "Diploma notuna göre OBP ve YKS katkısı",
        "basliklar": ["Diploma notu", "OBP", "Katkı (0,12)", "Katkı (0,06)"],
        "satirlar": [["50", "250", "30,0", "15,0"], ["60", "300", "36,0", "18,0"], ["70", "350", "42,0", "21,0"], ["80", "400", "48,0", "24,0"], ["85", "425", "51,0", "25,5"], ["90", "450", "54,0", "27,0"], ["95", "475", "57,0", "28,5"], ["100", "500", "60,0", "30,0"]],
        "not": "Katkı puanları TYT ve AYT yerleştirme puanlarına eklenir. Kaynak: ÖSYM YKS kılavuzu.",
    },
    "sss": [
        {"soru": "OBP nasıl hesaplanır?", "cevap": "Diploma notunuzu 5 ile çarpın. Diploma notu 78 ise OBP = 390."},
        {"soru": "OBP kaç puan katkı sağlar?", "cevap": "OBP × 0,12. En yüksek 60 puan (500 OBP). Önceki yıl yerleşmiş adaylarda katsayı 0,06 ve en yüksek katkı 30 puandır."},
        {"soru": "Geçen yıl yerleştim, OBP'm yarıya mı düşüyor?", "cevap": "OBP değil, katsayı düşüyor: 0,12 yerine 0,06 uygulanır. Kayıt yaptırmamış veya sildirmiş olmanız sonucu değiştirmez; yerleşmiş sayılırsınız."},
        {"soru": "Diploma notum 5'lik sistemde, ne yapmalıyım?", "cevap": "20 ile çarpıp 100'lük sisteme çevirin: 3,80 × 20 = 76 → OBP 380."},
        {"soru": "OBP'yi yükseltebilir miyim?", "cevap": "Mezun olduktan sonra diploma notu değişmez. Sorumluluk sınavı veya lise bitirme sınavıyla not düzeltmesi istisnai hallerde mümkündür; MEB mevzuatına bakın."},
        {"soru": "OBP sıralamayı ne kadar etkiler?", "cevap": "60 puanlık üst sınır, rekabetin yoğun olduğu bölümlerde binlerce sıra fark yaratabilir; TYT'de yaklaşık 3-4 net karşılığıdır."},
    ],
    "kaynaklar": [
        {"ad": "ÖSYM — 2026 YKS Kılavuzu (OBP ve puan hesaplama)", "url": "https://www.osym.gov.tr/2026yuksekogretim-kurumlari-sinavi-yks-kilavuzu"},
        {"ad": "MEB — e-Okul diploma notu bilgileri", "url": "https://www.meb.gov.tr/"},
    ],
    "ilgili": ["tyt-net-hesaplama", "ayt-net-hesaplama", "gano-hesaplama"],
}
