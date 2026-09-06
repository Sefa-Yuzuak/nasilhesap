# -*- coding: utf-8 -*-
HESAP = {
    "slug": "ayt-net-hesaplama",
    "baslik": "AYT Net Hesaplama",
    "h1": "AYT Net Hesaplama 2026 — Sayısal, Eşit Ağırlık, Sözel ve Dil",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "AYT net hesaplama: alanınıza göre (Sayısal, Eşit Ağırlık, Sözel, Dil) Matematik, Fizik, Kimya, Biyoloji, Edebiyat, Tarih, Coğrafya, Felsefe ve Din netleri; toplam net ve baraj bilgisi. 4 yanlış 1 doğruyu götürür.",
    "kisa_cevap": "AYT neti = doğru − (yanlış ÷ 4). AYT'de Matematik 40, Fen Bilimleri 40 (Fizik 14, Kimya 13, Biyoloji 13), Türk Dili ve Edebiyatı–Sosyal Bilimler-1 40 (Edebiyat 24, Tarih-1 10, Coğrafya-1 6) ve Sosyal Bilimler-2 40 (Tarih-2 11, Coğrafya-2 11, Felsefe 12, Din 6) soru vardır; alanınıza göre yalnızca ilgili testler değerlendirilir.",
    "senaryolar": [
        {"ad": "Sayısal — orta", "degerler": {"alan": "say", "mat_d": "20", "mat_y": "8", "fiz_d": "7", "fiz_y": "3", "kim_d": "7", "kim_y": "3", "biy_d": "7", "biy_y": "3"}},
        {"ad": "Sayısal — iyi", "degerler": {"alan": "say", "mat_d": "34", "mat_y": "3", "fiz_d": "12", "fiz_y": "1", "kim_d": "11", "kim_y": "1", "biy_d": "12", "biy_y": "1"}},
        {"ad": "Eşit ağırlık — iyi", "degerler": {"alan": "ea", "mat_d": "30", "mat_y": "5", "ede_d": "20", "ede_y": "2", "tar1_d": "8", "tar1_y": "1", "cog1_d": "5", "cog1_y": "1"}},
        {"ad": "Sözel — iyi", "degerler": {"alan": "soz", "ede_d": "21", "ede_y": "2", "tar1_d": "9", "tar1_y": "1", "cog1_d": "5", "cog1_y": "1", "tar2_d": "9", "tar2_y": "1", "cog2_d": "9", "cog2_y": "1", "fel_d": "10", "fel_y": "1", "din_d": "5", "din_y": "1"}},
    ],
    "girdiler": [
        {"id": "alan", "etiket": "Alanınız", "tip": "secim", "varsayilan": "say", "genis": True,
         "secenekler": [["say", "Sayısal (SAY)"], ["ea", "Eşit Ağırlık (EA)"], ["soz", "Sözel (SÖZ)"], ["dil", "Yabancı Dil (DİL / YDT)"]]},
        {"id": "mat_d", "etiket": "Matematik doğru", "tip": "tamsayi", "varsayilan": "25", "ipucu": "40 soru", "gizli": "alan=say,ea"},
        {"id": "mat_y", "etiket": "Matematik yanlış", "tip": "tamsayi", "varsayilan": "6", "gizli": "alan=say,ea"},
        {"id": "fiz_d", "etiket": "Fizik doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "14 soru", "gizli": "alan=say"},
        {"id": "fiz_y", "etiket": "Fizik yanlış", "tip": "tamsayi", "varsayilan": "3", "gizli": "alan=say"},
        {"id": "kim_d", "etiket": "Kimya doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "13 soru", "gizli": "alan=say"},
        {"id": "kim_y", "etiket": "Kimya yanlış", "tip": "tamsayi", "varsayilan": "3", "gizli": "alan=say"},
        {"id": "biy_d", "etiket": "Biyoloji doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "13 soru", "gizli": "alan=say"},
        {"id": "biy_y", "etiket": "Biyoloji yanlış", "tip": "tamsayi", "varsayilan": "3", "gizli": "alan=say"},
        {"id": "ede_d", "etiket": "Türk Dili ve Edebiyatı doğru", "tip": "tamsayi", "varsayilan": "16", "ipucu": "24 soru", "gizli": "alan=ea,soz"},
        {"id": "ede_y", "etiket": "Edebiyat yanlış", "tip": "tamsayi", "varsayilan": "4", "gizli": "alan=ea,soz"},
        {"id": "tar1_d", "etiket": "Tarih-1 doğru", "tip": "tamsayi", "varsayilan": "6", "ipucu": "10 soru", "gizli": "alan=ea,soz"},
        {"id": "tar1_y", "etiket": "Tarih-1 yanlış", "tip": "tamsayi", "varsayilan": "2", "gizli": "alan=ea,soz"},
        {"id": "cog1_d", "etiket": "Coğrafya-1 doğru", "tip": "tamsayi", "varsayilan": "4", "ipucu": "6 soru", "gizli": "alan=ea,soz"},
        {"id": "cog1_y", "etiket": "Coğrafya-1 yanlış", "tip": "tamsayi", "varsayilan": "1", "gizli": "alan=ea,soz"},
        {"id": "tar2_d", "etiket": "Tarih-2 doğru", "tip": "tamsayi", "varsayilan": "7", "ipucu": "11 soru", "gizli": "alan=soz"},
        {"id": "tar2_y", "etiket": "Tarih-2 yanlış", "tip": "tamsayi", "varsayilan": "2", "gizli": "alan=soz"},
        {"id": "cog2_d", "etiket": "Coğrafya-2 doğru", "tip": "tamsayi", "varsayilan": "7", "ipucu": "11 soru", "gizli": "alan=soz"},
        {"id": "cog2_y", "etiket": "Coğrafya-2 yanlış", "tip": "tamsayi", "varsayilan": "2", "gizli": "alan=soz"},
        {"id": "fel_d", "etiket": "Felsefe Grubu doğru", "tip": "tamsayi", "varsayilan": "8", "ipucu": "12 soru", "gizli": "alan=soz"},
        {"id": "fel_y", "etiket": "Felsefe Grubu yanlış", "tip": "tamsayi", "varsayilan": "2", "gizli": "alan=soz"},
        {"id": "din_d", "etiket": "Din Kültürü doğru", "tip": "tamsayi", "varsayilan": "4", "ipucu": "6 soru", "gizli": "alan=soz"},
        {"id": "din_y", "etiket": "Din Kültürü yanlış", "tip": "tamsayi", "varsayilan": "1", "gizli": "alan=soz"},
        {"id": "ydt_d", "etiket": "YDT doğru", "tip": "tamsayi", "varsayilan": "50", "ipucu": "80 soru", "gizli": "alan=dil"},
        {"id": "ydt_y", "etiket": "YDT yanlış", "tip": "tamsayi", "varsayilan": "12", "gizli": "alan=dil"},
    ],
    "js": r"""
var DERS = {
  say: [['Matematik','mat',40], ['Fizik','fiz',14], ['Kimya','kim',13], ['Biyoloji','biy',13]],
  ea:  [['Matematik','mat',40], ['Türk Dili ve Edebiyatı','ede',24], ['Tarih-1','tar1',10], ['Coğrafya-1','cog1',6]],
  soz: [['Türk Dili ve Edebiyatı','ede',24], ['Tarih-1','tar1',10], ['Coğrafya-1','cog1',6], ['Tarih-2','tar2',11], ['Coğrafya-2','cog2',11], ['Felsefe Grubu','fel',12], ['Din Kültürü','din',6]],
  dil: [['Yabancı Dil (YDT)','ydt',80]]
};
function hesapla(g){
  var liste = DERS[g.alan] || DERS.say, s = [], netler = [], adlar = [], top = 0, tD = 0, tY = 0, tSoru = 0;
  for (var i = 0; i < liste.length; i++) {
    var ad = liste[i][0], k = liste[i][1], soru = liste[i][2];
    var d = g[k + '_d'] > 0 ? g[k + '_d'] : 0, y = g[k + '_y'] > 0 ? g[k + '_y'] : 0;
    if (d + y > soru) return {hata: ad + ': doğru + yanlış toplamı ' + soru + ' soruyu aşamaz.'};
    var net = d - y / 4;
    top += net; tD += d; tY += y; tSoru += soru;
    netler.push(Math.round(net * 100) / 100); adlar.push(ad.split(' ')[0].slice(0, 9));
    s.push({etiket: ad + ' neti (' + soru + ' soru)', deger: net});
  }
  var adAlan = {say: 'Sayısal', ea: 'Eşit Ağırlık', soz: 'Sözel', dil: 'Dil'}[g.alan];
  s.unshift({etiket: adAlan + ' toplam AYT neti (' + tSoru + ' soru)', deger: top, vurgu: true});
  s.push({etiket: 'Toplam doğru / yanlış / boş', deger: tD + ' / ' + tY + ' / ' + (tSoru - tD - tY)});
  s.push({etiket: 'Yanlışların götürdüğü net', deger: tY / 4});
  var n = ['Net = doğru − yanlış ÷ 4. AYT\'de puan hesaplanabilmesi için ilgili testlerden en az 0,5 ham puan koşulu aranır.',
           'Yerleştirme puanı = TYT × 0,40 + AYT × 0,60 + OBP × 0,12. Netlerin puana dönüşümü ÖSYM\'nin sınav sonrası açıkladığı ortalama ve standart sapmayla yapılır; bu yüzden sınavdan önce kesin puan hesaplanamaz.'];
  if (g.alan === 'soz') n.push('Sözel adaylar Sosyal Bilimler-2 testinin tamamını (40 soru) çözer; Felsefe Grubu 12 sorunun 6\'sı felsefe, 6\'sı psikoloji-sosyoloji-mantık konularındandır.');
  if (g.alan === 'dil') n.push('DİL puanı YDT ve TYT\'den oluşur; AYT testleri kullanılmaz.');
  return {sonuclar: s, notlar: n,
    grafik: {tur: 'sutun', baslik: adAlan + ' — ders bazında netleriniz', etiketler: adlar, seriler: [{ad: 'Net', veri: netler}]}};
}
""",
    "nasil": [
        "Alan Yeterlilik Testleri (AYT) toplam 160 sorudan oluşur ve 180 dakika sürer: Matematik 40, Fen Bilimleri 40 (Fizik 14, Kimya 13, Biyoloji 13), Türk Dili ve Edebiyatı–Sosyal Bilimler-1 40 (Edebiyat 24, Tarih-1 10, Coğrafya-1 6) ve Sosyal Bilimler-2 40 (Tarih-2 11, Coğrafya-2 11, Felsefe Grubu 12, Din Kültürü 6). Aday tüm testleri çözmek zorunda değildir; puan türüne göre yalnızca ilgili testler değerlendirmeye alınır.",
        "Sayısal (SAY) puan türünde Matematik ve Fen Bilimleri; Eşit Ağırlık (EA) türünde Matematik ile Türk Dili ve Edebiyatı–Sosyal Bilimler-1; Sözel (SÖZ) türünde Edebiyat–Sosyal-1 ve Sosyal-2 testleri kullanılır. Yabancı dil bölümleri için AYT yerine 80 soruluk Yabancı Dil Testi (YDT) çözülür.",
        "Her testte net, doğru sayısından yanlışın dörtte biri çıkarılarak bulunur. Netler, ÖSYM'nin o yılki aday istatistikleriyle standart puana çevrilir; TYT %40, AYT %60 ağırlıkla birleştirilir ve OBP'nin 0,12 katsayılı katkısı eklenerek yerleştirme puanı oluşur.",
    ],
    "formul": [
        "Ders neti = doğru − (yanlış ÷ 4)",
        "AYT toplam net = alanınıza giren testlerin netleri toplamı",
        "Yerleştirme puanı = TYT puanı × 0,40 + AYT puanı × 0,60 + OBP × 0,12",
        "Önceki yıl yerleşenlerde OBP katsayısı 0,06'ya düşer",
    ],
    "ornekler": [
        {"baslik": "Sayısal: Mat 25D 6Y, Fizik 8D 3Y, Kimya 8D 3Y, Biyoloji 8D 3Y", "adimlar": ["Mat: 25 − 1,5 = 23,5", "Fizik: 8 − 0,75 = 7,25 · Kimya: 7,25 · Biyoloji: 7,25", "Toplam ≈ 45,25 net"]},
        {"baslik": "Eşit ağırlık: Mat 30D 5Y, Edebiyat 20D 2Y, Tarih-1 8D 1Y, Coğrafya-1 5D 1Y", "adimlar": ["28,75 + 19,5 + 7,75 + 4,75 = 60,75 net"]},
    ],
    "tablo": {
        "baslik": "AYT test yapısı ve puan türlerine göre kullanımı",
        "basliklar": ["Test", "Soru", "SAY", "EA", "SÖZ"],
        "satirlar": [["Matematik", "40", "✓", "✓", "—"], ["Fen Bilimleri (Fizik 14, Kimya 13, Biyoloji 13)", "40", "✓", "—", "—"], ["Türk Dili ve Edebiyatı–Sosyal Bilimler-1 (Edebiyat 24, Tarih-1 10, Coğrafya-1 6)", "40", "—", "✓", "✓"], ["Sosyal Bilimler-2 (Tarih-2 11, Coğrafya-2 11, Felsefe 12, Din 6)", "40", "—", "—", "✓"], ["Yabancı Dil Testi (YDT)", "80", "—", "—", "DİL"]],
        "not": "Ders içi soru sayıları yıllara göre ±1 değişebilir. Kaynak: ÖSYM YKS kılavuzu.",
    },
    "sss": [
        {"soru": "AYT'de kaç soru var?", "cevap": "Toplam 160 soru (4 test × 40). Alanınıza göre yalnızca 2-3 test değerlendirilir; sayısalcı 80, eşit ağırlıkçı 80, sözelci 80 soru çözer."},
        {"soru": "AYT neti nasıl hesaplanır?", "cevap": "Her testte doğru − yanlış/4. 4 yanlış 1 doğruyu götürür; boşlar etkilemez."},
        {"soru": "AYT'de baraj var mı?", "cevap": "AYT puanı için ilgili testlerden en az 0,5 ham puan gerekir; ayrıca TYT'de Türkçe veya Matematik'ten 0,5 net şartı vardır. Yerleştirmede programa göre 180 puan gibi barajlar uygulanır."},
        {"soru": "Sayısalcı sözel testleri de çözebilir mi?", "cevap": "Çözebilir ama SAY puanına katkısı olmaz; yalnızca ilgili testler hesaba katılır. Zaman kaybetmemek için alanınıza odaklanın."},
        {"soru": "TYT mi AYT mi daha önemli?", "cevap": "Yerleştirme puanında AYT %60, TYT %40 ağırlığa sahiptir; ancak TYT netleri hem doğrudan hem de sıralamada belirleyicidir. İkisi de kritiktir."},
    ],
    "kaynaklar": [
        {"ad": "ÖSYM — 2026 YKS Kılavuzu", "url": "https://www.osym.gov.tr/2026yuksekogretim-kurumlari-sinavi-yks-kilavuzu"},
        {"ad": "ÖSYM — YKS sonuç ve istatistikleri", "url": "https://www.osym.gov.tr/"},
    ],
    "ilgili": ["tyt-net-hesaplama", "obp-hesaplama", "gano-hesaplama"],
}
