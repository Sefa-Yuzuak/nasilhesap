# -*- coding: utf-8 -*-
HESAP = {
    "slug": "lgs-net-hesaplama",
    "baslik": "LGS Net Hesaplama",
    "h1": "LGS Net Hesaplama 2026 — 90 Soruda Netini ve Ağırlıklı Katkını Gör",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "LGS net hesaplama: Türkçe, Matematik, Fen, İnkılap Tarihi, Din Kültürü ve Yabancı Dil derslerinde doğru-yanlışa göre netler, ders katsayılarıyla ağırlıklı katkı ve toplam net. LGS'de 3 yanlış 1 doğruyu götürür.",
    "kisa_cevap": "LGS'de net = doğru − (yanlış ÷ 3); yani 3 yanlış 1 doğruyu götürür (YKS'den farklı). Sınav 90 sorudur: sözel bölümde Türkçe 20, İnkılap Tarihi 10, Din Kültürü 10, Yabancı Dil 10; sayısal bölümde Matematik 20, Fen Bilimleri 20. Merkezi Sınav Puanı hesaplanırken Türkçe, Matematik ve Fen 4; diğer üç ders 1 katsayıyla ağırlıklandırılır.",
    "senaryolar": [
        {"ad": "Orta (60 net)", "degerler": {"tur_d": "14", "tur_y": "4", "mat_d": "12", "mat_y": "5", "fen_d": "14", "fen_y": "4", "ink_d": "7", "ink_y": "2", "din_d": "8", "din_y": "1", "ydl_d": "7", "ydl_y": "2"}},
        {"ad": "İyi (75 net)", "degerler": {"tur_d": "18", "tur_y": "2", "mat_d": "16", "mat_y": "3", "fen_d": "18", "fen_y": "2", "ink_d": "9", "ink_y": "1", "din_d": "9", "din_y": "1", "ydl_d": "9", "ydl_y": "1"}},
        {"ad": "Çok iyi (85+ net)", "degerler": {"tur_d": "20", "tur_y": "0", "mat_d": "19", "mat_y": "1", "fen_d": "19", "fen_y": "1", "ink_d": "10", "ink_y": "0", "din_d": "10", "din_y": "0", "ydl_d": "9", "ydl_y": "1"}},
        {"ad": "Sayısalı güçlü", "degerler": {"tur_d": "13", "tur_y": "5", "mat_d": "19", "mat_y": "1", "fen_d": "19", "fen_y": "1", "ink_d": "6", "ink_y": "3", "din_d": "7", "din_y": "2", "ydl_d": "6", "ydl_y": "3"}},
    ],
    "girdiler": [
        {"id": "tur_d", "etiket": "Türkçe doğru", "tip": "tamsayi", "varsayilan": "16", "ipucu": "20 soru · katsayı 4"},
        {"id": "tur_y", "etiket": "Türkçe yanlış", "tip": "tamsayi", "varsayilan": "3"},
        {"id": "mat_d", "etiket": "Matematik doğru", "tip": "tamsayi", "varsayilan": "14", "ipucu": "20 soru · katsayı 4"},
        {"id": "mat_y", "etiket": "Matematik yanlış", "tip": "tamsayi", "varsayilan": "4"},
        {"id": "fen_d", "etiket": "Fen Bilimleri doğru", "tip": "tamsayi", "varsayilan": "16", "ipucu": "20 soru · katsayı 4"},
        {"id": "fen_y", "etiket": "Fen Bilimleri yanlış", "tip": "tamsayi", "varsayilan": "3"},
        {"id": "ink_d", "etiket": "İnkılap Tarihi doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "10 soru · katsayı 1"},
        {"id": "ink_y", "etiket": "İnkılap Tarihi yanlış", "tip": "tamsayi", "varsayilan": "2"},
        {"id": "din_d", "etiket": "Din Kültürü doğru", "tip": "tamsayi", "varsayilan": "9", "ipucu": "10 soru · katsayı 1"},
        {"id": "din_y", "etiket": "Din Kültürü yanlış", "tip": "tamsayi", "varsayilan": "1"},
        {"id": "ydl_d", "etiket": "Yabancı Dil doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "10 soru · katsayı 1"},
        {"id": "ydl_y", "etiket": "Yabancı Dil yanlış", "tip": "tamsayi", "varsayilan": "2"},
    ],
    "js": r"""
function hesapla(g){
  var D = [['Türkçe','tur',20,4], ['Matematik','mat',20,4], ['Fen Bilimleri','fen',20,4],
           ['İnkılap Tarihi','ink',10,1], ['Din Kültürü','din',10,1], ['Yabancı Dil','ydl',10,1]];
  var s = [], sat = [], adlar = [], agirlikli = [], topNet = 0, topD = 0, topY = 0, topSoru = 0, topAg = 0;
  var sozelNet = 0, sayisalNet = 0;
  for (var i = 0; i < D.length; i++) {
    var ad = D[i][0], k = D[i][1], soru = D[i][2], kat = D[i][3];
    var d = g[k + '_d'] > 0 ? g[k + '_d'] : 0, y = g[k + '_y'] > 0 ? g[k + '_y'] : 0;
    if (d + y > soru) return {hata: ad + ': doğru + yanlış toplamı ' + soru + ' soruyu aşamaz.'};
    var net = d - y / 3, ag = net * kat;
    topNet += net; topD += d; topY += y; topSoru += soru; topAg += ag;
    if (k === 'mat' || k === 'fen') sayisalNet += net; else sozelNet += net;
    adlar.push(ad.split(' ')[0].slice(0, 9)); agirlikli.push(Math.round(ag * 100) / 100);
    sat.push([ad, d, y, soru - d - y, Math.round(net * 100) / 100, kat, Math.round(ag * 100) / 100]);
    s.push({etiket: ad + ' neti (' + soru + ' soru)', deger: net});
  }
  s.unshift({etiket: 'Toplam LGS neti (90 soru)', deger: topNet, vurgu: true});
  s.push({etiket: 'Ağırlıklı net toplamı (katsayılı)', deger: topAg});
  s.push({etiket: 'Sözel bölüm neti (Türkçe, İnkılap, Din, Dil — 50 soru)', deger: sozelNet});
  s.push({etiket: 'Sayısal bölüm neti (Matematik, Fen — 40 soru)', deger: sayisalNet});
  s.push({etiket: 'Toplam doğru / yanlış / boş', deger: topD + ' / ' + topY + ' / ' + (topSoru - topD - topY)});
  s.push({etiket: 'Yanlışların götürdüğü net', deger: topY / 3});
  return {sonuclar: s,
    tablo: {basliklar: ['Ders', 'D', 'Y', 'Boş', 'Net', 'Katsayı', 'Ağırlıklı'], satirlar: sat},
    grafik: {tur: 'sutun', baslik: 'Derslerin ağırlıklı katkısı (net × katsayı)', etiketler: adlar, seriler: [{ad: 'Ağırlıklı net', veri: agirlikli}]},
    notlar: ['LGS\'de net = doğru − yanlış ÷ 3 (3 yanlış 1 doğruyu götürür). YKS\'deki 4 yanlış kuralıyla karıştırmayın.',
             'Merkezi Sınav Puanı (MSP) hesaplanırken netler önce ortalaması 50, standart sapması 10 olan standart puanlara çevrilir, sonra Türkçe/Matematik/Fen için 4, İnkılap/Din/Yabancı Dil için 1 katsayıyla ağırlıklandırılıp 100–500 aralığına ölçeklenir.',
             'Bu dönüşüm MEB\'in sınav sonrası açıkladığı ortalama ve standart sapma değerlerine dayandığı için sınavdan önce netten kesin puan hesaplanamaz; buradaki "ağırlıklı net" karşılaştırma amaçlıdır.']};
}
""",
    "nasil": [
        "Liselere Geçiş Sınavı (LGS) merkezi sınavı 90 sorudan oluşur ve iki oturumda yapılır. Sözel bölümde Türkçe 20, T.C. İnkılap Tarihi ve Atatürkçülük 10, Din Kültürü ve Ahlak Bilgisi 10, Yabancı Dil 10 soru; sayısal bölümde Matematik 20 ve Fen Bilimleri 20 soru bulunur.",
        "LGS'de net hesabı YKS'den farklıdır: doğru sayısından yanlış sayısının **üçte biri** çıkarılır, yani 3 yanlış 1 doğruyu götürür. Boş bırakılan sorular neti etkilemez. Bu fark nedeniyle LGS'de tahmin yapmanın maliyeti YKS'ye göre daha yüksektir.",
        "Merkezi Sınav Puanı (MSP) hesaplanırken netler doğrudan toplanmaz. Her ders için netler, o yıl sınava giren tüm öğrencilerin ortalaması 50 ve standart sapması 10 olacak şekilde standart puana dönüştürülür; ardından Türkçe, Matematik ve Fen Bilimleri 4, İnkılap Tarihi, Din Kültürü ve Yabancı Dil 1 katsayısıyla çarpılır. Ağırlıklı standart puanlar toplanıp 100–500 aralığına ölçeklenir. Bu istatistikler sınavdan sonra açıklandığından, sınav öncesinde netten kesin puan hesaplanamaz.",
    ],
    "formul": [
        "Ders neti = doğru − (yanlış ÷ 3)",
        "Ağırlıklı net = ders neti × katsayı (Türkçe/Mat/Fen = 4 · İnkılap/Din/Dil = 1)",
        "MSP: netler → standart puan (ort. 50, s.s. 10) → katsayıyla çarpım → toplam → 100–500 ölçeklemesi",
        "Toplam ağırlık payı: sayısal ve Türkçe ağırlıklı derslerin toplam katsayısı 12, diğerlerinin 3",
    ],
    "ornekler": [
        {"baslik": "Matematik 14 doğru 4 yanlış", "adimlar": ["Net = 14 − 4/3 = 14 − 1,33 = 12,67", "Ağırlıklı katkı = 12,67 × 4 = 50,68"]},
        {"baslik": "Toplam 71 doğru 15 yanlış", "adimlar": ["Toplam net = 71 − 15/3 = 71 − 5 = 66", "15 yanlış 5 net götürdü"]},
    ],
    "tablo": {
        "baslik": "LGS test yapısı ve katsayılar",
        "basliklar": ["Ders", "Soru", "Bölüm", "Katsayı"],
        "satirlar": [["Türkçe", "20", "Sözel", "4"], ["T.C. İnkılap Tarihi ve Atatürkçülük", "10", "Sözel", "1"], ["Din Kültürü ve Ahlak Bilgisi", "10", "Sözel", "1"], ["Yabancı Dil", "10", "Sözel", "1"], ["Matematik", "20", "Sayısal", "4"], ["Fen Bilimleri", "20", "Sayısal", "4"], ["Toplam", "90", "—", "—"]],
        "not": "Kaynak: MEB Ortaöğretime Geçiş (LGS) kılavuzu ve merkezi sınav puanı hesaplama esasları.",
    },
    "sss": [
        {"soru": "LGS'de kaç yanlış 1 doğruyu götürür?", "cevap": "3 yanlış 1 doğruyu götürür. Net = doğru − yanlış/3. YKS'deki 4 yanlış kuralıyla karıştırılmamalıdır."},
        {"soru": "LGS kaç sorudan oluşur?", "cevap": "90 soru: sözel bölümde Türkçe 20, İnkılap 10, Din 10, Yabancı Dil 10; sayısal bölümde Matematik 20, Fen 20."},
        {"soru": "Hangi dersler daha önemli?", "cevap": "Türkçe, Matematik ve Fen Bilimleri 4 katsayıyla, diğer üç ders 1 katsayıyla değerlendirilir; bu üç dersin puana etkisi çok daha yüksektir."},
        {"soru": "LGS'de kaç net kaç puan yapar?", "cevap": "Kesin karşılığı yoktur; MSP, o yılki öğrenci istatistikleriyle standart puana çevrilerek hesaplanır. Aynı net farklı yıllarda farklı puan ve yüzdelik dilim verir."},
        {"soru": "Boş bırakmak mı yanlış yapmak mı?", "cevap": "Boş nete etki etmez; 3 yanlış 1 doğru götürdüğü için eleme yapamadığınız soruyu boş bırakmak daha güvenlidir."},
    ],
    "kaynaklar": [
        {"ad": "MEB — Ortaöğretime Geçiş (LGS) kılavuzu ve merkezi sınav esasları", "url": "https://www.meb.gov.tr/"},
        {"ad": "MEB Ölçme, Değerlendirme ve Sınav Hizmetleri Genel Müdürlüğü", "url": "https://odsgm.meb.gov.tr/"},
    ],
    "ilgili": ["tyt-net-hesaplama", "vize-final-hesaplama", "yuzde-hesaplama"],
}
