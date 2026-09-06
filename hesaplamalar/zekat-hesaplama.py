# -*- coding: utf-8 -*-
HESAP = {
    "slug": "zekat-hesaplama",
    "baslik": "Zekât Hesaplama",
    "h1": "Zekât Hesaplama — Nisap Miktarı, Altın, Para ve Ticari Mal Zekâtı",
    "kategori": "gunluk",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Zekât hesaplama aracı: nakit, altın, gümüş, alacak ve ticari mallardan borçlar düşülerek zekât matrahı, nisap (80,18 gr altın) karşılaştırması ve %2,5 zekât tutarı. Diyanet ölçülerine göre.",
    "kisa_cevap": "Zekât, temel ihtiyaç ve borçlar dışında kalan ve üzerinden bir kamerî yıl geçen malın 1/40'ıdır (%2,5). Nisap, Diyanet'e göre 80,18 gram altın (veya 561,2 gram gümüş) değeridir; zekât mallarınızın toplamı bu değere ulaşıyorsa toplamın %2,5'i zekât olarak verilir. Örneğin nisabı aşan 500.000 ₺ birikim için zekât 12.500 ₺'dir.",
    "girdiler": [
        {"id": "altin_fiyat", "etiket": "Bugünkü gram altın fiyatı", "tip": "sayi", "varsayilan": "", "birim": "₺", "ipucu": "nisap için — güncel fiyatı girin", "genis": True},
        {"id": "nakit", "etiket": "Nakit, banka, döviz (₺ karşılığı)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "altin_gr", "etiket": "Altın (gram, 24 ayar karşılığı)", "tip": "sayi", "varsayilan": "0", "birim": "gr"},
        {"id": "gumus", "etiket": "Gümüş (₺ değeri)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "alacak", "etiket": "Tahsili beklenen alacaklar", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "ticari", "etiket": "Ticari mal ve stok (maliyet/piyasa)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "yatirim", "etiket": "Hisse, fon, kripto vb. (₺ değeri)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
        {"id": "borc", "etiket": "Vadesi gelmiş borçlar (düşülür)", "tip": "sayi", "varsayilan": "0", "birim": "₺"},
    ],
    "js": r"""
function hesapla(g){
  var af = g.altin_fiyat;
  if (!(af > 0)) return {hata: 'Nisap için bugünkü gram altın fiyatını girin (bankalar veya Darphane fiyatı).'};
  var top = function(x){ return x > 0 ? x : 0; };
  var altinTL = top(g.altin_gr) * af;
  var mal = top(g.nakit) + altinTL + top(g.gumus) + top(g.alacak) + top(g.ticari) + top(g.yatirim);
  var matrah = Math.max(0, mal - top(g.borc));
  var nisap = 80.18 * af;
  var zekat = matrah >= nisap ? matrah / 40 : 0;
  return {
    sonuclar: [
      {etiket: matrah >= nisap ? 'Verilecek zekât (%2,5)' : 'Zekât', deger: matrah >= nisap ? zekat : 'Nisaba ulaşılmadı — zekât düşmez', birim: matrah >= nisap ? '₺' : '', vurgu: true},
      {etiket: 'Zekât matrahı (mallar − borçlar)', deger: matrah, birim: '₺'},
      {etiket: 'Nisap (80,18 gr altın)', deger: nisap, birim: '₺'},
      {etiket: 'Altın değeri', deger: altinTL, birim: '₺'},
      {etiket: 'Toplam zekât malı', deger: mal, birim: '₺'},
      {etiket: 'Nisaba oran', deger: matrah / nisap * 100, birim: '%'}
    ],
    notlar: ['Zekât, malın üzerinden bir kamerî yıl (354 gün) geçmesi şartıyla verilir; yıl içindeki artışlar için farklı görüşler vardır.', 'Oturulan ev, binek araç, ev eşyası ve iş için kullanılan makineler zekâta tabi değildir. Kadının takı olarak kullandığı altın konusunda mezhepler farklı görüştedir (Hanefi: tabi; Şafii: tabi değil).', 'Kesin hüküm için Diyanet İşleri Başkanlığı Alo 190 veya il müftülüğüne danışın.']
  };
}
""",
    "nasil": [
        "Zekât, İslam'ın beş şartından biridir ve nisap miktarı mala sahip olan, bu malın üzerinden bir kamerî yıl geçen kişilere farzdır. Zekâta tabi mallar nakit para, döviz, altın-gümüş, alacaklar, ticari mallar, hisse senedi ve benzeri yatırım araçlarıdır; oturulan ev, binek araç, ev eşyası ve mesleki alet zekâta tabi değildir.",
        "Nisap, Diyanet İşleri Başkanlığı'nın ölçüsüne göre 80,18 gram altın (veya 561,2 gram gümüş) değeridir; para ve ticari mallarda altın nisabı esas alınır. Hesaplama günündeki gram altın fiyatı ile çarpılarak TL karşılığı bulunur. Zekât malları toplamından vadesi gelmiş borçlar düşülür; kalan tutar nisaba eşit veya fazlaysa zekât farzdır.",
        "Zekât oranı 1/40, yani %2,5'tir. Altın ve gümüşte hesap ağırlık üzerinden de yapılabilir: 100 gram altının zekâtı 2,5 gram altındır. Zekât, Kur'an'da sayılan sekiz sınıfa (fakirler, miskinler, borçlular vb.) verilir; usul, bakmakla yükümlü olunan yakınlara (anne-baba, çocuk, eş) verilmez.",
    ],
    "formul": [
        "Zekât matrahı = (nakit + altın + gümüş + alacaklar + ticari mal + yatırımlar) − vadesi gelmiş borçlar",
        "Nisap (₺) = 80,18 gr × gram altın fiyatı",
        "Zekât = matrah × 2,5 ÷ 100 (matrah ≥ nisap ise)",
        "Altının zekâtı (gram) = altın gramı × 2,5 ÷ 100",
    ],
    "ornekler": [
        {"baslik": "Gram altın 5.000 ₺, birikim 400.000 ₺ + 50 gr altın, borç 30.000 ₺", "adimlar": ["Nisap: 80,18 × 5.000 = 400.900 ₺", "Mallar: 400.000 + 250.000 = 650.000 ₺; matrah 620.000 ₺ ≥ nisap", "Zekât: 620.000 × 0,025 = 15.500 ₺"]},
        {"baslik": "Yalnızca 200 gram altın", "adimlar": ["200 gr > 80,18 gr nisap", "Zekât: 200 × 2,5% = 5 gram altın (veya TL karşılığı)"]},
    ],
    "tablo": {
        "baslik": "Zekâta tabi olan ve olmayan mallar",
        "basliklar": ["Zekâta tabi", "Zekâta tabi değil"],
        "satirlar": [["Nakit, banka hesabı, döviz", "Oturulan ev, arsa (satış niyeti yoksa)"], ["Altın, gümüş (takı için tartışmalı)", "Binek araç, ev eşyası"], ["Ticari mal ve stok", "Mesleki alet ve makineler"], ["Alacaklar (tahsili umulan)", "Kişisel kullanım eşyası"], ["Hisse, fon, kripto (yatırım amaçlı)", "Bir yılı dolmamış mal (görüşe göre)"]],
        "not": "Diyanet İşleri Başkanlığı Din İşleri Yüksek Kurulu görüşleri; mezheplere göre ayrıntılar farklılaşabilir.",
    },
    "sss": [
        {"soru": "2026 zekât nisabı ne kadar?", "cevap": "80,18 gram altının hesap günündeki TL karşılığıdır; altın fiyatına göre değişir. Aracımıza güncel gram altın fiyatını girerek bulabilirsiniz."},
        {"soru": "Maaştan zekât verilir mi?", "cevap": "Maaşın kendisinden değil, yıl sonunda birikip nisabı aşan ve üzerinden bir yıl geçen tasarruftan verilir."},
        {"soru": "Borçlar zekâttan düşülür mü?", "cevap": "Vadesi gelmiş borçlar düşülür. Uzun vadeli konut kredisinde çoğunluk görüşü yalnızca o yılın taksitlerinin düşülebileceği yönündedir."},
        {"soru": "Ev veya araba için zekât var mı?", "cevap": "Oturulan ev ve kullanılan araç zekâta tabi değildir. Kiraya verilen evin kendisi değil, birikmiş kira geliri zekâta tabidir; satış amaçlı gayrimenkul ise ticari mal sayılır."},
        {"soru": "Fitre ile zekât farkı nedir?", "cevap": "Fitre (fıtır sadakası) Ramazan'da kişi başı sabit tutarda verilir (Diyanet her yıl açıklar); zekât ise mal varlığının %2,5'idir."},
    ],
    "kaynaklar": [
        {"ad": "Diyanet İşleri Başkanlığı — Zekât nisabı ve fıkhi görüşler (Din İşleri Yüksek Kurulu)", "url": "https://kurul.diyanet.gov.tr/"},
        {"ad": "Diyanet — Zekât Rehberi", "url": "https://www.diyanet.gov.tr/"},
    ],
    "ilgili": ["yuzde-hesaplama", "bilesik-faiz-hesaplama"],
}
