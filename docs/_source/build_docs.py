"""Build the Sales Report Dashboard documentation (English + Bahasa Indonesia).

Usage:  python3 -I docs/_source/build_docs.py
Writes: docs/SalesReport-Documentation.html, docs/id/SalesReport-Dokumentasi.html and docs/index.html

Every text is a pair T(en, id) so both languages always have the same structure.
Styling lives in docs/_source/style.css (shared look with the other portfolio docs).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
OUT = {"en": ROOT / "docs" / "SalesReport-Documentation.html",
       "id": ROOT / "docs" / "id" / "SalesReport-Dokumentasi.html"}
OTHER = {"en": ("id/SalesReport-Dokumentasi.html", "Bahasa Indonesia", "id"),
         "id": ("../SalesReport-Documentation.html", "English", "en")}
IMG = {"en": "img/dashboard.png", "id": "../img/dashboard.png"}
DEMO = "https://diimasogan.github.io/PowerBI-SalesReport-Dashboard/"
REPO = "https://github.com/diimasogan/PowerBI-SalesReport-Dashboard"
LANG = "en"


class T(tuple):
    def __new__(cls, en, id_=None):
        return super().__new__(cls, (en, en if id_ is None else id_))

    def __str__(self):
        return self[0] if LANG == "en" else self[1]


def s(x):
    return str(x) if isinstance(x, T) else x


# ---------------------------------------------------------------- building blocks
ICONS = {
    "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8z"/>',
    "bars": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "table": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
}


def card(ic, title, text, amber=False):
    return (f'<div class="card{" amber" if amber else ""}"><div class="ihead">'
            f'<svg class="ico" viewBox="0 0 24 24">{ICONS[ic]}</svg><h3>{s(title)}</h3></div><p>{s(text)}</p></div>')


def grid(cards, cols=3):
    return f'<div class="grid g{cols}">{"".join(cards)}</div>'


def table(head, rows):
    h = "".join(f"<th>{s(x)}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{s(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section(id_, title, body):
    return f'<section id="{id_}"><h2>{s(title)}</h2>{body}</section>'


def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{s(a)}</b><span>{s(b)}</span></div>' for a, b in items) + "</div>"


def steps(items):
    out = []
    for i, (title, text) in enumerate(items, 1):
        out.append(f'<div class="card starter"><div class="snum{" amber" if i % 2 == 0 else ""}">{i}</div>'
                   f'<div><p class="q">{s(title)}</p><p>{s(text)}</p></div></div>')
    return '<div class="grid g2">' + "".join(out) + "</div>"


# ---------------------------------------------------------------- content
TOC = [("summary", T("Summary", "Ringkasan")), ("features", T("Features", "Fitur")),
       ("pages", T("Report pages", "Halaman report")), ("metrics", T("Metrics", "Metrik")),
       ("architecture", T("Architecture", "Arsitektur")), ("data", T("Data & anonymization", "Data & anonimisasi")),
       ("use", T("How to use", "Cara pakai")), ("run", T("Run locally", "Jalankan lokal")),
       ("notes", T("Limitations", "Keterbatasan"))]


def architecture_svg():
    lanes = [(10, T("Private · Power BI", "Privat · Power BI")), (340, T("Preparation · Python", "Persiapan · Python")),
             (670, T("Public · GitHub Pages", "Publik · GitHub Pages"))]
    boxes = [
        (30, 80, T("Source data (Excel)", "Data sumber (Excel)"), T("87,073 SO lines · 67 columns", "87.073 baris SO · 67 kolom"), ""),
        (30, 200, T("Power BI report (.pbix)", "Report Power BI (.pbix)"), T("5 pages · slicers · DAX measures", "5 halaman · slicer · measure DAX"), ""),
        (360, 80, T("Select & clean", "Pilih & bersihkan"), T("19 columns + 3 helper columns", "19 kolom + 3 kolom bantu"), ""),
        (360, 200, T("Anonymize", "Anonimkan"), T("generic names · scaled amounts + noise", "nama generik · nilai diskalakan + noise"), " amb"),
        (360, 320, T("Aggregate → data.json", "Agregasi → data.json"), T("57,603 grouped rows · dictionary-encoded", "57.603 baris agregat · kode kamus"), ""),
        (690, 200, T("Dashboard (index.html)", "Dashboard (index.html)"), T("filters · ECharts · Leaflet · tables", "filter · ECharts · Leaflet · tabel"), " hl"),
        (690, 320, T("Visitor's browser", "Browser pengunjung"), T("all filtering runs client-side", "semua filter berjalan di browser"), ""),
    ]
    out = ['<figure><svg viewBox="0 0 980 420" role="img" aria-label="Architecture">',
           '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0 0 10 5 0 10z" class="mk"/></marker></defs>']
    for x, t in lanes:
        out.append(f'<g class="lane"><rect x="{x}" y="20" width="300" height="390" rx="14"/><text x="{x + 150}" y="46" class="lt">{s(t)}</text></g>')
    for x, y, t, sm, cls in boxes:
        out.append(f'<g class="bx{cls}"><rect x="{x}" y="{y}" width="260" height="60" rx="10"/>'
                   f'<text x="{x + 130}" y="{y + 26}">{s(t)}</text><text x="{x + 130}" y="{y + 45}" class="sm">{s(sm)}</text></g>')
    for d in ["M160 140 V196", "M290 110 H356", "M490 140 V196", "M490 260 V316", "M620 350 C650 350 650 230 686 230", "M820 260 V316"]:
        out.append(f'<g class="ln"><path d="{d}" marker-end="url(#ar)"/></g>')
    out.append("</svg><figcaption>" + s(T(
        "The original data and .pbix stay in a private repository; only anonymized, aggregated data is published.",
        "Data asli dan .pbix tetap di repository privat; yang dipublikasikan hanya data agregat yang sudah dianonimkan.")) + "</figcaption></figure>")
    return "".join(out)


def body():
    parts = []
    parts.append(section("summary", T("Executive summary", "Ringkasan eksekutif"),
        '<p class="lead">' + s(T(
            "Sales Report Dashboard is an interactive property sales report. It was designed in Power BI for stakeholders who need a quick view of commercial performance (where sales come from, which business units drive them, and where cancellations happen) and was rebuilt as a static web page so anyone can explore it without a Power BI licence.",
            "Sales Report Dashboard adalah laporan penjualan properti yang interaktif. Awalnya dirancang di Power BI untuk stakeholder yang butuh gambaran cepat performa komersial (dari mana penjualan datang, unit bisnis mana yang mendorongnya, dan di mana pembatalan terjadi), lalu dibangun ulang sebagai halaman web statis supaya siapa saja bisa mencobanya tanpa lisensi Power BI.")) + "</p>"
        + stats([("87,073", T("sales-order lines", "baris sales order")), ("5", T("Power BI pages rebuilt", "halaman Power BI dibangun ulang")),
                 ("7", T("cross-linked filters", "filter yang saling terhubung")), ("45", T("cities on the map", "kota di peta"))])
        + f'<div class="note" style="margin-top:18px">⚠️ {s(T("All names and amounts in the demo are anonymized; the figures are realistic in shape but not real.", "Semua nama dan nilai di demo sudah dianonimkan; polanya realistis tetapi angkanya bukan angka asli."))}</div>'
        + f'<figure><a href="{DEMO}"><img src="{IMG[LANG]}" alt="{s(T("Dashboard overview page", "Halaman overview dashboard"))}" loading="lazy"></a>'
        + f'<figcaption>{s(T("Overview page (light mode)", "Halaman Overview (mode terang)"))}</figcaption></figure>'
        + f'<p><a class="btn" href="{DEMO}">{s(T("Open the live demo →", "Buka demo live →"))}</a></p>'))

    parts.append(section("features", T("Features", "Fitur"), grid([
        card("filter", T("Global filters", "Filter global"), T(
            "Province, City, SBU, Division, Cluster, Product type and SO year range. The City list narrows to the selected province.",
            "Province, City, SBU, Division, Cluster, Product type, dan rentang tahun SO. Daftar City menyesuaikan provinsi yang dipilih.")),
        card("bolt", T("Click to cross-filter", "Klik untuk cross-filter"), T(
            "Clicking a bar or a map bubble applies that value as a filter, like cross-filtering in Power BI.",
            "Klik bar atau bubble di peta untuk langsung memakai nilai itu sebagai filter, seperti cross-filter di Power BI.")),
        card("map", T("Sales map", "Peta penjualan"), T(
            "Bubble map of net sales by city; bubble area is proportional to net sales.",
            "Peta bubble net sales per kota; luas bubble sebanding dengan net sales.")),
        card("bars", T("Ranked comparisons", "Perbandingan berperingkat"), T(
            "Net sales by province, top 10 cities, SBU and product type (with share of total).",
            "Net sales per provinsi, 10 kota teratas, SBU, dan tipe produk (dengan persentase dari total).")),
        card("trend", T("Cancellation trend", "Tren pembatalan"), T(
            "Cancelled orders per calendar month, split by the four main product types plus Other.",
            "Order batal per bulan, dipecah per empat tipe produk utama ditambah Other.")),
        card("table", T("Summary & detail tables", "Tabel ringkasan & detail"), T(
            "An expandable province → city summary, and a sortable, searchable, paginated detail table.",
            "Ringkasan provinsi → kota yang bisa di-expand, dan tabel detail yang bisa di-sort, dicari, dan dipaginasi.")),
        card("moon", T("Light & dark mode", "Mode terang & gelap"), T(
            "Follows the system setting and the portfolio's theme toggle; chart colours are re-validated for each mode.",
            "Mengikuti pengaturan sistem dan tombol tema portofolio; warna chart divalidasi ulang untuk tiap mode."), True),
        card("phone", T("Responsive", "Responsif"), T(
            "Works on phones: filters and charts stack, and axis numbers hide when space is tight.",
            "Bisa dipakai di HP: filter dan chart tersusun ke bawah, angka sumbu disembunyikan saat ruang sempit."), True),
        card("shield", T("Privacy by design", "Privasi sejak desain"), T(
            "No real names or amounts are published; the original files stay in a private repository.",
            "Tidak ada nama atau nilai asli yang dipublikasikan; file asli tetap di repository privat."), True),
    ])))

    parts.append(section("pages", T("Report pages: Power BI → web", "Halaman report: Power BI → web"),
        '<p class="lead">' + s(T("Each Power BI page and visual has a web counterpart:", "Setiap halaman dan visual Power BI punya padanan di web:")) + "</p>"
        + table([T("Power BI page", "Halaman Power BI"), T("Power BI visual", "Visual Power BI"), T("Web dashboard", "Dashboard web")], [
            ("Cover", T("Title, logo, Last Refreshed card", "Judul, logo, kartu Last Refreshed"), T("Page header with data cut-off date (no company logo)", "Header halaman dengan tanggal cut-off data (tanpa logo perusahaan)")),
            ("Overview", T("Slicers (7)", "Slicer (7)"), T("Sticky filter bar shared by all tabs", "Filter bar menempel, dipakai bersama semua tab")),
            ("Overview", T("Azure Map (Province, City)", "Azure Map (Province, City)"), T("Leaflet bubble map on OpenStreetMap", "Peta bubble Leaflet di OpenStreetMap")),
            ("Overview", T("Top 10 bar charts (Province, City, SBU)", "Bar chart Top 10 (Province, City, SBU)"), T("ECharts horizontal bars with value labels", "Bar horizontal ECharts dengan label nilai")),
            ("Overview", T("Donut: net sales by product type", "Donut: net sales per tipe produk"), T("Ranked bars with % share (easier to compare close values)", "Bar berperingkat dengan % (lebih mudah membandingkan nilai yang mirip)")),
            ("Overview", T("Line: Cancellation Province by month", "Line: Cancellation Province per bulan"), T("Line chart by product type", "Line chart per tipe produk")),
            ("Summary", T("Matrix (Province → City → SBU → Division → Cluster)", "Matrix (Province → City → SBU → Division → Cluster)"), T("Expandable Province → City table with totals", "Tabel Province → City yang bisa di-expand, dengan total")),
            ("Detail", T("Table", "Tabel"), T("Sortable, searchable, paginated table", "Tabel dengan sort, pencarian, dan paginasi")),
            ("Detail | Drill Through", T("Drill-through page", "Halaman drill-through"), T("Replaced by click-to-filter + the Detail tab", "Diganti klik-untuk-filter + tab Detail")),
        ])))

    parts.append(section("metrics", T("Metric definitions", "Definisi metrik"), table(
        [T("Metric", "Metrik"), T("Definition", "Definisi"), T("Source column", "Kolom sumber")], [
            (T("Net sales (excl. VAT)", "Net sales (excl. PPN)"), T("Sum of net sales excluding VAT. Cancellation lines are negative, so this is already net of cancellations.", "Jumlah net sales tanpa PPN. Baris pembatalan bernilai negatif, jadi angka ini sudah dikurangi pembatalan."), "<code>SalesNetExPPNAmt</code>"),
            (T("Net sales (incl. VAT)", "Net sales (incl. PPN)"), T("Same as above, including VAT (PPN).", "Sama seperti di atas, termasuk PPN."), "<code>SalesNettInPPNAmt</code>"),
            (T("Net units sold", "Unit terjual (net)"), T("Sum of unit quantity: +1 for a sale line, −1 for a cancellation line.", "Jumlah kuantitas unit: +1 untuk baris penjualan, −1 untuk baris pembatalan."), "<code>UnitQty</code>"),
            (T("Cancellations", "Pembatalan"), T("Number of sales-order lines whose order type is a cancellation (ZC01 / ZC02). Includes cancel-and-rebook addenda.", "Jumlah baris sales order dengan tipe order pembatalan (ZC01 / ZC02). Termasuk addendum batal-lalu-buat-ulang."), "<code>OrderType</code> → <code>IsCancel</code>"),
            (T("Year filter", "Filter tahun"), T("Year of the first sales-order date.", "Tahun dari tanggal sales order pertama."), "<code>SOFirstDate</code>"),
            (T("Cancellation month", "Bulan pembatalan"), T("Calendar month of the sales-order date.", "Bulan kalender dari tanggal sales order."), "<code>MonthSODateNumber</code>"),
        ]) + '<p style="margin-top:12px;color:var(--muted)">' + s(T(
            "Amounts are shown in rupiah with T = trillion, B = billion, M = million.",
            "Nilai ditampilkan dalam rupiah dengan T = triliun, B = miliar, M = juta.")) + "</p>"))

    parts.append(section("architecture", T("Architecture", "Arsitektur"), architecture_svg() + grid([
        card("bolt", T("No backend", "Tanpa backend"), T(
            "One HTML file plus <code>data.json</code>. Aggregation for every filter combination happens in the browser in milliseconds.",
            "Satu file HTML plus <code>data.json</code>. Agregasi untuk setiap kombinasi filter dihitung di browser dalam hitungan milidetik.")),
        card("table", T("Compact data", "Data ringkas"), T(
            "Text values are stored once in dictionaries and rows reference them by index: 2.2 MB raw, about 0.5 MB gzipped.",
            "Nilai teks disimpan sekali di kamus dan baris merujuk lewat indeks: 2,2 MB mentah, sekitar 0,5 MB setelah gzip.")),
        card("layers", T("Libraries", "Library"), T(
            "Apache ECharts 5.5 for charts, Leaflet 1.9 with OpenStreetMap tiles for the map, both loaded from a CDN.",
            "Apache ECharts 5.5 untuk chart, Leaflet 1.9 dengan tile OpenStreetMap untuk peta, keduanya dimuat dari CDN.")),
    ])))

    parts.append(section("data", T("Data & anonymization", "Data & anonimisasi"),
        '<p class="lead">' + s(T(
            "The source is a sales-order view exported to Excel. Before anything was published, every identifying value was replaced:",
            "Sumbernya adalah view sales order yang diekspor ke Excel. Sebelum dipublikasikan, setiap nilai yang bisa mengidentifikasi sudah diganti:")) + "</p>"
        + table([T("Field", "Kolom"), T("Original", "Asli"), T("Published", "Dipublikasikan")], [
            (T("Company", "Perusahaan"), T("Real legal entity names", "Nama badan usaha asli"), "Company A, B, C…"),
            ("SBU", T("Business-unit names incl. location", "Nama unit bisnis termasuk lokasi"), T("Generic: Residential Core, Commercial Core, Regional East…", "Generik: Residential Core, Commercial Core, Regional East…")),
            (T("Division", "Divisi"), T("Real division names", "Nama divisi asli"), "Division A, B, C…"),
            (T("Cluster (373)", "Cluster (373)"), T("Real project / cluster names", "Nama proyek / cluster asli"), "Cluster 001, 002…"),
            (T("Amounts", "Nilai"), T("Real rupiah values", "Nilai rupiah asli"), T("× hidden random factor, plus ±15% noise per row", "× faktor acak tersembunyi, ditambah noise ±15% per baris")),
            (T("Order type", "Tipe order"), "ZS01, ZC01, …", T("Removed; only the derived IsCancel flag is kept", "Dihapus; hanya flag turunan IsCancel yang disimpan")),
            (T("Province, city, dates, product type", "Provinsi, kota, tanggal, tipe produk"), "—", T("Kept (not identifying)", "Tetap (tidak mengidentifikasi)")),
        ]) + '<div class="note" style="margin-top:14px">' + s(T(
            "The relative patterns (rankings, seasonality, product mix) remain realistic, so the dashboard still tells a credible story, but no figure can be traced back to the real business.",
            "Pola relatifnya (peringkat, musiman, komposisi produk) tetap realistis sehingga dashboard tetap bercerita dengan masuk akal, tetapi tidak ada angka yang bisa dilacak ke bisnis aslinya.")) + "</div>"))

    parts.append(section("use", T("How to use", "Cara pakai"), steps([
        (T("Start with the Overview", "Mulai dari Overview"), T("The KPI tiles show the totals for the current filters; the map and bars show where sales come from.", "Kartu KPI menampilkan total untuk filter saat ini; peta dan bar menunjukkan asal penjualan.")),
        (T("Narrow down", "Persempit"), T("Pick values in the filter bar, or click a bar or bubble. Press Reset to clear everything.", "Pilih nilai di filter bar, atau klik bar atau bubble. Tekan Reset untuk menghapus semua filter.")),
        (T("Compare regions", "Bandingkan wilayah"), T("Open Summary and click a province to see its cities side by side.", "Buka Summary lalu klik provinsi untuk melihat kota-kotanya berdampingan.")),
        (T("Find specific rows", "Cari baris tertentu"), T("Open Detail, search by city, company or cluster, and click a column header to sort.", "Buka Detail, cari berdasarkan kota, perusahaan, atau cluster, lalu klik judul kolom untuk mengurutkan.")),
    ]) + '<p style="margin-top:12px;color:var(--muted)">' + s(T(
        "Tip: tabs can be linked directly, e.g. <code>…/#summary</code> or <code>…/#detail</code>.",
        "Tips: tab bisa dibuka langsung lewat link, misalnya <code>…/#summary</code> atau <code>…/#detail</code>.")) + "</p>"))

    parts.append(section("run", T("Run locally", "Jalankan lokal"),
        "<p>" + s(T("The page loads <code>data.json</code> with <code>fetch</code>, so serve the folder over HTTP rather than opening the file directly:",
                    "Halaman memuat <code>data.json</code> dengan <code>fetch</code>, jadi jalankan folder lewat HTTP, jangan buka file-nya langsung:")) + "</p>"
        + '<pre class="cmd">git clone ' + REPO + '.git\ncd PowerBI-SalesReport-Dashboard\npython3 -m http.server 8000\n# ' + s(T("open", "buka")) + ' http://localhost:8000</pre>'
        + "<p>" + s(T("To rebuild this documentation after editing the text:", "Untuk membangun ulang dokumentasi ini setelah mengubah teks:")) + "</p>"
        + '<pre class="cmd">python3 -I docs/_source/build_docs.py</pre>'))

    parts.append(section("notes", T("Limitations & notes", "Keterbatasan & catatan"), '<ul class="clean">' + "".join(
        f"<li>{s(x)}</li>" for x in [
            T("Figures are anonymized and must not be read as real business results.", "Angka sudah dianonimkan dan tidak boleh dibaca sebagai hasil bisnis yang sebenarnya."),
            T("The Cancellations metric counts ZC01/ZC02 order lines. It mirrors, but may not exactly match, the original Power BI measure <code>Cancellation Province</code>.", "Metrik Cancellations menghitung baris order ZC01/ZC02. Metrik ini meniru, tetapi bisa saja tidak persis sama dengan, measure Power BI asli <code>Cancellation Province</code>."),
            T("The date filter works by year (Power BI used a date-range slicer).", "Filter tanggal bekerja per tahun (Power BI memakai slicer rentang tanggal)."),
            T("Drill-through is replaced by click-to-filter plus the Detail tab.", "Drill-through diganti dengan klik-untuk-filter ditambah tab Detail."),
            T("Map bubbles use standard city-centre coordinates, because the source coordinates pointed to a single project location.", "Bubble di peta memakai koordinat pusat kota standar, karena koordinat di data sumber hanya menunjuk satu lokasi proyek."),
            T("The original .pbix and source data are kept in a separate private repository.", "File .pbix dan data sumber asli disimpan di repository privat terpisah."),
        ]) + "</ul>"))
    return "".join(parts)


def page():
    css = (SRC / "style.css").read_text(encoding="utf-8")
    other_href, other_name, other_lang = OTHER[LANG]
    toc = "".join(f'<a href="#{i}">{s(t)}</a>' for i, t in TOC)
    return f"""<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sales Report Dashboard</title>
