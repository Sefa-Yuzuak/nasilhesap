# -*- coding: utf-8 -*-
HESAP = {
    "slug": "gelir-vergisi-hesaplama",
    "baslik": "Gelir Vergisi Hesaplama",
    "h1": "Gelir Vergisi Hesaplama 2026 — Vergi Dilimleri ve Oranları",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 gelir vergisi hesaplama: yıllık matraha göre ücret ve ücret dışı gelirler için dilimli vergi, efektif oran ve dilim dilim dökümü. 2026 vergi dilimleri: %15, %20, %27, %35, %40.",
    "kisa_cevap": "Gelir vergisi artan oranlı dilimlerle hesaplanır: 2026'da ilk 190.000 ₺ %15, 190.000–400.000 ₺ %20, ücretlerde 400.000–1.500.000 ₺ (diğer gelirlerde 400.000–1.000.000 ₺) %27, 5.300.000 ₺'ye kadar %35, üzeri %40. Matrahın tamamı tek orana tabi değildir; her dilim kendi oranıyla vergilenir.",
    "girdiler": [
        {"id": "matrah", "etiket": "Yıllık vergi matrahı", "tip": "sayi", "varsayilan": "600000", "birim": "₺", "ipucu": "kesintiler sonrası"},
        {"id": "tur", "etiket": "Gelir türü", "tip": "secim", "varsayilan": "ucret", "secenekler": [["ucret", "Ücret geliri"], ["diger", "Ücret dışı (kira, ticari, serbest meslek…)"]]},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.matrah >= 0)) return {hata: 'Matrahı girin.'};
  var dl = O.gelir_vergisi[g.tur], toplam = 0, alt = 0, satir = [];
  for (var i = 0; i < dl.length; i++) {
    var ust = dl[i][0] === null ? Infinity : dl[i][0], oran = dl[i][1];
    if (g.matrah > alt) {
      var dilim = Math.min(g.matrah, ust) - alt, v = dilim * oran; toplam += v;
      satir.push([NH.fmt(alt, 0) + ' – ' + (ust === Infinity ? '∞' : NH.fmt(ust, 0)) + ' ₺', '%' + Math.round(oran*100), NH.fmt(dilim) + ' ₺', NH.fmt(v) + ' ₺']);
    }
    alt = ust;
  }
  var ef = g.matrah > 0 ? toplam / g.matrah * 100 : 0;
  return {
    sonuclar: [
      {etiket: 'Yıllık gelir vergisi', deger: toplam, birim: '₺', vurgu: true},
      {etiket: 'Vergi sonrası kalan', deger: g.matrah - toplam, birim: '₺'},
      {etiket: 'Efektif (ortalama) vergi oranı', deger: ef, birim: '%'},
      {etiket: 'Marjinal (son dilim) oranı', deger: satir.length ? satir[satir.length-1][1] : '%15'}
    ],
    tablo: {basliklar: ['Dilim', 'Oran', 'Dilimdeki matrah', 'Vergi'], satirlar: satir},
    notlar: ['Ücret gelirlerinde vergi aylık kümülatif matraha göre kesilir; bu araç yıllık toplamı gösterir. Asgari ücret istisnası ve diğer indirimler dahil değildir.']
  };
}
""",
    "nasil": [
        "Gelir vergisi, artan oranlı (müterakki) bir tarifeyle hesaplanır: matrah dilimlere bölünür ve her dilim kendi oranıyla vergilenir. Yaygın yanılgı, matrahın tamamının 'girdiği dilimin' oranıyla vergilenmesidir; gerçekte 600.000 ₺ matrahın ilk 190.000 ₺'si %15, sonraki 210.000 ₺'si %20, kalan 200.000 ₺'si %27 ile vergilenir.",
        "2026 tarifesinde ücret gelirleri ile ücret dışı gelirler yalnızca üçüncü dilimde ayrışır: ücretlerde %27 dilimi 1.500.000 ₺'ye, diğer gelirlerde 1.000.000 ₺'ye kadar uygulanır. Dördüncü dilim her ikisinde de 5.300.000 ₺'de biter ve üzeri %40'tır.",
        "Ücretlilerde vergi, işveren tarafından her ay yıl başından itibaren biriken kümülatif matraha göre kesilir; yıl ilerledikçe dilim atlanır ve net maaş düşer. Ücret dışı gelirlerde (kira, serbest meslek, ticari kazanç) vergi yıllık beyannameyle Mart ayında hesaplanır ve iki taksitte (Mart-Temmuz) ödenir.",
    ],
    "formul": [
        "Vergi = Σ (her dilimdeki matrah × o dilimin oranı)",
        "Efektif oran = toplam vergi ÷ matrah × 100",
        "2026 ücret: 190.000 (%15) · 400.000 (%20) · 1.500.000 (%27) · 5.300.000 (%35) · üzeri %40",
        "2026 diğer: 190.000 (%15) · 400.000 (%20) · 1.000.000 (%27) · 5.300.000 (%35) · üzeri %40",
    ],
    "ornekler": [
        {"baslik": "600.000 ₺ yıllık ücret matrahı", "adimlar": ["190.000 × %15 = 28.500 ₺", "210.000 × %20 = 42.000 ₺", "200.000 × %27 = 54.000 ₺", "Toplam 124.500 ₺; efektif oran %20,75"]},
        {"baslik": "600.000 ₺ kira geliri matrahı (ücret dışı)", "adimlar": ["İlk iki dilim aynı: 70.500 ₺", "200.000 × %27 = 54.000 ₺ (3. dilim 1.000.000'a kadar)", "Toplam 124.500 ₺ — bu tutarda fark yok; fark 1.000.000 ₺ üzerinde başlar"]},
    ],
    "tablo": {
        "baslik": "2026 gelir vergisi tarifesi",
        "basliklar": ["Dilim (ücret)", "Dilim (ücret dışı)", "Oran"],
        "satirlar": [["0 – 190.000 ₺", "0 – 190.000 ₺", "%15"], ["190.000 – 400.000 ₺", "190.000 – 400.000 ₺", "%20"], ["400.000 – 1.500.000 ₺", "400.000 – 1.000.000 ₺", "%27"], ["1.500.000 – 5.300.000 ₺", "1.000.000 – 5.300.000 ₺", "%35"], ["5.300.000 ₺ üzeri", "5.300.000 ₺ üzeri", "%40"]],
        "not": "Resmî Gazete 31.12.2025, Sayı 33124 (5. Mükerrer) — Gelir Vergisi Genel Tebliği Seri No 332; 2025 yeniden değerleme oranı %25,49 ile güncellenmiştir.",
    },
    "sss": [
        {"soru": "2026 gelir vergisi dilimleri nedir?", "cevap": "%15 (190.000 ₺'ye kadar), %20 (400.000 ₺'ye kadar), %27 (ücrette 1.500.000, diğer gelirlerde 1.000.000 ₺'ye kadar), %35 (5.300.000 ₺'ye kadar) ve %40 (üzeri)."},
        {"soru": "Vergi dilimi atlayınca tüm maaşım daha yüksek oranla mı vergilenir?", "cevap": "Hayır. Yalnızca üst sınırı aşan kısım yeni oranla vergilenir; alt dilimler kendi oranlarını korur. Bu yüzden zam almak hiçbir zaman net gelirinizi düşürmez."},
        {"soru": "Ücret ile diğer gelirlerde tarife neden farklı?", "cevap": "Ücretliler lehine üçüncü dilim daha geniş tutulmuştur (1.500.000 ₺'ye kadar %27). Diğer gelirlerde %35 dilimi 1.000.000 ₺'de başlar."},
        {"soru": "Gelir vergisi beyannamesi ne zaman verilir?", "cevap": "Bir önceki yılın gelirleri için Mart ayında (1-31 Mart) verilir; vergi Mart ve Temmuz aylarında iki eşit taksitte ödenir. Tek işverenden ücret alanlar genellikle beyanname vermez."},
        {"soru": "Efektif vergi oranı ne demek?", "cevap": "Toplam ödediğiniz verginin matraha oranıdır; marjinal oran ise son diliminizin oranıdır. 600.000 ₺ matrahta marjinal %27 iken efektif oran %20,75'tir."},
    ],
    "kaynaklar": [
        {"ad": "GİB — Gelir Vergisi Tarifesi 2026 (PDF)", "url": "https://www.gib.gov.tr/"},
        {"ad": "193 sayılı Gelir Vergisi Kanunu m.103", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=193&MevzuatTur=1&MevzuatTertip=4"},
    ],
    "ilgili": ["brut-net-maas-hesaplama", "kira-geliri-vergisi-hesaplama", "kdv-hesaplama"],
}
