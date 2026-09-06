# -*- coding: utf-8 -*-
"""nasilhesap.com statik site üreteci.

Kullanım:  python build/derle.py   -> dist/ klasörüne tüm siteyi yazar

Her hesaplayıcı hesaplamalar/<slug>.py içinde HESAP sözlüğüdür (içerik + girdiler +
istemci tarafı JS). Oranlar data/oranlar-2026.json'dan gelir ve sayfaya window.ORAN
olarak gömülür. Sayfa başına: WebApplication + FAQPage + BreadcrumbList JSON-LD,
kısa cevap (GEO), formül, örnek, tablo, SSS, kaynak, ilgili araçlar.
"""
from __future__ import annotations
import importlib.util
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

sys.stdout.reconfigure(encoding="utf-8")

KOK = Path(__file__).resolve().parent.parent
DIST = KOK / "dist"
STATIC = KOK / "static"
TEMPLATES = KOK / "templates"
DATA = KOK / "data"
HESAP_DIR = KOK / "hesaplamalar"

ZORUNLU = ("slug", "baslik", "kategori", "aciklama", "kisa_cevap", "girdiler", "js", "nasil", "formul", "sss")


def yukle_json(ad):
    return json.loads((DATA / ad).read_text(encoding="utf-8"))


def hesaplamalari_yukle():
    liste = []
    for p in sorted(HESAP_DIR.glob("*.py")):
        if p.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(p.stem, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        h = getattr(mod, "HESAP", None)
        if not h:
            continue
        eksik = [k for k in ZORUNLU if k not in h]
        if eksik:
            raise SystemExit(f"{p.name}: eksik alanlar {eksik}")
        h.setdefault("h1", h["baslik"])
        h.setdefault("ornekler", [])
        h.setdefault("tablo", None)
        h.setdefault("kaynaklar", [])
        h.setdefault("ilgili", [])
        h.setdefault("populer", False)
        h.setdefault("guncelleme", "2026")
        h["url"] = f"/{h['slug']}/"
        liste.append(h)
    return liste


def sss_schema(sss):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": s["soru"],
                            "acceptedAnswer": {"@type": "Answer", "text": s["cevap"]}} for s in sss]}


