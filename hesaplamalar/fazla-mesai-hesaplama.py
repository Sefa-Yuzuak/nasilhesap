# -*- coding: utf-8 -*-
HESAP = {
    "slug": "fazla-mesai-hesaplama",
    "baslik": "Fazla Mesai Hesaplama",
    "h1": "Fazla Mesai Ücreti Hesaplama 2026 — Saatlik Ücret, %50 ve %25 Zamlı Çalışma",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Fazla mesai ücreti hesaplama: aylık brüt maaştan saatlik ücret (÷225), 45 saati aşan fazla çalışma (1,5 kat), 40-45 saat arası fazla sürelerle çalışma (1,25 kat), hafta tatili ve resmî tatil mesaisi ile yıllık 270 saat sınırı.",
    "kisa_cevap": "Saatlik brüt ücret = aylık brüt ÷ 225. Haftalık 45 saati aşan her saat için normal ücretin 1,5 katı (%50 zamlı), haftalık çalışma süresi sözleşmeyle 45 saatin altındaysa 45 saate kadar olan kısım için 1,25 katı (%25 zamlı) ödenir. 2026 asgari ücrette saatlik brüt 146,80 ₺, fazla mesai saati 220,20 ₺'dir. Yıllık fazla çalışma 270 saati aşamaz.",
    "senaryolar": [
        {"ad": "Asgari ücret · 20 saat", "degerler": {"brut": "33030", "fm_saat": "20", "fs_saat": "0", "tatil_saat": "0"}},
        {"ad": "50.000 ₺ · 30 saat", "degerler": {"brut": "50000", "fm_saat": "30", "fs_saat": "0", "tatil_saat": "0"}},
        {"ad": "50.000 ₺ · 20 FM + 10 FS", "degerler": {"brut": "50000", "fm_saat": "20", "fs_saat": "10", "tatil_saat": "0"}},
        {"ad": "Tatil mesaisi dahil", "degerler": {"brut": "60000", "fm_saat": "15", "fs_saat": "0", "tatil_saat": "8"}},
    ],
    "girdiler": [
        {"id": "brut", "etiket": "Aylık brüt ücret", "tip": "sayi", "varsayilan": "50000", "birim": "₺"},
        {"id": "fm_saat", "etiket": "Fazla mesai (45 saati aşan)", "tip": "sayi", "varsayilan": "20", "birim": "saat", "ipucu": "%50 zamlı"},
        {"id": "fs_saat", "etiket": "Fazla sürelerle çalışma (40–45 saat arası)", "tip": "sayi", "varsayilan": "0", "birim": "saat", "ipucu": "%25 zamlı"},
        {"id": "tatil_saat", "etiket": "Hafta/resmî tatil mesaisi", "tip": "sayi", "varsayilan": "0", "birim": "saat", "ipucu": "genellikle %100 zamlı"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.brut > 0)) return {hata: 'Aylık brüt ücreti girin.'};
  var saatlik = g.brut / 225;
  var fm = g.fm_saat > 0 ? g.fm_saat : 0, fs = g.fs_saat > 0 ? g.fs_saat : 0, tt = g.tatil_saat > 0 ? g.tatil_saat : 0;
  var fmUcret = saatlik * 1.5 * fm, fsUcret = saatlik * 1.25 * fs, ttUcret = saatlik * 2 * tt;
  var toplam = fmUcret + fsUcret + ttUcret;
  var n = ['Saatlik ücret = aylık brüt ÷ 225 (haftalık 45 saat × 52 hafta ÷ 12 ay ≈ 195 saat + hafta tatili ücretleri dahil yasal kabul).',
           'Fazla mesai brüt tutardır; gelir vergisi, damga vergisi ve SGK primi kesilir. Net karşılığı vergi diliminize göre değişir.',
           'Fazla çalışma için işçinin yazılı onayı gerekir ve yıllık toplam 270 saati aşamaz (İş Kanunu m.41).'];
  if (fm + fs > 270) n.push('DİKKAT: Girilen fazla çalışma (' + (fm + fs) + ' saat) yıllık 270 saat sınırının üzerinde. Bu sınır yıllık toplamdır.');
  if (tt > 0) n.push('Hafta tatili ve ulusal bayram/genel tatil çalışmasında uygulama farklıdır: tatil günü çalışılırsa o güne ait ücret ayrıca ödenir (fiilen %100 zam etkisi). Sözleşmenize ve bordronuza göre değişebilir.');
  return {
    sonuclar: [
      {etiket: 'Toplam fazla mesai ücreti (brüt)', deger: toplam, birim: '₺', vurgu: true},
      {etiket: 'Saatlik normal brüt ücret', deger: saatlik, birim: '₺'},
      {etiket: 'Fazla mesai saat ücreti (×1,5)', deger: saatlik * 1.5, birim: '₺'},
      {etiket: 'Fazla mesai tutarı (' + fm + ' saat)', deger: fmUcret, birim: '₺'},
      {etiket: 'Fazla sürelerle çalışma (×1,25, ' + fs + ' saat)', deger: fsUcret, birim: '₺'},
      {etiket: 'Tatil mesaisi (×2, ' + tt + ' saat)', deger: ttUcret, birim: '₺'},
      {etiket: 'Aylık brüt toplam (maaş + mesai)', deger: g.brut + toplam, birim: '₺'},
      {etiket: 'Mesainin maaşa oranı', deger: toplam / g.brut * 100, birim: '%'}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "Türkiye'de haftalık yasal çalışma süresi 45 saattir (İş Kanunu m.63). Bu süreyi aşan çalışmalar 'fazla çalışma' (fazla mesai) sayılır ve her saat için normal saatlik ücretin 1,5 katı ödenir. Sözleşmeyle haftalık çalışma süresi 45 saatin altında belirlenmişse (örneğin 40 saat), 40 ile 45 saat arasındaki çalışma 'fazla sürelerle çalışma' sayılır ve 1,25 kat ücretlendirilir.",
        "Saatlik ücret, aylık brüt ücretin 225'e bölünmesiyle bulunur. Bu 225 sayısı, haftalık 45 saatlik çalışmanın aylık karşılığıdır (45 × 52 ÷ 12 = 195 çalışma saati + hafta tatili ve genel tatil ücretlerinin karşılığı). 2026 asgari ücrette saatlik brüt 146,80 ₺, fazla mesai saati 220,20 ₺'dir.",
        "Fazla çalışma için işçinin yazılı onayı gerekir ve yıllık toplam 270 saati aşamaz. İşçi dilerse zamlı ücret yerine her fazla saat için 1,5 saat (fazla sürelerle çalışmada 1,25 saat) serbest zaman kullanabilir. Hafta tatili ve ulusal bayram/genel tatil günlerinde çalışma ayrı hükümlere tabidir ve fiilen daha yüksek ücretlendirilir.",
    ],
    "formul": [
        "Saatlik brüt ücret = aylık brüt ücret ÷ 225",
        "Fazla mesai (45 saat üstü) = saatlik ücret × 1,5 × saat",
        "Fazla sürelerle çalışma (40–45 saat) = saatlik ücret × 1,25 × saat",
        "Yıllık üst sınır: 270 saat fazla çalışma",
    ],
    "ornekler": [
        {"baslik": "50.000 ₺ brüt, 20 saat fazla mesai", "adimlar": ["Saatlik: 50.000 ÷ 225 = 222,22 ₺", "Mesai saati: 222,22 × 1,5 = 333,33 ₺", "Toplam: 333,33 × 20 = 6.666,67 ₺ brüt"]},
        {"baslik": "Asgari ücret, 10 saat", "adimlar": ["Saatlik: 33.030 ÷ 225 = 146,80 ₺", "Mesai saati: 220,20 ₺ → 10 saat = 2.202 ₺ brüt"]},
    ],
    "tablo": {
        "baslik": "Çalışma türüne göre zam oranları",
        "basliklar": ["Durum", "Çarpan", "Dayanak"],
        "satirlar": [["Fazla çalışma (haftalık 45 saat üstü)", "×1,50 (%50 zamlı)", "İş K. m.41"], ["Fazla sürelerle çalışma (sözleşme <45 saat, 45'e kadar)", "×1,25 (%25 zamlı)", "İş K. m.41"], ["Serbest zaman seçeneği", "1 saat çalışma → 1,5 saat izin", "İş K. m.41"], ["Ulusal bayram / genel tatil çalışması", "Ek 1 günlük ücret (fiilen ×2)", "İş K. m.47"], ["Yıllık fazla çalışma sınırı", "270 saat", "İş K. m.41"]],
        "not": "Gece çalışması, ara dinlenme ve denkleştirme uygulamalarında özel hükümler geçerlidir.",
    },
    "sss": [
        {"soru": "Fazla mesai ücreti nasıl hesaplanır?", "cevap": "Aylık brütü 225'e bölerek saatlik ücreti bulun, 1,5 ile çarpın ve fazla çalışma saatiyle çarpın. 40.000 ₺ brüt → 177,78 ₺ saatlik → 266,67 ₺ mesai saati."},
        {"soru": "Neden 225'e bölünüyor?", "cevap": "Haftalık 45 saatin aylık karşılığı; hafta tatili ve genel tatil ücretlerinin de içinde olduğu yasal kabuldür. Yargıtay uygulaması da bu bölüneni esas alır."},
        {"soru": "Yılda en fazla kaç saat fazla mesai yapılabilir?", "cevap": "270 saat. Bu sınır aşılsa bile yapılan çalışmanın ücreti ödenmelidir; sınır aşımı işveren açısından idari yaptırım doğurur."},
        {"soru": "Fazla mesai yerine izin kullanabilir miyim?", "cevap": "Evet. İşçi isterse her fazla çalışma saati için 1,5 saat (fazla sürelerle çalışmada 1,25 saat) serbest zaman kullanabilir; bu hak 6 ay içinde kullandırılmalıdır."},
        {"soru": "Maaşa fazla mesai dahil denilebilir mi?", "cevap": "Sözleşmeye 'ücrete 270 saat fazla çalışma dahildir' kaydı konulabilir; 270 saati aşan kısım ayrıca ödenmelidir. Asgari ücretlide bu kayıt geçersizdir."},
        {"soru": "Fazla mesai brüt mü net mi?", "cevap": "Hesaplanan tutar brüttür; gelir vergisi, damga vergisi ve SGK primi kesildikten sonra elinize geçen tutar vergi diliminize göre değişir."},
    ],
    "kaynaklar": [
        {"ad": "4857 sayılı İş Kanunu m.41, m.63 (fazla çalışma)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=4857&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "ÇSGB — Çalışma süreleri ve fazla çalışma", "url": "https://www.csgb.gov.tr/"},
    ],
    "ilgili": ["brut-net-maas-hesaplama", "asgari-ucret-hesaplama", "kidem-tazminati-hesaplama"],
}
