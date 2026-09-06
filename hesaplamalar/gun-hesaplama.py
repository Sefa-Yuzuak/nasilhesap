# -*- coding: utf-8 -*-
HESAP = {
    "slug": "gun-hesaplama",
    "baslik": "İki Tarih Arası Gün Hesaplama",
    "h1": "İki Tarih Arası Gün Hesaplama — Kaç Gün, Hafta, Ay ve İş Günü Var?",
    "kategori": "gunluk",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "İki tarih arasındaki gün sayısını, hafta ve gün, ay-yıl farkını ve iş günü (hafta içi) sayısını anında hesaplayın. Bitiş günü dahil/hariç seçeneği; tatil, vade, teslim tarihi ve geri sayım hesapları için.",
    "kisa_cevap": "İki tarih arasındaki gün sayısı, tarihlerin farkıdır; başlangıç günü sayılmaz, bitiş günü 'dahil' seçilirse 1 eklenir. 1 Ocak 2026 ile 6 Eylül 2026 arasında 248 gün (35 hafta 3 gün) vardır; iş günü sayısı hafta sonları düşülerek bulunur (resmî tatiller ayrıca çıkarılır).",
    "girdiler": [
        {"id": "bas", "etiket": "Başlangıç tarihi", "tip": "tarih", "varsayilan": "2026-01-01"},
        {"id": "bit", "etiket": "Bitiş tarihi", "tip": "tarih", "varsayilan": "2026-09-06"},
        {"id": "dahil", "etiket": "Sayım", "tip": "onay", "varsayilan": False, "onay_metin": "Bitiş günü dahil edilsin (+1 gün)"},
    ],
    "js": r"""
function hesapla(g){
  if (!g.bas || !g.bit) return {hata: 'İki tarihi de seçin.'};
  var a = new Date(g.bas + 'T00:00:00'), b = new Date(g.bit + 'T00:00:00');
  var ters = b < a; if (ters) { var tmp = a; a = b; b = tmp; }
  var gun = Math.round((b - a) / 86400000) + (g.dahil ? 1 : 0);
  // ay-yıl farkı
  var y = b.getFullYear() - a.getFullYear(), m = b.getMonth() - a.getMonth(), d = b.getDate() - a.getDate();
  if (d < 0) { m--; d += new Date(b.getFullYear(), b.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  // iş günü (Pzt-Cum)
  var is = 0, c = new Date(a), son = new Date(b);
  if (!g.dahil) c.setDate(c.getDate() + 1); // başlangıç günü sayılmaz, bitiş günü sayılır
  for (var t = new Date(c); t <= son; t.setDate(t.getDate() + 1)) { var w = t.getDay(); if (w !== 0 && w !== 6) is++; }
  return {
    sonuclar: [
      {etiket: 'Toplam gün', deger: gun, ondalik: 0, vurgu: true},
      {etiket: 'Hafta ve gün', deger: Math.floor(gun / 7) + ' hafta ' + (gun % 7) + ' gün'},
      {etiket: 'Yıl / ay / gün', deger: y + ' yıl ' + m + ' ay ' + d + ' gün'},
      {etiket: 'İş günü (Pzt–Cum)', deger: is, ondalik: 0},
      {etiket: 'Hafta sonu günü', deger: gun - is, ondalik: 0},
      {etiket: 'Saat', deger: gun * 24, ondalik: 0}
    ],
    notlar: [(ters ? 'Bitiş tarihi başlangıçtan önceydi; tarihler yer değiştirildi. ' : '') + 'İş günü sayısı yalnızca hafta sonlarını düşer; resmî ve dini tatiller dahil değildir.']
  };
}
""",
    "nasil": [
        "İki tarih arasındaki gün sayısı, tarihlerin birbirinden çıkarılmasıyla bulunur; takvim sayımında başlangıç günü sıfırıncı gün olarak alınır. Örneğin 1 Ocak'tan 3 Ocak'a 2 gün vardır. Bitiş gününü de saymak istediğiniz durumlarda (konaklama gecesi yerine gün sayısı, ceza süresi, izin günü gibi) 'bitiş günü dahil' seçeneğiyle 1 eklenir.",
        "Ay ve yıl farkı takvime göre hesaplanır: aylar 28-31 gün sürdüğünden '30 gün = 1 ay' varsayımı yanıltıcıdır. Araç, yıl-ay-gün farkını gerçek takvimle (artık yıllar dahil) bulur.",
        "İş günü hesabında Cumartesi ve Pazar düşülür. Türkiye'de resmî tatiller (1 Ocak, 23 Nisan, 1 Mayıs, 19 Mayıs, 15 Temmuz, 30 Ağustos, 29 Ekim) ve dini bayramlar (Ramazan 3,5 gün, Kurban 4,5 gün) her yıl farklı güne denk geldiğinden ayrıca çıkarılmalıdır.",
    ],
    "formul": [
        "Gün = bitiş tarihi − başlangıç tarihi (+1, bitiş dahil ise)",
        "Hafta = gün ÷ 7 (tam) · kalan gün = gün mod 7",
        "İş günü = aralıktaki Pazartesi–Cuma günleri sayısı",
    ],
    "ornekler": [
        {"baslik": "1 Ocak 2026 – 6 Eylül 2026", "adimlar": ["Gün farkı: 248 gün", "35 hafta 3 gün · 8 ay 5 gün", "İş günü: 176 (hafta sonu 72)"]},
        {"baslik": "Otel: 10–13 Temmuz", "adimlar": ["Gece sayısı = 3 (bitiş hariç)", "Konaklanan gün sayısı = 4 (bitiş dahil)"]},
    ],
    "tablo": None,
    "sss": [
        {"soru": "İki tarih arası gün nasıl hesaplanır?", "cevap": "Sonraki tarihten önceki tarihi çıkarın. 15 Mart'tan 20 Mart'a 5 gün vardır; 20 Mart'ı da sayıyorsanız 6 gün."},
        {"soru": "İş günü hesabına tatiller dahil mi?", "cevap": "Aracımız yalnızca Cumartesi ve Pazar'ı düşer. Resmî ve dini tatilleri kendiniz çıkarmalısınız; her yıl tarihleri değişir."},
        {"soru": "1 ay kaç gündür?", "cevap": "Takvimde 28, 29, 30 veya 31 gün. Ortalama 30,44 gündür; sözleşmelerde aksi belirtilmedikçe ay, takvim ayı olarak sayılır."},
        {"soru": "Bugüne kaç gün kaldı nasıl bulunur?", "cevap": "Başlangıç olarak bugünü, bitiş olarak hedef tarihi seçin; sonuç geri sayım gün sayısıdır."},
        {"soru": "Hafta sonu dahil mi?", "cevap": "Toplam gün sayısı hafta sonlarını içerir; 'iş günü' satırı hafta sonlarını hariç tutar."},
    ],
    "kaynaklar": [
        {"ad": "2429 sayılı Ulusal Bayram ve Genel Tatiller Hakkında Kanun (iş günü hesabı)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=2429&MevzuatTur=1&MevzuatTertip=5"},
        {"ad": "4857 sayılı İş Kanunu m.46-47 (hafta tatili ve genel tatil)", "url": "https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=4857&MevzuatTur=1&MevzuatTertip=5"},
    ],
    "ilgili": ["yas-hesaplama", "kidem-tazminati-hesaplama"],
}
