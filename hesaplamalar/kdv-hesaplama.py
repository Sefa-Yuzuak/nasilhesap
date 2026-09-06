# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kdv-hesaplama",
    "baslik": "KDV Hesaplama",
    "h1": "KDV Hesaplama 2026 — KDV Dahil ve KDV Hariç",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "KDV hesaplama aracı: KDV hariç tutardan KDV dahil fiyatı, KDV dahil fiyattan KDV hariç tutarı ve KDV tutarını %1, %10, %20 oranlarıyla anında hesaplayın. 2026 güncel KDV oranları ve formüller.",
    "kisa_cevap": "KDV tutarı = tutar × oran ÷ 100. KDV hariç 1.000 ₺'ye %20 KDV eklenince 1.200 ₺ olur; KDV dahil 1.200 ₺'nin KDV hariç değeri 1.200 ÷ 1,20 = 1.000 ₺'dir. Türkiye'de 2026'da geçerli KDV oranları %1, %10 ve %20'dir.",
    "senaryolar": [
        {"ad": "1.000 ₺ + %20", "degerler": {"yon": "haric", "tutar": "1000", "oran": "20"}},
        {"ad": "1.200 ₺ dahil → hariç", "degerler": {"yon": "dahil", "tutar": "1200", "oran": "20"}},
        {"ad": "Gıda %10", "degerler": {"yon": "haric", "tutar": "1000", "oran": "10"}},
        {"ad": "Temel gıda %1", "degerler": {"yon": "haric", "tutar": "1000", "oran": "1"}},
    ],
    "girdiler": [
        {"id": "yon", "etiket": "Ne hesaplanacak?", "tip": "secim", "varsayilan": "haric",
         "secenekler": [["haric", "KDV hariç tutardan → KDV dahil"], ["dahil", "KDV dahil tutardan → KDV hariç"]], "genis": True},
        {"id": "tutar", "etiket": "Tutar", "tip": "sayi", "varsayilan": "1000", "birim": "₺"},
        {"id": "oran", "etiket": "KDV oranı", "tip": "secim", "varsayilan": "20",
         "secenekler": [["20", "%20 (genel)"], ["10", "%10"], ["1", "%1"], ["ozel", "Özel oran"]]},
        {"id": "ozel_oran", "etiket": "Özel oran", "tip": "sayi", "varsayilan": "18", "birim": "%", "gizli": "oran=ozel"},
    ],
    "js": r"""
function hesapla(g, O){
  var oran = g.oran === 'ozel' ? g.ozel_oran : parseFloat(g.oran);
  if (!(oran >= 0)) return {hata: 'Geçerli bir KDV oranı girin.'};
  if (!(g.tutar >= 0)) return {hata: 'Tutarı girin.'};
  var haric, dahil, kdv;
  if (g.yon === 'haric') { haric = g.tutar; kdv = haric * oran / 100; dahil = haric + kdv; }
  else { dahil = g.tutar; haric = dahil / (1 + oran / 100); kdv = dahil - haric; }
  return {
    sonuclar: [
      {etiket: g.yon === 'haric' ? 'KDV dahil tutar' : 'KDV hariç tutar', deger: g.yon === 'haric' ? dahil : haric, birim: '₺', vurgu: true},
      {etiket: 'KDV tutarı (%' + oran + ')', deger: kdv, birim: '₺'},
      {etiket: 'KDV hariç tutar', deger: haric, birim: '₺'},
      {etiket: 'KDV dahil tutar', deger: dahil, birim: '₺'}
    ],
    notlar: ['Formül: ' + (g.yon === 'haric' ? 'KDV dahil = tutar × (1 + ' + oran + '/100)' : 'KDV hariç = tutar ÷ (1 + ' + oran + '/100)')]
  };
}
""",
    "nasil": [
        "KDV (Katma Değer Vergisi), mal ve hizmet satışında satış bedeli üzerinden alınan dolaylı bir vergidir. KDV hesaplamanın iki yönü vardır: elinizde KDV hariç (net) tutar varsa üzerine KDV eklersiniz; elinizde KDV dahil (brüt) fiyat varsa içindeki KDV'yi ayrıştırırsınız.",
        "KDV eklemek için tutarı oran ile çarpıp 100'e bölmeniz yeterlidir. KDV dahil fiyattan KDV hariç tutara ulaşmak için ise fiyatı (1 + oran/100) değerine bölersiniz — yaygın hata, dahil fiyattan doğrudan %20 düşmektir; bu yanlış sonuç verir çünkü KDV, hariç tutar üzerinden hesaplanır.",
        "Türkiye'de 7 Temmuz 2023'ten itibaren genel KDV oranı %20, indirimli oranlar %10 ve %1'dir. Hangi ürünün hangi orana tabi olduğu KDV Kanunu'na ekli (I) ve (II) sayılı listelerle belirlenir.",
    ],
    "formul": [
        "KDV tutarı = KDV hariç tutar × KDV oranı ÷ 100",
        "KDV dahil tutar = KDV hariç tutar × (1 + KDV oranı ÷ 100)",
        "KDV hariç tutar = KDV dahil tutar ÷ (1 + KDV oranı ÷ 100)",
        "KDV tutarı (dahil fiyattan) = KDV dahil tutar − KDV hariç tutar",
    ],
    "ornekler": [
        {"baslik": "KDV hariç 2.500 ₺'ye %20 KDV eklemek",
         "adimlar": ["KDV tutarı: 2.500 × 20 ÷ 100 = 500 ₺", "KDV dahil fiyat: 2.500 + 500 = 3.000 ₺"]},
        {"baslik": "KDV dahil 1.100 ₺'lik gıda ürününün (%10) KDV'sini bulmak",
         "adimlar": ["KDV hariç tutar: 1.100 ÷ 1,10 = 1.000 ₺", "KDV tutarı: 1.100 − 1.000 = 100 ₺"]},
        {"baslik": "KDV dahil 240 ₺'lik üründe (%20) KDV payı",
         "adimlar": ["KDV hariç: 240 ÷ 1,20 = 200 ₺", "KDV: 40 ₺ — dikkat: 240'ın %20'si (48 ₺) değildir."]},
    ],
    "tablo": {
        "baslik": "2026 KDV oranları ve kapsamı",
        "basliklar": ["Oran", "Başlıca kapsam"],
        "satirlar": [
            ["%1", "Temel gıda (ekmek, un, buğday, bakliyat, süt vb.), bazı tarım ürünleri, basılı gazete-kitap-dergi, ikinci el bazı işlemler"],
            ["%10", "Genel gıda, lokanta-kafe, konaklama, tekstil ve konfeksiyon, sağlık hizmetleri ve ilaç, eğitim, sinema-tiyatro, net alanı 150 m² altı konut (belirli şartlarla)"],
            ["%20", "Genel oran: beyaz eşya, elektronik, otomobil, mobilya, kozmetik, telekomünikasyon ve listelerde yer almayan tüm mal ve hizmetler"],
        ],
        "not": "Kapsam özet niteliğindedir; kesin sınıflandırma için KDV Kanunu'na ekli (I) ve (II) sayılı listelere ve GİB duyurularına bakın.",
    },
    "sss": [
        {"soru": "KDV dahil fiyattan KDV nasıl hesaplanır?",
         "cevap": "KDV dahil fiyatı (1 + oran/100) değerine bölerek KDV hariç tutarı bulun; ikisinin farkı KDV tutarıdır. Örneğin %20 için 1.200 ÷ 1,20 = 1.000 ₺ hariç tutar, 200 ₺ KDV."},
        {"soru": "2026'da KDV oranları kaç?",
         "cevap": "Genel oran %20, indirimli oranlar %10 ve %1'dir. Bu oranlar 7 Temmuz 2023'te yürürlüğe giren 7346 sayılı Cumhurbaşkanı Kararı ile belirlendi ve 2026'da geçerliliğini koruyor."},
        {"soru": "KDV oranı %18'den %20'ye ne zaman çıktı?",
         "cevap": "7 Temmuz 2023'te; aynı kararla %8 oranı da %10'a yükseltildi. %1 oranı değişmedi."},
        {"soru": "KDV matrahı nedir?",
         "cevap": "KDV'nin üzerinden hesaplandığı KDV hariç bedeldir. Fatura üzerindeki 'matrah' satırı KDV hariç tutarı, 'KDV' satırı verginin kendisini, 'genel toplam' ise KDV dahil tutarı gösterir."},
        {"soru": "1.000 TL'nin KDV'si ne kadar?",
         "cevap": "%20 oranında 200 ₺ (dahil fiyat 1.200 ₺), %10'da 100 ₺ (1.100 ₺), %1'de 10 ₺ (1.010 ₺)."},
        {"soru": "KDV tevkifatı ne demek?",
         "cevap": "Bazı işlemlerde KDV'nin belirli bir kısmının alıcı tarafından sorumlu sıfatıyla beyan edilip ödenmesidir (örneğin 5/10 veya 9/10). Bu araç tevkifatsız standart KDV hesaplar."},
    ],
    "kaynaklar": [
        {"ad": "GİB — Katma Değer Vergisi mevzuatı ve oran listeleri", "url": "https://www.gib.gov.tr/"},
        {"ad": "3065 sayılı Katma Değer Vergisi Kanunu (mevzuat.gov.tr)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=3065&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["yuzde-hesaplama", "brut-net-maas-hesaplama", "gelir-vergisi-hesaplama"],
}
