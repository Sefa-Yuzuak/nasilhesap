# -*- coding: utf-8 -*-
HESAP = {
    "slug": "brut-net-maas-hesaplama",
    "baslik": "Brüt Net Maaş Hesaplama",
    "h1": "Brüt Net Maaş Hesaplama 2026 — Brütten Nete, Netten Brüte",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 brüt net maaş hesaplama: SGK işçi payı (%14), işsizlik sigortası (%1), kümülatif gelir vergisi dilimleri, damga vergisi ve asgari ücret istisnasıyla aylık net maaşı 12 ay için hesaplayın. Netten brüte de çevirir.",
    "kisa_cevap": "Net maaş = brüt − SGK işçi payı (%14) − işsizlik (%1) − gelir vergisi − damga vergisi (‰7,59). Gelir vergisi kümülatif matraha göre %15'ten başlar ve yıl içinde dilim atladıkça artar; asgari ücrete (2026'da 33.030 ₺ brüt) denk gelen kısım vergiden istisnadır. 50.000 ₺ brüt maaş 2026 Ocak'ta yaklaşık 40.940 ₺ net eder.",
    "senaryolar": [
        {"ad": "Asgari ücret", "degerler": {"mod": "brutten", "tutar": "33030", "ay": "1"}},
        {"ad": "50.000 ₺ brüt", "degerler": {"mod": "brutten", "tutar": "50000", "ay": "1"}},
        {"ad": "75.000 ₺ brüt", "degerler": {"mod": "brutten", "tutar": "75000", "ay": "1"}},
        {"ad": "100.000 ₺ brüt", "degerler": {"mod": "brutten", "tutar": "100000", "ay": "1"}},
        {"ad": "Net 60.000 ₺ istiyorum", "degerler": {"mod": "netten", "tutar": "60000", "ay": "1"}},
    ],
    "girdiler": [
        {"id": "mod", "etiket": "Hesaplama yönü", "tip": "secim", "varsayilan": "brutten", "genis": True,
         "secenekler": [["brutten", "Brütten nete"], ["netten", "Netten brüte"]]},
        {"id": "tutar", "etiket": "Aylık maaş", "tip": "sayi", "varsayilan": "50000", "birim": "₺"},
        {"id": "ay", "etiket": "Hangi ayın maaşı?", "tip": "secim", "varsayilan": "1",
         "secenekler": [[str(i), a] for i, a in enumerate(["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"], 1)]},
    ],
    "js": r"""
function vergiHesap(matrah, dilimler){
  var v = 0, alt = 0;
  for (var i = 0; i < dilimler.length; i++) {
    var ust = dilimler[i][0] === null ? Infinity : dilimler[i][0], oran = dilimler[i][1];
    if (matrah > alt) v += (Math.min(matrah, ust) - alt) * oran;
    alt = ust;
  }
  return v;
}
function bordro(brut, O){
  var sgkM = Math.min(brut, O.sgk.tavan);
  var sgk = sgkM * O.sgk.isci_orani, iss = sgkM * O.sgk.issizlik_isci_orani;
  var gvM = brut - sgk - iss;
  var asg = O.asgari_ucret.brut, asgM = asg * (1 - O.sgk.isci_orani - O.sgk.issizlik_isci_orani);
  var dv = brut * O.damga_vergisi.ucret_oran, dvIst = asg * O.damga_vergisi.ucret_oran;
  var rows = [], kum = 0, kumA = 0, onceV = 0, onceA = 0;
  for (var m = 1; m <= 12; m++) {
    kum += gvM; kumA += asgM;
    var kv = vergiHesap(kum, O.gelir_vergisi.ucret), ka = vergiHesap(kumA, O.gelir_vergisi.ucret);
    var gv = kv - onceV, ist = ka - onceA; onceV = kv; onceA = ka;
    var gvNet = Math.max(0, gv - ist), dvNet = Math.max(0, dv - dvIst);
    rows.push({ay: m, gv: gvNet, dv: dvNet, net: brut - sgk - iss - gvNet - dvNet, kum: kum});
  }
  return {sgk: sgk, iss: iss, gvM: gvM, rows: rows};
}
function hesapla(g, O){
  if (!(g.tutar > 0)) return {hata: 'Maaş tutarını girin.'};
  var ay = parseInt(g.ay, 10) || 1, brut;
  if (g.mod === 'brutten') brut = g.tutar;
  else { // netten brüte: seçili ayın neti hedef, iki nokta arası arama
    var lo = g.tutar, hi = g.tutar * 3;
    for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (bordro(mid, O).rows[ay - 1].net < g.tutar) lo = mid; else hi = mid; }
    brut = (lo + hi) / 2;
  }
  var b = bordro(brut, O), r = b.rows[ay - 1];
  var aylar = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
  var isveren = brut + Math.min(brut, O.sgk.tavan) * (O.sgk.isveren_orani + O.sgk.issizlik_isveren_orani);
  return {
    sonuclar: [
      {etiket: g.mod === 'brutten' ? aylar[ay-1] + ' net maaş' : 'Gerekli brüt maaş (' + aylar[ay-1] + ')', deger: g.mod === 'brutten' ? r.net : brut, birim: '₺', vurgu: true},
      {etiket: 'Brüt maaş', deger: brut, birim: '₺'},
      {etiket: 'SGK işçi payı (%' + Math.round(O.sgk.isci_orani*100) + ')', deger: b.sgk, birim: '₺'},
      {etiket: 'İşsizlik sigortası (%' + Math.round(O.sgk.issizlik_isci_orani*100) + ')', deger: b.iss, birim: '₺'},
      {etiket: 'Gelir vergisi (istisna sonrası)', deger: r.gv, birim: '₺'},
      {etiket: 'Damga vergisi (istisna sonrası)', deger: r.dv, birim: '₺'},
      {etiket: 'Net maaş (' + aylar[ay-1] + ')', deger: r.net, birim: '₺'},
      {etiket: 'İşverene toplam maliyet (teşvik hariç)', deger: isveren, birim: '₺'}
    ],
    grafik: {tur: 'cizgi', baslik: 'Aylara göre net maaş (kümülatif vergi etkisi)', etiketler: aylar.map(function(a){ return a.slice(0,3); }),
             seriler: [{ad: 'Net maaş', veri: b.rows.map(function(x){ return x.net; })}, {ad: 'Brüt', veri: b.rows.map(function(){ return brut; }), renk: '#9ca3af'}]},
    tablo: {basliklar: ['Ay', 'Gelir vergisi', 'Damga', 'Net'], satirlar: b.rows.map(function(x){ return [aylar[x.ay-1], x.gv, x.dv, x.net]; })},
    notlar: ['Gelir vergisi matrahı: ' + NH.fmt(b.gvM) + ' ₺/ay (brüt − SGK − işsizlik). Kümülatif matrah dilim atladıkça vergi artar, net düşer.',
             'Asgari ücret istisnası uygulanmıştır (2026 brüt asgari ücret ' + NH.fmt(O.asgari_ucret.brut) + ' ₺). SGK tavanı ' + NH.fmt(O.sgk.tavan) + ' ₺.',
             'Engelli indirimi, AGİ benzeri özel indirimler, BES ve özel sigorta kesintileri dahil değildir.']
  };
}
""",
    "nasil": [
        "Brüt maaştan net maaşa geçmek için sırasıyla dört kesinti düşülür: SGK işçi primi (%14), işsizlik sigortası işçi payı (%1), gelir vergisi ve damga vergisi (‰7,59). SGK ve işsizlik primi brüt üzerinden hesaplanır ancak prime esas kazanç tavanla (2026'da 297.270 ₺) sınırlıdır.",
        "Gelir vergisi, brütten SGK ve işsizlik primi düşüldükten sonra kalan matrah üzerinden, yıl başından itibaren biriken (kümülatif) matraha göre dilimli tarifeyle hesaplanır. 2026'da ücret gelirleri için dilimler 190.000 ₺'ye kadar %15, 400.000 ₺'ye kadar %20, 1.500.000 ₺'ye kadar %27, 5.300.000 ₺'ye kadar %35 ve üzeri %40'tır. Bu yüzden aynı brüt maaşın neti Ocak'ta en yüksek, yıl sonunda en düşüktür.",
        "2022'den beri asgari ücrete denk gelen kazanç gelir ve damga vergisinden istisnadır: her ay, asgari ücret matrahına isabet eden vergi hesaplanan vergiden düşülür. Netten brüte çevirmek kapalı formülle mümkün olmadığı için araç, hedef neti veren brütü iteratif olarak bulur.",
    ],
    "formul": [
        "SGK işçi payı = min(brüt, tavan) × %14 · İşsizlik = min(brüt, tavan) × %1",
        "Gelir vergisi matrahı = brüt − SGK − işsizlik",
        "Gelir vergisi (ay) = kümülatif vergi(bu ay) − kümülatif vergi(önceki ay) − asgari ücret istisnası",
        "Damga vergisi = brüt × ‰7,59 − asgari ücret damga istisnası",
        "Net = brüt − SGK − işsizlik − gelir vergisi − damga vergisi",
    ],
    "ornekler": [
        {"baslik": "2026 asgari ücret: 33.030 ₺ brüt", "adimlar": ["SGK: 33.030 × 0,14 = 4.624,20 ₺ · İşsizlik: 330,30 ₺", "Gelir vergisi matrahı 28.075,50 ₺; vergi tamamen istisna kapsamında → 0 ₺; damga istisnası → 0 ₺", "Net: 33.030 − 4.624,20 − 330,30 = 28.075,50 ₺ (resmî net asgari ücretle birebir)"]},
        {"baslik": "50.000 ₺ brüt, Ocak 2026", "adimlar": ["SGK 7.000 ₺, işsizlik 500 ₺ → matrah 42.500 ₺", "Gelir vergisi: 42.500 × %15 = 6.375 ₺ − istisna 4.211,33 ₺ = 2.163,67 ₺", "Damga: 379,50 − 250,70 = 128,80 ₺", "Net ≈ 50.000 − 7.000 − 500 − 2.163,67 − 128,80 = 40.207,53 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 ücret gelirleri gelir vergisi tarifesi",
        "basliklar": ["Kümülatif matrah", "Oran"],
        "satirlar": [["0 – 190.000 ₺", "%15"], ["190.000 – 400.000 ₺", "%20"], ["400.000 – 1.500.000 ₺", "%27"], ["1.500.000 – 5.300.000 ₺", "%35"], ["5.300.000 ₺ üzeri", "%40"]],
        "not": "Resmî Gazete 31.12.2025, Sayı 33124 (5. Mükerrer) — Gelir Vergisi Genel Tebliği Seri No 332.",
    },
    "sss": [
        {"soru": "2026 asgari ücret net ne kadar?", "cevap": "Brüt 33.030 ₺, net 28.075,50 ₺. Asgari ücretten yalnızca SGK (%14) ve işsizlik (%1) primi kesilir; gelir ve damga vergisi istisna kapsamındadır."},
        {"soru": "Net maaşım neden yıl ortasında düştü?", "cevap": "Gelir vergisi kümülatif matraha göre hesaplanır. Yıl içinde biriken matrah 190.000 ₺'yi aşınca vergi oranı %15'ten %20'ye, 400.000 ₺'yi aşınca %27'ye çıkar; brüt aynı kalsa da net azalır."},
        {"soru": "Brütten nete kesinti oranı yüzde kaç?", "cevap": "Sabit bir oran yoktur. Asgari ücrette %15 (yalnızca SGK+işsizlik), orta maaşlarda %20-25, yüksek maaşlarda yıl sonuna doğru %35-40'a kadar çıkabilir."},
        {"soru": "Netten brüte nasıl hesaplanır?", "cevap": "Doğrudan formül yoktur; hedef neti veren brüt, deneme-yanılma (iterasyon) ile bulunur. Aracımız seçtiğiniz ay için bunu otomatik yapar."},
        {"soru": "İşverene maliyet nasıl bulunur?", "cevap": "Brüt + SGK işveren payı (%20,5) + işsizlik işveren payı (%2). 5 puanlık prim teşviki gibi indirimler uygulanırsa maliyet düşer; araç teşviksiz genel oranı gösterir."},
        {"soru": "SGK tavanı neyi etkiler?", "cevap": "2026'da prime esas kazanç tavanı 297.270 ₺'dir (asgari ücretin 9 katı). Bu tutarın üzerindeki brüt maaştan SGK ve işsizlik primi kesilmez; yalnızca vergi hesaplanır."},
    ],
    "kaynaklar": [
        {"ad": "GİB — 2026 Gelir Vergisi Tarifesi (Tebliğ 332)", "url": "https://www.gib.gov.tr/"},
        {"ad": "SGK — 2026 prime esas kazanç alt ve üst sınırları", "url": "https://www.sgk.gov.tr/"},
        {"ad": "ÇSGB — 2026 asgari ücret", "url": "https://www.csgb.gov.tr/"},
    ],
    "ilgili": ["kidem-tazminati-hesaplama", "gelir-vergisi-hesaplama", "kdv-hesaplama"],
}
