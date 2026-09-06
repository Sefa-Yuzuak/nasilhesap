# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kredi-karti-asgari-odeme-hesaplama",
    "baslik": "Kredi Kartı Asgari Ödeme ve Faiz Hesaplama",
    "h1": "Kredi Kartı Asgari Ödeme Hesaplama 2026 — Faiz, Gecikme Faizi ve Kalan Borç",
    "kategori": "kredi-finans",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Kredi kartı asgari ödeme tutarı (limit 50.000 ₺'ye kadar %20, üzeri %40), asgari ödeyince kalan borca işleyecek akdi faiz (TCMB: %3,25 / %3,75 / %4,25), gecikme faizi, BSMV-KKDF dahil gerçek maliyet ve borcun kaç ayda biteceği.",
    "kisa_cevap": "Asgari ödeme, dönem borcunun kart limiti 50.000 ₺ ve altındaysa %20'si, üzerindeyse %40'ıdır (BDDK, 26.09.2024). Kalan borca TCMB'nin borç kademesine göre belirlediği aylık akdi faiz (30.000 ₺'ye kadar %3,25; 180.000 ₺'ye kadar %3,75; üzeri %4,25) ve üzerine %15 BSMV + %15 KKDF işler; gecikmede faiz 0,30 puan yüksektir. 40.000 ₺ borç, 30.000 ₺ limitli kartta asgari 8.000 ₺; kalan 32.000 ₺'ye aylık ≈ 1.560 ₺ faiz+vergi biner.",
    "girdiler": [
        {"id": "limit", "etiket": "Kart limiti", "tip": "sayi", "varsayilan": "30000", "birim": "₺"},
        {"id": "borc", "etiket": "Dönem borcu (ekstre)", "tip": "sayi", "varsayilan": "40000", "birim": "₺"},
        {"id": "odeme", "etiket": "Ödemeyi planladığınız tutar (boş = asgari)", "tip": "sayi", "varsayilan": "", "birim": "₺"},
    ],
    "js": r"""
function akdi(borc, K){ for (var i = 0; i < K.akdi.length; i++) { var ust = K.akdi[i][0]; if (ust === null || borc <= ust) return K.akdi[i][1]; } return K.akdi[K.akdi.length-1][1]; }
function hesapla(g, O){
  if (!(g.borc > 0) || !(g.limit > 0)) return {hata: 'Limit ve dönem borcunu girin.'};
  var K = O.kredi_karti;
  var oranA = g.limit <= K.asgari_limit_esik ? K.asgari_alt : K.asgari_ust;
  var asgari = Math.min(g.borc, g.borc * oranA);
  var odeme = g.odeme > 0 ? Math.min(g.odeme, g.borc) : asgari;
  var kalan = g.borc - odeme;
  var fa = akdi(g.borc, K), fg = fa + K.gecikme_ek;
  var faizNet, faizTop, tur;
  if (odeme >= asgari) { faizNet = kalan * fa / 100; tur = 'Akdi faiz (%' + fa + ')'; }
  else { var eksik = asgari - odeme; faizNet = (kalan - eksik) * fa / 100 + eksik * fg / 100; tur = 'Akdi %' + fa + ' + gecikme %' + fg + ' (asgarinin eksik kısmına)'; }
  faizTop = faizNet * (1 + K.vergi);
  // yalnız asgari ödeyerek kapanış süresi (asgari oranıyla, faiz dahil)
  var ay = 0, b = g.borc, topFaiz = 0;
  if (odeme >= asgari) { while (b > 1 && ay < 600) { var od = Math.max(b * oranA, Math.min(b, 100)); b -= od; var f = b * akdi(b, K) / 100 * (1 + K.vergi); b += f; topFaiz += f; ay++; } }
  var s = [
    {etiket: 'Asgari ödeme tutarı (%' + Math.round(oranA*100) + ')', deger: asgari, birim: '₺', vurgu: true},
    {etiket: 'Planlanan ödeme', deger: odeme, birim: '₺'},
    {etiket: 'Kalan borç', deger: kalan, birim: '₺'},
    {etiket: 'Gelecek ekstreye binecek faiz + vergi', deger: faizTop, birim: '₺'},
    {etiket: '— faiz (' + tur + ')', deger: faizNet, birim: '₺'},
    {etiket: '— BSMV + KKDF (%30)', deger: faizTop - faizNet, birim: '₺'},
    {etiket: 'Etkin aylık maliyet (vergi dahil)', deger: fa * (1 + K.vergi), birim: '%'}
  ];
  if (odeme >= asgari && kalan > 0) { s.push({etiket: 'Hep asgari ödenirse kapanma süresi', deger: ay >= 600 ? '50 yıldan uzun' : ay + ' ay'}); s.push({etiket: 'Hep asgari ödenirse toplam faiz+vergi', deger: topFaiz, birim: '₺'}); }
  var n = ['TCMB akdi faiz oranları borç kademesine göre uygulanır ve her ay güncellenebilir (' + K.donem + ' oranları). Gecikme faizi akdi faizin 0,30 puan üzeridir.',
           'Asgari tutarı üst üste 3 dönem ödemeyen kartlar nakit çekime, sonra alışverişe kapatılır; asgari ödemenin altında kalan kısma gecikme faizi işler.'];
  if (g.limit <= K.asgari_limit_esik) n.push('Limit 50.000 ₺ ve altı: asgari ödeme dönem borcunun %20\'si.'); else n.push('Limit 50.000 ₺ üzeri: asgari ödeme dönem borcunun %40\'ı (BDDK 26.09.2024).');
  return {sonuclar: s, notlar: n};
}
""",
    "nasil": [
        "Kredi kartı ekstresinde 'asgari ödeme tutarı', o dönem borcunun kartı kapattırmamak için ödenmesi zorunlu kısmıdır. BDDK'nın 26 Eylül 2024 tarihli kararına göre oran kart limitine bağlıdır: limiti 50.000 ₺ ve altında olan kartlarda dönem borcunun %20'si, 50.000 ₺ üzerindeki kartlarda %40'ı. Asgariyi ödemek borcu kapatmaz; kalan tutara faiz işler.",
        "Kalan borca uygulanan aylık akdi faiz TCMB tarafından belirlenir ve 2026'dan itibaren borç tutarına göre kademelidir: 30.000 ₺'ye kadar %3,25, 30.000–180.000 ₺ arası %3,75, üzeri %4,25. Faizin üzerine %15 BSMV ve %15 KKDF eklendiği için gerçek maliyet ilan edilen faizin 1,3 katıdır (%3,75 → %4,875). Asgarinin altında ödeme yapılırsa eksik kısma 0,30 puan yüksek gecikme faizi işler.",
        "Sürekli yalnızca asgari ödemek borcu yıllara yayar: %20 asgari ile 40.000 ₺'lik borç, faiz+vergi eklene eklene onlarca ay sürer ve ödenen faiz anaparaya yaklaşır. Borcu kapatmanın en ucuz yolu asgarinin çok üzerinde ödemek ya da daha düşük faizli ihtiyaç kredisiyle yapılandırmaktır.",
    ],
    "formul": [
        "Asgari ödeme = dönem borcu × (%20 limit ≤ 50.000 ₺ · %40 limit > 50.000 ₺)",
        "Aylık faiz = kalan borç × akdi faiz (borç kademesine göre %3,25 / %3,75 / %4,25)",
        "Faiz + vergi = faiz × 1,30 (BSMV %15 + KKDF %15)",
        "Gecikme faizi = akdi faiz + 0,30 puan (asgarinin ödenmeyen kısmına)",
    ],
    "ornekler": [
        {"baslik": "30.000 ₺ limit, 40.000 ₺ borç, yalnızca asgari", "adimlar": ["Asgari: 40.000 × %20 = 8.000 ₺", "Kalan 32.000 ₺; borç kademesi 30.000–180.000 → %3,75", "Faiz 1.200 ₺ + vergi 360 ₺ = 1.560 ₺ gelecek ekstreye eklenir"]},
        {"baslik": "80.000 ₺ limit, 60.000 ₺ borç", "adimlar": ["Asgari: 60.000 × %40 = 24.000 ₺", "Kalan 36.000 ₺ → faiz %3,75 → 1.350 ₺ + 405 ₺ vergi"]},
    ],
    "tablo": {
        "baslik": "2026 kredi kartı faiz ve asgari ödeme parametreleri",
        "basliklar": ["Kalem", "Değer"],
        "satirlar": [["Asgari ödeme — limit ≤ 50.000 ₺", "%20"], ["Asgari ödeme — limit > 50.000 ₺", "%40"], ["Akdi faiz — borç ≤ 30.000 ₺", "%3,25 / ay"], ["Akdi faiz — 30.000–180.000 ₺", "%3,75 / ay"], ["Akdi faiz — > 180.000 ₺", "%4,25 / ay"], ["Gecikme faizi", "akdi + 0,30 puan"], ["BSMV + KKDF", "%15 + %15 (faiz üzerinden)"], ["Nakit avans faizi", "akdi faizle aynı kademeler"]],
        "not": "BDDK 26.09.2024 kararı; TCMB kredi kartı azami faiz oranları (Ocak 2026). TCMB oranları aylık güncelleyebilir; ekstrenizdeki oran esastır.",
    },
    "sss": [
        {"soru": "Kredi kartı asgari ödeme yüzde kaç?", "cevap": "Kart limiti 50.000 ₺ ve altındaysa dönem borcunun %20'si, limit 50.000 ₺ üzerindeyse %40'ı."},
        {"soru": "Asgari tutarı ödersem faiz işler mi?", "cevap": "Evet. Asgari ödeme yalnızca gecikme faizini ve kartın kapanmasını önler; kalan borca akdi faiz + BSMV + KKDF işler."},
        {"soru": "Kredi kartı faizi 2026'da yüzde kaç?", "cevap": "TCMB'ye göre borç kademeli: 30.000 ₺'ye kadar %3,25, 180.000 ₺'ye kadar %3,75, üzeri %4,25 (aylık). Vergilerle etkin maliyet 1,3 katıdır."},
        {"soru": "Asgariyi ödemezsem ne olur?", "cevap": "Eksik kısma gecikme faizi (akdi + 0,30 puan) işler; üst üste 3 dönem asgari ödenmezse kart önce nakit çekime, sonra alışverişe kapatılır ve kredi notu düşer."},
        {"soru": "Kart borcunu taksitlendirmek mantıklı mı?", "cevap": "Bankaların ekstre taksitlendirmesi genellikle akdi faizle yapılır; daha düşük faizli ihtiyaç kredisiyle kapatmak çoğu zaman daha ucuzdur. Karşılaştırmak için kredi hesaplayıcımızı kullanın."},
    ],
    "kaynaklar": [
        {"ad": "TCMB — Kredi kartı işlemlerinde uygulanacak azami faiz oranları", "url": "https://www.tcmb.gov.tr/"},
        {"ad": "BDDK — Banka Kartları ve Kredi Kartları Hakkında Yönetmelik (asgari ödeme)", "url": "https://www.bddk.org.tr/"},
    ],
    "ilgili": ["kredi-hesaplama", "yuzde-hesaplama", "bilesik-faiz-hesaplama"],
}
