# -*- coding: utf-8 -*-
HESAP = {
    "slug": "bilesik-faiz-hesaplama",
    "baslik": "Bileşik Faiz Hesaplama",
    "h1": "Bileşik Faiz Hesaplama — Birikim, Yatırım Getirisi ve Gelecek Değer",
    "kategori": "kredi-finans",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Bileşik faiz hesaplama: anapara, yıllık faiz oranı, süre, bileşik dönemi (yıllık/aylık/günlük) ve düzenli aylık yatırımla gelecek değer, toplam faiz kazancı ve yıl yıl birikim tablosu.",
    "kisa_cevap": "Bileşik faizde kazanılan faiz anaparaya eklenir ve sonraki dönemde faiz de faiz kazanır: gelecek değer = anapara × (1 + r/n)^(n×t). 100.000 ₺, yıllık %40, 3 yıl, aylık bileşikte para 100.000 × (1 + 0,40/12)^36 ≈ 325.579 ₺ olur; basit faizle 220.000 ₺'de kalırdı.",
    "girdiler": [
        {"id": "ana", "etiket": "Başlangıç anaparası", "tip": "sayi", "varsayilan": "100000", "birim": "₺"},
        {"id": "faiz", "etiket": "Yıllık faiz / getiri oranı", "tip": "sayi", "varsayilan": "40", "birim": "%"},
        {"id": "yil", "etiket": "Süre", "tip": "sayi", "varsayilan": "3", "birim": "yıl"},
        {"id": "n", "etiket": "Bileşik dönemi", "tip": "secim", "varsayilan": "12", "secenekler": [["1", "Yıllık"], ["4", "3 aylık"], ["12", "Aylık"], ["365", "Günlük"]]},
        {"id": "ek", "etiket": "Düzenli aylık ek yatırım (isteğe bağlı)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.ana >= 0) || !(g.faiz >= 0) || !(g.yil > 0)) return {hata: 'Anapara, faiz ve süreyi girin.'};
  var n = parseInt(g.n, 10) || 12, r = g.faiz / 100, t = g.yil, ek = g.ek > 0 ? g.ek : 0;
  var rows = [], deger = g.ana, yatirilan = g.ana;
  var aylikOran = Math.pow(1 + r / n, n / 12) - 1; // aylık efektif
  var toplamAy = Math.round(t * 12);
  var gD = [g.ana], gY = [g.ana], gEt = ['0'];
  for (var ay = 1; ay <= toplamAy; ay++) {
    deger = deger * (1 + aylikOran) + ek; yatirilan += ek;
    if (ay % 12 === 0 || ay === toplamAy) { rows.push([Math.ceil(ay / 12) + '. yıl', yatirilan, deger - yatirilan, deger]); gD.push(deger); gY.push(yatirilan); gEt.push(Math.ceil(ay / 12) + '. yıl'); }
  }
  var basit = g.ana * (1 + r * t) + ek * toplamAy;
  var efektif = (Math.pow(1 + r / n, n) - 1) * 100;
  return {
    sonuclar: [
      {etiket: 'Gelecek değer (' + t + ' yıl sonra)', deger: deger, birim: '₺', vurgu: true},
      {etiket: 'Toplam yatırılan', deger: yatirilan, birim: '₺'},
      {etiket: 'Toplam faiz / getiri', deger: deger - yatirilan, birim: '₺'},
      {etiket: 'Yıllık efektif oran', deger: efektif, birim: '%'},
      {etiket: 'Basit faizle olurdu', deger: basit, birim: '₺'},
      {etiket: 'Bileşik etkisi (fark)', deger: deger - basit, birim: '₺'}
    ],
    grafik: {tur: 'cizgi', baslik: 'Bileşik büyüme: toplam değer ve yatırılan anapara', etiketler: gEt,
             seriler: [{ad: 'Toplam değer', veri: gD}, {ad: 'Yatırılan', veri: gY, renk: '#9ca3af'}]},
    tablo: {basliklar: ['Dönem', 'Yatırılan', 'Birikmiş getiri', 'Toplam'], satirlar: rows},
    notlar: ['Stopaj/vergi, enflasyon ve masraflar dahil değildir; mevduatta net getiri için stopaj oranını düşün.', 'Ek yatırımlar her ay sonunda eklenmiş kabul edilir.']
  };
}
""",
    "nasil": [
        "Basit faizde faiz yalnızca anapara üzerinden hesaplanır; bileşik faizde ise her dönem kazanılan faiz anaparaya eklenir ve sonraki dönemde o da faiz getirir. Bu 'faizin faizi' etkisi zamanla üstel büyüme yaratır; uzun vadede en güçlü servet birikim mekanizmasıdır.",
        "Bileşik dönemi (n) yılda kaç kez faizin anaparaya ekleneceğini gösterir: yıllık 1, aylık 12, günlük 365. Aynı nominal oranda dönem sıklaştıkça yıllık efektif getiri artar: %40 nominal, aylık bileşikte yıllık efektif %48,2'ye çıkar. Bankaların 'yıllık bileşik getiri' ifadesi bu efektif orandır.",
        "Düzenli ek yatırım eklendiğinde (örneğin her ay sabit birikim) her katkı kendi kalan süresi boyunca bileşik büyür; bu yüzden erken başlamak, geç başlayıp daha çok yatırmaktan çoğu zaman daha etkilidir. 72 kuralı pratik bir kısayoldur: para 72 ÷ faiz yılda ikiye katlanır (%12'de yaklaşık 6 yıl).",
    ],
    "formul": [
        "Gelecek değer = A × (1 + r ÷ n)^(n × t)",
        "Yıllık efektif oran = (1 + r ÷ n)^n − 1",
        "Aylık ek yatırımla: her ay değer = önceki değer × (1 + aylık oran) + ek",
        "Basit faiz karşılaştırması = A × (1 + r × t)",
    ],
    "ornekler": [
        {"baslik": "100.000 ₺, %40 yıllık, 3 yıl, aylık bileşik", "adimlar": ["Aylık oran: 0,40 ÷ 12 = %3,333", "(1,03333)^36 ≈ 3,2558 → 325.579 ₺", "Basit faiz: 100.000 × (1 + 0,40 × 3) = 220.000 ₺; bileşik farkı ≈ 105.579 ₺"]},
        {"baslik": "Her ay 5.000 ₺, %30 yıllık, 10 yıl", "adimlar": ["Yatırılan: 600.000 ₺", "Birikim ≈ 2,03 milyon ₺ — getiri yatırılanın 2 katından fazla"]},
    ],
    "tablo": {
        "baslik": "72 kuralı — para kaç yılda ikiye katlanır?",
        "basliklar": ["Yıllık getiri", "İkiye katlanma süresi"],
        "satirlar": [["%6", "≈ 12 yıl"], ["%12", "≈ 6 yıl"], ["%24", "≈ 3 yıl"], ["%36", "≈ 2 yıl"], ["%48", "≈ 1,5 yıl"]],
        "not": "72 ÷ oran yaklaşımı; kesin değer ln2 ÷ ln(1+r) ile bulunur.",
    },
    "sss": [
        {"soru": "Bileşik faiz ile basit faiz farkı nedir?", "cevap": "Basit faiz yalnızca anaparaya işler; bileşik faizde kazanılan faiz de anaparaya eklenir ve faiz getirir. 3 yılda %40 ile fark 100.000 ₺'de yaklaşık 106.000 ₺'dir."},
        {"soru": "Aylık bileşik mi yıllık bileşik mi daha çok kazandırır?", "cevap": "Aynı nominal oranda daha sık bileşik (aylık, günlük) daha yüksek efektif getiri sağlar; ancak fark sınırlıdır (%40 nominal: yıllık %40, aylık %48,2, günlük %49,1)."},
        {"soru": "Mevduat faizi bileşik mi?", "cevap": "Vadeli mevduatta faiz vade sonunda ödenir; yenilenen her vadede anaparaya eklenirse fiilen bileşik olur. Getiriden stopaj düşülür."},
        {"soru": "Enflasyon bileşik faizi etkiler mi?", "cevap": "Nominal getiri değişmez ama reel (satın alma gücü) getiri = (1 + faiz) ÷ (1 + enflasyon) − 1'dir; enflasyon faizden yüksekse reel getiri negatiftir."},
        {"soru": "72 kuralı nedir?", "cevap": "Paranın ikiye katlanma süresini hızlıca bulma yöntemi: 72 ÷ yıllık getiri. %18 getiride yaklaşık 4 yıl."},
    ],
    "kaynaklar": [],
    "ilgili": ["kredi-hesaplama", "yuzde-hesaplama", "kira-artis-orani-hesaplama"],
}
