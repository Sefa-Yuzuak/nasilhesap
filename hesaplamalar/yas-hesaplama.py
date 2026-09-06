# -*- coding: utf-8 -*-
HESAP = {
    "slug": "yas-hesaplama",
    "baslik": "Yaş Hesaplama",
    "h1": "Yaş Hesaplama — Doğum Tarihine Göre Yıl, Ay, Gün Olarak Kaç Yaşındayım?",
    "kategori": "gunluk",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Yaş hesaplama aracı: doğum tarihinize göre tam yaşınızı yıl, ay ve gün olarak, toplam yaşadığınız gün sayısını ve bir sonraki doğum gününüze kalan süreyi anında hesaplayın. İstediğiniz tarihteki yaşınızı da bulabilirsiniz.",
    "kisa_cevap": "Yaş, doğum tarihinden bugüne geçen tam yıl sayısıdır: yıl farkından, doğum günü henüz gelmediyse 1 çıkarılır. 15 Mayıs 1990 doğumlu biri 6 Eylül 2026'da 36 yaşındadır (36 yıl 3 ay 22 gün). Toplam yaşanan gün, iki tarih arasındaki gün farkıdır.",
    "girdiler": [
        {"id": "dogum", "etiket": "Doğum tarihi", "tip": "tarih", "varsayilan": "1990-05-15"},
        {"id": "tarih", "etiket": "Hangi tarihteki yaş? (boş = bugün)", "tip": "tarih", "varsayilan": ""},
    ],
    "js": r"""
function hesapla(g){
  if (!g.dogum) return {hata: 'Doğum tarihini seçin.'};
  var d = new Date(g.dogum + 'T00:00:00'), t = g.tarih ? new Date(g.tarih + 'T00:00:00') : new Date();
  t.setHours(0,0,0,0);
  if (t < d) return {hata: 'Seçilen tarih doğum tarihinden önce olamaz.'};
  var y = t.getFullYear() - d.getFullYear(), m = t.getMonth() - d.getMonth(), gn = t.getDate() - d.getDate();
  if (gn < 0) { m--; gn += new Date(t.getFullYear(), t.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  var toplamGun = Math.round((t - d) / 86400000);
  var sonraki = new Date(t.getFullYear(), d.getMonth(), d.getDate());
  if (sonraki <= t) sonraki = new Date(t.getFullYear() + 1, d.getMonth(), d.getDate());
  var kalan = Math.round((sonraki - t) / 86400000);
  var gunler = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
  return {
    sonuclar: [
      {etiket: 'Yaş', deger: y + ' yıl ' + m + ' ay ' + gn + ' gün', vurgu: true},
      {etiket: 'Tam yaş', deger: y + ' yaşında'},
      {etiket: 'Toplam yaşanan gün', deger: toplamGun, ondalik: 0},
      {etiket: 'Toplam ay (yaklaşık)', deger: y * 12 + m, ondalik: 0},
      {etiket: 'Toplam hafta', deger: Math.floor(toplamGun / 7), ondalik: 0},
      {etiket: 'Sonraki doğum gününe kalan', deger: kalan === 0 ? 'Bugün! 🎂' : kalan + ' gün (' + sonraki.toLocaleDateString('tr-TR') + ')'},
      {etiket: 'Doğduğun gün', deger: gunler[d.getDay()]}
    ]
  };
}
""",
    "nasil": [
        "Yaş hesaplamanın en doğru yolu, tam yılları saymaktır: içinde bulunulan yıldan doğum yılını çıkarır, doğum günü o yıl henüz gelmediyse sonuçtan bir çıkarırsınız. Ay ve gün farkını bulmak için önce günler, sonra aylar karşılaştırılır; gün farkı negatifse bir önceki ayın gün sayısı kadar eklenip aydan bir düşülür.",
        "Toplam yaşanan gün sayısı ise iki tarih arasındaki gün farkıdır ve artık yılları (29 Şubat) otomatik olarak içerir. 'Yaş × 365' yaklaşımı artık yılları saymadığı için her 4 yılda yaklaşık 1 gün eksik verir.",
        "Resmî işlemlerde (askerlik, emeklilik, ehliyet, evlilik yaşı) 'yaşını doldurma' ölçütü kullanılır: 18 yaşını doldurmak, 18. doğum gününün gelmiş olması demektir. Bazı ülkelerde kullanılan 'Kore yaşı' gibi doğumda 1 sayan yöntemler Türkiye'de geçerli değildir.",
    ],
    "formul": [
        "Tam yaş = bugünün yılı − doğum yılı − (doğum günü bu yıl henüz gelmediyse 1, geldiyse 0)",
        "Toplam gün = (bugün − doğum tarihi) ÷ 86.400 saniye",
        "Sonraki doğum gününe kalan = bu yılki (gelmediyse) veya gelecek yılki doğum günü − bugün",
    ],
    "ornekler": [
        {"baslik": "15 Mayıs 1990 doğumlu, 6 Eylül 2026", "adimlar": ["2026 − 1990 = 36; doğum günü (15 Mayıs) geçmiş → 36 yaş", "Ay: Eylül − Mayıs = 3 ay; gün: 6 − 15 < 0 → bir ay geri, 6 + 31 − 15 = 22 gün", "Sonuç: 36 yıl 3 ay 22 gün"]},
        {"baslik": "29 Şubat 2000 doğumlu (artık yıl)", "adimlar": ["Artık olmayan yıllarda doğum günü 1 Mart kabul edilir", "6 Eylül 2026'da 26 yaşındadır"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "Yaşımı nasıl hesaplarım?", "cevap": "Bugünün yılından doğum yılınızı çıkarın; doğum gününüz bu yıl henüz gelmediyse bir eksiltin. Örneğin 10 Kasım 1995 doğumlu biri 6 Eylül 2026'da 30 yaşındadır (31 değil)."},
        {"soru": "Kaç gündür yaşıyorum?", "cevap": "Doğum tarihinizle bugün arasındaki gün farkı; 36 yaşındaki biri yaklaşık 13.150 gün yaşamıştır. Aracımız artık yılları dahil ederek tam sayıyı verir."},
        {"soru": "Artık yılda (29 Şubat) doğanlar yaşını ne zaman doldurur?", "cevap": "Türk hukukunda doğum günü ait olduğu yılda yoksa yaş, 1 Mart'ta dolmuş kabul edilir."},
        {"soru": "Resmî işlemlerde yaş nasıl sayılır?", "cevap": "Nüfus kayıtlarındaki doğum tarihine göre 'yaşın doldurulması' esastır: 18 yaşını doldurmak için 18. doğum günü gelmiş olmalıdır."},
        {"soru": "Ay olarak yaşım kaç?", "cevap": "Yıl × 12 + ay farkı. 2 yıl 5 aylık bir bebek 29 aylıktır; aracımız bunu da gösterir."},
    ],
    "kaynaklar": [],
    "ilgili": ["gun-hesaplama", "vki-hesaplama"],
}
