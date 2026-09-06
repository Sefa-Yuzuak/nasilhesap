# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kira-geliri-vergisi-hesaplama",
    "baslik": "Kira Geliri Vergisi Hesaplama",
    "h1": "Kira Geliri Vergisi Hesaplama 2026 — Konut ve İş Yeri Kira Beyanı",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 kira geliri vergisi hesaplama: konut kira istisnası (58.000 ₺), götürü gider (%15) veya gerçek gider, iş yeri kirasında %20 stopaj mahsubu, 2026 gelir vergisi dilimleriyle ödenecek vergi ve taksitler.",
    "kisa_cevap": "Konut kira gelirinden 2026 istisnası 58.000 ₺ düşülür, kalanın %15'i götürü gider olarak indirilir ve matrah gelir vergisi tarifesiyle (%15'ten başlayan) vergilenir. 300.000 ₺ yıllık konut kirasında matrah (300.000 − 58.000) × 0,85 = 205.700 ₺, vergi ≈ 31.640 ₺'dir. İş yerinde istisna yoktur; kiracının kestiği %20 stopaj vergiden mahsup edilir.",
    "girdiler": [
        {"id": "tur", "etiket": "Kira türü", "tip": "secim", "varsayilan": "konut", "secenekler": [["konut", "Konut (mesken)"], ["isyeri", "İş yeri (stopajlı)"]]},
        {"id": "kira", "etiket": "Yıllık toplam kira geliri (brüt)", "tip": "sayi", "varsayilan": "300000", "birim": "₺"},
        {"id": "gider", "etiket": "Gider yöntemi", "tip": "secim", "varsayilan": "goturu", "secenekler": [["goturu", "Götürü gider (%15)"], ["gercek", "Gerçek gider"]]},
        {"id": "gider_tutar", "etiket": "Belgeli gerçek gider", "tip": "sayi", "varsayilan": "0", "birim": "₺", "gizli": "gider=gercek"},
    ],
    "js": r"""
function vergiHesap(matrah, dl){ var v=0, alt=0; for (var i=0;i<dl.length;i++){ var ust=dl[i][0]===null?Infinity:dl[i][0]; if(matrah>alt) v+=(Math.min(matrah,ust)-alt)*dl[i][1]; alt=ust; } return v; }
function hesapla(g, O){
  if (!(g.kira > 0)) return {hata: 'Yıllık kira gelirini girin.'};
  var istisna = g.tur === 'konut' ? Math.min(O.kira_geliri_istisna.tutar, g.kira) : 0;
  var kalan = g.kira - istisna, gider;
  if (g.gider === 'goturu') gider = kalan * 0.15;
  else { // gerçek gider: istisnaya isabet eden kısım indirilemez
    var gd = g.gider_tutar > 0 ? g.gider_tutar : 0;
    gider = Math.min(kalan, gd * (g.kira > 0 ? kalan / g.kira : 1));
  }
  var matrah = Math.max(0, kalan - gider);
  var vergi = vergiHesap(matrah, O.gelir_vergisi.diger);
  var stopaj = g.tur === 'isyeri' ? g.kira * 0.20 : 0;
  var odenecek = vergi - stopaj;
  var s = [
    {etiket: odenecek >= 0 ? 'Ödenecek gelir vergisi' : 'İade alınacak stopaj', deger: Math.abs(odenecek), birim: '₺', vurgu: true},
    {etiket: 'Hesaplanan gelir vergisi', deger: vergi, birim: '₺'},
    {etiket: 'İstisna', deger: istisna, birim: '₺'},
    {etiket: g.gider === 'goturu' ? 'Götürü gider (%15)' : 'İndirilebilir gerçek gider', deger: gider, birim: '₺'},
    {etiket: 'Vergi matrahı', deger: matrah, birim: '₺'}
  ];
  if (stopaj) s.push({etiket: 'Kiracının kestiği stopaj (%20)', deger: stopaj, birim: '₺'});
  if (odenecek > 0) { s.push({etiket: '1. taksit (Mart)', deger: odenecek/2, birim: '₺'}); s.push({etiket: '2. taksit (Temmuz)', deger: odenecek/2, birim: '₺'}); }
  var n = ['Beyanname Mart ayında verilir; vergi Mart ve Temmuz aylarında iki taksitte ödenir. Damga vergisi (beyanname) dahil değildir.'];
  if (g.tur === 'konut') n.push('Konut istisnası, beyanı gereken tüm gelirlerin (ücret dahil) brüt toplamı 2026 için 1.500.000 ₺\'yi aşanlara uygulanmaz. Ticari/zirai/mesleki kazancı olanlar da istisnadan yararlanamaz.');
  else n.push('Stopajlı iş yeri kirası, 2026 beyan sınırı olan 400.000 ₺\'yi aşmıyorsa beyanname verilmez; stopaj nihai vergi olur.');
  if (g.gider === 'gercek') n.push('Gerçek giderde istisnaya isabet eden gider kısmı indirilemez; araç bu oranlamayı yapmıştır. Gerçek gider seçen mükellef 2 yıl götürüye dönemez.');
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Kira geliri (gayrimenkul sermaye iradı) yıllık gelir vergisi beyannamesiyle beyan edilir. Konut kiralarında 2026 için 58.000 ₺'lik istisna vardır: yıllık konut kira geliri bu tutarın altındaysa beyanname verilmez; üstündeyse istisna düşülüp kalan vergilenir. İş yeri kiralarında istisna yoktur, ancak kiracı (işletme) ödediği kiradan %20 stopaj keser ve bu stopaj hesaplanan vergiden mahsup edilir.",
        "Giderler iki yöntemle indirilir: götürü giderde istisna sonrası kalan hasılatın %15'i belge aranmadan düşülür; gerçek giderde ise faiz, sigorta, amortisman, aidat, onarım gibi belgeli giderler indirilir (istisnaya isabet eden kısım hariç). Gerçek gider seçen mükellef iki yıl boyunca götürüye dönemez.",
        "Kalan matrah, ücret dışı gelirler için geçerli 2026 tarifesiyle (190.000 ₺'ye kadar %15, 400.000 ₺'ye kadar %20, 1.000.000 ₺'ye kadar %27, 5.300.000 ₺'ye kadar %35, üzeri %40) vergilenir. Beyanname takip eden yılın Mart ayında verilir; vergi Mart ve Temmuz'da iki eşit taksitte ödenir. Stopajlı iş yeri kirası toplamı 2026 beyan sınırı olan 400.000 ₺'yi aşmıyorsa beyanname verilmez.",
    ],
    "formul": [
        "Konut: matrah = (yıllık kira − 58.000 istisna) × (1 − %15 götürü gider)",
        "İş yeri: matrah = yıllık kira × (1 − %15) · ödenecek = hesaplanan vergi − kesilen stopaj (%20)",
        "Vergi = matrah × 2026 ücret dışı tarife (dilimli)",
        "Taksit = ödenecek vergi ÷ 2 (Mart, Temmuz)",
    ],
    "ornekler": [
        {"baslik": "300.000 ₺ yıllık konut kirası, götürü gider", "adimlar": ["İstisna: 300.000 − 58.000 = 242.000 ₺", "Götürü gider: 242.000 × 0,15 = 36.300 ₺ → matrah 205.700 ₺", "Vergi: 190.000 × %15 + 15.700 × %20 = 28.500 + 3.140 = 31.640 ₺", "Taksitler: Mart 15.820 ₺, Temmuz 15.820 ₺"]},
        {"baslik": "600.000 ₺ yıllık iş yeri kirası (stopajlı)", "adimlar": ["Stopaj: 600.000 × %20 = 120.000 ₺ (kiracı ödedi)", "Matrah: 600.000 × 0,85 = 510.000 ₺ → vergi 28.500 + 42.000 + 29.700 = 100.200 ₺", "Ödenecek: 100.200 − 120.000 = −19.800 ₺ → 19.800 ₺ iade"]},
    ],
    "tablo": {
        "baslik": "2026 kira geliri beyanı parametreleri",
        "basliklar": ["Kalem", "2026 değeri"],
        "satirlar": [["Konut kira istisnası", "58.000 ₺"], ["Götürü gider oranı", "%15"], ["İş yeri kira stopajı", "%20"], ["Stopajlı gelirlerde beyan sınırı", "400.000 ₺"], ["İstisnadan yararlanma üst sınırı (toplam gelir)", "1.500.000 ₺"], ["Beyan dönemi", "1–31 Mart 2027 (2026 gelirleri)"], ["Ödeme", "Mart ve Temmuz, 2 taksit"]],
        "not": "GVK m.21, m.74, m.86, m.103; Gelir Vergisi Genel Tebliği Seri No 332 (RG 33124, 5. Mük.).",
    },
    "sss": [
        {"soru": "Kira geliri kaç TL'den sonra vergiye tabi?", "cevap": "Konutta 2026 yılı için yıllık 58.000 ₺'yi aşan kira geliri beyan edilir. İş yeri kirasında istisna yoktur; stopajlı gelir 400.000 ₺'yi aşınca beyanname verilir."},
        {"soru": "Götürü gider mi gerçek gider mi?", "cevap": "Kredi faizi, büyük onarım, sigorta gibi yüksek belgeli gideriniz yoksa götürü (%15) pratiktir. Yeni alınan konutta 5 yıl boyunca iktisap bedelinin %5'i de gerçek giderde indirilebilir; bu durumda gerçek gider avantajlı olabilir."},
        {"soru": "Kirayı bankadan almak zorunlu mu?", "cevap": "Evet: konut kiralarında 500 ₺ ve üzeri, iş yeri kiralarında tüm ödemeler banka/PTT üzerinden yapılmalıdır; aksi halde özel usulsüzlük cezası uygulanır."},
        {"soru": "Boş kalan aylar için vergi ödenir mi?", "cevap": "Hayır, yalnızca fiilen tahsil edilen kira beyan edilir. Ancak akrabaya bedelsiz/düşük kiraya verilen konutlarda emsal kira bedeli (vergi değerinin %5'i) esas alınabilir."},
        {"soru": "Kira gelirimi beyan etmezsem ne olur?", "cevap": "GİB, banka ve tapu verileriyle tespit ederse vergi ziyaı cezası (1 kat), gecikme faizi ve usulsüzlük cezası uygulanır; pişmanlıkla beyanda ceza kesilmez."},
    ],
    "kaynaklar": [
        {"ad": "GİB — Kira Geliri Elde Eden Mükellefler İçin Vergi Rehberi", "url": "https://www.gib.gov.tr/"},
        {"ad": "193 sayılı Gelir Vergisi Kanunu m.21, m.74, m.86", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=193&MevzuatTur=1&MevzuatTertip=4"},
    ],
    "ilgili": ["kira-artis-orani-hesaplama", "gelir-vergisi-hesaplama", "emlak-vergisi-hesaplama"],
}
