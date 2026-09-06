# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kredi-hesaplama",
    "baslik": "Kredi Hesaplama",
    "h1": "Kredi Hesaplama — Taksit, Toplam Geri Ödeme ve Faiz (İhtiyaç, Taşıt, Konut)",
    "kategori": "kredi-finans",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Kredi hesaplama aracı: kredi tutarı, aylık faiz oranı ve vadeye göre aylık taksit, toplam geri ödeme, toplam faiz ve KKDF-BSMV dahil maliyet. İhtiyaç, taşıt ve konut kredisi için ödeme planı.",
    "kisa_cevap": "Aylık taksit = kredi × r ÷ (1 − (1 + r)^−n); r = aylık faiz (vergiler dahil), n = vade ay. İhtiyaç ve taşıt kredilerinde faize %15 KKDF + %15 BSMV eklenir (etkin faiz = faiz × 1,30); konut kredisi bu vergilerden muaftır. 100.000 ₺, %3,5 aylık, 12 ay ihtiyaç kredisinin taksiti yaklaşık 10.998 ₺, toplam geri ödemesi 131.976 ₺'dir.",
    "senaryolar": [
        {"ad": "100.000 ₺ · 12 ay", "degerler": {"tutar": "100000", "faiz": "3.5", "vade": "12", "tur": "ihtiyac"}},
        {"ad": "250.000 ₺ · 24 ay", "degerler": {"tutar": "250000", "faiz": "3.5", "vade": "24", "tur": "ihtiyac"}},
        {"ad": "500.000 ₺ · 36 ay", "degerler": {"tutar": "500000", "faiz": "3.4", "vade": "36", "tur": "ihtiyac"}},
        {"ad": "Taşıt 750.000 ₺ · 48 ay", "degerler": {"tutar": "750000", "faiz": "3.2", "vade": "48", "tur": "tasit"}},
    ],
    "girdiler": [
        {"id": "tutar", "etiket": "Kredi tutarı", "tip": "sayi", "varsayilan": "100000", "birim": "₺"},
        {"id": "faiz", "etiket": "Aylık faiz oranı", "tip": "sayi", "varsayilan": "3.5", "birim": "%"},
        {"id": "vade", "etiket": "Vade", "tip": "tamsayi", "varsayilan": "12", "birim": "ay"},
        {"id": "tur", "etiket": "Kredi türü", "tip": "secim", "varsayilan": "ihtiyac",
         "secenekler": [["ihtiyac", "İhtiyaç kredisi (KKDF %15 + BSMV %15)"], ["tasit", "Taşıt kredisi (KKDF %15 + BSMV %15)"], ["konut", "Konut kredisi (vergisiz)"]]},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.tutar > 0) || !(g.faiz >= 0) || !(g.vade > 0)) return {hata: 'Tutar, faiz ve vadeyi girin.'};
  var vergi = g.tur === 'konut' ? 0 : 0.30;
  var r = g.faiz / 100 * (1 + vergi), n = g.vade;
  var taksit = r === 0 ? g.tutar / n : g.tutar * r / (1 - Math.pow(1 + r, -n));
  var toplam = taksit * n, maliyet = toplam - g.tutar;
  var faizNet = maliyet / (1 + vergi), vergiTop = maliyet - faizNet;
  var rows = [], kalan = g.tutar, gAna = [], gFaiz = [], gKalan = [], gEt = [];
  for (var i = 1; i <= n; i++) {
    var f = kalan * r, ana = taksit - f; kalan -= ana;
    gAna.push(ana); gFaiz.push(f); gKalan.push(Math.max(0, kalan)); gEt.push(i + '. ay');
    if (i <= 12 || i === n) rows.push([i, taksit, ana, f, Math.max(0, kalan)]);
    else if (i === 13) rows.push(['…', '', '', '', '']);
  }
  var yillik = (Math.pow(1 + r, 12) - 1) * 100;
  return {
    sonuclar: [
      {etiket: 'Aylık taksit', deger: taksit, birim: '₺', vurgu: true},
      {etiket: 'Toplam geri ödeme', deger: toplam, birim: '₺'},
      {etiket: 'Toplam faiz', deger: faizNet, birim: '₺'},
      {etiket: vergi ? 'KKDF + BSMV' : 'Vergi', deger: vergiTop, birim: '₺'},
      {etiket: 'Etkin aylık faiz (vergi dahil)', deger: r * 100, birim: '%'},
      {etiket: 'Yıllık bileşik maliyet oranı', deger: yillik, birim: '%'}
    ],
    grafik: {tur: 'cizgi', baslik: 'Taksitin dağılımı: anapara artar, faiz azalır', etiketler: gEt,
             seriler: [{ad: 'Anapara', veri: gAna}, {ad: 'Faiz + vergi', veri: gFaiz, renk: '#dc2626'}, {ad: 'Kalan borç', veri: gKalan, renk: '#9ca3af'}]},
    tablo: {basliklar: ['Ay', 'Taksit', 'Anapara', 'Faiz+vergi', 'Kalan'], satirlar: rows},
    notlar: ['Dosya masrafı, hayat sigortası ve ekspertiz gibi ek ücretler dahil değildir; banka teklifinde "toplam maliyet oranı"nı karşılaştırın.']
  };
}
""",
    "nasil": [
        "Bankalar tüketici kredilerinde eşit taksitli (anüite) ödeme planı kullanır: her ay aynı tutarı ödersiniz, ancak ilk aylarda taksitin büyük kısmı faiz, son aylarda anaparadır. Taksit, kredi tutarı ile aylık faiz oranı ve vadeye bağlı anüite formülüyle bulunur.",
        "İhtiyaç ve taşıt kredilerinde faiz tutarı üzerinden %15 Kaynak Kullanımını Destekleme Fonu (KKDF) ve %15 Banka ve Sigorta Muameleleri Vergisi (BSMV) alınır; bu nedenle bankanın ilan ettiği %3,5'lik faiz, fiilen %4,55'lik etkin aylık maliyete dönüşür. Konut kredileri her iki vergiden de muaftır.",
        "Kredi tekliflerini karşılaştırırken yalnızca faiz oranına değil, dosya masrafı ve sigorta dahil 'yıllık toplam maliyet oranı'na bakın. Vade uzadıkça taksit düşer ama toplam geri ödeme artar.",
    ],
    "formul": [
        "Etkin aylık faiz r = ilan edilen faiz × (1 + KKDF + BSMV) → ihtiyaç/taşıt: × 1,30 · konut: × 1",
        "Aylık taksit = K × r ÷ (1 − (1 + r)^−n)",
        "Toplam geri ödeme = taksit × n · Toplam maliyet = toplam − K",
        "Her ay: faiz = kalan anapara × r · anapara ödemesi = taksit − faiz",
    ],
    "ornekler": [
        {"baslik": "100.000 ₺ ihtiyaç kredisi, %3,5 aylık, 12 ay", "adimlar": ["Etkin faiz: 3,5 × 1,30 = %4,55 → r = 0,0455", "Taksit: 100.000 × 0,0455 ÷ (1 − 1,0455^−12) ≈ 10.998 ₺", "Toplam: ≈ 131.976 ₺; maliyet ≈ 31.976 ₺ (faiz ≈ 24.597 + vergi ≈ 7.379)"]},
        {"baslik": "1.000.000 ₺ konut kredisi, %2,5 aylık, 120 ay", "adimlar": ["Vergi yok → r = 0,025", "Taksit: 1.000.000 × 0,025 ÷ (1 − 1,025^−120) ≈ 26.362 ₺", "Toplam ≈ 3.163.415 ₺; faiz ≈ 2.163.415 ₺"]},
    ],
    "tablo": {
        "baslik": "Kredi türüne göre vergi yükü",
        "basliklar": ["Kredi türü", "KKDF", "BSMV", "Etkin çarpan"],
        "satirlar": [["İhtiyaç kredisi", "%15", "%15", "×1,30"], ["Taşıt kredisi", "%15", "%15", "×1,30"], ["Konut kredisi", "%0", "%0", "×1,00"], ["Ticari kredi (KOBİ)", "%0", "%5", "×1,05"]],
        "not": "Oranlar faiz tutarı üzerinden uygulanır. Kamu düzenlemeleriyle değişebilir; güncel oran için BDDK ve GİB duyurularına bakın.",
    },
    "sss": [
        {"soru": "Kredi taksiti nasıl hesaplanır?", "cevap": "Anüite formülüyle: taksit = tutar × r ÷ (1 − (1+r)^−vade). r, vergiler dahil aylık faizdir. Aracımız ödeme planını da ay ay gösterir."},
        {"soru": "KKDF ve BSMV nedir?", "cevap": "İhtiyaç ve taşıt kredilerinde faiz üzerinden alınan iki kesintidir: KKDF %15, BSMV %15. Faizin %30'u kadar ek maliyet oluşturur; konut kredilerinde alınmaz."},
        {"soru": "Aylık faiz %3,5 ise yıllık faiz %42 mi?", "cevap": "Basit çarpımla %42 görünür ama bileşik etkiyle yıllık maliyet daha yüksektir; vergiler dahil %4,55 aylık faizin yıllık bileşik karşılığı yaklaşık %70,6'dır."},
        {"soru": "Erken kapatmada ne olur?", "cevap": "Kalan anaparayı ödersiniz; ödenmemiş aylara ait faiz alınmaz. Tüketici kredilerinde erken ödeme cezası bulunmaz (6502 sayılı Kanun)."},
        {"soru": "Dosya masrafı yasal mı?", "cevap": "Tüketici kredilerinde bankalar tahsis ücreti alabilir; BDDK tebliğine göre üst sınır kredi tutarının binde 5'idir. Bunun dışındaki dosya masrafı adı altında kesintiler iade konusu olabilir."},
    ],
    "kaynaklar": [
        {"ad": "BDDK — Tüketici kredisi düzenlemeleri", "url": "https://www.bddk.org.tr/"},
        {"ad": "GİB — KKDF ve BSMV oranları", "url": "https://www.gib.gov.tr/"},
        {"ad": "6502 sayılı Tüketicinin Korunması Hakkında Kanun", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6502&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["konut-kredisi-hesaplama", "elbirligi-sistemi-hesaplama", "yuzde-hesaplama"],
}
