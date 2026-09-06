# -*- coding: utf-8 -*-
"""nasilhesap.com tam site denetimi: SEO, GEO, erişilebilirlik, iç bağlantı, şema.

Kullanım:  python build/derle.py && python build/denetim.py
Çıkış kodu 1 ise KRİTİK bulgu var.
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parent.parent
DIST = KOK / "dist"

kritik, uyari, bilgi = [], [], []


def K(m): kritik.append(m)
def U(m): uyari.append(m)
def B(m): bilgi.append(m)


def sayfalar():
    for p in DIST.rglob("index.html"):
        bagil = p.parent.relative_to(DIST).as_posix()
        yield ("/" if bagil == "." else f"/{bagil}/", p)


def main():
    if not DIST.exists():
        print("dist yok — önce python build/derle.py"); return 1

    sf = list(sayfalar())
    print(f"=== {len(sf)} sayfa denetleniyor ===\n")

    basliklar, aciklamalar, ic_hedefler = Counter(), Counter(), Counter()
    tum_urller = {u for u, _ in sf} | {"/404.html"}
    sema_sayac = Counter()

    for url, p in sf:
        h = p.read_text(encoding="utf-8")

        # --- title / description ---
        t = re.search(r"<title>(.*?)</title>", h, re.S)
        t = t.group(1).strip() if t else ""
        if not t: K(f"{url}: <title> yok")
        elif len(t) > 65: U(f"{url}: title {len(t)} karakter (>65, SERP'te kesilir): {t[:70]}…")
        elif len(t) < 20: U(f"{url}: title çok kısa ({len(t)})")
        basliklar[t] += 1

        d = re.search(r'<meta name="description" content="(.*?)"', h, re.S)
        d = d.group(1).strip() if d else ""
        if not d: K(f"{url}: meta description yok")
        elif len(d) > 175: U(f"{url}: description {len(d)} karakter (>175)")
        elif len(d) < 70: U(f"{url}: description çok kısa ({len(d)})")
        aciklamalar[d] += 1

        # --- h1 ---
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        if len(h1) == 0: K(f"{url}: h1 yok")
        elif len(h1) > 1: K(f"{url}: {len(h1)} adet h1 (tek olmalı)")

        # --- başlık hiyerarşisi ---
        seviyeler = [int(m) for m in re.findall(r"<h([1-6])[ >]", h)]
        for a, b in zip(seviyeler, seviyeler[1:]):
            if b > a + 1:
                U(f"{url}: başlık atlaması h{a} → h{b}"); break

        # --- canonical / og ---
        if 'rel="canonical"' not in h: K(f"{url}: canonical yok")
        if 'property="og:title"' not in h: U(f"{url}: og:title yok")
        if 'property="og:image"' not in h: U(f"{url}: og:image yok")

        # --- lang / viewport ---
        if 'lang="tr"' not in h: K(f"{url}: html lang=tr yok")
        if "viewport" not in h: K(f"{url}: viewport meta yok")

        # --- JSON-LD geçerliliği ---
        for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                veri = json.loads(blok)
            except Exception as e:
                K(f"{url}: bozuk JSON-LD ({e})"); continue
            for obj in (veri if isinstance(veri, list) else [veri]):
                tip = obj.get("@type", "?")
                sema_sayac[tip] += 1
                if "@context" not in obj: K(f"{url}: {tip} şemasında @context yok")
                if tip == "FAQPage":
                    q = obj.get("mainEntity", [])
                    if len(q) < 3: U(f"{url}: FAQPage yalnızca {len(q)} soru (≥3 önerilir)")
                    for s in q:
                        if not s.get("acceptedAnswer", {}).get("text"): K(f"{url}: FAQ cevabı boş")
                if tip == "BreadcrumbList" and not obj.get("itemListElement"):
                    K(f"{url}: boş BreadcrumbList")

        # --- görsel alt ---
        for img in re.findall(r"<img[^>]*>", h):
            if "alt=" not in img: K(f"{url}: alt'sız <img>")

        # --- iç bağlantılar ---
        for hedef in re.findall(r'href="(/[^"#?]*)"', h):
            ic_hedefler[hedef] += 1
            if hedef.endswith((".xml", ".txt", ".svg", ".png", ".ico", ".js", ".css", ".json")):
                if not (DIST / hedef.lstrip("/")).exists(): K(f"{url}: kırık dosya bağlantısı {hedef}")
            elif hedef not in tum_urller:
                K(f"{url}: kırık iç bağlantı {hedef}")

        # --- GEO sinyalleri (hesap sayfaları) ---
        if url.count("/") == 2 and url not in ("/hakkinda/", "/gizlilik/", "/kaynaklar/") and "kisa-cevap" in h:
            kc = re.search(r'class="kisa-cevap">(.*?)</p>', h, re.S)
            if kc:
                metin = re.sub(r"<[^>]+>", "", kc.group(1)).replace("Kısa cevap:", "").strip()
                if len(metin) < 120: U(f"{url}: kısa cevap çok kısa ({len(metin)} krk, 150-350 ideal)")
                if len(metin) > 500: U(f"{url}: kısa cevap çok uzun ({len(metin)} krk)")
            if "<details" not in h: U(f"{url}: SSS bölümü yok")
            if "Kaynaklar" not in h: U(f"{url}: kaynak bölümü yok")

    # --- yinelenen title/description ---
    for t, n in basliklar.items():
        if n > 1 and t: K(f"YİNELENEN title ({n}×): {t[:70]}")
    for d, n in aciklamalar.items():
        if n > 1 and d: K(f"YİNELENEN description ({n}×): {d[:70]}…")

    # --- öksüz sayfalar (hiç iç bağlantı almayan) ---
    for u, _ in sf:
        if u == "/": continue
        if ic_hedefler.get(u, 0) == 0: K(f"ÖKSÜZ sayfa (hiç iç bağlantı yok): {u}")
        elif ic_hedefler.get(u, 0) < 2: U(f"az iç bağlantı ({ic_hedefler[u]}): {u}")

    # --- sitemap tutarlılığı ---
    sm = (DIST / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = set(re.findall(r"<loc>https://nasilhesap\.com(/[^<]*)</loc>", sm))
    eksik = {u for u, _ in sf} - sm_urls
    fazla = sm_urls - {u for u, _ in sf}
    if eksik: K(f"sitemap'te eksik: {sorted(eksik)[:5]}")
    if fazla: K(f"sitemap'te olmayan sayfa: {sorted(fazla)[:5]}")

    # --- llms.txt / robots ---
    llms = (DIST / "llms.txt").read_text(encoding="utf-8")
    if len(llms) < 2000: U("llms.txt zayıf (<2 KB)")
    B(f"llms.txt {len(llms)//1024} KB · sitemap {len(sm_urls)} URL")
    rb = (DIST / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap:" not in rb: K("robots.txt'te Sitemap satırı yok")

    # --- performans (boyut) ---
    for ad, yol in (("CSS", DIST / "static/s.css"), ("JS", DIST / "static/h.js")):
        kb = yol.stat().st_size / 1024
        if kb > 60: U(f"{ad} {kb:.0f} KB (>60)")
        else: B(f"{ad} {kb:.1f} KB")
    en_buyuk = max(sf, key=lambda x: x[1].stat().st_size)
    B(f"en büyük sayfa: {en_buyuk[0]} ({en_buyuk[1].stat().st_size/1024:.0f} KB)")
    B("şemalar: " + ", ".join(f"{k}×{v}" for k, v in sema_sayac.most_common()))

    # --- rapor ---
    for ad, liste, ikon in (("KRİTİK", kritik, "✗"), ("UYARI", uyari, "!"), ("BİLGİ", bilgi, "·")):
        if liste:
            print(f"\n--- {ad} ({len(liste)}) ---")
            for m in liste[:40]:
                print(f" {ikon} {m}")
            if len(liste) > 40: print(f"   … +{len(liste)-40} tane daha")
    print(f"\n=== SONUÇ: {len(kritik)} kritik, {len(uyari)} uyarı ===")
    return 1 if kritik else 0


if __name__ == "__main__":
    sys.exit(main())
