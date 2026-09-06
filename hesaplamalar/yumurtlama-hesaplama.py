# -*- coding: utf-8 -*-
HESAP = {
    "slug": "yumurtlama-hesaplama",
    "baslik": "Yumurtlama Günü Hesaplama",
    "h1": "Yumurtlama Günü Hesaplama — Doğurgan Dönem ve Adet Takvimi",
    "kategori": "saglik",
    "populer": False,
    "guncelleme": "2026-09-06",
    "aciklama": "Yumurtlama hesaplama: son adet tarihi ve döngü uzunluğuna göre yumurtlama günü, en verimli (doğurgan) günler, sonraki adet tarihi ve gelecek 3 döngünün takvimi.",
    "kisa_cevap": "Yumurtlama, bir sonraki adetten yaklaşık 14 gün önce olur: yumurtlama günü = son adet tarihi + (döngü uzunluğu − 14). 28 günlük döngüde 14. gün, 32 günlük döngüde 18. gündür. Doğurgan pencere yumurtlamadan 5 gün önce başlayıp yumurtlama günü sonrasına kadar sürer (6 gün).",
    "girdiler": [
        {"id": "sat", "etiket": "Son adet tarihi (ilk gün)", "tip": "tarih", "varsayilan": "2026-09-01"},
        {"id": "dongu", "etiket": "Döngü uzunluğu", "tip": "tamsayi", "varsayilan": "28", "birim": "gün", "ipucu": "iki adet başlangıcı arası"},
        {"id": "luteal", "etiket": "Luteal faz", "tip": "tamsayi", "varsayilan": "14", "birim": "gün", "ipucu": "bilinmiyorsa 14"},
    ],
    "js": r"""
function hesapla(g){
  if (!g.sat) return {hata: 'Son adet tarihini seçin.'};
  var d = (g.dongu >= 21 && g.dongu <= 45) ? g.dongu : 28, l = (g.luteal >= 10 && g.luteal <= 17) ? g.luteal : 14;
  var sat = new Date(g.sat + 'T00:00:00');
  var f = function(x){ return x.toLocaleDateString('tr-TR', {day: 'numeric', month: 'long', weekday: 'short'}); };
  var gunEkle = function(t, n){ var x = new Date(t); x.setDate(x.getDate() + n); return x; };
  var rows = [];
  for (var i = 0; i < 3; i++) {
    var bas = gunEkle(sat, d * i), yum = gunEkle(bas, d - l), pen1 = gunEkle(yum, -5), pen2 = gunEkle(yum, 1), sonraki = gunEkle(bas, d);
    rows.push([(i + 1) + '. döngü', f(bas), f(yum), f(pen1) + ' – ' + f(pen2), f(sonraki)]);
  }
  var yum0 = gunEkle(sat, d - l);
  return {
    sonuclar: [
      {etiket: 'Yumurtlama günü', deger: f(yum0) + ' (' + (d - l + 1) + '. gün)', vurgu: true},
      {etiket: 'Doğurgan pencere (6 gün)', deger: f(gunEkle(yum0, -5)) + ' – ' + f(gunEkle(yum0, 1))},
      {etiket: 'En verimli 3 gün', deger: f(gunEkle(yum0, -2)) + ' – ' + f(yum0)},
      {etiket: 'Sonraki adet (tahmini)', deger: f(gunEkle(sat, d))},
      {etiket: 'Gebelik testi için uygun tarih', deger: f(gunEkle(sat, d + 1)) + ' ve sonrası'}
    ],
    tablo: {basliklar: ['Döngü', 'Adet başlangıcı', 'Yumurtlama', 'Doğurgan pencere', 'Sonraki adet'], satirlar: rows},
    notlar: ['Takvim yöntemi tahminidir; düzensiz döngüde yanılma payı yüksektir. Ovulasyon testi (LH), bazal vücut ısısı ve servikal mukus takibi daha kesin sonuç verir.', 'Gebelikten korunma amacıyla yalnızca takvim yöntemine güvenilmemelidir.']
  };
}
""",
    "nasil": [
        "Adet döngüsü, adetin ilk gününden bir sonraki adetin ilk gününe kadar sürer ve ortalama 28 gündür (21-35 gün normal kabul edilir). Yumurtlama (ovulasyon) döngünün ortasında değil, bir sonraki adetten yaklaşık 14 gün önce gerçekleşir; çünkü yumurtlama sonrası luteal faz görece sabittir (12-16 gün). Bu yüzden 32 günlük döngüde yumurtlama 18. gündedir.",
        "Sperm kadın üreme sisteminde 5 güne kadar canlı kalabilir, yumurta ise yumurtlamadan sonra yalnızca 12-24 saat döllenebilir. Bu nedenle 'doğurgan pencere' yumurtlamadan 5 gün önce başlar ve yumurtlama gününü izleyen günde biter; gebelik olasılığı yumurtlamadan 1-2 gün önce en yüksektir.",
        "Takvim yöntemi, düzenli döngüsü olan kadınlarda planlama için yararlı bir tahmindir ama kesin değildir; stres, hastalık ve kilo değişimi yumurtlamayı kaydırabilir. Daha kesin takip için idrarda LH testi, bazal vücut ısısı ölçümü ve servikal mukus gözlemi birlikte kullanılır.",
    ],
    "formul": [
        "Yumurtlama günü = son adet tarihi + (döngü uzunluğu − luteal faz [14])",
        "Doğurgan pencere = yumurtlama − 5 gün … yumurtlama + 1 gün",
        "Sonraki adet = son adet tarihi + döngü uzunluğu",
    ],
    "ornekler": [
        {"baslik": "SAT 1 Eylül, 28 günlük döngü", "adimlar": ["Yumurtlama: 1 Eylül + 14 = 15 Eylül", "Doğurgan pencere: 10–16 Eylül", "Sonraki adet: 29 Eylül"]},
        {"baslik": "SAT 1 Eylül, 35 günlük döngü", "adimlar": ["Yumurtlama: 1 Eylül + 21 = 22 Eylül", "Pencere: 17–23 Eylül; sonraki adet 6 Ekim"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Yumurtlama günü nasıl hesaplanır?", "cevap": "Son adet tarihinize (döngü uzunluğu − 14) gün ekleyin. 30 günlük döngüde 16. gün."},
        {"soru": "Adetten kaç gün sonra hamile kalınır?", "cevap": "28 günlük döngüde en verimli günler adetin 10-15. günleridir; döngü uzadıkça bu pencere ileri kayar."},
        {"soru": "Düzensiz adette yumurtlama nasıl bulunur?", "cevap": "Takvim yöntemi güvenilir olmaz. LH ovulasyon testi ve bazal vücut ısısı takibi önerilir; sürekli düzensizlikte kadın doğum uzmanına başvurun."},
        {"soru": "Adet döneminde hamile kalınır mı?", "cevap": "Kısa döngülerde (21-24 gün) adetin son günlerinde ilişki, spermin 5 gün yaşayabilmesi nedeniyle gebelikle sonuçlanabilir; olasılık düşük ama sıfır değildir."},
    ],
    "kaynaklar": [
        {"ad": "T.C. Sağlık Bakanlığı — Üreme Sağlığı ve Aile Planlaması", "url": "https://hsgm.saglik.gov.tr/"},
        {"ad": "ACOG — Fertility Awareness-Based Methods of Family Planning", "url": "https://www.acog.org/"},
    ],
    "ilgili": ["gebelik-hesaplama", "gun-hesaplama"],
}
