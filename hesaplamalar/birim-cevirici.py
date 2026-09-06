# -*- coding: utf-8 -*-
_U = [
    ("uzunluk", [("mm", "milimetre"), ("cm", "santimetre"), ("m", "metre"), ("km", "kilometre"), ("inc", "inç"), ("fit", "fit (feet)"), ("yarda", "yarda"), ("mil", "mil"), ("dmil", "deniz mili")]),
    ("agirlik", [("mg", "miligram"), ("g", "gram"), ("kg", "kilogram"), ("ton", "ton"), ("ons", "ons"), ("libre", "libre (pound)")]),
    ("hacim", [("ml", "mililitre"), ("l", "litre"), ("m3", "metreküp"), ("galon", "galon (US)"), ("bardak", "su bardağı (200 ml)"), ("ck", "çay kaşığı"), ("yk", "yemek kaşığı")]),
    ("alan", [("cm2", "santimetrekare"), ("m2", "metrekare"), ("donum", "dönüm (dekar)"), ("hektar", "hektar"), ("km2", "kilometrekare"), ("fit2", "fit kare"), ("akre", "akre")]),
    ("hiz", [("ms", "metre/saniye"), ("kmh", "km/saat"), ("mph", "mil/saat"), ("knot", "knot")]),
    ("sicaklik", [("c", "°C"), ("f", "°F"), ("k", "Kelvin")]),
]
_SEC = [[k, f"{ad}"] for kat, liste in _U for k, ad in liste]

