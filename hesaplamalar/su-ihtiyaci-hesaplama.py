# -*- coding: utf-8 -*-
HESAP = {
    "slug": "su-ihtiyaci-hesaplama",
    "baslik": "Günlük Su İhtiyacı Hesaplama",
    "h1": "Günlük Su İhtiyacı Hesaplama — Kiloya Göre Kaç Litre Su İçmeliyim?",
    "kategori": "saglik",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Günlük su ihtiyacı hesaplama: kilo, aktivite düzeyi, sıcak hava ve gebelik-emzirme durumuna göre içmeniz gereken su miktarı litre ve bardak olarak. Kilo başına 30-35 ml kuralı.",
    "kisa_cevap": "Günlük su ihtiyacı yaklaşık kilo başına 30–35 ml'dir: 70 kg için 2,1–2,5 litre (10–12 bardak). Egzersizde her 30 dakika için ~350 ml, sıcak havada ~500 ml, gebelikte ~300 ml, emzirmede ~700 ml eklenir. Bu miktar içecek olarak alınan sıvıdır; besinlerden gelen su ayrıca sayılır.",
    "girdiler": [
        {"id": "kilo", "etiket": "Kilo", "tip": "sayi", "varsayilan": "70", "birim": "kg"},
        {"id": "egz", "etiket": "Günlük egzersiz süresi", "tip": "tamsayi", "varsayilan": "0", "birim": "dk"},
        {"id": "durum", "etiket": "Özel durum", "tip": "secim", "varsayilan": "yok", "secenekler": [["yok", "Yok"], ["gebe", "Gebelik"], ["emzir", "Emzirme"]]},
        {"id": "sicak", "etiket": "Hava", "tip": "onay", "varsayilan": False, "onay_metin": "Sıcak/nemli hava veya yüksek rakım"},
    ],
    "js": r"""
function hesapla(g){
  if (!(g.kilo > 10)) return {hata: 'Kilonuzu girin.'};
  var alt = g.kilo * 30, ust = g.kilo * 35, ek = 0, n = [];
  if (g.egz > 0) { ek += Math.round(g.egz / 30) * 350; n.push('Egzersiz için +' + Math.round(g.egz / 30) * 350 + ' ml eklendi (her 30 dk ~350 ml).'); }
  if (g.sicak) { ek += 500; n.push('Sıcak hava için +500 ml eklendi.'); }
  if (g.durum === 'gebe') { ek += 300; n.push('Gebelik için +300 ml eklendi.'); }
  if (g.durum === 'emzir') { ek += 700; n.push('Emzirme için +700 ml eklendi.'); }
  var hedef = (ust + ek) / 1000;
  n.push('Böbrek, kalp yetmezliği veya sıvı kısıtlaması gerektiren hastalıklarda hekiminizin önerisi geçerlidir.');
  return {
    sonuclar: [
      {etiket: 'Günlük su hedefi', deger: Math.round(hedef * 10) / 10, birim: 'litre', vurgu: true},
      {etiket: 'Su bardağı (200 ml)', deger: Math.round(hedef * 5), ondalik: 0},
      {etiket: 'Temel ihtiyaç aralığı (30–35 ml/kg)', deger: (alt/1000).toFixed(1) + ' – ' + (ust/1000).toFixed(1) + ' litre'},
      {etiket: 'Ek ihtiyaç', deger: ek / 1000, birim: 'litre'},
      {etiket: 'Saatte (16 uyanık saat)', deger: Math.round(hedef * 1000 / 16), birim: 'ml', ondalik: 0}
    ],
    notlar: n
  };
}
""",
    "nasil": [
        "Vücut ağırlığının yaklaşık %60'ı sudur ve her gün idrar, ter, solunum yoluyla 2-3 litre sıvı kaybedilir. Pratik kural, kilo başına 30-35 ml sıvı almaktır; bu, Avrupa Gıda Güvenliği Otoritesi'nin (EFSA) yetişkin kadın için 2,0 L, erkek için 2,5 L toplam sıvı önerisiyle uyumludur. Bu miktarın yaklaşık %20'si besinlerden gelir; kalanı içecek olarak alınmalıdır.",
        "İhtiyaç fiziksel aktivite, sıcaklık ve fizyolojik durumla artar: her 30 dakikalık orta-yoğun egzersiz için 300-500 ml, sıcak ve nemli havada ya da yüksek rakımda günde 500 ml kadar ek sıvı gerekir. Gebelikte günlük ihtiyaç ~300 ml, emzirmede ~700 ml daha fazladır. Ateşli hastalık, ishal ve kusma kayıpları da ayrıca karşılanmalıdır.",
        "Susuzluk hissi genellikle hafif dehidrasyon başladıktan sonra ortaya çıkar; özellikle yaşlılarda bu his azalır. İdrar renginin açık sarı olması yeterli sıvı alımının pratik göstergesidir. Aşırı su içmek (kısa sürede litrelerce) sodyum düşüklüğüne yol açabilir; hedef, gün içine yayarak içmektir.",
    ],
    "formul": [
        "Temel ihtiyaç (ml) = kilo (kg) × 30–35",
        "Ek: egzersiz +350 ml / 30 dk · sıcak hava +500 ml · gebelik +300 ml · emzirme +700 ml",
        "Bardak sayısı = toplam ml ÷ 200",
    ],
    "ornekler": [
        {"baslik": "70 kg, egzersiz yok, normal hava", "adimlar": ["70 × 35 = 2.450 ml ≈ 2,5 litre (12 bardak)"]},
        {"baslik": "85 kg, günde 60 dk spor, sıcak hava", "adimlar": ["85 × 35 = 2.975 ml", "+ 2 × 350 = 700 ml (egzersiz) + 500 ml (sıcak)", "Toplam ≈ 4,2 litre"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Günde kaç litre su içmeliyim?", "cevap": "Kilonuzu 30-35 ml ile çarpın: 60 kg için 1,8-2,1 L, 80 kg için 2,4-2,8 L. Spor ve sıcakta artırın."},
        {"soru": "Günde 8 bardak su kuralı doğru mu?", "cevap": "8 × 250 ml = 2 litre, ortalama bir yetişkin için makul bir yaklaşımdır ama kiloya ve aktiviteye göre değişir; kişiselleştirilmiş hesap daha doğrudur."},
        {"soru": "Çay ve kahve su yerine geçer mi?", "cevap": "Kısmen. Kafeinli içecekler de sıvı sağlar; ılımlı tüketimde (3-4 fincan) net sıvı kaybına yol açmazlar. Yine de günlük hedefin çoğunu su oluşturmalıdır."},
        {"soru": "Fazla su içmek zararlı mı?", "cevap": "Kısa sürede çok fazla (saatte >1 L) su içmek hiponatremiye yol açabilir. Günlük hedefi gün içine yayarak içmek güvenlidir."},
    ],
    "kaynaklar": [
        {"ad": "EFSA — Scientific Opinion on Dietary Reference Values for water (2010)", "url": "https://www.efsa.europa.eu/"},
        {"ad": "T.C. Sağlık Bakanlığı — Türkiye Beslenme Rehberi (sıvı tüketimi)", "url": "https://hsgm.saglik.gov.tr/"},
    ],
    "ilgili": ["kalori-hesaplama", "vki-hesaplama"],
}
