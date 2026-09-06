# -*- coding: utf-8 -*-
HESAP = {
    "slug": "ev-alma-maliyeti-hesaplama",
    "baslik": "Ev Alma Maliyeti Hesaplama",
    "h1": "Ev Alma Maliyeti Hesaplama 2026 — Tapu Harcı, Emlakçı Komisyonu ve Tüm Masraflar",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Ev alırken toplam maliyet: satış bedeline ek tapu harcı (‰20), döner sermaye, emlakçı komisyonu (%2 + KDV), ekspertiz, DASK, kredi tahsis ücreti ve ipotek masrafları. 2026 oranlarıyla kalem kalem.",
    "kisa_cevap": "Ev alma maliyeti satış bedelinin yaklaşık %4,5–6'sı kadar ek masraf içerir: tapu harcı ‰20 (%2), emlakçı komisyonu %2 + %20 KDV (= %2,4), döner sermaye 3.400–6.700 ₺, kredi kullanılıyorsa ekspertiz, tahsis ücreti (en fazla ‰5) ve sigortalar. 4.000.000 ₺'lik ev için ek masraf ≈ 190.000 ₺'dir.",
    "girdiler": [
        {"id": "fiyat", "etiket": "Satış bedeli", "tip": "sayi", "varsayilan": "4000000", "birim": "₺"},
        {"id": "il", "etiket": "İl", "tip": "secim", "varsayilan": "buyuksehir", "secenekler": [["buyuksehir", "Büyükşehir"], ["diger", "Diğer"]]},
        {"id": "komisyon", "etiket": "Emlakçı komisyonu (KDV hariç)", "tip": "sayi", "varsayilan": "2", "birim": "%", "ipucu": "emlakçı yoksa 0"},
        {"id": "kredi", "etiket": "Kullanılan konut kredisi", "tip": "sayi", "varsayilan": "0", "birim": "₺", "ipucu": "kredi yoksa 0"},
        {"id": "ekspertiz", "etiket": "Ekspertiz ücreti", "tip": "sayi", "varsayilan": "0", "birim": "₺", "ipucu": "bankanın bildirdiği tutar"},
        {"id": "sigorta", "etiket": "DASK + konut sigortası (yıllık)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.fiyat > 0)) return {hata: 'Satış bedelini girin.'};
  var T = O.tapu_harci, harc = g.fiyat * T.alici_binde / 1000;
  var doner = g.il === 'buyuksehir' ? T.doner_sermaye_buyuksehir : T.doner_sermaye_diger;
  var kom = g.fiyat * (g.komisyon > 0 ? g.komisyon : 0) / 100, komKdv = kom * 0.20;
  var kredi = g.kredi > 0 ? g.kredi : 0, tahsis = kredi * 0.005, ipotek = 0; // konut kredisi ipoteği harçtan istisna
  var eks = g.ekspertiz > 0 ? g.ekspertiz : 0, sig = g.sigorta > 0 ? g.sigorta : 0;
  var ek = harc + doner + kom + komKdv + tahsis + eks + sig;
  var s = [
    {etiket: 'Toplam ek masraf', deger: ek, birim: '₺', vurgu: true},
    {etiket: 'Ek masraf / satış bedeli', deger: ek / g.fiyat * 100, birim: '%'},
    {etiket: 'Tapu harcı (alıcı ‰' + T.alici_binde + ')', deger: harc, birim: '₺'},
    {etiket: 'Döner sermaye ücreti (yaklaşık)', deger: doner, birim: '₺'},
    {etiket: 'Emlakçı komisyonu', deger: kom, birim: '₺'},
    {etiket: 'Komisyon KDV (%20)', deger: komKdv, birim: '₺'}
  ];
  if (kredi) { s.push({etiket: 'Kredi tahsis ücreti (en fazla ‰5)', deger: tahsis, birim: '₺'}); s.push({etiket: 'İpotek tesis harcı', deger: 'İstisna (konut kredisi)'}); }
  if (eks) s.push({etiket: 'Ekspertiz', deger: eks, birim: '₺'});
  if (sig) s.push({etiket: 'DASK + konut sigortası', deger: sig, birim: '₺'});
  s.push({etiket: 'Peşin ödenecek toplam (bedel − kredi + masraflar)', deger: g.fiyat - kredi + ek, birim: '₺'});
  return {sonuclar: s, notlar: ['Satıcı da ayrıca ‰' + T.satici_binde + ' tapu harcı ve (varsa) %2 + KDV emlakçı komisyonu öder; bu araç alıcı masraflarını gösterir.', 'Emlakçı hizmet bedeli, Taşınmaz Ticareti Yönetmeliği\'ne göre alıcı ve satıcıdan toplam en fazla %4 (KDV hariç) alınabilir.', 'Taşınma, tadilat, abonelik (elektrik-su-doğalgaz) ve aidat gibi giderler dahil değildir.']};
}
""",
    "nasil": [
        "Bir evin gerçek maliyeti, satış bedelinden ibaret değildir. Alıcının ödediği zorunlu kalemler tapu harcı (satış bedelinin binde 20'si) ve Tapu Müdürlüğü döner sermaye ücretidir. Emlakçı aracılığıyla alımda hizmet bedeli genellikle satış bedelinin %2'si + %20 KDV'dir; yönetmelik gereği alıcı ve satıcıdan toplam alınabilecek bedel KDV hariç %4'ü aşamaz.",
        "Konut kredisi kullanılıyorsa bankaya ekspertiz ücreti (bağımsız değerleme), kredi tahsis ücreti (BDDK sınırı: kredi tutarının binde 5'i) ve zorunlu DASK ile genellikle istenen konut ve hayat sigortası primleri eklenir. Konut finansmanı kapsamındaki ipotek tesisi harçtan istisnadır; ipotek fekki (kaldırma) için küçük bir döner sermaye ücreti alınır.",
        "Toplamda ek masraflar satış bedelinin %4,5–6'sına ulaşır; 4 milyon ₺'lik bir evde 180-240 bin ₺ demektir. Bütçe planlarken peşinatın üzerine bu tutarı eklemek gerekir; bankalar masrafları krediye dahil etmez.",
    ],
    "formul": [
        "Tapu harcı (alıcı) = satış bedeli × ‰20",
        "Emlakçı = satış bedeli × %2 · KDV = komisyon × %20 → toplam %2,4",
        "Kredi tahsis ücreti ≤ kredi × ‰5 · ipotek harcı = 0 (konut kredisi istisnası)",
        "Toplam ek masraf = harç + döner sermaye + komisyon + KDV + tahsis + ekspertiz + sigortalar",
    ],
    "ornekler": [
        {"baslik": "4.000.000 ₺ ev, İstanbul, emlakçı %2, kredi yok", "adimlar": ["Tapu harcı 80.000 ₺ + döner sermaye 6.700 ₺", "Komisyon 80.000 ₺ + KDV 16.000 ₺", "Toplam ek masraf ≈ 182.700 ₺ (%4,6)"]},
        {"baslik": "Aynı ev, 3.000.000 ₺ konut kredisiyle", "adimlar": ["+ Tahsis ücreti 15.000 ₺ + ekspertiz (banka bildirir) + sigortalar", "Toplam ek masraf ≈ 200.000 ₺'ye yaklaşır"]},
    ],
    "tablo": {
        "baslik": "Ev alırken alıcı masrafları (2026)",
        "basliklar": ["Kalem", "Tutar / oran", "Zorunlu mu?"],
        "satirlar": [["Tapu harcı", "‰20 (satış bedeli)", "Evet"], ["Döner sermaye ücreti", "≈ 3.400 – 6.700 ₺", "Evet"], ["Emlakçı hizmet bedeli", "%2 + KDV %20 (üst sınır toplam %4)", "Emlakçı varsa"], ["Ekspertiz", "Bankaya göre", "Kredi varsa"], ["Kredi tahsis ücreti", "≤ ‰5 (kredi tutarı)", "Kredi varsa"], ["İpotek tesisi", "Harç istisna", "Kredi varsa"], ["DASK", "Bina büyüklüğü/bölgeye göre", "Evet"], ["Konut + hayat sigortası", "Bankaya göre", "Kredi varsa (genelde)"]],
        "not": "Harçlar Kanunu (4) sayılı tarife; Taşınmaz Ticareti Hakkında Yönetmelik m.20; BDDK tüketici kredisi ücret tebliği.",
    },
    "sss": [
        {"soru": "Ev alırken ne kadar masraf çıkar?", "cevap": "Satış bedelinin yaklaşık %4,5–6'sı: %2 tapu harcı, %2,4 emlakçı (KDV dahil), döner sermaye ve kredi masrafları."},
        {"soru": "Emlakçı komisyonu ne kadar, kim öder?", "cevap": "Yönetmeliğe göre KDV hariç toplam %4'ü aşamaz; uygulamada alıcı %2, satıcı %2 öder ve üzerine %20 KDV eklenir."},
        {"soru": "Tapu masrafını alıcı mı satıcı mı öder?", "cevap": "Kanunen her ikisi de ‰20 harç öder; döner sermayeyi genellikle alıcı öder. Taraflar aralarında farklı anlaşabilir."},
        {"soru": "Kredi masraflarını banka krediye ekler mi?", "cevap": "Hayır. Ekspertiz, tahsis ücreti ve sigortalar peşin ödenir; tahsis ücreti kredi tutarının binde 5'ini geçemez."},
        {"soru": "DASK zorunlu mu?", "cevap": "Evet, tapu devri ve abonelikler için Zorunlu Deprem Sigortası şarttır; prim bina yüzölçümü, yapı tarzı ve risk bölgesine göre belirlenir."},
    ],
    "kaynaklar": [
        {"ad": "Taşınmaz Ticareti Hakkında Yönetmelik (hizmet bedeli sınırı)", "url": "https://www.mevzuat.gov.tr/"},
        {"ad": "492 sayılı Harçlar Kanunu — tapu harçları", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=492&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "BDDK — Finansal Tüketicilerden Alınacak Ücretlere İlişkin Usul ve Esaslar", "url": "https://www.bddk.org.tr/"},
    ],
    "ilgili": ["tapu-harci-hesaplama", "konut-kredisi-hesaplama", "emlak-vergisi-hesaplama", "elbirligi-sistemi-hesaplama"],
}