<meta name="description" content="{s(T('Documentation for an interactive sales report dashboard, rebuilt from Power BI for the web with anonymized data.', 'Dokumentasi dashboard laporan penjualan interaktif, dibangun ulang dari Power BI untuk web dengan data yang dianonimkan.'))}">
<style>
{css}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="eyebrow">{s(T('Project Documentation', 'Dokumentasi Proyek'))}</div>
  <h1>Sales Report Dashboard</h1>
  <p>{s(T('An interactive property sales report built in Power BI and rebuilt for the web with ECharts and Leaflet', 'Laporan penjualan properti interaktif yang dibuat di Power BI dan dibangun ulang untuk web dengan ECharts dan Leaflet'))}</p>
  <div class="meta">{s(T('Version 1.0 · November 2026 · Portfolio project · Anonymized data', 'Versi 1.0 · November 2026 · Proyek portofolio · Data dianonimkan'))}</div>
</div></header>
<nav class="toc" aria-label="{s(T('Contents', 'Daftar isi'))}"><div class="wrap">
{toc}
<span class="spacer"></span>
  <a class="tgl" href="{other_href}" hreflang="{other_lang}">{other_name}</a>
  <button class="tgl" id="present" title="{s(T('One section per screen (F = full screen)', 'Satu bagian per layar (F = layar penuh)'))}">{s(T('Presentation mode', 'Mode presentasi'))}</button>
  <button class="tgl" id="theme">{s(T('Theme', 'Tema'))}</button>
