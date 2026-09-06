# -*- coding: utf-8 -*-
HESAP = {
    "slug": "konut-kredisi-hesaplama",
    "baslik": "Konut Kredisi Hesaplama",
    "h1": "Konut Kredisi Hesaplama 2026 — Taksit, Peşinat ve Toplam Maliyet",
    "kategori": "ev-emlak",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Konut kredisi hesaplama: ev fiyatı, peşinat oranı, aylık faiz ve vadeye göre aylık taksit, toplam geri ödeme, toplam faiz ve tapu harcı dahil ev alma maliyeti. KKDF-BSMV muafiyeti, ödeme planı.",
    "kisa_cevap": "Konut kredisi taksiti = kredi × r ÷ (1 − (1 + r)^−n); konut kredilerinde KKDF ve BSMV alınmadığı için r doğrudan bankanın aylık faizidir. 5.000.000 ₺'lik evde %20 peşinatla 4.000.000 ₺ krediyi %2,5 aylık faiz ve 120 ay vadeyle aylık yaklaşık 104.145 ₺ taksitle ödersiniz; tapu harcı alıcı için ‰20'dir.",
    "girdiler": [
        {"id": "fiyat", "etiket": "Ev fiyatı", "tip": "sayi", "varsayilan": "5000000", "birim": "₺"},
        {"id": "pesinat", "etiket": "Peşinat oranı", "tip": "sayi", "varsayilan": "20", "birim": "%"},
        {"id": "faiz", "etiket": "Aylık faiz oranı", "tip": "sayi", "varsayilan": "2.5", "birim": "%"},
        {"id": "vade", "etiket": "Vade", "tip": "tamsayi", "varsayilan": "120", "birim": "ay"},
    ],
    "js": r"""
function hesapla(g, O){
  if (!(g.fiyat > 0) || !(g.faiz >= 0) || !(g.vade > 0)) return {hata: 'Fiyat, faiz ve vadeyi girin.'};
  var pes = g.fiyat * (g.pesinat || 0) / 100, kredi = g.fiyat - pes;
  if (kredi <= 0) return {hata: 'Peşinat ev fiyatına eşit veya büyük olamaz.'};
  var r = g.faiz / 100, n = g.vade;
  var taksit = r === 0 ? kredi / n : kredi * r / (1 - Math.pow(1 + r, -n));
  var toplam = taksit * n, faiz = toplam - kredi;
  var harc = g.fiyat * O.tapu_harci.alici_binde / 1000;
  var rows = [], kalan = kredi;
  for (var i = 1; i <= n; i++) { var f = kalan * r, a = taksit - f; kalan -= a; if (i <= 6 || i === n) rows.push([i, taksit, a, f, Math.max(0, kalan)]); else if (i === 7) rows.push(['…','','','','']); }
  return {
    sonuclar: [
      {etiket: 'Aylık taksit', deger: taksit, birim: '₺', vurgu: true},
      {etiket: 'Kredi tutarı', deger: kredi, birim: '₺'},
      {etiket: 'Peşinat', deger: pes, birim: '₺'},
      {etiket: 'Toplam geri ödeme', deger: toplam, birim: '₺'},
      {etiket: 'Toplam faiz', deger: faiz, birim: '₺'},
      {etiket: 'Tapu harcı (alıcı, ‰' + O.tapu_harci.alici_binde + ')', deger: harc, birim: '₺'},
      {etiket: 'Evin toplam maliyeti (peşinat + taksitler + harç)', deger: pes + toplam + harc, birim: '₺'},
      {etiket: 'Taksit / kredi oranı (aylık)', deger: taksit / kredi * 100, birim: '%'}
    ],
    tablo: {basliklar: ['Ay', 'Taksit', 'Anapara', 'Faiz', 'Kalan'], satirlar: rows},
    notlar: ['Konut kredilerinde KKDF ve BSMV alınmaz. Ekspertiz, ipotek tesis ücreti, DASK ve konut sigortası dahil değildir.',
             'Peşinat: BDDK düzenlemelerine göre kredi tutarı, konut değerinin belirli bir oranını (genellikle %75-90, değere göre kademeli) aşamaz; bankanız kesin oranı bildirir.']
  };
}
""",
    "nasil": [
        "Konut kredisi de diğer krediler gibi eşit taksitli (anüite) planla ödenir; farkı, faiz üzerinden KKDF ve BSMV alınmamasıdır. Bu nedenle bankanın ilan ettiği aylık faiz doğrudan hesaba girer ve aynı faizli bir ihtiyaç kredisine göre %30 daha ucuzdur.",
        "Kredi tutarı, ev fiyatından peşinat düşülerek bulunur. BDDK, kredi/değer (LTV) oranına üst sınır koyar; konutun değerine göre kademeli olarak değişen bu sınır nedeniyle bankalar genellikle en az %10-25 peşinat ister. Ekspertiz değeri satış fiyatının altında çıkarsa kredi ekspertiz değeri üzerinden hesaplanır.",
        "Toplam maliyeti görmek için taksitlerin toplamına peşinatı, alıcı tapu harcını (‰20) ve döner sermaye ücretini ekleyin. 120 ay gibi uzun vadelerde toplam faiz, anaparanın iki katını aşabilir; vadeyi kısaltmak toplam maliyeti belirgin biçimde düşürür.",
    ],
    "formul": [
        "Kredi = ev fiyatı × (1 − peşinat %)",
        "Aylık taksit = kredi × r ÷ (1 − (1 + r)^−n) · r = aylık faiz (vergi yok)",
        "Toplam faiz = taksit × n − kredi",
        "Tapu harcı (alıcı) = ev fiyatı × ‰20",
    ],
    "ornekler": [
        {"baslik": "5.000.000 ₺ ev, %20 peşinat, %2,5 aylık, 120 ay", "adimlar": ["Peşinat 1.000.000 ₺ → kredi 4.000.000 ₺", "Taksit ≈ 4.000.000 × 0,025 ÷ (1 − 1,025^−120) ≈ 104.145 ₺", "Toplam geri ödeme ≈ 12.497.400 ₺; faiz ≈ 8.497.400 ₺", "Tapu harcı 100.000 ₺ → toplam maliyet ≈ 13.597.400 ₺"]},
        {"baslik": "Aynı kredi, 60 ay vade", "adimlar": ["Taksit ≈ 134.632 ₺ (daha yüksek)", "Toplam ≈ 8.077.900 ₺; faiz ≈ 4.077.900 ₺ — 120 aya göre 4,4 milyon ₺ daha az"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Konut kredisinde KKDF ve BSMV alınır mı?", "cevap": "Hayır. Konut finansmanı kredileri her iki vergiden de muaftır; bu yüzden aynı faizli ihtiyaç kredisinden %30 daha düşük maliyetlidir."},
        {"soru": "Konut kredisi için ne kadar peşinat gerekir?", "cevap": "BDDK'nın kredi/değer sınırına göre bankalar genellikle konut değerinin %10-25'i kadar peşinat ister; sınır konutun değerine göre kademelidir ve dönemsel olarak değişir."},
        {"soru": "Faiz oranı düşerse ne yapmalıyım?", "cevap": "Mevcut krediyi daha düşük faizle yeniden yapılandırabilir veya başka bankaya taşıyabilirsiniz; konut kredilerinde erken kapatmada kalan vade 36 ayı geçiyorsa %2'ye kadar erken ödeme ücreti alınabilir."},
        {"soru": "Aylık taksit gelirimin ne kadarı olmalı?", "cevap": "Bankalar genellikle taksitin net hane gelirinin %50'sini aşmamasını ister; güvenli bütçe için %30-40 önerilir."},
        {"soru": "Ekspertiz değeri neyi etkiler?", "cevap": "Kredi, satış fiyatı ile ekspertiz değerinden düşük olanı üzerinden hesaplanır. Ekspertiz düşük çıkarsa aradaki farkı peşinat olarak karşılamanız gerekir."},
    ],
    "kaynaklar": [
        {"ad": "BDDK — Bankaların Kredi İşlemlerine İlişkin Yönetmelik (kredi/değer oranı)", "url": "https://www.bddk.org.tr/"},
        {"ad": "TKGM — Tapu harcı ve döner sermaye ücretleri", "url": "https://www.tkgm.gov.tr/"},
    ],
    "ilgili": ["kredi-hesaplama", "tapu-harci-hesaplama", "elbirligi-sistemi-hesaplama", "emlak-vergisi-hesaplama"],
}
