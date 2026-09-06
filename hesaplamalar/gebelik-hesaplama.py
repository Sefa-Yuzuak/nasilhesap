# -*- coding: utf-8 -*-
HESAP = {
    "slug": "gebelik-hesaplama",
    "baslik": "Gebelik ve Doğum Tarihi Hesaplama",
    "h1": "Gebelik Hesaplama — Kaç Haftalık Hamileyim, Tahmini Doğum Tarihi",
    "kategori": "saglik",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Gebelik hesaplama: son adet tarihine göre kaç haftalık hamile olduğunuz, tahmini doğum tarihi (Naegele kuralı), trimester, tahmini gebe kalma tarihi ve doğuma kalan gün. Adet döngüsü düzeltmesiyle.",
    "kisa_cevap": "Gebelik haftası son adet tarihinin (SAT) ilk gününden itibaren sayılır; tahmini doğum tarihi SAT + 280 gün (40 hafta)'dır (Naegele kuralı). Döngü 28 günden uzun/kısaysa fark eklenir/çıkarılır. Örneğin SAT 1 Ocak 2026 ise tahmini doğum 8 Ekim 2026'dır ve 6 Eylül 2026'da gebelik 35 hafta 3 gündür.",
    "girdiler": [
        {"id": "sat", "etiket": "Son adet tarihi (ilk gün)", "tip": "tarih", "varsayilan": "2026-01-01"},
        {"id": "dongu", "etiket": "Adet döngüsü uzunluğu", "tip": "tamsayi", "varsayilan": "28", "birim": "gün"},
        {"id": "tarih", "etiket": "Hangi tarih için? (boş = bugün)", "tip": "tarih", "varsayilan": ""},
    ],
    "js": r"""
function hesapla(g){
  if (!g.sat) return {hata: 'Son adet tarihini seçin.'};
  var sat = new Date(g.sat + 'T00:00:00'), bugun = g.tarih ? new Date(g.tarih + 'T00:00:00') : new Date();
  bugun.setHours(0,0,0,0);
  var duz = (g.dongu >= 20 && g.dongu <= 45) ? g.dongu - 28 : 0;
  var dogum = new Date(sat); dogum.setDate(dogum.getDate() + 280 + duz);
  var gebe = new Date(sat); gebe.setDate(gebe.getDate() + 14 + duz);
  var gun = Math.round((bugun - sat) / 86400000) - duz;
  if (gun < 0) return {hata: 'Seçilen tarih son adet tarihinden önce.'};
  if (gun > 310) return {hata: 'Son adet tarihinden 44 haftadan fazla geçmiş; tarihi kontrol edin.'};
  var hafta = Math.floor(gun / 7), kg = gun % 7;
  var tri = hafta < 13 ? '1. trimester (0–12. hafta)' : hafta < 27 ? '2. trimester (13–26. hafta)' : '3. trimester (27–40. hafta)';
  var kalan = Math.round((dogum - bugun) / 86400000);
  var f = function(d){ return d.toLocaleDateString('tr-TR', {day: 'numeric', month: 'long', year: 'numeric'}); };
  return {
    sonuclar: [
      {etiket: 'Gebelik haftası', deger: hafta + ' hafta ' + kg + ' gün', vurgu: true},
      {etiket: 'Tahmini doğum tarihi', deger: f(dogum)},
      {etiket: 'Doğuma kalan', deger: kalan >= 0 ? kalan + ' gün (' + Math.floor(kalan/7) + ' hafta)' : 'Tahmini tarih ' + (-kalan) + ' gün önce geçti'},
      {etiket: 'Trimester', deger: tri},
      {etiket: 'Tahmini gebe kalma (yumurtlama) tarihi', deger: f(gebe)},
      {etiket: 'Gebelik ayı', deger: Math.min(9, Math.floor(hafta / 4.345) + 1) + '. ay'},
      {etiket: 'Doğuma uygun aralık (37–42. hafta)', deger: f(new Date(dogum.getTime() - 21*86400000)) + ' – ' + f(new Date(dogum.getTime() + 14*86400000))}
    ],
    notlar: ['Döngü 28 günden farklıysa fark (' + (duz >= 0 ? '+' : '') + duz + ' gün) uygulanmıştır. Kesin gebelik yaşı ilk trimester ultrason ölçümüyle (CRL) belirlenir; hekiminizin tarihi esastır.']
  };
}
""",
    "nasil": [
        "Gebelik yaşı, tıpta son adet tarihinin (SAT) ilk gününden itibaren sayılır; döllenme genellikle bundan yaklaşık iki hafta sonra gerçekleştiği için 'kaç haftalık' bilgisi döllenme yaşından iki hafta fazladır. Tahmini doğum tarihi, Naegele kuralıyla SAT'a 280 gün (40 hafta) eklenerek bulunur.",
        "Adet döngüsü 28 günden uzun veya kısa olan kadınlarda yumurtlama günü kayar; bu nedenle döngü uzunluğu ile 28 arasındaki fark doğum tarihine eklenir veya çıkarılır. Düzensiz döngüde veya SAT bilinmiyorsa gebelik yaşı erken ultrasonda baş-popo mesafesi (CRL) ölçümüyle belirlenir ve bu ölçüm SAT'a göre daha güvenilirdir.",
        "Doğumların yalnızca yaklaşık %4-5'i tam tahmini tarihte gerçekleşir; 37-42. hafta arası 'term' (zamanında) kabul edilir. Gebelik 3 trimestere ayrılır: 1-12, 13-26 ve 27-40. haftalar. Takip, tarama testleri ve ultrason zamanlaması bu haftalara göre planlanır.",
    ],
    "formul": [
        "Gebelik günü = bugün − SAT − (döngü − 28)",
        "Gebelik haftası = gebelik günü ÷ 7 (tam) · kalan gün = gebelik günü mod 7",
        "Tahmini doğum tarihi = SAT + 280 gün + (döngü − 28)",
        "Tahmini gebe kalma tarihi = SAT + 14 gün + (döngü − 28)",
    ],
    "ornekler": [
        {"baslik": "SAT 1 Ocak 2026, 28 günlük döngü, bugün 6 Eylül 2026", "adimlar": ["Geçen gün: 248 → 35 hafta 3 gün", "Doğum: 1 Ocak + 280 gün = 8 Ekim 2026", "Kalan: 32 gün; 3. trimester"]},
        {"baslik": "Aynı SAT, 32 günlük döngü", "adimlar": ["Düzeltme +4 gün → doğum 12 Ekim 2026", "Gebelik haftası 4 gün daha küçük: 34 hafta 6 gün"]},
    ],
    "tablo": {
        "baslik": "Gebelik takvimi kilometre taşları",
        "basliklar": ["Hafta", "Olay"],
        "satirlar": [["4-5", "Gebelik testi pozitif; ilk ultrason 6-8. hafta"], ["11-14", "İkili tarama testi (NT ölçümü)"], ["16-18", "Üçlü/dörtlü test, cinsiyet görülebilir"], ["18-22", "Ayrıntılı (anomali) ultrasonu"], ["24-28", "Şeker yükleme testi (OGTT)"], ["28", "3. trimester başlar; Rh negatifse anti-D"], ["35-37", "GBS kültürü; doğum planı"], ["37-42", "Term (zamanında) doğum aralığı"]],
        "not": "T.C. Sağlık Bakanlığı Doğum Öncesi Bakım Yönetim Rehberi'ne göre genel takvim; hekim planı esastır.",
    },
    "sss": [
        {"soru": "Kaç haftalık hamileyim nasıl hesaplanır?", "cevap": "Son adet tarihinizin ilk gününden bugüne geçen günü 7'ye bölün. SAT 1 Ocak ise 6 Eylül'de 35 hafta 3 günlük gebesiniz."},
        {"soru": "Doğum tarihi nasıl hesaplanır?", "cevap": "Naegele kuralı: SAT + 7 gün − 3 ay + 1 yıl (= SAT + 280 gün). 1 Ocak 2026 → 8 Ekim 2026. Düzensiz döngüde ultrason tarihi esas alınır."},
        {"soru": "Gebelik 9 ay mı 10 ay mı?", "cevap": "40 hafta = 280 gün ≈ 9 takvim ayı + 1 hafta. 'Ay' 4 hafta sayılırsa 10 ay çıkar; tıbbi takip haftayla yapılır."},
        {"soru": "Ultrason tarihi ile SAT tarihi farklıysa hangisi geçerli?", "cevap": "İlk trimester ultrasonu (CRL) ile SAT arasında 7 günden fazla fark varsa ultrason tarihi esas alınır; sonraki ultrasonlar tarihi değiştirmez."},
        {"soru": "Yumurtlama günü nasıl bulunur?", "cevap": "Bir sonraki adetten yaklaşık 14 gün önce; 28 günlük döngüde SAT + 14. gün. Döngü 32 günse SAT + 18. gün."},
    ],
    "kaynaklar": [
        {"ad": "T.C. Sağlık Bakanlığı — Doğum Öncesi Bakım Yönetim Rehberi", "url": "https://hsgm.saglik.gov.tr/"},
        {"ad": "ACOG Committee Opinion 700 — Methods for Estimating the Due Date", "url": "https://www.acog.org/"},
    ],
    "ilgili": ["gun-hesaplama", "yas-hesaplama", "vki-hesaplama"],
}
