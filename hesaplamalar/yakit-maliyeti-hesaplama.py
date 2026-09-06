# -*- coding: utf-8 -*-
HESAP = {
    "slug": "yakit-maliyeti-hesaplama",
    "baslik": "Yakıt Maliyeti Hesaplama",
    "h1": "Yakıt Maliyeti Hesaplama — Yol Masrafı, Litre Tüketimi ve Kişi Başı Pay",
    "kategori": "gunluk",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Yol yakıt maliyeti hesaplama: mesafe, 100 km'de ortalama tüketim ve litre fiyatına göre harcanacak yakıt, toplam maliyet, gidiş-dönüş, kişi başı pay ve km başına maliyet.",
    "kisa_cevap": "Yakıt maliyeti = (mesafe ÷ 100) × 100 km'deki tüketim × litre fiyatı. 450 km yol, 100 km'de 7 litre tüketen ve litresi 50 ₺ olan bir araçta 31,5 litre yakıt, 1.575 ₺ maliyet çıkar; gidiş-dönüş 3.150 ₺'dir. 4 kişi paylaşırsa kişi başı 787,50 ₺ olur.",
    "senaryolar": [
        {"ad": "Ankara–İstanbul (450 km)", "degerler": {"mesafe": "450", "tuketim": "7", "fiyat": "50", "gidis_donus": True, "kisi": "1"}},
        {"ad": "İstanbul–İzmir (480 km) · 4 kişi", "degerler": {"mesafe": "480", "tuketim": "7", "fiyat": "50", "gidis_donus": True, "kisi": "4"}},
        {"ad": "Günlük işe gidiş (30 km)", "degerler": {"mesafe": "30", "tuketim": "8", "fiyat": "50", "gidis_donus": True, "kisi": "1"}},
        {"ad": "LPG'li araç (uzun yol)", "degerler": {"mesafe": "450", "tuketim": "9", "fiyat": "27", "gidis_donus": True, "kisi": "1"}},
    ],
    "girdiler": [
        {"id": "mesafe", "etiket": "Mesafe (tek yön)", "tip": "sayi", "varsayilan": "450", "birim": "km"},
        {"id": "tuketim", "etiket": "100 km'de ortalama tüketim", "tip": "sayi", "varsayilan": "7", "birim": "L", "ipucu": "aracın ortalaması"},
        {"id": "fiyat", "etiket": "Yakıt litre fiyatı", "tip": "sayi", "varsayilan": "50", "birim": "₺"},
        {"id": "gidis_donus", "etiket": "Yolculuk", "tip": "onay", "varsayilan": True, "onay_metin": "Gidiş-dönüş hesapla"},
        {"id": "kisi", "etiket": "Masrafı paylaşan kişi sayısı", "tip": "tamsayi", "varsayilan": "1", "birim": "kişi"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.mesafe > 0)) return {hata: 'Mesafeyi girin.'};
  if (!(g.tuketim > 0)) return {hata: '100 km\'deki ortalama tüketimi girin.'};
  if (!(g.fiyat > 0)) return {hata: 'Litre fiyatını girin.'};
  var kat = g.gidis_donus ? 2 : 1, toplamKm = g.mesafe * kat;
  var litre = toplamKm / 100 * g.tuketim, maliyet = litre * g.fiyat;
  var kisi = g.kisi > 0 ? g.kisi : 1;
  var kmMaliyet = maliyet / toplamKm;
  var s = [
    {etiket: (kat === 2 ? 'Gidiş-dönüş' : 'Tek yön') + ' toplam yakıt maliyeti', deger: maliyet, birim: '₺', vurgu: true},
    {etiket: 'Toplam mesafe', deger: toplamKm, birim: 'km'},
    {etiket: 'Harcanacak yakıt', deger: litre, birim: 'litre'},
    {etiket: 'Kilometre başına maliyet', deger: kmMaliyet, birim: '₺/km'},
    {etiket: 'Tek yön maliyeti', deger: maliyet / kat, birim: '₺'}
  ];
  if (kisi > 1) s.push({etiket: kisi + ' kişide kişi başı', deger: maliyet / kisi, birim: '₺'});
  s.push({etiket: 'Aylık (20 iş günü gidiş-dönüş varsayımı)', deger: (g.mesafe * 2 / 100 * g.tuketim * g.fiyat) * 20, birim: '₺'});
  // tüketim senaryoları
  var sat = [], et = [], vr = [];
  for (var t = Math.max(3, Math.round(g.tuketim) - 3); t <= Math.round(g.tuketim) + 4; t++) {
    var m = toplamKm / 100 * t * g.fiyat;
    sat.push([t + ' L/100km', Math.round(toplamKm / 100 * t * 100) / 100 + ' L', m]);
    et.push(t + 'L'); vr.push(Math.round(m));
  }
  return {sonuclar: s,
    tablo: {basliklar: ['Tüketim', 'Yakıt', 'Maliyet'], satirlar: sat},
    grafik: {tur: 'cizgi', baslik: '100 km tüketimine göre toplam maliyet', etiketler: et, seriler: [{ad: 'Maliyet (₺)', veri: vr}]},
    notlar: ['Gerçek tüketim; hız, klima, yük, lastik basıncı, yol eğimi ve şehir içi/dışı farkına göre değişir. Şehir içinde tüketim genelde %20-40 daha yüksektir.',
             'Köprü, otoyol ve tünel geçiş ücretleri ile park masrafı dahil değildir; uzun yolda bunları ayrıca ekleyin.',
             'Aracınızın gerçek ortalamasını bilmiyorsanız depo dolduğunda kilometre sayacını sıfırlayıp bir sonraki dolumda (alınan litre ÷ gidilen km) × 100 ile ölçebilirsiniz.']};
}
""",
    "nasil": [
        "Yol yakıt maliyeti üç değerden hesaplanır: gidilecek mesafe, aracın 100 kilometrede ortalama kaç litre yaktığı ve yakıtın litre fiyatı. Önce mesafe 100'e bölünüp tüketimle çarpılarak harcanacak litre bulunur, sonra litre fiyatıyla çarpılarak toplam maliyet elde edilir.",
        "Aracınızın gerçek ortalama tüketimini bilmek hesabın doğruluğu için kritiktir. Ölçmek için depoyu doldurun, kilometre sayacını sıfırlayın; bir sonraki tam dolumda alınan litreyi gidilen kilometreye bölüp 100 ile çarpın. Üretici verileri genellikle laboratuvar koşullarına aittir ve gerçek kullanımda %10-20 daha yüksek tüketim görülür.",
        "Şehir içi sürüşte dur-kalk nedeniyle tüketim şehirlerarası yola göre belirgin biçimde artar; klima kullanımı, yüksek hız (110 km/s üzeri), tavan bagajı, düşük lastik basıncı ve ağır yük de tüketimi yükseltir. Toplam yol bütçesi hesaplarken köprü-otoyol geçiş ücretlerini ve park masrafını ayrıca eklemeyi unutmayın.",
    ],
    "formul": [
        "Harcanan yakıt (litre) = (mesafe ÷ 100) × 100 km tüketimi",
        "Yakıt maliyeti = harcanan litre × litre fiyatı",
        "Gidiş-dönüş = tek yön × 2",
        "Kişi başı = toplam maliyet ÷ kişi sayısı · km başına = toplam ÷ toplam km",
    ],
    "ornekler": [
        {"baslik": "450 km, 7 L/100km, 50 ₺/L (tek yön)", "adimlar": ["Yakıt: 450 ÷ 100 × 7 = 31,5 litre", "Maliyet: 31,5 × 50 = 1.575 ₺", "Km başına: 3,50 ₺"]},
        {"baslik": "Aynı yol gidiş-dönüş, 4 kişi", "adimlar": ["Toplam: 3.150 ₺", "Kişi başı: 787,50 ₺"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Yakıt maliyeti nasıl hesaplanır?", "cevap": "Mesafeyi 100'e bölün, aracın 100 km tüketimiyle çarpın, çıkan litreyi litre fiyatıyla çarpın. 300 km, 6 L/100km, 50 ₺ → 18 litre × 50 = 900 ₺."},
        {"soru": "Aracımın ortalama tüketimini nasıl öğrenirim?", "cevap": "Depoyu doldurup km sayacını sıfırlayın; bir sonraki tam dolumda (alınan litre ÷ gidilen km) × 100 formülüyle bulun. Araç bilgisayarındaki ortalama genelde iyimserdir."},
        {"soru": "Şehir içi ve şehirlerarası tüketim farkı ne kadar?", "cevap": "Şehir içinde dur-kalk nedeniyle genellikle %20-40 daha fazla yakıt harcanır. Uzun yolda sabit hızda tüketim düşer."},
        {"soru": "LPG'li araçta hesap değişir mi?", "cevap": "Formül aynıdır ama LPG tüketimi benzine göre yaklaşık %20-25 daha yüksektir; litre fiyatı düşük olduğu için toplam maliyet yine de daha azdır. Tüketim alanına LPG ortalamanızı girin."},
        {"soru": "Köprü ve otoyol ücretleri dahil mi?", "cevap": "Hayır, yalnızca yakıt hesaplanır. HGS/OGS geçiş ücretlerini ve varsa park masrafını ayrıca ekleyin."},
    ],
    "kaynaklar": [
        {"ad": "EPDK — Akaryakıt fiyatları ve piyasa verileri", "url": "https://www.epdk.gov.tr/"},
    ],
    "ilgili": ["yuzde-hesaplama", "birim-cevirici", "mtv-hesaplama"],
}
