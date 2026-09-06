# -*- coding: utf-8 -*-
HESAP = {
    "slug": "indirim-hesaplama",
    "baslik": "İndirim Hesaplama",
    "h1": "İndirim Hesaplama — İndirimli Fiyat, Tasarruf ve Sepette Ek İndirim",
    "kategori": "gunluk",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "İndirim hesaplama: fiyat ve indirim yüzdesine göre indirimli fiyat ve tasarruf; sepette ek indirimle toplam indirim oranı; indirimli fiyattan orijinal fiyatı bulma. Formül ve örneklerle.",
    "kisa_cevap": "İndirimli fiyat = fiyat × (1 − indirim ÷ 100). 1.500 ₺'lik üründe %30 indirim 450 ₺ tasarruf sağlar, fiyat 1.050 ₺ olur. Ardışık indirimler toplanmaz, çarpılır: %30 + sepette %10 = toplam %37 indirim (0,70 × 0,90 = 0,63).",
    "girdiler": [
        {"id": "mod", "etiket": "Hesaplama", "tip": "secim", "varsayilan": "fiyat", "genis": True,
         "secenekler": [["fiyat", "Fiyattan indirimli fiyatı bul"], ["orijinal", "İndirimli fiyattan orijinal fiyatı bul"], ["oran", "İki fiyattan indirim oranını bul"]]},
        {"id": "a", "etiket": "Fiyat", "tip": "sayi", "varsayilan": "1500", "birim": "₺"},
        {"id": "b", "etiket": "İndirim", "tip": "sayi", "varsayilan": "30", "birim": "%"},
        {"id": "c", "etiket": "Sepette ek indirim (isteğe bağlı)", "tip": "sayi", "varsayilan": "0", "birim": "%"},
    ],
    "js": r"""
function hesapla(g){
  if (isNaN(g.a) || isNaN(g.b)) return {hata: 'Değerleri girin.'};
  var c = g.c > 0 ? g.c : 0, s = [], n = [];
  if (g.mod === 'fiyat') {
    var f1 = g.a * (1 - g.b / 100), f2 = f1 * (1 - c / 100);
    var toplamOran = (1 - f2 / g.a) * 100;
    s.push({etiket: 'İndirimli fiyat', deger: f2, birim: '₺', vurgu: true});
    s.push({etiket: 'Toplam tasarruf', deger: g.a - f2, birim: '₺'});
    if (c) { s.push({etiket: 'İlk indirim sonrası', deger: f1, birim: '₺'}); s.push({etiket: 'Toplam indirim oranı', deger: toplamOran, birim: '%'}); n.push('Ardışık indirimler çarpılır: (1 − ' + g.b + '%) × (1 − ' + c + '%) → toplam %' + toplamOran.toFixed(2)); }
  } else if (g.mod === 'orijinal') {
    var oran = (1 - g.b / 100) * (1 - c / 100);
    if (oran <= 0) return {hata: 'İndirim %100 veya üzeri olamaz.'};
    var orj = g.a / oran;
    s.push({etiket: 'Orijinal (indirimsiz) fiyat', deger: orj, birim: '₺', vurgu: true});
    s.push({etiket: 'Yapılan indirim', deger: orj - g.a, birim: '₺'});
    n.push('Bu modda "Fiyat" alanına indirimli fiyatı girin.');
  } else {
    if (!(g.a > 0)) return {hata: 'Orijinal fiyat sıfırdan büyük olmalı.'};
    var ind = (1 - g.b / g.a) * 100;
    s.push({etiket: 'İndirim oranı', deger: ind, birim: '%', vurgu: true});
    s.push({etiket: 'İndirim tutarı', deger: g.a - g.b, birim: '₺'});
    n.push('Bu modda "Fiyat" = orijinal fiyat, "İndirim" alanı = indirimli fiyat (₺) olarak girilir.');
  }
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "İndirim tutarı, fiyatın indirim yüzdesiyle çarpılıp 100'e bölünmesiyle bulunur; indirimli fiyat ise fiyattan bu tutarın düşülmesidir. Pratik yol, fiyatı (1 − indirim/100) ile çarpmaktır: %30 indirim için 0,70.",
        "Ardışık indirimler (etiket indirimi + sepette ek indirim + kupon) birbirine eklenmez, çarpılır. %30 ve %10 indirim %40 değil %37 eder, çünkü ikinci indirim zaten düşmüş fiyata uygulanır. Mağazaların 'toplamda %40'a varan' ifadesi genellikle bu çarpımın en yüksek halini anlatır.",
        "İndirimli fiyattan orijinali bulmak için indirimli fiyatı (1 − indirim/100)'e bölersiniz; 'fiyat + %30 ekle' yaparsanız yanlış sonuç alırsınız (1.050 × 1,30 = 1.365 ≠ 1.500). Ticaret Bakanlığı yönetmeliğine göre indirimli satışta indirim öncesi fiyat, son 30 günün en düşük fiyatı olmak zorundadır.",
    ],
    "formul": [
        "İndirim tutarı = fiyat × indirim ÷ 100",
        "İndirimli fiyat = fiyat × (1 − indirim ÷ 100)",
        "Ardışık indirim: son fiyat = fiyat × (1 − i₁/100) × (1 − i₂/100) · toplam oran = 1 − çarpım",
        "Orijinal fiyat = indirimli fiyat ÷ (1 − indirim ÷ 100)",
    ],
    "ornekler": [
        {"baslik": "1.500 ₺, %30 indirim + sepette %10", "adimlar": ["1.500 × 0,70 = 1.050 ₺", "1.050 × 0,90 = 945 ₺", "Toplam indirim: 555 ₺ = %37"]},
        {"baslik": "İndirimli fiyat 945 ₺, indirim %37 → orijinal?", "adimlar": ["945 ÷ 0,63 = 1.500 ₺"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "%30 + %10 indirim toplam %40 mı?", "cevap": "Hayır, %37. İkinci indirim ilk indirimden sonraki fiyata uygulanır: 0,70 × 0,90 = 0,63 → %37 indirim."},
        {"soru": "İndirimli fiyattan orijinal fiyat nasıl bulunur?", "cevap": "İndirimli fiyatı (1 − indirim/100)'e bölün. %25 indirimle 300 ₺ olan ürün: 300 ÷ 0,75 = 400 ₺."},
        {"soru": "Yüzde kaç indirim yapıldı nasıl hesaplanır?", "cevap": "(1 − indirimli ÷ orijinal) × 100. 400 ₺'den 300 ₺'ye: (1 − 0,75) × 100 = %25."},
        {"soru": "Mağaza 'indirim öncesi fiyat'ı istediği gibi yazabilir mi?", "cevap": "Hayır. Fiyat Etiketi Yönetmeliği'ne göre indirim öncesi fiyat, indirimden önceki 30 gün içindeki en düşük satış fiyatıdır."},
    ],
    "kaynaklar": [
        {"ad": "Ticaret Bakanlığı — Fiyat Etiketi Yönetmeliği (indirimli satışlar)", "url": "https://www.ticaret.gov.tr/"},
    ],
    "ilgili": ["yuzde-hesaplama", "kdv-hesaplama"],
}
