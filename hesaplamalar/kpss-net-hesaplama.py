# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kpss-net-hesaplama",
    "baslik": "KPSS Net Hesaplama",
    "h1": "KPSS Net Hesaplama 2026 — Lisans, Ön Lisans, Ortaöğretim ve Eğitim Bilimleri",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "KPSS net hesaplama: Genel Yetenek ve Genel Kültür testlerinde doğru-yanlışa göre netler, ağırlıklı standart puan mantığı ve KPSSP3/P93/P94 puan türlerinin bileşimi. 4 yanlış 1 doğruyu götürür.",
    "kisa_cevap": "KPSS neti = doğru − (yanlış ÷ 4). Lisans düzeyinde Genel Yetenek 60, Genel Kültür 60 olmak üzere 120 soru vardır; KPSSP3 puanı Genel Yetenek ve Genel Kültür ağırlıklı standart puanlarının %50-%50 birleşimiyle hesaplanır. Puanın oluşması için her iki testten de en az 1 net gerekir.",
    "senaryolar": [
        {"ad": "Ortalama (70 net)", "degerler": {"duzey": "lisans", "gy_d": "38", "gy_y": "12", "gk_d": "40", "gk_y": "10", "eb_d": "0", "eb_y": "0"}},
        {"ad": "İyi (90 net)", "degerler": {"duzey": "lisans", "gy_d": "48", "gy_y": "8", "gk_d": "48", "gk_y": "8", "eb_d": "0", "eb_y": "0"}},
        {"ad": "Çok iyi (105 net)", "degerler": {"duzey": "lisans", "gy_d": "55", "gy_y": "4", "gk_d": "54", "gk_y": "4", "eb_d": "0", "eb_y": "0"}},
        {"ad": "Öğretmen adayı (+EB)", "degerler": {"duzey": "lisans", "gy_d": "45", "gy_y": "10", "gk_d": "45", "gk_y": "10", "eb_d": "55", "eb_y": "15"}},
        {"ad": "Ön lisans", "degerler": {"duzey": "onlisans", "gy_d": "40", "gy_y": "10", "gk_d": "40", "gk_y": "10", "eb_d": "0", "eb_y": "0"}},
    ],
    "girdiler": [
        {"id": "duzey", "etiket": "Öğrenim düzeyi", "tip": "secim", "varsayilan": "lisans", "genis": True,
         "secenekler": [["lisans", "Lisans (KPSSP1/P2/P3) — 60+60 soru"], ["onlisans", "Ön lisans (KPSSP93) — 60+60 soru"], ["ortaogretim", "Ortaöğretim (KPSSP94) — 60+60 soru"]]},
        {"id": "gy_d", "etiket": "Genel Yetenek doğru", "tip": "tamsayi", "varsayilan": "40", "ipucu": "60 soru"},
        {"id": "gy_y", "etiket": "Genel Yetenek yanlış", "tip": "tamsayi", "varsayilan": "12"},
        {"id": "gk_d", "etiket": "Genel Kültür doğru", "tip": "tamsayi", "varsayilan": "42", "ipucu": "60 soru"},
        {"id": "gk_y", "etiket": "Genel Kültür yanlış", "tip": "tamsayi", "varsayilan": "10"},
        {"id": "eb_d", "etiket": "Eğitim Bilimleri doğru (öğretmen adayları)", "tip": "tamsayi", "varsayilan": "0", "ipucu": "80 soru · yoksa 0", "gizli": "duzey=lisans"},
        {"id": "eb_y", "etiket": "Eğitim Bilimleri yanlış", "tip": "tamsayi", "varsayilan": "0", "gizli": "duzey=lisans"},
    ],
    "js": r"""
function hesapla(g){
  var testler = [['Genel Yetenek','gy',60], ['Genel Kültür','gk',60]];
  if (g.duzey === 'lisans' && ((g.eb_d > 0) || (g.eb_y > 0))) testler.push(['Eğitim Bilimleri','eb',80]);
  var s = [], adlar = [], netler = [], top = 0, tD = 0, tY = 0, tSoru = 0, gyNet = 0, gkNet = 0;
  for (var i = 0; i < testler.length; i++) {
    var ad = testler[i][0], k = testler[i][1], soru = testler[i][2];
    var d = g[k + '_d'] > 0 ? g[k + '_d'] : 0, y = g[k + '_y'] > 0 ? g[k + '_y'] : 0;
    if (d + y > soru) return {hata: ad + ': doğru + yanlış toplamı ' + soru + ' soruyu aşamaz.'};
    var net = d - y / 4;
    if (k === 'gy') gyNet = net; if (k === 'gk') gkNet = net;
    top += net; tD += d; tY += y; tSoru += soru;
    adlar.push(ad.split(' ')[1] || ad); netler.push(Math.round(net * 100) / 100);
    s.push({etiket: ad + ' neti (' + soru + ' soru)', deger: net});
  }
  var pt = {lisans: 'KPSSP1 / P2 / P3', onlisans: 'KPSSP93', ortaogretim: 'KPSSP94'}[g.duzey];
  s.unshift({etiket: 'Toplam net (' + tSoru + ' soru)', deger: top, vurgu: true});
  s.push({etiket: 'GY + GK toplam neti (120 soru)', deger: gyNet + gkNet});
  s.push({etiket: 'Puan türü', deger: pt});
  s.push({etiket: 'Toplam doğru / yanlış / boş', deger: tD + ' / ' + tY + ' / ' + (tSoru - tD - tY)});
  s.push({etiket: 'Yanlışların götürdüğü net', deger: tY / 4});
  s.push({etiket: 'Puan koşulu (her testten en az 1 net)', deger: (gyNet >= 1 && gkNet >= 1) ? 'Sağlanıyor ✓' : 'SAĞLANMIYOR — puanınız hesaplanmaz'});
  var n = ['Net = doğru − yanlış ÷ 4 (4 yanlış 1 doğruyu götürür).',
           'KPSSP3 (ve benzeri temel puan türleri) Genel Yetenek ağırlıklı standart puanının %50\'si ile Genel Kültür ağırlıklı standart puanının %50\'sinin toplamıdır. Diğer puan türlerinde (P1, P2, alan sınavlı türler) ağırlıklar değişir.',
           'Ağırlıklı standart puanın 100\'lük KPSS puanına dönüşümü ÖSYM formülüyle yapılır: KPSS Puanı = 70 + 30 × [2(ASP − X) − S] ÷ [2(B − X) − S]; buradaki X (ortalama), S (standart sapma) ve B (en yüksek ASP) değerleri sınavdan sonra açıklandığı için netten kesin puan önceden hesaplanamaz.'];
  if (g.duzey === 'lisans' && (g.eb_d > 0 || g.eb_y > 0)) n.push('Eğitim Bilimleri testi öğretmen adayları içindir ve KPSSP10 gibi öğretmenlik puan türlerinde kullanılır; P3 hesabına girmez.');
  return {sonuclar: s, notlar: n,
    grafik: {tur: 'sutun', baslik: 'Test bazında netleriniz', etiketler: adlar, seriler: [{ad: 'Net', veri: netler}]}};
}
""",
    "nasil": [
        "Kamu Personel Seçme Sınavı'nda (KPSS) her düzeyde Genel Yetenek 60 ve Genel Kültür 60 olmak üzere 120 soru sorulur. Genel Yetenek testi Türkçe ve Matematik, Genel Kültür testi Tarih, Coğrafya, Vatandaşlık ve Güncel Bilgiler alt başlıklarından oluşur. Öğretmen adayları ayrıca 80 soruluk Eğitim Bilimleri testine girer. Net, doğru sayısından yanlışın dörtte biri çıkarılarak bulunur.",
        "Netler doğrudan puan değildir. ÖSYM önce her testin ham puanlarını, o yılki adayların ortalaması ve standart sapmasıyla standart puana çevirir. Ardından puan türüne göre ağırlıklandırır: KPSSP3'te Genel Yetenek %50, Genel Kültür %50 ağırlığa sahiptir. Elde edilen ağırlıklı standart puan (ASP), KPSS Puanı = 70 + 30 × [2(ASP − X) − S] ÷ [2(B − X) − S] formülüyle 100'lük ölçeğe taşınır.",
        "Bu formüldeki X (ASP ortalaması), S (standart sapma) ve B (en yüksek ASP) değerleri ancak sınavdan sonra belli olur; dolayısıyla sınav öncesinde hiçbir araç netten kesin KPSS puanı hesaplayamaz. Puanınızın oluşabilmesi için Genel Yetenek ve Genel Kültür testlerinin her birinden en az 1 net yapmanız gerekir.",
    ],
    "formul": [
        "Test neti = doğru − (yanlış ÷ 4)",
        "KPSSP3 ASP = 0,50 × Genel Yetenek ASP + 0,50 × Genel Kültür ASP",
        "KPSS Puanı = 70 + 30 × [2(ASP − X) − S] ÷ [2(B − X) − S]",
        "X: ASP ortalaması · S: standart sapma · B: en yüksek ASP (sınav sonrası ÖSYM açıklar)",
    ],
    "ornekler": [
        {"baslik": "Genel Yetenek 40 doğru 12 yanlış", "adimlar": ["Net = 40 − 12/4 = 40 − 3 = 37"]},
        {"baslik": "GY 45D 10Y, GK 45D 10Y", "adimlar": ["GY net 42,5 · GK net 42,5", "Toplam 85 net (120 soruda)"]},
    ],
    "tablo": {
        "baslik": "KPSS test yapısı ve puan türleri",
        "basliklar": ["Düzey", "Genel Yetenek", "Genel Kültür", "Ek test", "Temel puan türü"],
        "satirlar": [["Lisans", "60", "60", "Eğitim Bilimleri 80 (öğretmenlik) / Alan sınavı (A grubu)", "KPSSP1, P2, P3"], ["Ön lisans", "60", "60", "—", "KPSSP93"], ["Ortaöğretim", "60", "60", "—", "KPSSP94"]],
        "not": "Alan bilgisi sınavları (A grubu kadrolar) ve ÖABT ayrı puan türlerinde kullanılır. Kaynak: ÖSYM KPSS kılavuzu.",
    },
    "sss": [
        {"soru": "KPSS'de kaç yanlış 1 doğruyu götürür?", "cevap": "4 yanlış 1 doğruyu götürür: net = doğru − yanlış/4."},
        {"soru": "KPSS kaç sorudan oluşur?", "cevap": "Genel Yetenek 60 + Genel Kültür 60 = 120 soru. Öğretmen adayları için ayrıca 80 soruluk Eğitim Bilimleri testi vardır."},
        {"soru": "KPSSP3 nasıl hesaplanır?", "cevap": "Genel Yetenek ve Genel Kültür ağırlıklı standart puanlarının %50-%50 birleşimidir. Ham netler ÖSYM istatistikleriyle standart puana çevrildikten sonra hesaplanır."},
        {"soru": "Kaç net kaç puan yapar?", "cevap": "Kesin karşılığı yoktur; o yılki aday ortalaması, standart sapması ve en yüksek puana bağlıdır. Yayınlanan net-puan tabloları geçmiş yıl tahminidir."},
        {"soru": "Atanmak için kaç puan gerekir?", "cevap": "Kadro ve yıla göre değişir; taban puanlar tercih döneminde ÖSYM ve kurum kılavuzlarında ilan edilir. Puanınız 2 yıl geçerlidir."},
    ],
    "kaynaklar": [
        {"ad": "ÖSYM — KPSS kılavuzları ve puan hesaplama esasları", "url": "https://www.osym.gov.tr/"},
    ],
    "ilgili": ["tyt-net-hesaplama", "gano-hesaplama", "ortalama-hesaplama"],
}
