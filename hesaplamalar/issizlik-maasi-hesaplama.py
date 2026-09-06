# -*- coding: utf-8 -*-
HESAP = {
    "slug": "issizlik-maasi-hesaplama",
    "baslik": "İşsizlik Maaşı Hesaplama",
    "h1": "İşsizlik Maaşı Hesaplama 2026 — İŞKUR Ödeneği Tutarı ve Süresi",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 işsizlik maaşı hesaplama: son 4 ayın brüt ortalamasına göre günlük ve aylık işsizlik ödeneği, taban 13.212 ₺ – tavan 26.424 ₺ sınırları, damga vergisi sonrası net tutar ve prim gününe göre ödeme süresi.",
    "kisa_cevap": "İşsizlik ödeneği, son 4 aylık prime esas günlük brüt kazanç ortalamasının %40'ıdır. 2026'da aylık tutar en az 13.212 ₺ (brüt asgari ücretin %40'ı), en çok 26.424 ₺ (brüt asgari ücretin %80'i) olabilir; ödenekten yalnızca ‰7,59 damga vergisi kesilir. Ödeme süresi son 3 yıldaki prim gününe göre 180, 240 veya 300 gündür.",
    "senaryolar": [
        {"ad": "Asgari ücretli · 600 gün", "degerler": {"brut": "33030", "gun": "600"}},
        {"ad": "50.000 ₺ brüt · 900 gün", "degerler": {"brut": "50000", "gun": "900"}},
        {"ad": "80.000 ₺ brüt (tavan) · 1080 gün", "degerler": {"brut": "80000", "gun": "1080"}},
        {"ad": "Yetersiz prim (500 gün)", "degerler": {"brut": "40000", "gun": "500"}},
    ],
    "girdiler": [
        {"id": "brut", "etiket": "Son 4 ayın aylık brüt ortalaması", "tip": "sayi", "varsayilan": "50000", "birim": "₺", "genis": True, "ipucu": "prime esas kazanç"},
        {"id": "gun", "etiket": "Son 3 yıldaki prim gün sayısı", "tip": "tamsayi", "varsayilan": "900", "birim": "gün", "ipucu": "son 120 gün kesintisiz çalışma şartıyla"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.brut > 0)) return {hata: 'Son 4 ayın brüt ortalamasını girin.'};
  var A = O.asgari_ucret.brut, dv = O.damga_vergisi.ucret_oran;
  var taban = A * 0.40, tavan = A * 0.80;
  var ham = g.brut * 0.40;
  var aylik = Math.min(Math.max(ham, taban), tavan);
  var net = aylik * (1 - dv);
  var gun = g.gun > 0 ? g.gun : 0;
  var sure = gun >= 1080 ? 300 : gun >= 900 ? 240 : gun >= 600 ? 180 : 0;
  var s = [];
  if (sure === 0) {
    s.push({etiket: 'İşsizlik ödeneği', deger: 'Hak yok — son 3 yılda en az 600 prim günü gerekir', vurgu: true});
    s.push({etiket: 'Girilen prim günü', deger: gun + ' gün (600 gün gerekli)'});
  } else {
    s.push({etiket: 'Aylık net işsizlik maaşı', deger: net, birim: '₺', vurgu: true});
    s.push({etiket: 'Aylık brüt ödenek', deger: aylik, birim: '₺'});
    s.push({etiket: 'Damga vergisi (‰7,59)', deger: aylik - net, birim: '₺'});
    s.push({etiket: 'Günlük brüt ödenek', deger: aylik / 30, birim: '₺'});
    s.push({etiket: 'Ödeme süresi', deger: sure + ' gün (' + (sure / 30) + ' ay)'});
    s.push({etiket: 'Toplam alacağınız (net)', deger: net * sure / 30, birim: '₺'});
  }
  s.push({etiket: '2026 taban / tavan (brüt)', deger: NH.fmt(taban) + ' ₺ / ' + NH.fmt(tavan) + ' ₺'});
  var n = ['Ödenek = son 4 aylık prime esas günlük brüt kazanç ortalaması × %40. Bu tutar brüt asgari ücretin %40\'ından az, %80\'inden çok olamaz.',
           'Şartlar: son 3 yılda en az 600 gün prim, son 120 gün kesintisiz hizmet akdine tabi çalışma ve kendi istek/kusuru dışında işten ayrılma. Fesih tarihinden itibaren 30 gün içinde İŞKUR\'a başvurulmalıdır.',
           'Ödenekten yalnızca damga vergisi kesilir; gelir vergisi ve SGK primi kesilmez. Genel sağlık sigortası primi İşsizlik Sigortası Fonu\'ndan karşılanır.'];
  if (ham > tavan) n.push('Kazancınızın %40\'ı (' + NH.fmt(ham) + ' ₺) tavanı aştığı için ödenek tavandan (' + NH.fmt(tavan) + ' ₺) ödenir.');
  if (ham < taban && sure > 0) n.push('Kazancınızın %40\'ı tabanın altında kaldığı için ödenek tabandan ödenir.');
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "İşsizlik ödeneği (halk arasında işsizlik maaşı), 4447 sayılı Kanun kapsamında, kendi istek ve kusuru dışında işini kaybeden sigortalılara İŞKUR tarafından ödenir. Tutarı, sigortalının son dört aylık prime esas kazançları dikkate alınarak hesaplanan günlük ortalama brüt kazancının %40'ıdır.",
        "Bu tutarın alt ve üst sınırı vardır: aylık ödenek brüt asgari ücretin %40'ından az, %80'inden çok olamaz. 2026'da brüt asgari ücret 33.030 ₺ olduğundan taban 13.212 ₺, tavan 26.424 ₺'dir. Ödenekten yalnızca ‰7,59 damga vergisi kesilir; gelir vergisi ve SGK primi kesilmez, genel sağlık sigortası primi Fon tarafından karşılanır.",
        "Ödeme süresi, işten ayrılmadan önceki son üç yıldaki prim gün sayısına bağlıdır: 600 gün prim ödeyene 180 gün, 900 gün ödeyene 240 gün, 1080 gün ödeyene 300 gün ödeme yapılır. Ayrıca son 120 gün hizmet akdine tabi kesintisiz çalışmış olmak ve fesihten itibaren 30 gün içinde İŞKUR'a başvurmak gerekir.",
    ],
    "formul": [
        "Günlük ödenek = son 4 aylık günlük ortalama brüt kazanç × %40",
        "Aylık ödenek = günlük ödenek × 30, en az brüt asgari ücret × %40, en çok × %80",
        "2026: taban 13.212 ₺ · tavan 26.424 ₺ (brüt)",
        "Net = brüt ödenek × (1 − ‰7,59) · Süre: 600 gün → 180 · 900 gün → 240 · 1080 gün → 300 gün",
    ],
    "ornekler": [
        {"baslik": "50.000 ₺ brüt ortalama, 900 prim günü", "adimlar": ["Ödenek: 50.000 × %40 = 20.000 ₺ (taban-tavan arasında)", "Damga: 151,80 ₺ → net 19.848,20 ₺", "Süre 240 gün (8 ay) → toplam ≈ 158.785 ₺ net"]},
        {"baslik": "Asgari ücretli, 600 prim günü", "adimlar": ["33.030 × %40 = 13.212 ₺ (taban ile aynı)", "Net ≈ 13.111,72 ₺ · süre 180 gün (6 ay)"]},
        {"baslik": "80.000 ₺ brüt, 1080 prim günü", "adimlar": ["80.000 × %40 = 32.000 ₺ → tavan 26.424 ₺ uygulanır", "Net ≈ 26.223,44 ₺ · süre 300 gün (10 ay)"]},
    ],
    "tablo": {
        "baslik": "2026 işsizlik ödeneği sınırları ve süreler",
        "basliklar": ["Kalem", "Değer"],
        "satirlar": [["Hesaplama oranı", "Son 4 ay günlük brüt ortalamanın %40'ı"], ["Aylık taban (brüt)", "13.212,00 ₺"], ["Aylık tavan (brüt)", "26.424,00 ₺"], ["Aylık taban (net)", "≈ 13.111,72 ₺"], ["Aylık tavan (net)", "≈ 26.223,44 ₺"], ["600 gün prim", "180 gün ödeme"], ["900 gün prim", "240 gün ödeme"], ["1080 gün prim", "300 gün ödeme"], ["Kesinti", "Yalnızca damga vergisi ‰7,59"], ["Başvuru süresi", "Fesihten itibaren 30 gün"]],
        "not": "4447 sayılı İşsizlik Sigortası Kanunu m.50-51; 2026 asgari ücret esas alınmıştır.",
    },
    "sss": [
        {"soru": "2026 işsizlik maaşı ne kadar?", "cevap": "En az 13.212 ₺ brüt (≈13.111 ₺ net), en çok 26.424 ₺ brüt (≈26.223 ₺ net). Tutar son 4 ayın brüt ortalamasının %40'ıdır."},
        {"soru": "İşsizlik maaşı kaç ay ödenir?", "cevap": "Son 3 yıldaki prim gününe göre: 600 gün → 6 ay, 900 gün → 8 ay, 1080 gün → 10 ay."},
        {"soru": "Kimler işsizlik maaşı alamaz?", "cevap": "İstifa edenler, haklı nedenle (ahlak ve iyi niyet kurallarına aykırılık) işten çıkarılanlar, son 120 günü kesintisiz olmayanlar ve son 3 yılda 600 günü doldurmayanlar."},
        {"soru": "İşsizlik maaşından vergi kesilir mi?", "cevap": "Yalnızca ‰7,59 damga vergisi. Gelir vergisi ve SGK primi kesilmez; sağlık sigortanız Fon tarafından karşılanır."},
        {"soru": "Ne zaman başvurmalıyım?", "cevap": "İş sözleşmesinin feshinden itibaren 30 gün içinde İŞKUR'a (e-Devlet veya şube) başvurmalısınız. Geç başvuruda gecikilen süre toplam hak edilen süreden düşülür."},
        {"soru": "İşsizlik maaşı alırken işe girersem ne olur?", "cevap": "Ödeme kesilir. Yeniden işsiz kalırsanız, hak ettiğiniz süreden kalan kısmı yeni şartları sağlamanız hâlinde kullanabilirsiniz."},
    ],
    "kaynaklar": [
        {"ad": "4447 sayılı İşsizlik Sigortası Kanunu (m.50-51)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=4447&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "İŞKUR — İşsizlik ödeneği başvuru ve şartları", "url": "https://www.iskur.gov.tr/"},
    ],
    "ilgili": ["kidem-tazminati-hesaplama", "brut-net-maas-hesaplama", "asgari-ucret-hesaplama"],
}
