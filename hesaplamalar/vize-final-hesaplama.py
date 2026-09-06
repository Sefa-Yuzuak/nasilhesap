# -*- coding: utf-8 -*-
HESAP = {
    "slug": "vize-final-hesaplama",
    "baslik": "Vize Final Ortalama Hesaplama",
    "h1": "Vize Final Hesaplama — Ders Ortalaması ve Geçmek İçin Gereken Final Notu",
    "kategori": "sinav-egitim",
    "populer": True,
    "guncelleme": "2026-09-06",
    "aciklama": "Vize final ortalama hesaplama: vize ve final notunuzla ağırlıklı ders ortalaması, geçmek için finalden almanız gereken not, bütünleme senaryosu ve harf notu karşılığı.",
    "kisa_cevap": "Ders ortalaması = vize × vize ağırlığı + final × final ağırlığı; yaygın uygulama %40 vize + %60 finaldir. Vizeden 60 alan bir öğrenci, 50 ortalamayla geçmek için finalden en az (50 − 60×0,40) ÷ 0,60 = 43,3 almalıdır. Çoğu üniversitede ayrıca finalden en az 50 gibi bir baraj bulunur.",
    "senaryolar": [
        {"ad": "Vize 60 · %40-60", "degerler": {"vize": "60", "vize_a": "40", "final": "50", "gecme": "50", "final_baraj": "0"}},
        {"ad": "Vize 40 · zor durum", "degerler": {"vize": "40", "vize_a": "40", "final": "60", "gecme": "50", "final_baraj": "50"}},
        {"ad": "Vize 80 · %30-70", "degerler": {"vize": "80", "vize_a": "30", "final": "60", "gecme": "50", "final_baraj": "0"}},
        {"ad": "Vize 55 · geçme 60", "degerler": {"vize": "55", "vize_a": "40", "final": "70", "gecme": "60", "final_baraj": "50"}},
    ],
    "girdiler": [
        {"id": "vize", "etiket": "Vize notu", "tip": "sayi", "varsayilan": "60", "birim": "/100"},
        {"id": "vize_a", "etiket": "Vize ağırlığı", "tip": "sayi", "varsayilan": "40", "birim": "%", "ipucu": "final ağırlığı otomatik"},
        {"id": "final", "etiket": "Final notu (tahmini)", "tip": "sayi", "varsayilan": "50", "birim": "/100"},
        {"id": "gecme", "etiket": "Geçme notu", "tip": "sayi", "varsayilan": "50", "birim": "/100"},
        {"id": "final_baraj", "etiket": "Final barajı (yoksa 0)", "tip": "sayi", "varsayilan": "0", "birim": "/100", "ipucu": "ör. finalden en az 50"},
    ],
    "js": r"""
function harf(o){
  return o >= 90 ? 'AA (4,00)' : o >= 85 ? 'BA (3,50)' : o >= 80 ? 'BB (3,00)' : o >= 75 ? 'CB (2,50)' :
         o >= 65 ? 'CC (2,00)' : o >= 58 ? 'DC (1,50)' : o >= 50 ? 'DD (1,00)' : o >= 40 ? 'FD (0,50)' : 'FF (0,00)';
}
function hesapla(g){
  if (!(g.vize >= 0 && g.vize <= 100)) return {hata: 'Vize notu 0-100 arasında olmalı.'};
  var va = (g.vize_a >= 0 && g.vize_a <= 100) ? g.vize_a : 40, fa = 100 - va;
  if (fa <= 0) return {hata: 'Vize ağırlığı 100 olamaz; finalin de ağırlığı olmalı.'};
  var f = (g.final >= 0 && g.final <= 100) ? g.final : 0;
  var gecme = (g.gecme > 0 && g.gecme <= 100) ? g.gecme : 50;
  var baraj = g.final_baraj > 0 ? g.final_baraj : 0;
  var ort = g.vize * va / 100 + f * fa / 100;
  var gerekli = (gecme - g.vize * va / 100) / (fa / 100);
  var gerekliGercek = Math.max(gerekli, baraj);
  var gecti = ort >= gecme && f >= baraj;
  var s = [
    {etiket: 'Ders ortalaması', deger: Math.round(ort * 100) / 100, birim: '/100', vurgu: true},
    {etiket: 'Harf notu karşılığı (yaklaşık)', deger: harf(ort)},
    {etiket: 'Durum', deger: gecti ? 'GEÇTİ ✓' : (ort >= gecme && f < baraj ? 'Ortalama yeterli ama FİNAL BARAJI aşılmadı' : 'KALDI')},
    {etiket: 'Geçmek için finalden gereken not', deger: gerekliGercek > 100 ? 'İmkânsız (100\'den fazla gerekiyor)' : Math.round(gerekliGercek * 100) / 100},
    {etiket: 'Vizenin ortalamaya katkısı', deger: g.vize * va / 100, birim: 'puan'},
    {etiket: 'Finalin ortalamaya katkısı', deger: f * fa / 100, birim: 'puan'},
    {etiket: 'Ağırlıklar', deger: '%' + va + ' vize · %' + fa + ' final'}
  ];
  // final senaryoları
  var sat = [], gEt = [], gV = [];
  for (var x = 0; x <= 100; x += 10) {
    var o = g.vize * va / 100 + x * fa / 100;
    var d = (o >= gecme && x >= baraj) ? 'Geçer' : 'Kalır';
    sat.push([x, Math.round(o * 100) / 100, harf(o).split(' ')[0], d]);
    gEt.push(String(x)); gV.push(Math.round(o * 100) / 100);
  }
  var n = ['Ağırlıklar üniversiteye ve derse göre değişir; en yaygın uygulama %40 vize + %60 finaldir. Bazı derslerde kısa sınav, ödev veya laboratuvar notu da ortalamaya girer.'];
  if (baraj > 0) n.push('Final barajı ' + baraj + ' olarak alındı: ortalama yeterli olsa bile finalden bu notun altında kalırsanız dersten kalırsınız.');
  if (gerekli > 100) n.push('Bu vize notuyla geçme notuna ulaşmak matematiksel olarak mümkün değil; bütünleme veya ders tekrarı gerekir.');
  n.push('Bütünlemede genellikle final notu yerine bütünleme notu konur ve aynı formül uygulanır.');
  return {sonuclar: s, notlar: n,
    tablo: {basliklar: ['Final notu', 'Ortalama', 'Harf', 'Sonuç'], satirlar: sat},
    grafik: {tur: 'cizgi', baslik: 'Final notuna göre ders ortalaması', etiketler: gEt, seriler: [{ad: 'Ortalama', veri: gV}, {ad: 'Geçme notu', veri: gEt.map(function(){ return gecme; }), renk: '#dc2626'}]}};
}
""",
    "nasil": [
        "Bir dersin başarı notu, ara sınav (vize) ve yarıyıl sonu sınavı (final) notlarının ağırlıklı ortalamasıdır. Türkiye'de en yaygın uygulama vizenin %40, finalin %60 ağırlıkta olmasıdır; bazı üniversitelerde %30-70 veya %50-50 kullanılır, ayrıca kısa sınav, ödev, proje ve laboratuvar notları da ağırlıklandırılabilir.",
        "Geçmek için finalden almanız gereken notu bulmak, formülü tersine çevirmekle olur: gereken final = (geçme notu − vize × vize ağırlığı) ÷ final ağırlığı. Vizeden 60 alan ve %40-60 ağırlıklı bir derste 50 ile geçmek isteyen öğrenci finalden 43,33 almalıdır.",
        "Ortalamanın yeterli olması her zaman yetmez: birçok üniversitede finalden en az 50 (bazılarında 45 veya 40) alma şartı — final barajı — vardır. Baraj altında kalan öğrenci ortalaması yüksek olsa bile dersten kalır ve bütünlemeye girer. Bütünlemede alınan not finalin yerine geçer ve aynı formül uygulanır.",
    ],
    "formul": [
        "Ders ortalaması = vize × (vize ağırlığı ÷ 100) + final × (final ağırlığı ÷ 100)",
        "Gereken final notu = (geçme notu − vize × vize ağırlığı ÷ 100) ÷ (final ağırlığı ÷ 100)",
        "Final ağırlığı = 100 − vize ağırlığı",
        "Geçme koşulu: ortalama ≥ geçme notu VE final ≥ final barajı",
    ],
    "ornekler": [
        {"baslik": "Vize 60, final 50, %40-60", "adimlar": ["Ortalama = 60×0,40 + 50×0,60 = 24 + 30 = 54", "Geçme 50 → geçti; harf karşılığı DD/CC bandı"]},
        {"baslik": "Vize 40, geçmek için gereken final (%40-60, geçme 50)", "adimlar": ["(50 − 40×0,40) ÷ 0,60 = (50 − 16) ÷ 0,60 = 56,67", "Final barajı 50 varsa yine 56,67 gerekir"]},
        {"baslik": "Vize 20 ile geçilebilir mi? (%40-60, geçme 50)", "adimlar": ["(50 − 8) ÷ 0,60 = 70 → finalden 70 gerekiyor, mümkün ama zor"]},
    ],
    "tablo": {
        "baslik": "Yaygın ağırlıklandırmalar",
        "basliklar": ["Ağırlık", "Vize", "Final", "Not"],
        "satirlar": [["Standart", "%40", "%60", "En yaygın uygulama"], ["Final ağırlıklı", "%30", "%70", "Bazı temel derslerde"], ["Eşit", "%50", "%50", "Bazı uygulamalı derslerde"], ["Çok bileşenli", "%30 vize + %20 ödev/quiz", "%50", "Ders izlencesinde belirtilir"]],
        "not": "Kesin ağırlıklar ders izlencesinde (syllabus) ve üniversite yönetmeliğinde yer alır.",
    },
    "sss": [
        {"soru": "Vize final ortalaması nasıl hesaplanır?", "cevap": "Vizeyi ağırlığıyla, finali kendi ağırlığıyla çarpıp toplayın. %40-60 ağırlıkta vize 70, final 60 ise: 70×0,4 + 60×0,6 = 28 + 36 = 64."},
        {"soru": "Geçmek için finalden kaç almalıyım?", "cevap": "(Geçme notu − vize × vize ağırlığı) ÷ final ağırlığı. Vize 55, %40-60, geçme 50 → (50 − 22) ÷ 0,6 = 46,67."},
        {"soru": "Final barajı nedir?", "cevap": "Ortalamadan bağımsız olarak finalden alınması gereken en düşük nottur (çoğunlukla 50). Baraj altında kalırsanız ortalamanız yeterli olsa da dersten kalırsınız."},
        {"soru": "Bütünleme notu nasıl hesaplanır?", "cevap": "Bütünleme notu finalin yerine yazılır ve aynı ağırlıkla ortalama yeniden hesaplanır; vize notu değişmez."},
        {"soru": "Vize ağırlığı %40 değilse ne yapmalıyım?", "cevap": "Aracımızdaki vize ağırlığı alanını dersinizin izlencesindeki değere göre değiştirin; final ağırlığı otomatik olarak 100'e tamamlanır."},
    ],
    "kaynaklar": [
        {"ad": "YÖK — Yükseköğretim kurumları eğitim-öğretim yönetmelikleri", "url": "https://www.yok.gov.tr/"},
    ],
    "ilgili": ["gano-hesaplama", "yuzde-hesaplama", "ortalama-hesaplama"],
}
