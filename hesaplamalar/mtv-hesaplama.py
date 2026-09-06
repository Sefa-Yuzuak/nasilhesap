# -*- coding: utf-8 -*-
HESAP = {
    "slug": "mtv-hesaplama",
    "baslik": "MTV Hesaplama",
    "h1": "MTV Hesaplama 2026 — Motorlu Taşıtlar Vergisi Tutarı, Taksitler ve Tablo",
    "kategori": "vergi-maas",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "2026 MTV hesaplama: motor hacmi, model yılı, taşıt değeri ve araç türüne (otomobil, motosiklet, minibüs, panelvan, otobüs, kamyonet) göre yıllık motorlu taşıtlar vergisi ve Ocak-Temmuz taksitleri. Resmî Gazete Tebliğ 58 tablosu.",
    "kisa_cevap": "MTV, aracın motor hacmi, yaşı ve (2018'den sonra tescilli otomobillerde) taşıt değeri kademesine göre yıllık sabit tutardır; 2026 tutarları %18,95 artırıldı. 2022 model, 1.4 litrelik (1301-1600 cm³), değeri 541.500 ₺ üzeri bir otomobil 2026'da 5 yaşındadır (4-6 grubu) ve yıllık MTV'si 9.012 ₺'dir; Ocak ve Temmuz'da 4.506 ₺'lik iki taksitte ödenir.",
    "senaryolar": [
        {"ad": "2024 model 1.4 (1400 cm³)", "degerler": {"tur": "I", "model": "2024", "cc": "1400", "deger": "1200000"}},
        {"ad": "2022 model 1.6 (1600 cm³)", "degerler": {"tur": "I", "model": "2022", "cc": "1600", "deger": "900000"}},
        {"ad": "2018 model 1.6 dizel", "degerler": {"tur": "I", "model": "2018", "cc": "1598", "deger": "500000"}},
        {"ad": "2013 model 1.3 (eski tarife)", "degerler": {"tur": "IA", "model": "2013", "cc": "1300"}},
        {"ad": "2023 model 250 cm³ motosiklet", "degerler": {"tur": "moto", "model": "2023", "cc": "250"}},
    ],
    "girdiler": [
        {"id": "tur", "etiket": "Araç türü", "tip": "secim", "varsayilan": "I", "genis": True,
         "secenekler": [["I", "Otomobil / arazi taşıtı — 1.1.2018 ve sonrası tescilli"], ["IA", "Otomobil / arazi taşıtı — 31.12.2017 ve öncesi tescilli"], ["moto", "Motosiklet"], ["minibus", "Minibüs"], ["panelvan", "Panelvan / motorlu karavan"], ["otobus", "Otobüs"], ["kamyonet", "Kamyonet / kamyon / çekici"]]},
        {"id": "model", "etiket": "Model yılı", "tip": "tamsayi", "varsayilan": "2022", "birim": "yıl"},
        {"id": "cc", "etiket": "Motor silindir hacmi (otomobil, motosiklet, panelvan)", "tip": "sayi", "varsayilan": "1400", "birim": "cm³"},
        {"id": "deger", "etiket": "Taşıt değeri (ÖTV+KDV hariç ilk iktisap bedeli)", "tip": "sayi", "varsayilan": "600000", "birim": "₺", "gizli": "tur=I"},
        {"id": "kisi", "etiket": "Oturma yeri (otobüs)", "tip": "tamsayi", "varsayilan": "30", "birim": "kişi", "gizli": "tur=otobus"},
        {"id": "kg", "etiket": "Azami toplam ağırlık (kamyonet/kamyon)", "tip": "sayi", "varsayilan": "3000", "birim": "kg", "gizli": "tur=kamyonet"},
    ],
    "js": r"""
function bul(liste, x){ for (var i = 0; i < liste.length; i++) { var ust = liste[i][0]; if (ust === null || x <= ust) return liste[i]; } return liste[liste.length - 1]; }
function hesapla(g, O){
  var M = O.mtv, yil = O.yil;
  if (!(g.model >= 1950 && g.model <= yil + 1)) return {hata: 'Model yılını girin.'};
  var yas = Math.max(1, yil - g.model + 1);
  var g5 = yas <= 3 ? 0 : yas <= 6 ? 1 : yas <= 11 ? 2 : yas <= 15 ? 3 : 4;
  var g3 = yas <= 6 ? 0 : yas <= 15 ? 1 : 2;
  var ad5 = ['1-3 yaş', '4-6 yaş', '7-11 yaş', '12-15 yaş', '16 ve üzeri yaş'], ad3 = ['1-6 yaş', '7-15 yaş', '16 ve üzeri yaş'];
  var tutar, aciklama = '', n = [];
  if (g.tur === 'I') {
    if (!(g.cc > 0)) return {hata: 'Motor hacmini girin.'};
    var grp = null; for (var i = 0; i < M.I.length; i++) { if (M.I[i].cc === null || g.cc <= M.I[i].cc) { grp = M.I[i]; break; } }
    var k = bul(grp.kademe, g.deger > 0 ? g.deger : 0);
    tutar = k[1][g5];
    aciklama = (grp.cc === null ? '4001 cm³ ve üzeri' : '≤ ' + NH.fmt(grp.cc, 0) + ' cm³') + ' · değer ' + (k[0] === null ? NH.fmt(grp.kademe[grp.kademe.length-2][0], 0) + ' ₺ üzeri' : '≤ ' + NH.fmt(k[0], 0) + ' ₺') + ' · ' + ad5[g5];
    n.push('Taşıt değeri kademesi ilk tescil yılında belirlenir ve sonraki yıllarda aynı satır esas alınır; bu araç 2026 eşiklerine göre eşleştirme yapar. Kesin satır için GİB Dijital Vergi Dairesi "MTV Hesaplama" ekranını kullanın.');
  } else if (g.tur === 'IA') {
    if (!(g.cc > 0)) return {hata: 'Motor hacmini girin.'};
    var r = bul(M.IA, g.cc); tutar = r[1][g5]; aciklama = (r[0] === null ? '4001 cm³ ve üzeri' : '≤ ' + NH.fmt(r[0], 0) + ' cm³') + ' · ' + ad5[g5];
  } else if (g.tur === 'moto') {
    if (!(g.cc > 0)) return {hata: 'Motor hacmini girin.'};
    var rm = bul(M.motosiklet, g.cc); tutar = rm[1][g5]; aciklama = (rm[0] === null ? '1201 cm³ ve üzeri' : '≤ ' + NH.fmt(rm[0], 0) + ' cm³') + ' · ' + ad5[g5];
    if (g.cc < 100) n.push('100 cm³ altı motosikletler MTV\'den muaftır (elektrikli motosikletler için ayrı hükümler vardır).');
  } else if (g.tur === 'minibus') { tutar = M.II.minibus[g3]; aciklama = 'Minibüs · ' + ad3[g3]; }
  else if (g.tur === 'panelvan') { if (!(g.cc > 0)) return {hata: 'Motor hacmini girin.'}; var rp = bul(M.II.panelvan, g.cc); tutar = rp[1][g3]; aciklama = 'Panelvan ' + (rp[0] === null ? '1901 cm³+' : '≤ 1900 cm³') + ' · ' + ad3[g3]; }
  else if (g.tur === 'otobus') { var ro = bul(M.II.otobus, g.kisi > 0 ? g.kisi : 1); tutar = ro[1][g3]; aciklama = 'Otobüs ' + (ro[0] === null ? '46+ kişi' : '≤ ' + ro[0] + ' kişi') + ' · ' + ad3[g3]; }
  else { var rk = bul(M.II.kamyonet, g.kg > 0 ? g.kg : 1); tutar = rk[1][g3]; aciklama = 'Kamyonet/kamyon ' + (rk[0] === null ? '20.001 kg+' : '≤ ' + NH.fmt(rk[0], 0) + ' kg') + ' · ' + ad3[g3]; }
  n.push('Araç yaşı = ' + yil + ' − model yılı + 1 = ' + yas + '. MTV Ocak ve Temmuz aylarında iki eşit taksitte ödenir; 2026 tutarları 2025\'e göre %' + M.artis_orani + ' artırılmıştır.');
  return {
    sonuclar: [
      {etiket: yil + ' yıllık MTV', deger: tutar, birim: '₺', ondalik: 0, vurgu: true},
      {etiket: '1. taksit (Ocak)', deger: tutar / 2, birim: '₺'},
      {etiket: '2. taksit (Temmuz)', deger: tutar / 2, birim: '₺'},
      {etiket: 'Araç yaşı', deger: yas + ' (' + (g.tur === 'minibus' || g.tur === 'panelvan' || g.tur === 'otobus' || g.tur === 'kamyonet' ? ad3[g3] : ad5[g5]) + ')'},
      {etiket: 'Tarife satırı', deger: aciklama},
      {etiket: 'Aylık karşılığı', deger: tutar / 12, birim: '₺'}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "Motorlu Taşıtlar Vergisi her yıl Ocak ayında Resmî Gazete'de yayımlanan tebliğle belirlenen sabit tutarlardır; 2026 tutarları 31 Aralık 2025 tarihli Tebliğ (Seri No: 58) ile %18,95 artırıldı. Otomobillerde vergi üç ölçüte bağlıdır: motor silindir hacmi, araç yaşı ve 1 Ocak 2018'den sonra tescil edilen araçlarda taşıt değeri kademesi. Araç yaşı, içinde bulunulan yıldan model yılı çıkarılıp 1 eklenerek bulunur: 2022 model bir araç 2026'da 5 yaşındadır.",
        "2018 ve sonrası tescilli otomobiller (I) sayılı tarifeye tabidir: her motor hacmi grubunda taşıt değerine göre 2-3 kademe vardır (örneğin 1301-1600 cm³ için 309.100 ₺'ye kadar, 309.100-541.500 ₺ arası ve 541.500 ₺ üzeri). Kademe, aracın ilk tescil yılındaki değerine göre bir kez belirlenir ve sonraki yıllarda o satır esas alınır. 2017 ve öncesi tescilli otomobiller değer kademesi olmayan (I/A) tarifesine, motosikletler motor hacmine, minibüs-otobüs-kamyonet gibi ticari araçlar (II) sayılı tarifeye tabidir.",
        "MTV, Ocak ve Temmuz aylarında iki eşit taksitte ödenir; ödeme GİB İnteraktif Vergi Dairesi, bankalar veya e-Devlet üzerinden yapılır. Ödenmeyen MTV aylık gecikme zammıyla birikir ve araç satışında, muayenede borcun kapatılması istenir. Engelli araçları, elektrikli araçlarda özel indirimler ve bazı kamu araçları muafiyet kapsamındadır.",
    ],
    "formul": [
        "Araç yaşı = içinde bulunulan yıl − model yılı + 1",
        "Otomobil (2018+): tutar = tablo[(motor hacmi grubu, taşıt değeri kademesi)][yaş grubu]",
        "Otomobil (2017 ve öncesi): tutar = tablo(I/A)[motor hacmi grubu][yaş grubu]",
        "Taksit = yıllık MTV ÷ 2 (Ocak, Temmuz)",
    ],
    "ornekler": [
        {"baslik": "2022 model, 1.4 litre (1400 cm³), taşıt değeri 600.000 ₺", "adimlar": ["Yaş: 2026 − 2022 + 1 = 5 → 4-6 grubu", "1301-1600 cm³, 541.500 ₺ üzeri → satır 6", "2026 MTV: 9.012 ₺ → Ocak 4.506 + Temmuz 4.506 ₺"]},
        {"baslik": "2015 model, 1.6 litre (I/A tarifesi)", "adimlar": ["Yaş: 12 → 12-15 grubu", "1301-1600 cm³ → 3.077 ₺"]},
        {"baslik": "2024 model 250 cm³ motosiklet", "adimlar": ["Yaş 3 → 1-3 grubu; 100-250 cm³ → 1.069 ₺"]},
    ],
    "tablo": {
        "baslik": "2026 MTV — otomobil (I) sayılı tarife, en yüksek değer kademesi (özet)",
        "basliklar": ["Motor hacmi", "1-3 yaş", "4-6 yaş", "7-11 yaş", "12-15 yaş", "16+ yaş"],
        "satirlar": [["≤ 1300 cm³ (541.500 ₺ üzeri)", "6.902", "4.807", "2.693", "2.032", "706"], ["1301-1600 (541.500 ₺ üzeri)", "12.028", "9.012", "5.220", "3.685", "1.408"], ["1601-1800 (775.100 ₺ üzeri)", "21.251", "16.600", "9.775", "5.964", "2.307"], ["1801-2000 (775.100 ₺ üzeri)", "33.474", "25.784", "15.147", "9.012", "3.547"], ["2001-2500 (968.100 ₺ üzeri)", "50.217", "36.448", "22.768", "13.606", "5.378"], ["2501-3000 (1.937.500 ₺ üzeri)", "70.018", "60.905", "38.053", "20.466", "7.503"], ["3001-3500 (1.937.500 ₺ üzeri)", "106.641", "95.940", "57.791", "28.839", "10.578"], ["3501-4000 (3.101.800 ₺ üzeri)", "167.671", "144.770", "85.271", "38.053", "15.147"], ["4001+ (3.683.200 ₺ üzeri)", "274.415", "205.781", "121.873", "54.769", "21.251"]],
        "not": "Tutarlar TL. Düşük değer kademeleri ve (I/A), motosiklet, (II) tarifeleri hesaplayıcıda tam olarak yer alır. Kaynak: RG 31.12.2025, 33124 (5. Mük.), Tebliğ 58.",
    },
    "sss": [
        {"soru": "2026 MTV ne kadar arttı?", "cevap": "Cumhurbaşkanı Kararı (10783) ile 2025 yeniden değerleme oranı %25,49 yerine MTV için %18,95 artış uygulandı."},
        {"soru": "Araç yaşı nasıl hesaplanır?", "cevap": "İçinde bulunulan yıldan model yılı çıkarılıp 1 eklenir; 2026 model araç 2026'da 1 yaşındadır, 2020 model 7 yaşında."},
        {"soru": "Taşıt değeri nedir, nereden bulurum?", "cevap": "Aracın ÖTV ve KDV hariç ilk iktisap bedelidir; kademe ilk tescil yılında belirlenir. Ruhsat/e-Devlet araç bilgilerinde ve GİB MTV sorgusunda görünür."},
        {"soru": "MTV ne zaman ödenir?", "cevap": "Ocak (1-31) ve Temmuz (1-31) aylarında iki eşit taksitte. İsteyen tamamını Ocak'ta ödeyebilir."},
        {"soru": "Elektrikli araçların MTV'si nasıl?", "cevap": "Sadece elektrik motorlu otomobiller motor gücüne (kW) göre ayrı satırlarla ve indirimli tutarlarla vergilendirilir; bu hesaplayıcıda yer almaz, GİB sorgusundan öğrenebilirsiniz."},
        {"soru": "Engelli araçları MTV öder mi?", "cevap": "%90 ve üzeri engelli adına kayıtlı veya engelliler için özel tertibatlı araçlar MTV'den muaftır (MTVK m.4/c)."},
    ],
    "kaynaklar": [
        {"ad": "Resmî Gazete 31.12.2025, Sayı 33124 (5. Mük.) — MTV Genel Tebliği Seri No 58 (PDF)", "url": "https://www.resmigazete.gov.tr/eskiler/2025/12/20251231M5-23.pdf"},
        {"ad": "GİB — Dijital Vergi Dairesi MTV hesaplama ve sorgulama", "url": "https://dijital.gib.gov.tr/"},
        {"ad": "197 sayılı Motorlu Taşıtlar Vergisi Kanunu", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=197&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["kredi-hesaplama", "damga-vergisi-hesaplama", "kdv-hesaplama"],
}
