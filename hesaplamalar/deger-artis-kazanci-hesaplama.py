# -*- coding: utf-8 -*-
HESAP = {
    "slug": "deger-artis-kazanci-hesaplama",
    "baslik": "Değer Artış Kazancı Vergisi Hesaplama",
    "h1": "Değer Artış Kazancı Vergisi Hesaplama 2026 — 5 Yıl İçinde Ev Satışında Vergi",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Gayrimenkulü alış tarihinden itibaren 5 yıl içinde satanlar için değer artış kazancı vergisi: Yİ-ÜFE endekslemesi (%10 şartı), 2026 istisnası 150.000 ₺, masraf indirimi ve gelir vergisi tarifesiyle ödenecek vergi.",
    "kisa_cevap": "Konut, arsa gibi taşınmazlar iktisap tarihinden itibaren 5 yıl içinde satılırsa satış bedeli ile endekslenmiş alış bedeli arasındaki fark 'değer artış kazancı' olarak vergilenir; 5 yıl dolduysa vergi yoktur. Alış bedeli, Yİ-ÜFE artışı %10 veya üzerindeyse endekslenir; masraflar düşülür; 2026 için 150.000 ₺ istisna uygulanır ve kalan kazanç gelir vergisi tarifesiyle (%15'ten başlar) vergilenir.",
    "girdiler": [
        {"id": "alis", "etiket": "Alış bedeli (tapuda)", "tip": "sayi", "varsayilan": "2000000", "birim": "₺"},
        {"id": "satis", "etiket": "Satış bedeli", "tip": "sayi", "varsayilan": "4000000", "birim": "₺"},
        {"id": "alis_t", "etiket": "Alış (tapu) tarihi", "tip": "tarih", "varsayilan": "2023-03-15"},
        {"id": "satis_t", "etiket": "Satış tarihi", "tip": "tarih", "varsayilan": "2026-09-01"},
        {"id": "ufe1", "etiket": "Yİ-ÜFE — alış ayından önceki ay", "tip": "sayi", "varsayilan": "", "ipucu": "TÜİK endeks değeri"},
        {"id": "ufe2", "etiket": "Yİ-ÜFE — satış ayından önceki ay", "tip": "sayi", "varsayilan": "", "ipucu": "TÜİK endeks değeri"},
        {"id": "masraf", "etiket": "Belgeli masraflar (tapu harcı, komisyon, tadilat)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
    ],
    "js": r"""
function vergiHesap(matrah, dl){ var v=0, alt=0; for (var i=0;i<dl.length;i++){ var ust=dl[i][0]===null?Infinity:dl[i][0]; if(matrah>alt) v+=(Math.min(matrah,ust)-alt)*dl[i][1]; alt=ust; } return v; }
function hesapla(g, O){
  if (!(g.alis > 0) || !(g.satis > 0)) return {hata: 'Alış ve satış bedellerini girin.'};
  if (!g.alis_t || !g.satis_t) return {hata: 'Alış ve satış tarihlerini seçin.'};
  var a = new Date(g.alis_t + 'T00:00:00'), s = new Date(g.satis_t + 'T00:00:00');
  if (s <= a) return {hata: 'Satış tarihi alış tarihinden sonra olmalı.'};
  var D = O.deger_artis, n = [];
  var besYil = new Date(a); besYil.setFullYear(besYil.getFullYear() + D.sure_yil);
  var gun = Math.round((s - a) / 86400000);
  if (s >= besYil) return {sonuclar: [{etiket: 'Değer artış kazancı vergisi', deger: 'Yok — 5 yıl dolmuş', vurgu: true}, {etiket: 'Elde tutma süresi', deger: Math.floor(gun / 365) + ' yıl ' + Math.floor((gun % 365) / 30) + ' ay'}], notlar: ['İktisap tarihinden itibaren 5 yıl geçtikten sonra yapılan satışlar değer artış kazancı vergisine tabi değildir (GVK mük. m.80/6). Ticari faaliyet kapsamındaki (sık alım-satım) satışlar ayrıca değerlendirilir.']};
  var endeksli = g.alis, artis = null;
  if (g.ufe1 > 0 && g.ufe2 > 0) {
    artis = g.ufe2 / g.ufe1 - 1;
    if (artis >= D.endeks_esik) { endeksli = g.alis * g.ufe2 / g.ufe1; n.push('Yİ-ÜFE artışı %' + (artis*100).toFixed(2) + ' ≥ %10 → alış bedeli endekslendi.'); }
    else n.push('Yİ-ÜFE artışı %' + (artis*100).toFixed(2) + ' < %10 → endeksleme yapılamaz.');
  } else n.push('ÜFE endeks değerleri girilmediği için endeksleme yapılmadı; gerçek vergi daha düşük olabilir. TÜİK Yİ-ÜFE (2003=100) alış ve satış aylarından önceki ay değerlerini girin.');
  var masraf = g.masraf > 0 ? g.masraf : 0;
  var kazanc = Math.max(0, g.satis - endeksli - masraf);
  var matrah = Math.max(0, kazanc - D.istisna);
  var vergi = vergiHesap(matrah, O.gelir_vergisi.diger);
  n.push('Beyanname satışı izleyen yılın Mart ayında verilir; vergi Mart ve Temmuz\'da iki taksitte ödenir. Miras/bağış yoluyla edinilen taşınmazların satışında vergi yoktur.');
  return {
    sonuclar: [
      {etiket: 'Ödenecek gelir vergisi', deger: vergi, birim: '₺', vurgu: true},
      {etiket: 'Elde tutma süresi', deger: Math.floor(gun / 365) + ' yıl ' + Math.floor((gun % 365) / 30) + ' ay (5 yıl dolmamış)'},
      {etiket: 'Endekslenmiş alış bedeli', deger: endeksli, birim: '₺'},
      {etiket: 'Safi kazanç (satış − endeksli alış − masraf)', deger: kazanc, birim: '₺'},
      {etiket: 'İstisna (2026)', deger: Math.min(D.istisna, kazanc), birim: '₺'},
      {etiket: 'Vergi matrahı', deger: matrah, birim: '₺'},
      {etiket: 'Efektif vergi / kazanç', deger: kazanc > 0 ? vergi / kazanc * 100 : 0, birim: '%'}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "Gelir Vergisi Kanunu mükerrer 80. maddeye göre, ivazlı (bedel karşılığı) edinilen taşınmazlar iktisap tarihinden itibaren beş yıl içinde elden çıkarılırsa doğan kazanç 'değer artış kazancı' olarak vergilenir. Beş yıl dolduktan sonra yapılan satışlarda tutar ne olursa olsun vergi yoktur; miras ve bağışla edinilen taşınmazlar ise süreye bakılmaksızın kapsam dışıdır.",
        "Kazanç hesaplanırken alış bedeli, alış ve satış aylarından önceki ayların Yİ-ÜFE endeksleri oranında artırılır (endeksleme); ancak bu artışın %10 veya üzerinde olması şarttır. Endekslenmiş alış bedeli ile tapu harcı, komisyon ve belgeli tadilat gibi masraflar satış bedelinden düşülür; kalan safi kazançtan yıllık istisna (2026 için 150.000 ₺) indirilir.",
        "İstisna sonrası kalan tutar, ücret dışı gelirler için geçerli tarifeyle (%15'ten %40'a) vergilenir ve satışı izleyen yılın Mart ayında beyan edilir. Tapuda düşük bedel gösterilerek kazancın azaltılması, GİB'in banka ve kredi verileriyle yaptığı çapraz kontrollerde cezalı tarhiyata yol açabilir; satış bedeli gerçek bedel olmalıdır.",
    ],
    "formul": [
        "Süre kontrolü: satış tarihi < alış tarihi + 5 yıl ise vergiye tabi",
        "Endeksli alış = alış bedeli × (satış öncesi ay Yİ-ÜFE ÷ alış öncesi ay Yİ-ÜFE)   [artış ≥ %10 ise]",
        "Safi kazanç = satış bedeli − endeksli alış − belgeli masraflar",
        "Matrah = safi kazanç − 150.000 ₺ istisna · Vergi = matrah × 2026 ücret dışı tarife",
    ],
    "ornekler": [
        {"baslik": "2.000.000 ₺'ye alınan ev 3,5 yıl sonra 4.000.000 ₺'ye satıldı; ÜFE artışı %85", "adimlar": ["Endeksli alış: 2.000.000 × 1,85 = 3.700.000 ₺", "Safi kazanç: 4.000.000 − 3.700.000 = 300.000 ₺; istisna sonrası matrah 150.000 ₺", "Vergi: 150.000 × %15 = 22.500 ₺"]},
        {"baslik": "Aynı satış, endeks değerleri girilmezse", "adimlar": ["Kazanç 2.000.000 ₺; matrah 1.850.000 ₺", "Vergi ≈ 28.500 + 42.000 + 162.000 + 297.500 = 530.000 ₺ — endekslemenin önemi"]},
    ],
    "tablo": {
        "baslik": "2026 değer artış kazancı parametreleri",
        "basliklar": ["Kalem", "Değer"],
        "satirlar": [["Vergiye tabi elde tutma süresi", "5 yıldan az"], ["Yıllık istisna (2026)", "150.000 ₺"], ["Endeksleme şartı", "Yİ-ÜFE artışı ≥ %10"], ["Endeks", "Yİ-ÜFE (2003=100), alış/satış aylarından önceki ay"], ["Vergi tarifesi", "Ücret dışı gelirler (%15 – %40)"], ["Beyan / ödeme", "Mart; Mart ve Temmuz taksitleri"], ["Kapsam dışı", "Miras, bağış; 5 yılı dolan satışlar"]],
        "not": "GVK mükerrer m.80/6 ve m.81; Gelir Vergisi Genel Tebliği Seri No 332.",
    },
    "sss": [
        {"soru": "Evi 5 yıl dolmadan satarsam vergi öder miyim?", "cevap": "Evet, endekslenmiş alış bedeli ile satış bedeli arasındaki fark 150.000 ₺ istisnayı aşarsa aşan kısım vergilenir. 5 yıl dolduktan sonra vergi yoktur."},
        {"soru": "5 yıl hangi tarihten başlar?", "cevap": "Tapuda iktisap (tescil) tarihinden. Kat karşılığı veya kooperatiften edinilenlerde fiili kullanım/tahsis tarihi esas alınabilir; müteahhitten alımda tapu tarihi geçerlidir."},
        {"soru": "ÜFE endeks değerlerini nereden bulurum?", "cevap": "TÜİK veri portalında Yİ-ÜFE (2003=100) aylık tablosundan; alış ayından önceki ay ve satış ayından önceki ay değerlerini alın."},
        {"soru": "Miras kalan evi hemen satsam vergi var mı?", "cevap": "Hayır. Miras ve bağış yoluyla edinilen taşınmazların satışı değer artış kazancı kapsamında değildir (veraset ve intikal vergisi ayrıdır)."},
        {"soru": "Sık ev alıp satarsam durum değişir mi?", "cevap": "Evet. Aynı yıl içinde birden fazla veya süreklilik arz eden alım-satım ticari kazanç sayılabilir; o zaman 5 yıl kuralı ve istisna uygulanmaz."},
    ],
    "kaynaklar": [
        {"ad": "193 sayılı GVK mükerrer m.80, m.81 (değer artışı kazançları)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=193&MevzuatTur=1&MevzuatTertip=4"},
        {"ad": "TÜİK — Yurt İçi Üretici Fiyat Endeksi (Yİ-ÜFE)", "url": "https://data.tuik.gov.tr/"},
        {"ad": "GİB — Değer Artış Kazancı Rehberi", "url": "https://www.gib.gov.tr/"},
    ],
    "ilgili": ["tapu-harci-hesaplama", "gelir-vergisi-hesaplama", "kira-geliri-vergisi-hesaplama", "enflasyon-hesaplama"],
}
