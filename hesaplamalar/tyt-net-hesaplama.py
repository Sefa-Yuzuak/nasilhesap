# -*- coding: utf-8 -*-
HESAP = {
    "slug": "tyt-net-hesaplama",
    "baslik": "TYT Net Hesaplama",
    "h1": "TYT Net Hesaplama 2026 — Doğru Yanlış Gir, Netini Anında Gör",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "TYT net hesaplama: Türkçe, Sosyal Bilimler, Temel Matematik ve Fen Bilimleri testlerinde doğru-yanlış sayınıza göre ders netleri, toplam net, boş sayısı ve baraj kontrolü. 4 yanlış 1 doğruyu götürür.",
    "kisa_cevap": "TYT neti = doğru sayısı − (yanlış sayısı ÷ 4); yani 4 yanlış 1 doğruyu götürür, boşlar puanı etkilemez. TYT'de Türkçe 40, Sosyal Bilimler 20, Temel Matematik 40, Fen Bilimleri 20 olmak üzere 120 soru vardır. Puanınızın hesaplanması için Türkçe veya Temel Matematik testinden en az 0,5 net yapmanız gerekir.",
    "senaryolar": [
        {"ad": "Ortalama aday (60 net)", "degerler": {"tur_d": "24", "tur_y": "8", "sos_d": "10", "sos_y": "4", "mat_d": "16", "mat_y": "8", "fen_d": "8", "fen_y": "4"}},
        {"ad": "İyi aday (85 net)", "degerler": {"tur_d": "34", "tur_y": "4", "sos_d": "16", "sos_y": "2", "mat_d": "28", "mat_y": "4", "fen_d": "12", "fen_y": "3"}},
        {"ad": "Çok iyi (105 net)", "degerler": {"tur_d": "38", "tur_y": "2", "sos_d": "19", "sos_y": "1", "mat_d": "36", "mat_y": "2", "fen_d": "17", "fen_y": "2"}},
        {"ad": "Sadece sözelci", "degerler": {"tur_d": "36", "tur_y": "3", "sos_d": "18", "sos_y": "2", "mat_d": "8", "mat_y": "4", "fen_d": "3", "fen_y": "2"}},
    ],
    "girdiler": [
        {"id": "tur_d", "etiket": "Türkçe doğru", "tip": "tamsayi", "varsayilan": "30", "ipucu": "40 soru"},
        {"id": "tur_y", "etiket": "Türkçe yanlış", "tip": "tamsayi", "varsayilan": "6"},
        {"id": "sos_d", "etiket": "Sosyal Bilimler doğru", "tip": "tamsayi", "varsayilan": "14", "ipucu": "20 soru"},
        {"id": "sos_y", "etiket": "Sosyal Bilimler yanlış", "tip": "tamsayi", "varsayilan": "4"},
        {"id": "mat_d", "etiket": "Temel Matematik doğru", "tip": "tamsayi", "varsayilan": "20", "ipucu": "40 soru"},
        {"id": "mat_y", "etiket": "Temel Matematik yanlış", "tip": "tamsayi", "varsayilan": "8"},
        {"id": "fen_d", "etiket": "Fen Bilimleri doğru", "tip": "tamsayi", "varsayilan": "10", "ipucu": "20 soru"},
        {"id": "fen_y", "etiket": "Fen Bilimleri yanlış", "tip": "tamsayi", "varsayilan": "4"},
    ],
    "js": r"""
function hesapla(g){
  var T = [['Türkçe','tur',40], ['Sosyal Bilimler','sos',20], ['Temel Matematik','mat',40], ['Fen Bilimleri','fen',20]];
  var s = [], n = [], toplamNet = 0, toplamD = 0, toplamY = 0, toplamB = 0, netler = [], adlar = [];
  for (var i = 0; i < T.length; i++) {
    var ad = T[i][0], k = T[i][1], soru = T[i][2];
    var d = g[k + '_d'] > 0 ? g[k + '_d'] : 0, y = g[k + '_y'] > 0 ? g[k + '_y'] : 0;
    if (d + y > soru) return {hata: ad + ': doğru + yanlış toplamı ' + soru + ' soruyu aşamaz (' + (d + y) + ' girdiniz).'};
    var net = d - y / 4, bos = soru - d - y;
    toplamNet += net; toplamD += d; toplamY += y; toplamB += bos;
    netler.push(Math.round(net * 100) / 100); adlar.push(ad.split(' ')[0]);
    s.push({etiket: ad + ' neti (' + soru + ' soru)', deger: net});
  }
  var turNet = (g.tur_d > 0 ? g.tur_d : 0) - (g.tur_y > 0 ? g.tur_y : 0) / 4;
  var matNet = (g.mat_d > 0 ? g.mat_d : 0) - (g.mat_y > 0 ? g.mat_y : 0) / 4;
  var barajOk = turNet >= 0.5 || matNet >= 0.5;
  s.unshift({etiket: 'Toplam TYT neti (120 soru)', deger: toplamNet, vurgu: true});
  s.push({etiket: 'Toplam doğru / yanlış / boş', deger: toplamD + ' / ' + toplamY + ' / ' + toplamB});
  s.push({etiket: 'Yanlışların götürdüğü net', deger: toplamY / 4});
  s.push({etiket: 'Baraj (Türkçe veya Mat ≥ 0,5 net)', deger: barajOk ? 'Sağlanıyor ✓' : 'SAĞLANMIYOR — puanınız hesaplanmaz'});
  n.push('Net = doğru − yanlış ÷ 4. Boş bırakılan sorular neti etkilemez; emin olmadığınız 4 soruyu işaretlemek ortalama 1 net kaybettirir.');
  n.push('TYT puanı, netlerin ÖSYM tarafından sınav sonrası açıklanan ortalama ve standart sapma değerleriyle standart puana çevrilmesiyle bulunur; bu nedenle sınavdan önce net → puan dönüşümü kesin olarak hesaplanamaz (aşağıda ayrıntılı anlatıldı).');
  return {sonuclar: s, notlar: n,
    grafik: {tur: 'sutun', baslik: 'Ders bazında netleriniz', etiketler: adlar, seriler: [{ad: 'Net', veri: netler}]}};
}
""",
    "nasil": [
        "Temel Yeterlilik Testi (TYT) 120 sorudan oluşur: Türkçe 40, Sosyal Bilimler 20, Temel Matematik 40 ve Fen Bilimleri 20. Süre 165 dakikadır. Her testte net, doğru sayısından yanlış sayısının dörtte biri çıkarılarak bulunur — kısaca 4 yanlış 1 doğruyu götürür. Boş bırakılan sorular nete etki etmez, bu yüzden hiçbir fikriniz olmayan soruyu boş bırakmak istatistiksel olarak doğru stratejidir.",
        "Netler doğrudan puan değildir. ÖSYM her testin ham puanlarını, o yıl sınava giren tüm adayların ortalaması ve standart sapmasını kullanarak ortalaması 50, standart sapması 10 olan standart puanlara dönüştürür. Ardından bu standart puanlar test ağırlıklarıyla çarpılıp toplanır ve 100 taban puan eklenerek TYT puanı elde edilir. Bu istatistikler sınavdan sonra açıklandığı için, sınav öncesinde hiçbir araç netten kesin puan hesaplayamaz; 'net → puan' tabloları geçmiş yıllara dayalı tahmindir.",
        "Puanınızın hesaplanabilmesi için TYT'de Türkçe veya Temel Matematik testinin en az birinden 0,5 net yapmış olmanız gerekir. TYT puanı hem tek başına (2 yıllık ön lisans ve bazı programlar için) hem de AYT puan türlerinin %40'lık bileşeni olarak kullanılır.",
    ],
    "formul": [
        "Ders neti = doğru − (yanlış ÷ 4)",
        "Toplam TYT neti = Türkçe + Sosyal + Matematik + Fen netleri",
        "TYT ham puanı → standart puan → ağırlıklı toplam + 100 taban puan (ÖSYM istatistikleriyle)",
        "Yerleştirme: SAY/SÖZ/EA puanı = TYT × 0,40 + AYT × 0,60 + OBP × 0,12",
    ],
    "ornekler": [
        {"baslik": "Türkçe 30 doğru 6 yanlış", "adimlar": ["Net = 30 − 6/4 = 30 − 1,5 = 28,5", "Boş: 40 − 36 = 4 soru"]},
        {"baslik": "Tüm testler: 74D 22Y", "adimlar": ["Toplam net = 74 − 22/4 = 74 − 5,5 = 68,5", "22 yanlış toplam 5,5 net götürdü"]},
    ],
    "tablo": {
        "baslik": "TYT test yapısı (2026)",
        "basliklar": ["Test", "Soru", "Süre payı"],
        "satirlar": [["Türkçe", "40", "—"], ["Sosyal Bilimler (Tarih 5, Coğrafya 5, Felsefe 5, Din/Ek felsefe 5)", "20", "—"], ["Temel Matematik", "40", "—"], ["Fen Bilimleri (Fizik 7, Kimya 7, Biyoloji 6)", "20", "—"], ["Toplam", "120", "165 dakika"]],
        "not": "Ders içi soru dağılımları yıllara göre ±1-2 değişebilir; toplam test soru sayıları sabittir. Kaynak: ÖSYM YKS kılavuzu.",
    },
    "sss": [
        {"soru": "TYT'de kaç yanlış 1 doğruyu götürür?", "cevap": "4 yanlış 1 doğruyu götürür. Net = doğru − yanlış/4 formülüyle hesaplanır; bu kural TYT, AYT, YDT, KPSS ve DGS'de aynıdır (LGS'de 3 yanlış 1 doğruyu götürür)."},
        {"soru": "Boş bırakmak net kaybettirir mi?", "cevap": "Hayır, boşlar nete etki etmez. 4 soruyu rastgele işaretlerseniz ortalama 1 doğru 3 yanlış beklenir ve net değişmez; ancak eleme yapabildiğiniz sorularda işaretlemek avantajlıdır."},
        {"soru": "TYT'de kaç net kaç puan yapar?", "cevap": "Kesin bir karşılık yoktur. Puan, o yılki adayların ortalama ve standart sapmasına göre hesaplanır. Aynı net farklı yıllarda farklı puan getirir; yayınlanan net-puan tabloları geçmiş yıl tahminidir."},
        {"soru": "TYT barajı kaç net?", "cevap": "Sayı olarak baraj yoktur; Türkçe veya Temel Matematik testlerinden en az 0,5 net yapmanız gerekir. Ayrıca yerleştirme için programa göre 150/180 gibi puan barajları uygulanır."},
        {"soru": "TYT puanı tek başına yeterli mi?", "cevap": "2 yıllık ön lisans programları ve bazı açıköğretim programları için TYT puanı yeterlidir. 4 yıllık lisans programları için AYT (veya YDT) puanı da gerekir."},
    ],
    "kaynaklar": [
        {"ad": "ÖSYM — 2026 Yükseköğretim Kurumları Sınavı (YKS) Kılavuzu", "url": "https://www.osym.gov.tr/2026yuksekogretim-kurumlari-sinavi-yks-kilavuzu"},
        {"ad": "ÖSYM — Ana sayfa ve sınav duyuruları", "url": "https://www.osym.gov.tr/"},
    ],
    "ilgili": ["ayt-net-hesaplama", "obp-hesaplama", "gano-hesaplama"],
}