</div></nav>
<main class="wrap">
{body()}
</main>
<footer><div class="wrap">Sales Report Dashboard · <a href="{REPO}">GitHub</a> · <a href="{DEMO}">{s(T('Live demo', 'Demo live'))}</a> · <a href="https://diimasogan.github.io/#projects">Portfolio</a></div></footer>
<script>
(function(){{var r=document.documentElement,k='doc-theme';
function set(t){{if(t)r.setAttribute('data-theme',t);else r.removeAttribute('data-theme');try{{localStorage.setItem(k,t)}}catch(e){{}}}}
try{{var t=localStorage.getItem(k);if(t)r.setAttribute('data-theme',t)}}catch(e){{}}
document.getElementById('theme').onclick=function(){{var c=r.getAttribute('data-theme');set(c==='dark'?'light':c==='light'?'':'dark')}};
document.getElementById('present').onclick=function(){{document.body.classList.toggle('present')}};
document.addEventListener('keydown',function(e){{if(e.key==='f'&&document.body.classList.contains('present')){{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen()}}}});
}})();
</script>
</body>
</html>
"""


def main():
    global LANG
    for LANG in ("en", "id"):
        OUT[LANG].parent.mkdir(parents=True, exist_ok=True)
        OUT[LANG].write_text(page(), encoding="utf-8")
        print("wrote", OUT[LANG].relative_to(ROOT))
    (ROOT / "docs" / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=SalesReport-Documentation.html">\n'
        '<title>Sales Report Dashboard documentation</title></head><body><a href="SalesReport-Documentation.html">English</a> · '
        '<a href="id/SalesReport-Dokumentasi.html">Bahasa Indonesia</a></body></html>\n', encoding="utf-8")


if __name__ == "__main__":
    main()
