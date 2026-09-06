# -*- coding: utf-8 -*-
HESAP = {
    "slug": "ortalama-hesaplama",
    "baslik": "Ortalama Hesaplama",
    "h1": "Ortalama Hesaplama — Aritmetik, Ağırlıklı Ortalama, Medyan ve Standart Sapma",
    "kategori": "gunluk",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Ortalama hesaplama aracı: sayıları girin, aritmetik ortalama, ağırlıklı ortalama, medyan, mod, toplam, en küçük-en büyük ve standart sapmayı anında hesaplayın. Not ortalaması ve ders ağırlığı için ideal.",
    "kisa_cevap": "Aritmetik ortalama = sayıların toplamı ÷ sayı adedi (85, 90, 72 → 247 ÷ 3 = 82,33). Ağırlıklı ortalama = Σ(değer × ağırlık) ÷ Σağırlık; ders kredileriyle not ortalaması böyle hesaplanır. Medyan, sıralı listenin ortadaki değeridir ve uç değerlerden etkilenmez.",
    "girdiler": [
        {"id": "sayilar", "etiket": "Sayılar (virgül, boşluk veya satırla ayırın)", "tip": "metin", "varsayilan": "85, 90, 72, 64, 95", "genis": True, "placeholder": "85, 90, 72"},
        {"id": "agirliklar", "etiket": "Ağırlıklar (isteğe bağlı; sayılarla aynı sırada)", "tip": "metin", "varsayilan": "", "genis": True, "placeholder": "3, 2, 4, 2, 3"},
    ],
    "js": r"""
function ayir(s){ return String(s || '').split(/[\s,;]+/).map(function(x){ return x.trim().replace(',', '.'); }).filter(Boolean).map(parseFloat).filter(function(x){ return !isNaN(x); }); }
function hesapla(g){
  var v = ayir(g.sayilar);
  if (v.length < 1) return {hata: 'En az bir sayı girin.'};
  var n = v.length, toplam = v.reduce(function(a, b){ return a + b; }, 0), ort = toplam / n;
  var sr = v.slice().sort(function(a, b){ return a - b; });
  var medyan = n % 2 ? sr[(n - 1) / 2] : (sr[n / 2 - 1] + sr[n / 2]) / 2;
  var say = {}, mod = [], maxS = 0;
  v.forEach(function(x){ say[x] = (say[x] || 0) + 1; });
  Object.keys(say).forEach(function(k){ if (say[k] > maxS) { maxS = say[k]; mod = [k]; } else if (say[k] === maxS) mod.push(k); });
  var varyans = v.reduce(function(a, x){ return a + (x - ort) * (x - ort); }, 0) / n;
  var s = [{etiket: 'Aritmetik ortalama', deger: ort, vurgu: true}];
  var w = ayir(g.agirliklar), notlar = [];
  if (w.length) {
    if (w.length !== n) notlar.push('Ağırlık sayısı (' + w.length + ') sayı adediyle (' + n + ') eşleşmiyor; ağırlıklı ortalama hesaplanmadı.');
    else { var wt = w.reduce(function(a, b){ return a + b; }, 0), wo = v.reduce(function(a, x, i){ return a + x * w[i]; }, 0) / wt; s.push({etiket: 'Ağırlıklı ortalama', deger: wo}); s.push({etiket: 'Toplam ağırlık', deger: wt}); }
  }
  s.push({etiket: 'Medyan', deger: medyan});
  s.push({etiket: 'Mod', deger: maxS > 1 ? mod.join(', ') : 'Tekrar eden değer yok'});
  s.push({etiket: 'Toplam', deger: toplam});
  s.push({etiket: 'Adet', deger: n, ondalik: 0});
  s.push({etiket: 'En küçük / en büyük', deger: NH.fmt(sr[0]) + ' / ' + NH.fmt(sr[n - 1])});
  s.push({etiket: 'Standart sapma (popülasyon)', deger: Math.sqrt(varyans)});
  if (n > 1) s.push({etiket: 'Standart sapma (örneklem)', deger: Math.sqrt(varyans * n / (n - 1))});
  return {sonuclar: s, notlar: notlar};
}
""",
    "nasil": [
        "Aritmetik ortalama, en yaygın 'ortalama'dır: tüm değerler toplanıp adede bölünür. Sınıf notu, aylık harcama, ortalama hız gibi günlük hesapların çoğu budur. Uç değerlere duyarlıdır: 10 kişilik grupta bir kişinin geliri çok yüksekse ortalama yanıltır.",
        "Ağırlıklı ortalamada her değerin bir önem katsayısı vardır: değerler ağırlıklarıyla çarpılıp toplanır ve ağırlıkların toplamına bölünür. Üniversite not ortalaması (kredi × not), vize-final (%40-%60) ve endeksler böyle hesaplanır.",
        "Medyan sıralı verinin ortasıdır; uç değerlerden etkilenmediği için gelir ve fiyat verilerinde ortalamadan daha temsil edicidir. Mod en sık tekrar eden değer, standart sapma ise verilerin ortalamadan ne kadar yayıldığının ölçüsüdür (küçükse veriler birbirine yakın).",
    ],
    "formul": [
        "Aritmetik ortalama = (x₁ + x₂ + … + xₙ) ÷ n",
        "Ağırlıklı ortalama = Σ(xᵢ × wᵢ) ÷ Σwᵢ",
        "Medyan = sıralı verinin ortadaki değeri (çift adette ortadaki ikisinin ortalaması)",
        "Standart sapma = √[ Σ(xᵢ − ortalama)² ÷ n ]  (örneklem için n − 1)",
    ],
    "ornekler": [
        {"baslik": "Notlar: 85, 90, 72, 64, 95", "adimlar": ["Toplam 406 ÷ 5 = 81,2 (aritmetik)", "Sıralı: 64, 72, 85, 90, 95 → medyan 85", "Standart sapma ≈ 11,5"]},
        {"baslik": "Vize 70 (%40), final 85 (%60)", "adimlar": ["70 × 0,4 + 85 × 0,6 = 28 + 51 = 79 (ağırlıklı)"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Ortalama nasıl hesaplanır?", "cevap": "Sayıları toplayıp kaç tane olduklarına bölün. 12, 15, 18 → 45 ÷ 3 = 15."},
        {"soru": "Ağırlıklı ortalama ne zaman kullanılır?", "cevap": "Değerlerin önemi farklıysa: ders kredileri, vize-final yüzdeleri, portföy getirisi. Her değer ağırlığıyla çarpılır, toplam ağırlığa bölünür."},
        {"soru": "Medyan ile ortalama farkı nedir?", "cevap": "Ortalama toplam ÷ adet; medyan ortadaki değer. 1, 2, 3, 4, 100 → ortalama 22, medyan 3. Uç değer varsa medyan daha gerçekçidir."},
        {"soru": "Standart sapma neyi gösterir?", "cevap": "Verilerin ortalamadan ortalama ne kadar uzaklaştığını. Aynı ortalamaya sahip iki sınıftan sapması küçük olanın notları daha homojendir."},
    ],
    "kaynaklar": [],
    "ilgili": ["yuzde-hesaplama", "gun-hesaplama"],
}