def kirintilar(site, *parcalar):
    items = [{"@type": "ListItem", "position": 1, "name": "Ana sayfa", "item": site["url"] + "/"}]
    for i, (ad, url) in enumerate(parcalar, 2):
        items.append({"@type": "ListItem", "position": i, "name": ad, "item": site["url"] + url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def app_schema(site, h, kat):
    return {"@context": "https://schema.org", "@type": "WebApplication",
            "name": h["h1"], "url": site["url"] + h["url"], "description": h["aciklama"],
            "applicationCategory": kat.get("schema_kategori", "UtilitiesApplication"),
            "operatingSystem": "Web", "browserRequirements": "Requires JavaScript",
            "inLanguage": "tr-TR", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
            "publisher": {"@type": "Organization", "name": site["ad"], "url": site["url"] + "/"},
            "dateModified": h["guncelleme"]}


def liste_schema(site, ad, url, hesaplar):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": ad, "url": site["url"] + url,
            "numberOfItems": len(hesaplar),
            "itemListElement": [{"@type": "ListItem", "position": i, "name": h["baslik"], "url": site["url"] + h["url"]}
                                for i, h in enumerate(hesaplar, 1)]}


def main():
    site = yukle_json("site.json")
    oranlar = yukle_json("oranlar-2026.json")
    kategoriler = yukle_json("kategoriler.json")
    hesaplar = hesaplamalari_yukle()
    kat_map = {k["slug"]: k for k in kategoriler}
    slug_map = {h["slug"]: h for h in hesaplar}
    for h in hesaplar:
        if h["kategori"] not in kat_map:
            raise SystemExit(f"{h['slug']}: bilinmeyen kategori {h['kategori']}")
        h["kat"] = kat_map[h["kategori"]]
        h["ilgili_hesaplar"] = [slug_map[s] for s in h["ilgili"] if s in slug_map]
    for k in kategoriler:
        k["url"] = f"/{k['slug']}/"
        k["hesaplar"] = [h for h in hesaplar if h["kategori"] == k["slug"]]
    site["derleme_zamani"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    site["oranlar_guncelleme"] = oranlar["guncelleme"]

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["json"] = lambda v: json.dumps(v, ensure_ascii=False)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST / "static")
    shutil.copy(STATIC / "favicon.svg", DIST / "favicon.svg")
    (DIST / "static" / "oranlar.json").write_text(json.dumps(oranlar, ensure_ascii=False), encoding="utf-8")

    sayfalar = []  # (url, lastmod, oncelik)

    def sayfa(url, sablon, **ctx):
        hedef = DIST / url.strip("/") / "index.html" if url != "/" else DIST / "index.html"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        ctx.setdefault("site", site)
        ctx.setdefault("kategoriler", kategoriler)
        ctx.setdefault("oranlar", oranlar)
        ctx.setdefault("canonical", url)
        ctx.setdefault("schema", [])
        hedef.write_text(env.get_template(sablon).render(**ctx), encoding="utf-8")
        sayfalar.append((url, ctx.get("lastmod", oranlar["guncelleme"]), ctx.get("oncelik", "0.7")))

    populer = [h for h in hesaplar if h["populer"]] or hesaplar[:8]
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": site["ad"], "url": site["url"] + "/",
               "inLanguage": "tr-TR",
               "potentialAction": {"@type": "SearchAction", "target": site["url"] + "/?q={search_term_string}",
                                   "query-input": "required name=search_term_string"}}
    org = {"@context": "https://schema.org", "@type": "Organization", "name": site["ad"], "url": site["url"] + "/",
           "logo": site["url"] + "/static/logo.svg"}
    sayfa("/", "index.html", baslik=f"{site['ad']} — {site['slogan']}", meta_desc=site["aciklama"],
          hesaplar=hesaplar, populer=populer, schema=[website, org], oncelik="1.0")

    for k in kategoriler:
        sayfa(k["url"], "kategori.html", baslik=f"{k['ad']} Hesaplamaları 2026 | {site['ad']}",
              meta_desc=f"{k['ad']} hesaplamaları: {k['aciklama']} {site['yil']} güncel oranlarla, anında ve ücretsiz.",
              kat=k, schema=[liste_schema(site, k["ad"], k["url"], k["hesaplar"]), kirintilar(site, (k["ad"], k["url"]))],
              oncelik="0.8")

    for h in hesaplar:
        sayfa(h["url"], "hesap.html", baslik=f"{h['h1']} | {site['ad']}", meta_desc=h["aciklama"], h=h,
              schema=[app_schema(site, h, h["kat"]), sss_schema(h["sss"]),
                      kirintilar(site, (h["kat"]["ad"], h["kat"]["url"]), (h["baslik"], h["url"]))],
              lastmod=h["guncelleme"] if len(h["guncelleme"]) == 10 else oranlar["guncelleme"], oncelik="0.9")

    for slug, baslik, sablon in (("hakkinda", "Hakkında", "hakkinda.html"), ("gizlilik", "Gizlilik ve Çerez Politikası", "gizlilik.html"),
                                 ("kaynaklar", "Veri Kaynakları ve Güncelleme", "kaynaklar.html")):
        sayfa(f"/{slug}/", sablon, baslik=f"{baslik} | {site['ad']}", meta_desc=f"{site['ad']} — {baslik.lower()}.",
              hesaplar=hesaplar, schema=[kirintilar(site, (baslik, f"/{slug}/"))], oncelik="0.3")

    (DIST / "404.html").write_text(env.get_template("404.html").render(site=site, kategoriler=kategoriler, oranlar=oranlar,
                                                                       baslik="Sayfa bulunamadı", meta_desc="", canonical="/404.html", schema=[]),
                                   encoding="utf-8")

    # arama dizini
    (DIST / "static" / "araclar.json").write_text(json.dumps(
        [{"s": h["slug"], "b": h["baslik"], "k": h["kat"]["ad"], "a": h["aciklama"][:120], "i": h["kat"]["ikon"]} for h in hesaplar],
        ensure_ascii=False), encoding="utf-8")

    # sitemap / robots / llms
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, onc in sayfalar:
        sm.append(f"  <url><loc>{site['url']}{url}</loc><lastmod>{lastmod}</lastmod><priority>{onc}</priority></url>")
    sm.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}/sitemap.xml\n", encoding="utf-8")

    llms = [f"# {site['ad']}", "", f"> {site['aciklama']}", "",
            f"Tüm oranlar resmî kaynaklıdır (GİB, SGK, TÜİK, Resmî Gazete). Son oran güncellemesi: {oranlar['guncelleme']}.", ""]
    for k in kategoriler:
        llms.append(f"## {k['ad']}")
        for h in k["hesaplar"]:
            llms.append(f"- [{h['baslik']}]({site['url']}{h['url']}): {h['kisa_cevap']}")
        llms.append("")
    (DIST / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    print(f"✓ {len(hesaplar)} hesaplayıcı, {len(kategoriler)} kategori, {len(sayfalar)} sayfa -> {DIST}")


if __name__ == "__main__":
    main()
