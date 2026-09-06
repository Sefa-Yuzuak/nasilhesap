# -*- coding: utf-8 -*-
HESAP = {
    "slug": "kdv-tevkifat-hesaplama",
    "baslik": "KDV Tevkifat Hesaplama",
    "h1": "KDV Tevkifat Hesaplama — 2/10, 5/10, 7/10, 9/10 Tevkifatlı Fatura",
    "kategori": "vergi-maas",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "KDV tevkifat hesaplama: KDV hariç tutar, KDV oranı ve tevkifat oranına (2/10, 3/10, 4/10, 5/10, 7/10, 9/10, 10/10) göre tevkif edilen KDV, satıcıya ödenecek KDV ve fatura toplamı.",
    "kisa_cevap": "KDV tevkifatında faturadaki KDV'nin belirli bir kısmını alıcı, satıcıya ödemek yerine sorumlu sıfatıyla doğrudan vergi dairesine beyan eder. 100.000 ₺ + %20 KDV = 20.000 ₺'lik faturada 5/10 tevkifatla alıcı 10.000 ₺ KDV'yi kendisi beyan eder, satıcıya 100.000 + 10.000 = 110.000 ₺ öder.",
    "girdiler": [
        {"id": "tutar", "etiket": "KDV hariç tutar (matrah)", "tip": "sayi", "varsayilan": "100000", "birim": "₺"},
        {"id": "kdv", "etiket": "KDV oranı", "tip": "secim", "varsayilan": "20", "secenekler": [["20", "%20"], ["10", "%10"], ["1", "%1"]]},
        {"id": "tev", "etiket": "Tevkifat oranı", "tip": "secim", "varsayilan": "5", "genis": True,
         "secenekler": [["2", "2/10 — bazı hizmet ve teslimler"], ["3", "3/10 — yük taşımacılığı vb."], ["4", "4/10 — yapım işleri, makine-ekipman bakım"], ["5", "5/10 — danışmanlık, denetim, servis, temizlik (belirli alıcılar)"], ["7", "7/10 — bakır, alüminyum, çinko, hurda vb."], ["9", "9/10 — işgücü temini, fason tekstil, özel güvenlik, yemek servisi"], ["10", "10/10 — tam tevkifat"]]},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.tutar > 0)) return {hata: 'KDV hariç tutarı girin.'};
  var kdvO = parseFloat(g.kdv) / 100, pay = parseInt(g.tev, 10);
  var kdv = g.tutar * kdvO, tevkif = kdv * pay / 10, satici = kdv - tevkif;
  return {
    sonuclar: [
      {etiket: 'Satıcıya ödenecek toplam', deger: g.tutar + satici, birim: '₺', vurgu: true},
      {etiket: 'Hesaplanan KDV (%' + (kdvO*100) + ')', deger: kdv, birim: '₺'},
      {etiket: 'Tevkif edilen KDV (' + pay + '/10) — alıcı beyan eder', deger: tevkif, birim: '₺'},
      {etiket: 'Satıcıya ödenen KDV (' + (10 - pay) + '/10)', deger: satici, birim: '₺'},
      {etiket: 'Fatura genel toplamı (tevkifat öncesi)', deger: g.tutar + kdv, birim: '₺'}
    ],
    notlar: ['Alıcı, tevkif ettiği KDV\'yi 2 No.lu KDV beyannamesiyle beyan edip öder; aynı tutarı 1 No.lu beyannamede indirim konusu yapabilir.',
             'Tevkifat, KDV dahil fatura tutarı belirli sınırı (2026 için güncel sınır GİB tebliğinde) aşmıyorsa uygulanmaz; sınır her yıl güncellenir.',
             'Hangi işlemin hangi oranda tevkifata tabi olduğu KDV Genel Uygulama Tebliği I/C-2.1.3 bölümünde listelenir; alıcının türü (belirlenmiş alıcı / KDV mükellefi) oranı etkiler.']
  };
}
""",
    "nasil": [
        "KDV tevkifatı, vergi güvenliği amacıyla bazı işlemlerde KDV'nin bir kısmının satıcı yerine alıcı tarafından beyan edilip ödenmesidir. Satıcı faturada KDV'nin tamamını hesaplar ancak tevkifata isabet eden kısmı tahsil etmez; alıcı bu kısmı '2 No.lu KDV beyannamesi' ile sorumlu sıfatıyla vergi dairesine yatırır.",
        "Tevkifat oranları işlem türüne ve alıcının niteliğine göre KDV Genel Uygulama Tebliği'nde belirlenir: yapım işleri 4/10, danışmanlık-denetim 5/10 (belirlenmiş alıcılara), temizlik-bahçe-çevre 9/10 → (güncel tebliğe göre değişebilir), işgücü temini 9/10, hurda metal 7/10, yük taşımacılığı 2/10 gibi. Kamu kurumları, bankalar, halka açık şirketler gibi 'belirlenmiş alıcılar' daha geniş bir liste için tevkifat yapmakla yükümlüdür.",
        "Satıcı açısından tevkifat, tahsil edemediği KDV'yi indirimle gideremiyorsa iade hakkı doğurur; bu nedenle tevkifatlı fatura kesen firmalar KDV iadesi alabilir. Alıcı ise ödediği tevkifat KDV'sini aynı dönemde indirim konusu yaptığı için net vergi yükü değişmez.",
    ],
    "formul": [
        "KDV = matrah × KDV oranı",
        "Tevkif edilen KDV = KDV × tevkifat payı ÷ 10",
        "Satıcıya ödenen = matrah + KDV × (10 − pay) ÷ 10",
        "Alıcı 2 No.lu beyannamede beyan eder: KDV × pay ÷ 10",
    ],
    "ornekler": [
        {"baslik": "100.000 ₺ danışmanlık, %20 KDV, 5/10", "adimlar": ["KDV 20.000 ₺; tevkif edilen 10.000 ₺", "Satıcıya ödenen: 100.000 + 10.000 = 110.000 ₺", "Alıcı 10.000 ₺'yi 2 No.lu KDV beyannamesiyle öder"]},
        {"baslik": "500.000 ₺ yapım işi, 4/10", "adimlar": ["KDV 100.000 ₺; tevkifat 40.000 ₺", "Yükleniciye 560.000 ₺ ödenir"]},
    ],
    "tablo": {
        "baslik": "Başlıca KDV tevkifat oranları (KDV GUT I/C-2.1.3)",
        "basliklar": ["İşlem", "Oran"],
        "satirlar": [["Yapım işleri ile bu işlere ilişkin mühendislik-mimarlık", "4/10"], ["Etüt, plan-proje, danışmanlık, denetim", "5/10"], ["Makine, teçhizat, demirbaş bakım-onarım", "7/10"], ["Yemek servisi, organizasyon hizmetleri", "5/10"], ["İşgücü temini, özel güvenlik, fason tekstil", "9/10"], ["Temizlik, çevre ve bahçe bakımı", "9/10"], ["Yük taşımacılığı", "2/10"], ["Hurda metal, bakır-çinko-alüminyum ürünleri", "7/10"], ["Ağaç ve orman ürünleri", "5/10"]],
        "not": "Oranlar tebliğ değişiklikleriyle güncellenebilir; işlem öncesi GİB'in güncel listesine bakın.",
    },
    "sss": [
        {"soru": "KDV tevkifatı nedir?", "cevap": "Faturadaki KDV'nin belirli bir payını alıcının satıcıya ödemek yerine doğrudan vergi dairesine beyan etmesidir. Satıcı yalnızca kalan payı tahsil eder."},
        {"soru": "Tevkifatlı faturada satıcıya ne kadar ödenir?", "cevap": "Matrah + tevkifat dışı KDV. 100.000 ₺ + %20 KDV ve 5/10 tevkifatta 110.000 ₺."},
        {"soru": "Tevkifat sınırı nedir?", "cevap": "KDV dahil fatura tutarı belirli bir sınırın altındaysa tevkifat uygulanmaz; sınır her yıl yeniden değerlemeyle artar ve GİB tebliğinde ilan edilir."},
        {"soru": "Tevkif edilen KDV alıcı için maliyet mi?", "cevap": "Hayır. Alıcı 2 No.lu beyannamede ödediği tutarı 1 No.lu beyannamede indirir; net etki sıfırdır."},
        {"soru": "Satıcı tevkifat nedeniyle KDV iadesi alabilir mi?", "cevap": "Evet. Tevkifata tabi işlemlerde indirilemeyen KDV için mahsuben veya nakden iade talep edilebilir."},
    ],
    "kaynaklar": [
        {"ad": "GİB — KDV Genel Uygulama Tebliği (I/C-2.1.3 kısmi tevkifat)", "url": "https://www.gib.gov.tr/"},
        {"ad": "3065 sayılı KDV Kanunu m.9 (vergi sorumlusu)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=3065&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["kdv-hesaplama", "stopaj-hesaplama"],
}
