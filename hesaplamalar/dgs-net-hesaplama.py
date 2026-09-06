# -*- coding: utf-8 -*-
HESAP = {
    "slug": "dgs-net-hesaplama",
    "baslik": "DGS Net Hesaplama",
    "h1": "DGS Net Hesaplama 2026 — Sayısal ve Sözel Netleri, SAY/SÖZ/EA Puan Türleri",
    "kategori": "sinav-egitim",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "DGS net hesaplama: Sayısal ve Sözel bölümlerde doğru-yanlışa göre netler, toplam net, puan türlerinin (SAY, SÖZ, EA) bileşimi ve ÖBP katkısı. 4 yanlış 1 doğruyu götürür.",
    "kisa_cevap": "DGS neti = doğru − (yanlış ÷ 4). Sınav 100 sorudur: Sayısal 50, Sözel 50. Üç puan türü hesaplanır — SAY sayısal ağırlıklı, SÖZ sözel ağırlıklı, EA ikisinin dengeli bileşimidir. Puanınızın hesaplanabilmesi için her iki bölümden de en az 0,5 ham puan gerekir; ayrıca Ön Lisans Başarı Puanı (ÖBP) katkı olarak eklenir.",
    "senaryolar": [
        {"ad": "Orta (50 net)", "degerler": {"say_d": "28", "say_y": "12", "soz_d": "28", "soz_y": "12"}},
        {"ad": "İyi (70 net)", "degerler": {"say_d": "38", "say_y": "8", "soz_d": "38", "soz_y": "8"}},
        {"ad": "Sayısalcı", "degerler": {"say_d": "44", "say_y": "4", "soz_d": "25", "soz_y": "15"}},
        {"ad": "Sözelci", "degerler": {"say_d": "22", "say_y": "16", "soz_d": "45", "soz_y": "4"}},
    ],
    "girdiler": [
        {"id": "say_d", "etiket": "Sayısal doğru", "tip": "tamsayi", "varsayilan": "30", "ipucu": "50 soru"},
        {"id": "say_y", "etiket": "Sayısal yanlış", "tip": "tamsayi", "varsayilan": "10"},
        {"id": "soz_d", "etiket": "Sözel doğru", "tip": "tamsayi", "varsayilan": "32", "ipucu": "50 soru"},
        {"id": "soz_y", "etiket": "Sözel yanlış", "tip": "tamsayi", "varsayilan": "10"},
        {"id": "obp", "etiket": "Ön Lisans Başarı Puanı (ÖBP) — isteğe bağlı", "tip": "sayi", "varsayilan": "", "genis": True, "ipucu": "mezuniyet notu × 4 ile bulunur (100–400)"},
    ],
    "js": r"""
function hesapla(g){
  var sd = g.say_d > 0 ? g.say_d : 0, sy = g.say_y > 0 ? g.say_y : 0;
  var zd = g.soz_d > 0 ? g.soz_d : 0, zy = g.soz_y > 0 ? g.soz_y : 0;
  if (sd + sy > 50) return {hata: 'Sayısal: doğru + yanlış 50 soruyu aşamaz.'};
  if (zd + zy > 50) return {hata: 'Sözel: doğru + yanlış 50 soruyu aşamaz.'};
  var sayNet = sd - sy / 4, sozNet = zd - zy / 4, top = sayNet + sozNet;
  var s = [
    {etiket: 'Toplam DGS neti (100 soru)', deger: top, vurgu: true},
    {etiket: 'Sayısal net (50 soru)', deger: sayNet},
    {etiket: 'Sözel net (50 soru)', deger: sozNet},
    {etiket: 'Toplam doğru / yanlış / boş', deger: (sd + zd) + ' / ' + (sy + zy) + ' / ' + (100 - sd - sy - zd - zy)},
    {etiket: 'Yanlışların götürdüğü net', deger: (sy + zy) / 4},
    {etiket: 'Baraj (her bölümden en az 0,5 ham puan)', deger: (sayNet >= 0.5 && sozNet >= 0.5) ? 'Sağlanıyor ✓' : 'SAĞLANMIYOR — puanınız hesaplanmaz'},
    {etiket: 'Güçlü olduğunuz alan', deger: sayNet > sozNet ? 'Sayısal (SAY puanı avantajlı)' : sozNet > sayNet ? 'Sözel (SÖZ puanı avantajlı)' : 'Dengeli (EA avantajlı)'}
  ];
  var n = ['Net = doğru − yanlış ÷ 4 (4 yanlış 1 doğruyu götürür).',
           'DGS\'de üç puan türü hesaplanır: SAY (sayısal ağırlıklı), SÖZ (sözel ağırlıklı) ve EA (dengeli). Tercih edeceğiniz lisans programının hangi puan türünü istediğine göre güçlü olduğunuz alan önem kazanır.',
           'Netler, ÖSYM\'nin sınav sonrası açıkladığı ortalama ve standart sapmayla standart puana çevrilir; bu nedenle sınav öncesinde netten kesin puan hesaplanamaz. Yayınlanan "net-puan" tabloları geçmiş yıl katsayılarına dayalı tahminlerdir.'];
  if (g.obp > 0) {
    if (g.obp < 100 || g.obp > 400) n.push('ÖBP genellikle 100–400 aralığındadır (mezuniyet notu × 4); girdiğiniz değeri kontrol edin.');
    s.push({etiket: 'Girilen ÖBP', deger: g.obp});
    n.push('ÖBP, DGS puanınıza katkı olarak eklenir; katsayı ÖSYM tarafından her yıl kılavuzda belirlenir ve önceden kesin bilinemez.');
  }
  return {sonuclar: s, notlar: n,
    grafik: {tur: 'sutun', baslik: 'Bölüm bazında netleriniz', etiketler: ['Sayısal', 'Sözel'], seriler: [{ad: 'Net', veri: [Math.round(sayNet*100)/100, Math.round(sozNet*100)/100]}]}};
}
""",
    "nasil": [
        "Dikey Geçiş Sınavı (DGS), ön lisans mezunlarının lisans programlarına geçişi için yapılır ve 100 sorudan oluşur: 50 Sayısal, 50 Sözel. Sayısal bölümde temel matematik ve sayısal mantık, sözel bölümde sözel mantık ve Türkçe akıl yürütme soruları yer alır; her iki bölüm de ezber bilgiden çok muhakeme ölçer.",
        "Net, doğru sayısından yanlış sayısının dörtte biri çıkarılarak bulunur (4 yanlış 1 doğruyu götürür). Netler, o yılki adayların ortalaması ve standart sapmasıyla standart puana dönüştürülür; ardından SAY, SÖZ ve EA olmak üzere üç ayrı puan türü hesaplanır. Tercih edeceğiniz programın istediği puan türü, hangi bölümde güçlü olmanız gerektiğini belirler.",
        "Puanınızın hesaplanabilmesi için hem Sayısal hem Sözel bölümden en az 0,5 ham puan almanız gerekir. Ayrıca Ön Lisans Başarı Puanı (ÖBP), mezuniyet notunuzun 4 ile çarpılmasıyla bulunur ve DGS puanınıza katkı olarak eklenir; katkı katsayısı her yıl ÖSYM kılavuzunda ilan edilir.",
    ],
    "formul": [
        "Bölüm neti = doğru − (yanlış ÷ 4)",
        "Toplam net = sayısal net + sözel net (100 soru)",
        "Standart puan → SAY / SÖZ / EA puan türleri (ÖSYM istatistikleriyle)",
        "ÖBP = ön lisans mezuniyet notu × 4 (100–400) · DGS puanına katkı olarak eklenir",
    ],
    "ornekler": [
        {"baslik": "Sayısal 30D 10Y, Sözel 32D 10Y", "adimlar": ["Sayısal: 30 − 2,5 = 27,5", "Sözel: 32 − 2,5 = 29,5", "Toplam 57 net"]},
        {"baslik": "Sayısal ağırlıklı: 44D 4Y / 25D 15Y", "adimlar": ["Sayısal 43 · Sözel 21,25 → toplam 64,25", "SAY puan türünde avantajlı"]},
    ],
    "tablo": {
        "baslik": "DGS sınav yapısı",
        "basliklar": ["Bölüm", "Soru", "İçerik"],
        "satirlar": [["Sayısal", "50", "Temel matematik, sayısal mantık ve muhakeme"], ["Sözel", "50", "Sözel mantık, Türkçe akıl yürütme, paragraf"], ["Toplam", "100", "Süre: 150 dakika"]],
        "not": "Puan türleri: SAY, SÖZ, EA. Tercih edilecek lisans programının puan türü ÖSYM tercih kılavuzunda belirtilir.",
    },
    "sss": [
        {"soru": "DGS'de kaç soru var?", "cevap": "100 soru: 50 sayısal, 50 sözel. Süre 150 dakikadır."},
        {"soru": "DGS'de kaç yanlış 1 doğruyu götürür?", "cevap": "4 yanlış 1 doğruyu götürür; net = doğru − yanlış/4."},
        {"soru": "DGS puan türleri nelerdir?", "cevap": "SAY (sayısal ağırlıklı), SÖZ (sözel ağırlıklı) ve EA (eşit ağırlık). Tercih edeceğiniz programın istediği türe göre hangi bölümde güçlü olmanız gerektiği değişir."},
        {"soru": "ÖBP nasıl hesaplanır?", "cevap": "Ön lisans mezuniyet notunuz 4 ile çarpılır (örn. 80 → 320). DGS puanına katkı olarak eklenir; katsayı her yıl kılavuzda ilan edilir."},
        {"soru": "DGS'de baraj var mı?", "cevap": "Puanınızın hesaplanması için her iki bölümden de en az 0,5 ham puan gerekir. Yerleştirmede programlara göre taban puanlar geçerlidir."},
    ],
    "kaynaklar": [
        {"ad": "ÖSYM — DGS kılavuzu ve puan hesaplama esasları", "url": "https://www.osym.gov.tr/"},
    ],
    "ilgili": ["tyt-net-hesaplama", "gano-hesaplama", "kpss-net-hesaplama"],
}