HESAP = {
    "slug": "birim-cevirici",
    "baslik": "Birim Çevirici",
    "h1": "Birim Çevirici — Uzunluk, Ağırlık, Hacim, Alan, Hız ve Sıcaklık Dönüştürme",
    "kategori": "gunluk",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Birim çevirici: km-mil, inç-cm, kg-libre, litre-galon, dönüm-m², km/saat-knot, °C-°F dönüşümleri anında. Dönüm, dekar, hektar gibi Türkiye'ye özgü birimler dahil.",
    "kisa_cevap": "Birim çevirmek için değer, kaynak birimin temel birime oranıyla çarpılıp hedef birimin oranına bölünür. 1 mil = 1,609 km, 1 inç = 2,54 cm, 1 libre = 0,4536 kg, 1 galon (US) = 3,785 L, 1 dönüm = 1.000 m², 1 knot = 1,852 km/sa; °F = °C × 1,8 + 32.",
    "girdiler": [
        {"id": "deger", "etiket": "Değer", "tip": "sayi", "varsayilan": "1"},
        {"id": "kaynak", "etiket": "Birimden", "tip": "secim", "varsayilan": "km", "secenekler": _SEC},
        {"id": "hedef", "etiket": "Birime", "tip": "secim", "varsayilan": "mil", "secenekler": _SEC},
    ],
    "js": r"""
var B = {
  uzunluk: {mm: 0.001, cm: 0.01, m: 1, km: 1000, inc: 0.0254, fit: 0.3048, yarda: 0.9144, mil: 1609.344, dmil: 1852},
  agirlik: {mg: 1e-6, g: 0.001, kg: 1, ton: 1000, ons: 0.028349523, libre: 0.45359237},
  hacim: {ml: 0.001, l: 1, m3: 1000, galon: 3.785411784, bardak: 0.2, ck: 0.005, yk: 0.015},
  alan: {cm2: 0.0001, m2: 1, donum: 1000, hektar: 10000, km2: 1e6, fit2: 0.09290304, akre: 4046.8564224},
  hiz: {ms: 1, kmh: 1/3.6, mph: 0.44704, knot: 0.514444},
  sicaklik: {c: 1, f: 1, k: 1}
};
function kat(u){ for (var k in B) if (B[k][u] !== undefined) return k; return null; }
function hesapla(g){
  if (isNaN(g.deger)) return {hata: 'Değer girin.'};
  var k1 = kat(g.kaynak), k2 = kat(g.hedef);
  if (k1 !== k2) return {hata: 'İki birim de aynı türden olmalı (ör. km → mil). Seçili: ' + k1 + ' → ' + k2 + '.'};
  var sonuc;
  if (k1 === 'sicaklik') {
    var c = g.kaynak === 'c' ? g.deger : g.kaynak === 'f' ? (g.deger - 32) / 1.8 : g.deger - 273.15;
    sonuc = g.hedef === 'c' ? c : g.hedef === 'f' ? c * 1.8 + 32 : c + 273.15;
  } else sonuc = g.deger * B[k1][g.kaynak] / B[k1][g.hedef];
  var ters = k1 === 'sicaklik' ? null : 1 * B[k1][g.hedef] / B[k1][g.kaynak];
  var AD = {mm:'mm', cm:'cm', m:'m', km:'km', inc:'inç', fit:'fit', yarda:'yarda', mil:'mil', dmil:'deniz mili', mg:'mg', g:'g', kg:'kg', ton:'ton', ons:'ons', libre:'libre', ml:'ml', l:'litre', m3:'m³', galon:'galon', bardak:'su bardağı', ck:'çay kaşığı', yk:'yemek kaşığı', cm2:'cm²', m2:'m²', donum:'dönüm', hektar:'hektar', km2:'km²', fit2:'fit²', akre:'akre', ms:'m/s', kmh:'km/sa', mph:'mil/sa', knot:'knot', c:'°C', f:'°F', k:'K'};
  var a1 = AD[g.kaynak] || g.kaynak, a2 = AD[g.hedef] || g.hedef;
  var fmt = function(x){ return Math.abs(x) >= 1e6 || (Math.abs(x) < 0.001 && x !== 0) ? x.toExponential(4) : String(Math.round(x * 1e6) / 1e6).replace('.', ','); };
  var s = [{etiket: String(g.deger).replace('.', ',') + ' ' + a1 + ' =', deger: fmt(sonuc) + ' ' + a2, vurgu: true}];
  if (ters !== null) { s.push({etiket: '1 ' + a1 + ' =', deger: fmt(B[k1][g.kaynak] / B[k1][g.hedef]) + ' ' + a2}); s.push({etiket: '1 ' + a2 + ' =', deger: fmt(ters) + ' ' + a1}); }
  return {sonuclar: s, notlar: k1 === 'alan' ? ['Türkiye\'de dönüm = dekar = 1.000 m² olarak kullanılır (eski dönüm bölgeye göre 919-2.500 m² arasında değişirdi).'] : k1 === 'hacim' ? ['Su bardağı 200 ml, çay kaşığı 5 ml, yemek kaşığı 15 ml kabul edilmiştir.'] : []};
}
""",
    "nasil": [
        "Birim dönüşümü, her birimin sistemdeki temel birime (metre, kilogram, litre, metrekare, m/s) oranına dayanır: kaynak birimdeki değer önce temel birime çevrilir, sonra hedef birime bölünür. Sıcaklık ise oransal değil kaydırmalı olduğu için ayrı formülle çevrilir: °F = °C × 1,8 + 32, K = °C + 273,15.",
        "Türkiye'de günlük hayatta sık gereken çevrimler: inç-santimetre (ekran, boru çapı), mil-kilometre (araç, uçuş), libre-kilogram (kargo, spor), galon-litre (yakıt), dönüm-metrekare (arsa), knot-km/saat (denizcilik, rüzgâr). Dönüm ve dekar bugün eşdeğer olarak 1.000 m² kabul edilir; tapularda alan m² olarak yazılır.",
        "Uluslararası standartlarda 1 inç tam olarak 2,54 cm, 1 libre 0,45359237 kg, 1 kara mili 1.609,344 m ve 1 deniz mili 1.852 m olarak tanımlanmıştır; bu değerler yaklaşık değil kesindir.",
    ],
    "formul": [
        "Hedef değer = kaynak değer × (kaynak birim ÷ temel birim) ÷ (hedef birim ÷ temel birim)",
        "°F = °C × 1,8 + 32 · °C = (°F − 32) ÷ 1,8 · K = °C + 273,15",
        "1 mil = 1,609344 km · 1 inç = 2,54 cm · 1 libre = 0,45359237 kg · 1 galon (US) = 3,7854 L · 1 dönüm = 1.000 m² · 1 knot = 1,852 km/sa",
    ],
    "ornekler": [
        {"baslik": "100 mil kaç km?", "adimlar": ["100 × 1,609344 = 160,93 km"]},
        {"baslik": "5 dönüm arsa kaç m²?", "adimlar": ["5 × 1.000 = 5.000 m² (0,5 hektar)"]},
        {"baslik": "98,6 °F kaç °C?", "adimlar": ["(98,6 − 32) ÷ 1,8 = 37 °C"]},
    ],
    "tablo": {
        "baslik": "Sık kullanılan dönüşüm katsayıları",
        "basliklar": ["Birim", "Karşılığı"],
        "satirlar": [["1 inç", "2,54 cm"], ["1 fit", "30,48 cm"], ["1 mil", "1,609 km"], ["1 deniz mili", "1,852 km"], ["1 libre", "453,6 g"], ["1 ons", "28,35 g"], ["1 galon (US)", "3,785 L"], ["1 dönüm", "1.000 m²"], ["1 hektar", "10 dönüm"], ["1 akre", "4.047 m²"], ["1 knot", "1,852 km/sa"], ["1 m/s", "3,6 km/sa"]],
        "not": "SI ve uluslararası yarda-libre tanımları (1959 anlaşması).",
    },
    "sss": [
        {"soru": "1 mil kaç kilometre?", "cevap": "1 kara mili = 1,609 km; 1 deniz mili = 1,852 km."},
        {"soru": "1 dönüm kaç metrekare?", "cevap": "Günümüzde 1 dönüm = 1 dekar = 1.000 m². Eski (Osmanlı) dönümü yaklaşık 919 m² idi; bölgesel 'büyük dönüm' 2.500 m²'ye kadar çıkardı."},
        {"soru": "Fahrenheit'ı Celsius'a nasıl çeviririm?", "cevap": "32 çıkarıp 1,8'e bölün: 77 °F → (77 − 32) ÷ 1,8 = 25 °C."},
        {"soru": "1 inç kaç cm?", "cevap": "Tam olarak 2,54 cm. 55 inç ekran köşegeni 139,7 cm'dir."},
        {"soru": "1 libre kaç kilo?", "cevap": "0,4536 kg (453,6 g). 10 libre ≈ 4,5 kg."},
    ],
    "kaynaklar": [
        {"ad": "BIPM — Uluslararası Birimler Sistemi (SI) Broşürü", "url": "https://www.bipm.org/"},
        {"ad": "TSE — Ölçü birimleri ve dönüşümler", "url": "https://www.tse.org.tr/"},
    ],
    "ilgili": ["yuzde-hesaplama", "ortalama-hesaplama"],
}
