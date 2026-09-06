# -*- coding: utf-8 -*-
HESAP = {
    "slug": "elbirligi-sistemi-hesaplama",
    "baslik": "Elbirliği (Tasarruf Finansman) Hesaplama",
    "h1": "Elbirliği Sistemi Hesaplama — Faizsiz Ev ve Araç Finansmanı Taksit ve Teslim",
    "kategori": "ev-emlak",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Elbirliği / tasarruf finansman sistemi hesaplama: finansman tutarı, peşinat, organizasyon ücreti, vade ve teslim ayına göre aylık taksit, teslime kadar biriken tutar, toplam ödeme ve teslim sonrası kalan borç. Faizsiz ev-araç edinme modeli nasıl çalışır?",
    "kisa_cevap": "Elbirliği (tasarruf finansman) sisteminde faiz yoktur; finansman tutarı eşit taksitlere bölünür ve tek maliyet sözleşme başında alınan organizasyon ücretidir. Aylık taksit = (finansman − peşinat) ÷ vade; toplam ödeme = finansman + organizasyon ücreti. 2.000.000 ₺ finansman, 120 ay, %7 organizasyon ücretiyle taksit 16.667 ₺, toplam 2.140.000 ₺'dir; teslim ayına kadar biriken tasarruf sıra/çekilişle belirlenen teslim anında finansmana dönüşür.",
    "girdiler": [
        {"id": "tutar", "etiket": "Finansman tutarı", "tip": "sayi", "varsayilan": "2000000", "birim": "₺", "ipucu": "ev/araç bedeli"},
        {"id": "pesinat", "etiket": "Peşinat", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "org", "etiket": "Organizasyon ücreti", "tip": "sayi", "varsayilan": "7", "birim": "%", "ipucu": "sözleşmenizdeki oran"},
        {"id": "vade", "etiket": "Vade", "tip": "tamsayi", "varsayilan": "120", "birim": "ay"},
        {"id": "teslim", "etiket": "Tahmini teslim ayı", "tip": "tamsayi", "varsayilan": "40", "birim": "ay", "ipucu": "sıra/çekiliş ayı"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.tutar > 0) || !(g.vade > 0)) return {hata: 'Finansman tutarı ve vadeyi girin.'};
  var pes = g.pesinat || 0, kalan = g.tutar - pes;
  if (kalan <= 0) return {hata: 'Peşinat finansman tutarından küçük olmalı.'};
  var taksit = kalan / g.vade, org = g.tutar * (g.org || 0) / 100;
  var teslim = Math.min(Math.max(1, g.teslim || 1), g.vade);
  var biriken = pes + taksit * teslim, teslimSonrasi = kalan - taksit * teslim;
  var toplam = g.tutar + org;
  return {
    sonuclar: [
      {etiket: 'Aylık taksit', deger: taksit, birim: '₺', vurgu: true},
      {etiket: 'Organizasyon ücreti (%' + (g.org||0) + ')', deger: org, birim: '₺'},
      {etiket: 'Toplam ödeme (finansman + ücret)', deger: toplam, birim: '₺'},
      {etiket: 'Teslim ayına (' + teslim + '. ay) kadar biriken', deger: biriken, birim: '₺'},
      {etiket: 'Teslimde şirketin sağladığı finansman', deger: g.tutar - biriken, birim: '₺'},
      {etiket: 'Teslim sonrası kalan borç', deger: Math.max(0, teslimSonrasi), birim: '₺'},
      {etiket: 'Teslim sonrası kalan taksit sayısı', deger: (g.vade - teslim) + ' ay'}
    ],
    notlar: ['Sistemde faiz yoktur; taksitler sabittir. Organizasyon ücreti genellikle sözleşme başında (veya ilk taksitlere yayılarak) ödenir ve çoğu sözleşmede iade edilmez.',
             'Teslim ayı; sıra, çekiliş veya peşinat oranına göre belirlenir ve şirketten şirkete değişir. Erken teslim için daha yüksek peşinat veya "ara ödeme" seçenekleri olabilir.',
             'Tasarruf finansman şirketleri 6361 sayılı Kanun kapsamında BDDK lisansı ve denetimine tabidir; sözleşme öncesi şirketin lisanslı olduğunu BDDK listesinden doğrulayın.']
  };
}
""",
    "nasil": [
        "Elbirliği sistemi (yasal adıyla tasarruf finansman), bir grup katılımcının düzenli tasarruflarını bir havuzda toplayıp sırayla ev veya araç edinmesini sağlayan faizsiz modeldir. Katılımcı, sözleşmede belirlenen finansman tutarını eşit aylık taksitlere böler; teslim anına kadar ödediği taksitler tasarruf, teslimden sonrası ise şirketin sağladığı finansmanın geri ödemesidir.",
        "Sistemin tek maliyeti, sözleşme başında alınan organizasyon (hizmet) ücretidir; bu oran şirkete, vadeye ve teslim seçeneğine göre değişir ve genellikle finansman tutarının yüzde birkaçı ile %10'u arasındadır. Faiz olmadığı için toplam ödeme, finansman tutarı ile organizasyon ücretinin toplamına eşittir — bu, aynı tutardaki banka kredisinin toplam faiz yüküyle karşılaştırıldığında belirgin fark yaratır.",
        "Teslim zamanı sistemin en kritik değişkenidir: sıralı (peşinat oranına göre), çekilişli veya belirli ay seçenekleri bulunur. Teslim ayına kadar biriken tutar peşinat + o aya kadar ödenen taksitlerdir; teslimde şirket kalan kısmı finanse eder ve katılımcı taksitleri vade sonuna kadar ödemeye devam eder. Bu şirketler 2021'den itibaren 6361 sayılı Kanun'la BDDK düzenleme ve denetimine alınmıştır.",
    ],
    "formul": [
        "Aylık taksit = (finansman tutarı − peşinat) ÷ vade (ay)",
        "Organizasyon ücreti = finansman tutarı × ücret oranı ÷ 100",
        "Toplam ödeme = finansman tutarı + organizasyon ücreti (faiz yok)",
        "Teslime kadar biriken = peşinat + taksit × teslim ayı · Şirket finansmanı = finansman − biriken",
    ],
    "ornekler": [
        {"baslik": "2.000.000 ₺ ev finansmanı, 120 ay, %7 ücret, 40. ayda teslim",
         "adimlar": ["Taksit: 2.000.000 ÷ 120 = 16.667 ₺", "Organizasyon ücreti: 140.000 ₺ → toplam ödeme 2.140.000 ₺", "40. aya kadar biriken: 666.667 ₺; şirket 1.333.333 ₺ finanse eder", "Teslim sonrası 80 ay daha 16.667 ₺ ödenir"]},
        {"baslik": "Aynı ev banka konut kredisiyle (%2,5 aylık, 120 ay)",
         "adimlar": ["Taksit ≈ 52.073 ₺, toplam ≈ 6.248.700 ₺", "Fark: elbirliğinde toplam 2.140.000 ₺ — ancak evi 40 ay bekleyerek alırsınız; kredide hemen"]},
    ],
    "tablo": {
        "baslik": "Elbirliği sistemi ile banka kredisi karşılaştırması",
        "basliklar": ["Kriter", "Elbirliği / tasarruf finansman", "Banka konut kredisi"],
        "satirlar": [["Faiz", "Yok", "Var (aylık %)"], ["Ana maliyet", "Organizasyon ücreti (tek seferlik)", "Toplam faiz + masraflar"],
                     ["Teslim", "Sıra/çekiliş ile ileri tarihte", "Hemen"], ["Denetim", "BDDK (6361 s.K.)", "BDDK (5411 s.K.)"],
                     ["Kredi notu", "Genelde aranmaz", "Gerekli"], ["Erken çıkış", "Sözleşmeye göre; ücret iadesi sınırlı", "Erken kapatma mümkün"]],
        "not": "Karşılaştırma genel niteliktedir; sözleşme koşulları şirkete göre farklılık gösterir.",
    },
    "sss": [
        {"soru": "Elbirliği sisteminde gerçekten faiz yok mu?", "cevap": "Evet, faiz yoktur; taksitler sabittir. Tek maliyet organizasyon ücretidir. Ancak evi teslim ayına kadar beklersiniz; bu bekleme süresinin fırsat maliyetini de hesaba katın."},
        {"soru": "Organizasyon ücreti ne kadar ve iade edilir mi?", "cevap": "Şirkete ve plana göre değişir; genellikle finansman tutarının yüzde birkaçı ile %10'u arasındadır. Çoğu sözleşmede iade edilmez veya sınırlı iade edilir; sözleşme öncesi cayma ve iade koşullarını mutlaka okuyun."},
        {"soru": "Teslim ayı nasıl belirlenir?", "cevap": "Üç yaygın model vardır: peşinat oranına göre sıralı teslim, aylık çekilişle teslim ve belirli bir ayda kesin teslim (daha yüksek ücret/peşinatla). Aracımızda tahmini teslim ayınızı girerek biriken tutarı görebilirsiniz."},
        {"soru": "Bu şirketler güvenli mi, kim denetliyor?", "cevap": "Tasarruf finansman şirketleri 2021'den beri 6361 sayılı Kanun kapsamında BDDK lisansına ve denetimine tabidir. Sözleşme yapmadan önce şirketin BDDK'nın yayımladığı lisanslı şirketler listesinde olduğunu doğrulayın."},
        {"soru": "Kredi notum düşük, elbirliği uygun mu?", "cevap": "Sistemde banka kredisi kullanılmadığı için kredi notu genellikle aranmaz; bu, krediye erişemeyenler için temel avantajdır. Ancak düzenli taksit ödeme gücünüz olmalı; gecikmeler sözleşmede yaptırıma bağlıdır."},
        {"soru": "Elbirliği mi banka kredisi mi daha avantajlı?", "cevap": "Toplam maliyette elbirliği belirgin biçimde düşüktür (faiz yok); zamanlamada banka kredisi avantajlıdır (hemen teslim). Evi hemen almanız gerekmiyorsa ve düzenli tasarruf edebiliyorsanız elbirliği, hemen taşınmanız gerekiyorsa kredi daha uygundur."},
    ],
    "kaynaklar": [
        {"ad": "BDDK — Tasarruf finansman şirketleri (lisanslı şirket listesi ve düzenlemeler)", "url": "https://www.bddk.org.tr/"},
        {"ad": "6361 sayılı Finansal Kiralama, Faktoring, Finansman ve Tasarruf Finansman Şirketleri Kanunu", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6361&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["konut-kredisi-hesaplama", "kredi-hesaplama", "tapu-harci-hesaplama"],
}
