# -*- coding: utf-8 -*-
HESAP = {
    "slug": "tapu-harci-hesaplama",
    "baslik": "Tapu Harcı Hesaplama",
    "h1": "Tapu Harcı Hesaplama 2026 — Alıcı, Satıcı ve Döner Sermaye Ücreti",
    "kategori": "ev-emlak",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 tapu harcı hesaplama: satış bedeli üzerinden alıcı ‰20, satıcı ‰20 tapu harcı, döner sermaye ücreti ve toplam tapu masrafı. Konut, iş yeri ve arsa için aynı oran; muafiyetler ve ödeme.",
    "kisa_cevap": "Tapu harcı, satış bedelinin binde 20'si (yüzde 2) alıcıdan ve binde 20'si satıcıdan olmak üzere toplam yüzde 4'tür. 3.000.000 ₺'lik bir evde alıcı 60.000 ₺, satıcı 60.000 ₺ öder; ayrıca yaklaşık 3.400–6.700 ₺ döner sermaye ücreti alınır. Beyan edilen bedel emlak vergisi değerinden düşük olamaz.",
    "girdiler": [
        {"id": "bedel", "etiket": "Satış bedeli", "tip": "sayi", "varsayilan": "3000000", "birim": "₺"},
        {"id": "il", "etiket": "Taşınmazın bulunduğu il", "tip": "secim", "varsayilan": "buyuksehir",
         "secenekler": [["buyuksehir", "Büyükşehir (İstanbul, Ankara, İzmir vb.)"], ["diger", "Diğer iller"]]},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.bedel > 0)) return {hata: 'Satış bedelini girin.'};
  var alici = g.bedel * O.tapu_harci.alici_binde / 1000, satici = g.bedel * O.tapu_harci.satici_binde / 1000;
  var doner = g.il === 'buyuksehir' ? O.tapu_harci.doner_sermaye_buyuksehir : O.tapu_harci.doner_sermaye_diger;
  return {
    sonuclar: [
      {etiket: 'Toplam tapu harcı (alıcı + satıcı)', deger: alici + satici, birim: '₺', vurgu: true},
      {etiket: 'Alıcı harcı (‰' + O.tapu_harci.alici_binde + ')', deger: alici, birim: '₺'},
      {etiket: 'Satıcı harcı (‰' + O.tapu_harci.satici_binde + ')', deger: satici, birim: '₺'},
      {etiket: 'Döner sermaye ücreti (yaklaşık)', deger: doner, birim: '₺'},
      {etiket: 'Alıcının toplam tapu masrafı', deger: alici + doner, birim: '₺'}
    ],
    notlar: ['Uygulamada döner sermaye ücreti genellikle alıcı tarafından ödenir; taraflar harcı da anlaşarak paylaşabilir ancak kanuni sorumluluk her iki taraftadır.',
             'Döner sermaye ücreti ' + O.tapu_harci.doner_sermaye_not + '.']
  };
}
""",
    "nasil": [
        "Tapu harcı, taşınmaz alım-satımında 492 sayılı Harçlar Kanunu'na göre alınan devlet harcıdır. 2026'da oran alıcı için binde 20, satıcı için binde 20'dir; yani toplam yüzde 4. Harç, tapuda beyan edilen satış bedeli üzerinden hesaplanır ve bu bedel belediyenin emlak vergisi değerinin altında olamaz.",
        "Harca ek olarak Tapu ve Kadastro Genel Müdürlüğü'nün döner sermaye ücreti alınır; bu ücret her yıl güncellenir ve büyükşehir/diğer il ile işlem türüne göre değişir (2026'da yaklaşık 3.400–6.700 ₺). Harç ve ücret, işlem öncesi bankaya veya GİB üzerinden yatırılır; dekont olmadan tapu devri yapılmaz.",
        "Beyan edilen bedelin gerçek satış bedelinden düşük gösterilmesi halinde GİB, kredi kayıtları ve banka transferlerini çapraz kontrol ederek eksik harcı cezalı tahsil eder (izaha davet). Miras yoluyla intikal ve 6306 sayılı Kanun kapsamındaki kentsel dönüşüm işlemleri harçtan istisnadır.",
    ],
    "formul": [
        "Alıcı harcı = satış bedeli × 20 ÷ 1.000",
        "Satıcı harcı = satış bedeli × 20 ÷ 1.000",
        "Toplam harç = satış bedeli × %4",
        "Alıcı toplam masraf = alıcı harcı + döner sermaye ücreti",
    ],
    "ornekler": [
        {"baslik": "3.000.000 ₺ konut, İstanbul", "adimlar": ["Alıcı: 3.000.000 × 0,02 = 60.000 ₺", "Satıcı: 60.000 ₺", "Döner sermaye ≈ 6.700 ₺ → alıcı toplam ≈ 66.700 ₺"]},
        {"baslik": "1.200.000 ₺ arsa, Anadolu ili", "adimlar": ["Alıcı 24.000 ₺ + satıcı 24.000 ₺ = 48.000 ₺", "Döner sermaye ≈ 3.400 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 tapu harcı oranları",
        "basliklar": ["İşlem", "Alıcı", "Satıcı", "Not"],
        "satirlar": [["Alım-satım (konut, iş yeri, arsa, arazi)", "‰20", "‰20", "Toplam %4"], ["İpotek tesisi", "‰4,55 (borç tutarı üzerinden)", "—", "Konut kredisi ipotekleri istisna"],
                     ["Miras yoluyla intikal", "Harç yok", "—", "Veraset ve intikal vergisi ayrıca"], ["Kentsel dönüşüm (6306)", "İstisna", "İstisna", "İlk satış"]],
        "not": "492 sayılı Harçlar Kanunu (4) sayılı tarife. Oranlar Cumhurbaşkanı kararıyla değiştirilebilir.",
    },
    "sss": [
        {"soru": "Tapu harcını kim öder?", "cevap": "Kanunen alıcı ve satıcı ayrı ayrı binde 20 öder. Uygulamada taraflar anlaşarak tamamını bir tarafa yükleyebilir; döner sermaye ücretini genellikle alıcı öder."},
        {"soru": "Tapu harcı hangi bedel üzerinden hesaplanır?", "cevap": "Tapuda beyan edilen gerçek satış bedeli üzerinden. Bu bedel, belediyenin bildirdiği emlak vergisi değerinden düşük olamaz."},
        {"soru": "Düşük bedel beyan edersem ne olur?", "cevap": "GİB banka ve kredi kayıtlarından tespit ederse eksik harç, vergi ziyaı cezası ve gecikme faiziyle birlikte her iki taraftan alınır. Ayrıca satıcıda değer artış kazancı hesabı etkilenir."},
        {"soru": "Tapu harcı nereye ödenir?", "cevap": "GİB İnteraktif Vergi Dairesi, anlaşmalı bankalar veya vergi dairesi veznesine; ödeme dekontu ile randevu günü tapu işlemi yapılır."},
        {"soru": "Konut kredisiyle alımda ek harç var mı?", "cevap": "Konut finansmanı kapsamındaki ipotek tesisi harçtan istisnadır; yalnızca alım-satım harcı ve döner sermaye ödenir."},
    ],
    "kaynaklar": [
        {"ad": "492 sayılı Harçlar Kanunu — (4) sayılı tarife", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=492&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "TKGM — Döner sermaye hizmet bedelleri", "url": "https://www.tkgm.gov.tr/"},
        {"ad": "GİB — Tapu harcı ödeme", "url": "https://www.gib.gov.tr/"},
    ],
    "ilgili": ["konut-kredisi-hesaplama", "emlak-vergisi-hesaplama", "elbirligi-sistemi-hesaplama"],
}
