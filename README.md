# nasilhesap.com

Türkiye için güncel, kaynaklı, reklamsız hesaplama araçları. Statik site; hesaplamalar tarayıcıda çalışır.

## Çalıştırma

```
pip install jinja2 pillow
python build/og.py          # sosyal görsel (bir kez)
python build/derle.py       # dist/ üretir
python -m http.server 8000 --directory dist
```

## Yapı

- `hesaplamalar/<slug>.py` — her araç bir `HESAP` sözlüğü: içerik (kısa cevap, nasıl, formül, örnek, tablo, SSS, kaynak) + `girdiler` + istemci JS (`hesapla(g, O)`).
- `data/oranlar-2026.json` — tüm resmî oranlar tek yerde (kaynaklı); sayfaya `window.ORAN` olarak gömülür.
- `data/kategoriler.json`, `data/site.json`
- `templates/` — Jinja2; `static/h.js` hesaplayıcı çalışma zamanı + arama; `static/s.css`.
- Çıktı: `/<slug>/`, `/<kategori>/`, `sitemap.xml`, `robots.txt`, `llms.txt`, `static/araclar.json` (arama dizini).

## İlke

Hiçbir oran tahminle yazılmaz; her kalemin kaynağı `oranlar-2026.json` ve sayfa altındaki "Kaynaklar" bölümündedir. Yıl değişince yalnızca oran dosyası ve ilgili tablolar güncellenir.

## Deploy

Dockerfile (python build → nginx). `.github/workflows/deploy.yml` push + günlük cron ile Coolify deploy API'sini çağırır (`COOLIFY_DEPLOY_URL`, `COOLIFY_TOKEN` secret'ları).
