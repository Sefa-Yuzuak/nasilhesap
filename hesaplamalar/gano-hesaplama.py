# -*- coding: utf-8 -*-
HESAP = {
    "slug": "gano-hesaplama",
    "baslik": "GANO / Not Ortalaması Hesaplama",
    "h1": "Üniversite Not Ortalaması Hesaplama — GANO, YANO ve AKTS Ağırlıklı Ortalama",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Üniversite not ortalaması (GANO/AGNO/YANO) hesaplama: ders kredileri (AKTS) ve harf notlarınızla ağırlıklı ortalama, 4'lük–100'lük dönüşüm, önceki dönem ortalamasıyla birleştirme ve hedef ortalama için gereken not.",
    "kisa_cevap": "GANO = Σ(harf notu katsayısı × ders kredisi) ÷ Σ(kredi). Örneğin AA (4,00) 6 AKTS, BB (3,00) 5 AKTS ve CC (2,00) 4 AKTS alan bir öğrencinin ortalaması (24 + 15 + 8) ÷ 15 = 3,13'tür. Yüksek kredili dersler ortalamayı daha çok etkiler; yarıyıl ortalaması YANO, tüm öğrenimin ortalaması GANO'dur.",
    "senaryolar": [
        {"ad": "İyi dönem (3,4)", "degerler": {"krediler": "6 5 4 5 3", "notlar": "AA BA BB BA CB", "onceki_gano": "", "onceki_kredi": ""}},
        {"ad": "Orta dönem (2,6)", "degerler": {"krediler": "6 5 4 5 3", "notlar": "BB CB CC BB DC", "onceki_gano": "", "onceki_kredi": ""}},
        {"ad": "Şartlı geçme riski", "degerler": {"krediler": "6 6 5 4", "notlar": "CC DC DD CB", "onceki_gano": "", "onceki_kredi": ""}},
        {"ad": "Önceki GANO ile birleştir", "degerler": {"krediler": "6 5 4 5", "notlar": "AA BA BB BA", "onceki_gano": "2.85", "onceki_kredi": "90"}},
    ],
    "girdiler": [
        {"id": "krediler", "etiket": "Ders kredileri (AKTS veya ulusal kredi)", "tip": "metin", "varsayilan": "6 5 4 5 3", "genis": True, "placeholder": "6 5 4 5 3", "ipucu": "boşluk veya virgülle ayırın"},
        {"id": "notlar", "etiket": "Harf notları (aynı sırayla)", "tip": "metin", "varsayilan": "AA BA BB BA CB", "genis": True, "placeholder": "AA BA BB CC", "ipucu": "AA, BA, BB, CB, CC, DC, DD, FF veya 4'lük sayı"},
        {"id": "onceki_gano", "etiket": "Önceki GANO (isteğe bağlı)", "tip": "sayi", "varsayilan": "", "ipucu": "birleşik ortalama için"},
        {"id": "onceki_kredi", "etiket": "Önceki toplam kredi", "tip": "sayi", "varsayilan": "", "ipucu": "önceki GANO girdiyseniz"},
    ],
    "js": r"""
var HARF = {AA:4.00, BA:3.50, BB:3.00, CB:2.50, CC:2.00, DC:1.50, DD:1.00, FD:0.50, FF:0.00, F:0.00, NA:0.00};
function ayir(s){ return String(s||'').trim().split(/[\s,;]+/).filter(Boolean); }
function hesapla(g){
  var kr = ayir(g.krediler).map(function(x){ return parseFloat(x.replace(',', '.')); });
  var nt = ayir(g.notlar).map(function(x){ return x.toUpperCase().replace('İ','I'); });
  if (!kr.length || !nt.length) return {hata: 'Kredi ve harf notlarını girin.'};
  if (kr.length !== nt.length) return {hata: 'Kredi sayısı (' + kr.length + ') ile not sayısı (' + nt.length + ') eşleşmiyor.'};
  var topAgirlik = 0, topKredi = 0, satir = [], bilinmeyen = [], notlar = [];
  for (var i = 0; i < kr.length; i++) {
    var k = kr[i], h = nt[i];
    if (!(k > 0)) return {hata: (i+1) + '. dersin kredisi geçersiz.'};
    var kat = HARF[h];
    if (kat === undefined) { var sayi = parseFloat(h.replace(',', '.')); if (sayi >= 0 && sayi <= 4) kat = sayi; else { bilinmeyen.push(h); continue; } }
    topAgirlik += kat * k; topKredi += k;
    satir.push([(i+1) + '. ders', h, k, kat.toFixed(2), (kat*k).toFixed(2)]);
  }
  if (bilinmeyen.length) return {hata: 'Tanınmayan harf notu: ' + bilinmeyen.join(', ') + '. Geçerli: AA, BA, BB, CB, CC, DC, DD, FD, FF veya 0-4 arası sayı.'};
  if (!topKredi) return {hata: 'Geçerli ders bulunamadı.'};
  var gano = topAgirlik / topKredi;
  var s = [{etiket: 'Dönem ortalaması (YANO)', deger: Math.round(gano * 100) / 100, vurgu: true},
           {etiket: 'Toplam kredi', deger: topKredi},
           {etiket: 'Toplam ağırlıklı puan', deger: topAgirlik},
           {etiket: '100\'lük yaklaşık karşılığı', deger: gano * 25, birim: '/100'}];
  if (g.onceki_gano > 0 && g.onceki_kredi > 0) {
    var bKredi = topKredi + g.onceki_kredi, bGano = (topAgirlik + g.onceki_gano * g.onceki_kredi) / bKredi;
    s.unshift({etiket: 'Genel ortalama (GANO)', deger: Math.round(bGano * 100) / 100, vurgu: true});
    s[1].vurgu = false;
    s.push({etiket: 'Birleşik toplam kredi', deger: bKredi});
    s.push({etiket: 'GANO değişimi', deger: (bGano - g.onceki_gano >= 0 ? '+' : '') + (bGano - g.onceki_gano).toFixed(3)});
  }
  var durum = gano >= 3.5 ? 'Yüksek onur (genelde ≥3,50)' : gano >= 3.0 ? 'Onur öğrencisi (genelde ≥3,00)' : gano >= 2.0 ? 'Başarılı (≥2,00)' : 'Şartlı / başarısız (<2,00) — çoğu üniversitede mezuniyet için GANO ≥ 2,00 şart';
  s.push({etiket: 'Durum', deger: durum});
  notlar.push('4\'lük–100\'lük dönüşüm üniversiteye göre değişir; YÖK\'ün eşdeğerlik tablosu ile kurumunuzun yönetmeliği farklı sonuç verebilir. Buradaki ×25 yalnızca kaba bir yaklaşımdır.');
  notlar.push('Harf notu katsayıları çoğu üniversitede aynıdır (AA 4,00 … FF 0,00) ancak CB/DC eşikleri ve şartlı geçme kuralları kurumdan kuruma değişir; yönetmeliğinizi kontrol edin.');
  if (g.onceki_gano > 0 && !(g.onceki_kredi > 0)) notlar.push('Önceki GANO girdiniz ama önceki toplam krediyi girmediniz; birleşik GANO hesaplanamadı.');
  return {sonuclar: s, notlar: notlar,
    tablo: {basliklar: ['Ders', 'Not', 'Kredi', 'Katsayı', 'Ağırlıklı'], satirlar: satir},
    grafik: {tur: 'sutun', baslik: 'Derslerin ortalamaya katkısı (katsayı × kredi)', etiketler: satir.map(function(r){ return r[1]; }), seriler: [{ad: 'Ağırlıklı puan', veri: satir.map(function(r){ return parseFloat(r[4]); })}]}};
}
""",
    "nasil": [
        "Üniversitede not ortalaması, derslerin harf notu katsayılarının kredilerle ağırlıklandırılmasıyla hesaplanır. Her dersin katsayısı (AA 4,00; BA 3,50; BB 3,00; CB 2,50; CC 2,00; DC 1,50; DD 1,00; FF 0,00) kredisiyle çarpılır, çıkan değerler toplanır ve toplam krediye bölünür. Kredi olarak çoğu üniversite AKTS'yi, bazıları ulusal krediyi kullanır — yönetmeliğinizde hangisi yazıyorsa onu girin.",
        "YANO (yarıyıl ağırlıklı not ortalaması) yalnızca o dönemin derslerini, GANO (genel ağırlıklı not ortalaması) ise öğrenim boyunca alınan tüm dersleri kapsar. Bu araçta önceki GANO'nuzu ve o ana kadarki toplam kredinizi girerseniz, yeni dönemle birleşik GANO'nuzu ve değişim miktarını da hesaplar.",
        "Yüksek kredili dersler ortalamayı orantılı olarak daha çok etkiler: 8 AKTS'lik bir dersten alınan CC, 3 AKTS'lik bir dersten alınan AA'dan daha ağır basar. Çoğu üniversitede mezuniyet için GANO'nun en az 2,00 olması, onur/yüksek onur için 3,00/3,50 eşiklerinin aşılması gerekir; tekrar edilen derslerde genellikle son not geçerlidir.",
    ],
    "formul": [
        "YANO = Σ(harf katsayısı × kredi) ÷ Σ(kredi)   [tek dönem]",
        "GANO = Σ(tüm dönemlerin ağırlıklı puanları) ÷ Σ(tüm krediler)",
        "Birleşik GANO = (yeni ağırlıklı toplam + eski GANO × eski kredi) ÷ (yeni kredi + eski kredi)",
        "Katsayılar: AA 4,00 · BA 3,50 · BB 3,00 · CB 2,50 · CC 2,00 · DC 1,50 · DD 1,00 · FF 0,00",
    ],
    "ornekler": [
        {"baslik": "AA(6), BA(5), BB(4)", "adimlar": ["4,00×6 = 24 · 3,50×5 = 17,5 · 3,00×4 = 12", "Toplam 53,5 ÷ 15 kredi = 3,57"]},
        {"baslik": "Önceki GANO 2,85 (90 kredi) + yeni dönem 3,60 (20 kredi)", "adimlar": ["(3,60×20 + 2,85×90) ÷ 110 = (72 + 256,5) ÷ 110 = 2,99", "GANO 0,14 puan yükseldi"]},
    ],
    "tablo": {
        "baslik": "Harf notu katsayıları (yaygın uygulama)",
        "basliklar": ["Harf", "Katsayı", "100'lük aralık (yaklaşık)", "Durum"],
        "satirlar": [["AA", "4,00", "90–100", "Başarılı"], ["BA", "3,50", "85–89", "Başarılı"], ["BB", "3,00", "80–84", "Başarılı"], ["CB", "2,50", "75–79", "Başarılı"], ["CC", "2,00", "65–74", "Başarılı"], ["DC", "1,50", "58–64", "Şartlı başarılı"], ["DD", "1,00", "50–57", "Şartlı başarılı"], ["FD", "0,50", "40–49", "Başarısız"], ["FF", "0,00", "0–39", "Başarısız"]],
        "not": "Katsayılar çoğu üniversitede ortaktır; 100'lük karşılıklar ve şartlı geçme kuralları kurumun yönetmeliğine göre değişir.",
    },
    "sss": [
        {"soru": "GANO nasıl hesaplanır?", "cevap": "Her dersin harf notu katsayısını kredisiyle çarpın, hepsini toplayın ve toplam krediye bölün. AA(4) 6 kredi + BB(3) 4 kredi → (24+12) ÷ 10 = 3,60."},
        {"soru": "GANO ile YANO farkı nedir?", "cevap": "YANO tek bir yarıyılın, GANO ise tüm öğrenim boyunca alınan derslerin ağırlıklı ortalamasıdır. Bazı üniversiteler AGNO terimini GANO ile aynı anlamda kullanır."},
        {"soru": "AKTS mi ulusal kredi mi kullanmalıyım?", "cevap": "Üniversitenizin yönetmeliği hangisini esas alıyorsa onu girin. Çoğu üniversite artık AKTS kullanır; transkriptinizde ortalamanın hangi krediyle hesaplandığı yazar."},
        {"soru": "4'lük not 100'lük sistemde kaç eder?", "cevap": "Kesin bir formül yoktur; kaba yaklaşım ×25'tir. Resmî işlemler için YÖK'ün dönüşüm tablosu veya üniversitenizin kendi tablosu kullanılır."},
        {"soru": "Ders tekrarında hangi not sayılır?", "cevap": "Çoğu üniversitede son alınan not geçerlidir ve eski not ortalamadan çıkarılır; bazılarında en yüksek not alınır. Yönetmeliğinizi kontrol edin."},
        {"soru": "Mezuniyet için GANO kaç olmalı?", "cevap": "Genellikle en az 2,00. 3,00–3,49 onur, 3,50 ve üzeri yüksek onur derecesi verir (kurumlara göre değişebilir)."},
    ],
    "kaynaklar": [
        {"ad": "YÖK — Yükseköğretim mevzuatı ve not dönüşüm tabloları", "url": "https://www.yok.gov.tr/"},
    ],
    "ilgili": ["vize-final-hesaplama", "obp-hesaplama", "ortalama-hesaplama"],
}
