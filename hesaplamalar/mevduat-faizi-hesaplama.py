# -*- coding: utf-8 -*-
HESAP = {
    "slug": "mevduat-faizi-hesaplama",
    "baslik": "Mevduat Faizi Hesaplama",
    "h1": "Mevduat Faizi Hesaplama 2026 — Vadeli Hesap Net Getiri, Stopaj Dahil",
    "kategori": "kredi-finans",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Vadeli mevduat faizi hesaplama: anapara, yıllık faiz ve vade gününe göre brüt faiz, stopaj (6 aya kadar %17,5, 1 yıla kadar %15, 1 yıldan uzun %10) ve net getiri. 32 günlük vadede 100.000 ₺ ne kazandırır?",
    "kisa_cevap": "Mevduat faizi = anapara × yıllık faiz × vade günü ÷ 365; bulunan brüt faizden stopaj düşülür. 2026'da TL mevduat stopajı 6 aya kadar vadede %17,5, 1 yıla kadar %15, 1 yıldan uzun vadede %10'dur. 100.000 ₺, yıllık %40, 32 gün vadede brüt faiz 3.506,85 ₺, stopaj 613,70 ₺, net 2.893,15 ₺'dir.",
    "girdiler": [
        {"id": "ana", "etiket": "Anapara", "tip": "sayi", "varsayilan": "100000", "birim": "₺"},
        {"id": "faiz", "etiket": "Yıllık brüt faiz oranı", "tip": "sayi", "varsayilan": "40", "birim": "%"},
        {"id": "gun", "etiket": "Vade", "tip": "tamsayi", "varsayilan": "32", "birim": "gün"},
        {"id": "yenile", "etiket": "Kaç kez üst üste yenilensin? (bileşik)", "tip": "tamsayi", "varsayilan": "1", "birim": "kez"},
    ],
    "js": r"""
function stopajOran(gun, O){ var ay = gun / 30.4375; var L = O.mevduat_stopaj.tl; for (var i = 0; i < L.length; i++) { if (L[i][0] === null || ay <= L[i][0]) return L[i][1]; } return L[L.length-1][1]; }
function hesapla(g, O){
  if (!(g.ana > 0) || !(g.faiz >= 0) || !(g.gun > 0)) return {hata: 'Anapara, faiz ve vadeyi girin.'};
  var st = stopajOran(g.gun, O), kez = g.yenile > 0 ? Math.min(g.yenile, 120) : 1;
  var brutFaiz = g.ana * g.faiz / 100 * g.gun / 365, stopaj = brutFaiz * st, net = brutFaiz - stopaj;
  var bakiye = g.ana, topNet = 0, topStopaj = 0, rows = [];
  for (var i = 1; i <= kez; i++) { var bf = bakiye * g.faiz / 100 * g.gun / 365, sp = bf * st; bakiye += bf - sp; topNet += bf - sp; topStopaj += sp; if (i <= 12 || i === kez) rows.push([i + '. vade', bf, sp, bakiye]); else if (i === 13) rows.push(['…','','','']); }
  var yillikNet = g.faiz * (1 - st), gunlukNet = net / g.gun;
  var s = [
    {etiket: 'Vade sonu net faiz', deger: net, birim: '₺', vurgu: true},
    {etiket: 'Brüt faiz', deger: brutFaiz, birim: '₺'},
    {etiket: 'Stopaj (%' + (st*100).toFixed(1).replace('.', ',') + ')', deger: stopaj, birim: '₺'},
    {etiket: 'Vade sonu toplam (anapara + net faiz)', deger: g.ana + net, birim: '₺'},
    {etiket: 'Net yıllık faiz (stopaj sonrası)', deger: yillikNet, birim: '%'},
    {etiket: 'Günlük net getiri', deger: gunlukNet, birim: '₺'}
  ];
  if (kez > 1) { s.push({etiket: kez + ' yenileme sonunda bakiye', deger: bakiye, birim: '₺'}); s.push({etiket: 'Toplam net faiz (' + kez + ' vade)', deger: topNet, birim: '₺'}); }
  return {sonuclar: s, tablo: kez > 1 ? {basliklar: ['Vade', 'Brüt faiz', 'Stopaj', 'Bakiye'], satirlar: rows} : null,
    notlar: ['Stopaj vadeye göre: 6 aya kadar %17,5 · 1 yıla kadar %15 · 1 yıldan uzun %10 (CB Kararı 11444, 31.12.2026\'ya kadar). Katılım hesaplarında aynı oranlar geçerlidir.',
             'Bankalar faizi 365 gün üzerinden hesaplar; vade bozulursa faiz ödenmez. Enflasyon dikkate alınmamıştır (reel getiri için enflasyon hesaplayıcısına bakın).']};
}
""",
    "nasil": [
        "Vadeli mevduatta banka, anaparaya yıllık faiz oranını vade günüyle orantılı uygular: brüt faiz = anapara × faiz × gün ÷ 365. 32 günlük vadede yıllık %40 faiz, 100.000 ₺ için 3.506,85 ₺ brüt faiz getirir. Vade dolmadan para çekilirse faiz ödenmez; bu yüzden 32 günlük kısa vadeler yaygındır.",
        "Brüt faizden gelir vergisi stopajı kesilir ve bu stopaj nihai vergidir (beyan gerekmez). Oran vadeye göre değişir ve uzun vadeyi teşvik eder: 2026'da 6 aya kadar %17,5, 1 yıla kadar %15, 1 yıldan uzun vadede %10 (Cumhurbaşkanı Kararı 11444, 31 Aralık 2026'ya kadar geçerli). Net faiz = brüt faiz − stopaj.",
        "Vade sonunda faiz anaparaya eklenip yenilenirse getiri bileşik büyür; 12 kez yenilenen 32 günlük vade, yıllık %40 nominalde yaklaşık %38 net bileşik getiriye ulaşır. Getiriyi değerlendirirken enflasyonu düşerek reel getiriye bakmak gerekir; faiz enflasyonun altındaysa satın alma gücü azalır.",
    ],
    "formul": [
        "Brüt faiz = anapara × yıllık faiz ÷ 100 × vade günü ÷ 365",
        "Stopaj = brüt faiz × oran (≤6 ay %17,5 · ≤1 yıl %15 · >1 yıl %10)",
        "Net faiz = brüt faiz − stopaj · Net yıllık oran = brüt oran × (1 − stopaj)",
        "Yenilemede: yeni anapara = anapara + net faiz (bileşik)",
    ],
    "ornekler": [
        {"baslik": "100.000 ₺, %40, 32 gün", "adimlar": ["Brüt: 100.000 × 0,40 × 32 ÷ 365 = 3.506,85 ₺", "Stopaj %17,5: 613,70 ₺", "Net: 2.893,15 ₺ → vade sonu 102.893,15 ₺"]},
        {"baslik": "500.000 ₺, %38, 1 yıl (365 gün)", "adimlar": ["Brüt: 190.000 ₺", "Stopaj %15 (1 yıla kadar): 28.500 ₺", "Net: 161.500 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 mevduat stopaj oranları (TL, katılım hesapları dahil)",
        "basliklar": ["Vade", "Stopaj"],
        "satirlar": [["Vadesiz ve 6 aya kadar", "%17,5"], ["6 ay – 1 yıl", "%15"], ["1 yıldan uzun", "%10"], ["Devlet tahvili / hazine bonosu / kira sertifikası", "%0"]],
        "not": "Cumhurbaşkanı Kararı 11444 (RG 20.06.2026, Sayı 33286); 31.12.2026'ya kadar geçerli. Döviz mevduatında oranlar farklıdır.",
    },
    "sss": [
        {"soru": "100.000 TL 32 günde ne kadar faiz getirir?", "cevap": "Yıllık %40 faizle brüt 3.506,85 ₺, stopaj sonrası net 2.893,15 ₺. Oranınızı ve vadeyi girerek kendi tutarınızı hesaplayabilirsiniz."},
        {"soru": "Mevduat faizinden vergi kesilir mi?", "cevap": "Evet, stopaj: 6 aya kadar vadede %17,5, 1 yıla kadar %15, 1 yıldan uzun vadede %10. Banka otomatik keser, beyanname gerekmez."},
        {"soru": "Vadeyi bozarsam ne olur?", "cevap": "Vade sonu beklenmeden çekilen paraya faiz ödenmez; yalnızca anapara alınır. Bazı bankalar kısmi çekim hakkı veren ürünler sunar."},
        {"soru": "Faiz günlük mü hesaplanır?", "cevap": "Evet, yıllık oran vade gününe oranlanır (gün ÷ 365). 32 gün için yıllık oranın 32/365'i uygulanır."},
        {"soru": "Katılım hesabı kâr payında stopaj var mı?", "cevap": "Evet, mevduat faiziyle aynı vadeye göre oranlar uygulanır."},
    ],
    "kaynaklar": [
        {"ad": "Resmî Gazete 20.06.2026 Sayı 33286 — Cumhurbaşkanı Kararı 11444 (GVK geçici 67 stopaj oranları)", "url": "https://www.resmigazete.gov.tr/"},
        {"ad": "TCMB — Bankalarca açılan mevduatlara uygulanan ağırlıklı ortalama faiz oranları", "url": "https://www.tcmb.gov.tr/"},
    ],
    "ilgili": ["bilesik-faiz-hesaplama", "kredi-hesaplama", "enflasyon-hesaplama"],
}
