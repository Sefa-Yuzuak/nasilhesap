# -*- coding: utf-8 -*-
HESAP = {
    "slug": "stopaj-hesaplama",
    "baslik": "Stopaj Hesaplama",
    "h1": "Stopaj Hesaplama 2026 — Serbest Meslek Makbuzu, Kira Stopajı, Brütten Nete",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Stopaj hesaplama: serbest meslek makbuzunda %20 gelir vergisi stopajı ve %20 KDV ile net ele geçen ve müşterinin ödeyeceği tutar; iş yeri kira stopajı; netten brüte çevirme.",
    "kisa_cevap": "Stopaj, ödemeyi yapanın vergiyi kaynakta kesip vergi dairesine yatırmasıdır. Serbest meslek ödemelerinde ve iş yeri kiralarında oran %20'dir. 10.000 ₺ brüt serbest meslek makbuzunda stopaj 2.000 ₺, KDV (%20) 2.000 ₺'dir: serbest meslek erbabının eline 8.000 ₺ geçer, müşteri 10.000 ₺ öder (KDV dahil 12.000 − stopaj 2.000).",
    "girdiler": [
        {"id": "tur", "etiket": "Ödeme türü", "tip": "secim", "varsayilan": "smm", "genis": True,
         "secenekler": [["smm", "Serbest meslek makbuzu (%20 stopaj + %20 KDV)"], ["kira", "İş yeri kirası — gerçek kişiye (%20 stopaj, KDV yok)"], ["ozel", "Özel stopaj oranı"]]},
        {"id": "yon", "etiket": "Bilinen tutar", "tip": "secim", "varsayilan": "brut", "secenekler": [["brut", "Brüt (stopaj öncesi)"], ["net", "Net (elime geçen)"]]},
        {"id": "tutar", "etiket": "Tutar", "tip": "sayi", "varsayilan": "10000", "birim": "₺"},
        {"id": "oran", "etiket": "Stopaj oranı", "tip": "sayi", "varsayilan": "20", "birim": "%", "gizli": "tur=ozel"},
        {"id": "kdv", "etiket": "KDV oranı (özel türde)", "tip": "sayi", "varsayilan": "20", "birim": "%", "gizli": "tur=ozel"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.tutar > 0)) return {hata: 'Tutarı girin.'};
  var oran = g.tur === 'ozel' ? (g.oran || 0) / 100 : 0.20;
  var kdvO = g.tur === 'smm' ? 0.20 : g.tur === 'ozel' ? (g.kdv || 0) / 100 : 0;
  var brut = g.yon === 'brut' ? g.tutar : g.tutar / (1 - oran);
  var stopaj = brut * oran, net = brut - stopaj, kdv = brut * kdvO;
  var s = [
    {etiket: g.yon === 'brut' ? 'Net ele geçen' : 'Brüt tutar', deger: g.yon === 'brut' ? net : brut, birim: '₺', vurgu: true},
    {etiket: 'Brüt (stopaj matrahı)', deger: brut, birim: '₺'},
    {etiket: 'Stopaj (%' + (oran*100) + ')', deger: stopaj, birim: '₺'},
    {etiket: 'Net ele geçen', deger: net, birim: '₺'}
  ];
  if (kdvO) { s.push({etiket: 'Hesaplanan KDV (%' + (kdvO*100) + ')', deger: kdv, birim: '₺'}); s.push({etiket: 'Makbuz toplamı (brüt + KDV)', deger: brut + kdv, birim: '₺'}); s.push({etiket: 'Müşterinin ödeyeceği (toplam − stopaj)', deger: brut + kdv - stopaj, birim: '₺'}); }
  else s.push({etiket: 'Ödeyenin (kiracının) ödeyeceği', deger: net, birim: '₺'});
  var n = ['Stopajı ödemeyi yapan (müşteri/kiracı) muhtasar beyanname ile vergi dairesine yatırır; alan taraf bunu yıllık beyannamesinde mahsup eder.'];
  if (g.tur === 'smm') n.push('KDV, brüt ücret üzerinden hesaplanır ve müşteri tarafından ödenir; serbest meslek erbabı KDV beyannamesiyle devlete aktarır. Müşteri vergi mükellefi değilse (nihai tüketici) stopaj yapılmaz.');
  if (g.tur === 'kira') n.push('Stopaj yalnızca kiracı vergi mükellefi (şirket, işletme) ise yapılır; mal sahibi şirketse kira faturalı ve KDV\'li olur, stopaj yapılmaz.');
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Stopaj (tevkifat), gelirin sahibine ödenmeden önce vergisinin ödemeyi yapan tarafça kesilip devlete yatırılmasıdır; Gelir Vergisi Kanunu m.94'te hangi ödemelerden hangi oranda kesinti yapılacağı sayılır. En sık karşılaşılan ikisi serbest meslek ödemeleri (avukat, doktor, mühendis, danışman, freelancer) ve gerçek kişilere ödenen iş yeri kiralarıdır; her ikisinde de oran %20'dir.",
        "Serbest meslek makbuzunda üç kalem vardır: brüt ücret, bunun %20'si stopaj ve %20 KDV. Meslek erbabının eline brüt − stopaj geçer; müşteri ise brüt + KDV − stopaj öder ve stopajı muhtasar beyannameyle vergi dairesine yatırır. KDV'yi meslek erbabı beyan eder. Müşteri vergi mükellefi değilse (ör. bireysel danışan) stopaj kesilmez, tam tutar ödenir.",
        "Netten brüte çevirmek için net tutar (1 − stopaj oranı)'na bölünür: 8.000 ₺ net için brüt 10.000 ₺. Serbest meslek erbabı ve mal sahibi, kesilen stopajı yıllık gelir vergisi beyannamesinde hesaplanan vergiden düşer; fazla kesinti varsa iade alır.",
    ],
    "formul": [
        "Stopaj = brüt × oran (%20)",
        "Net = brüt − stopaj · Brüt = net ÷ (1 − oran)",
        "Serbest meslek: KDV = brüt × %20 · müşteri ödemesi = brüt + KDV − stopaj",
        "İş yeri kirası (gerçek kişiye): kiracı öder = brüt − stopaj; stopajı vergi dairesine yatırır",
    ],
    "ornekler": [
        {"baslik": "10.000 ₺ brüt danışmanlık makbuzu", "adimlar": ["Stopaj: 2.000 ₺ · KDV: 2.000 ₺", "Danışmanın eline: 8.000 ₺", "Müşteri öder: 10.000 + 2.000 − 2.000 = 10.000 ₺ (+ 2.000 ₺ stopaj vergi dairesine)"]},
        {"baslik": "Net 20.000 ₺ elime geçsin istiyorum", "adimlar": ["Brüt: 20.000 ÷ 0,80 = 25.000 ₺", "Stopaj 5.000 ₺, KDV 5.000 ₺, makbuz toplamı 30.000 ₺"]},
        {"baslik": "Şirket, gerçek kişiden 30.000 ₺ brüt kira", "adimlar": ["Stopaj: 6.000 ₺ → mal sahibine 24.000 ₺ ödenir", "6.000 ₺ muhtasar beyannameyle yatırılır"]},
    ],
    "tablo": {
        "baslik": "Sık karşılaşılan stopaj oranları (GVK m.94, 2026)",
        "basliklar": ["Ödeme", "Oran"],
        "satirlar": [["Serbest meslek ödemeleri", "%20"], ["Gerçek kişilere iş yeri kirası", "%20"], ["Telif (GVK 18 istisnası kapsamı)", "%17"], ["Yıllara yaygın inşaat hakedişleri", "%5"], ["Gider pusulası (esnaf muaflığı, mal/hizmet)", "%2 – %20"], ["Mevduat faizi (6 aya kadar)", "%19,5"], ["Kâr payı (temettü)", "%15"]],
        "not": "Oranlar Cumhurbaşkanı kararlarıyla değişebilir; güncel liste için GİB'e bakın.",
    },
    "sss": [
        {"soru": "Stopaj ne demek?", "cevap": "Vergiyi gelir sahibi yerine ödemeyi yapanın kesip devlete yatırmasıdır (kaynakta kesinti). Kesilen tutar, gelir sahibinin yıllık vergisinden mahsup edilir."},
        {"soru": "Stopajı kim öder?", "cevap": "Ekonomik yükü gelir sahibi taşır (brütten düşülür) ama vergi dairesine ödemeyi yapan taraf (müşteri, kiracı, işveren) muhtasar beyannameyle yatırır."},
        {"soru": "Serbest meslek makbuzunda KDV ve stopaj birlikte mi hesaplanır?", "cevap": "Evet, ikisi de brüt ücret üzerinden ayrı ayrı hesaplanır: %20 stopaj ve %20 KDV. Stopaj düşülür, KDV eklenir."},
        {"soru": "Bireysel müşteriye stopaj kesilir mi?", "cevap": "Hayır. Stopaj yalnızca ödemeyi yapan vergi mükellefi (şirket, işletme, kamu kurumu) ise kesilir; nihai tüketiciye düzenlenen makbuzda stopaj olmaz."},
        {"soru": "Kesilen stopajı geri alabilir miyim?", "cevap": "Yıllık beyannamede hesaplanan vergi kesilen stopajdan azsa fark iade edilir (mahsuben veya nakden)."},
    ],
    "kaynaklar": [
        {"ad": "193 sayılı Gelir Vergisi Kanunu m.94 (vergi tevkifatı)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=193&MevzuatTur=1&MevzuatTertip=4"},
        {"ad": "GİB — Serbest Meslek Kazançları Vergi Rehberi", "url": "https://www.gib.gov.tr/"},
    ],
    "ilgili": ["kdv-hesaplama", "kira-geliri-vergisi-hesaplama", "gelir-vergisi-hesaplama"],
}
