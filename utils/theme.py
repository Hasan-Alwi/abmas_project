"""
Tema visual dashboard "Keuangan Syariah" — SMA Integral Ar-Rohmah, Malang.

Pakai di setiap halaman:

    import streamlit as st
    from utils.theme import inject_css, sidebar_brand, navbar, hero

    inject_css()
    with st.sidebar:
        sidebar_brand(active="Beranda")
    navbar(active="Beranda")

CATATAN PENTING
Semua HTML yang dikirim ke st.markdown() harus bebas baris kosong. Streamlit
memakai parser Markdown, dan baris kosong menutup blok HTML lebih awal sehingga
sisanya tampil sebagai teks mentah. inject_css() sudah membuang baris kosong
secara otomatis, jadi CSS di bawah boleh ditulis rapi.
"""

import streamlit as st

# ---------------------------------------------------------------- tokens ----
COLORS = {
    "green_900": "#0B3A26",
    "green_800": "#0E4A33",
    "green_700": "#14532D",
    "green_600": "#1B6B45",
    "green_500": "#2E8B5A",
    "green_400": "#5DB187",
    "green_300": "#8FCDAE",
    "green_200": "#C9E2D4",
    "green_100": "#E8F3EC",
    "green_50": "#F4F9F6",
    "gold_500": "#C99A2E",
    "gold_400": "#F2C94C",
    "orange": "#E08A3C",
    "brown": "#A97C3F",
    "ink": "#1F2A24",
    "muted": "#6B7C74",
    "border": "#E3EAE6",
    "surface": "#FFFFFF",
}

# Urutan warna untuk grafik (kontras cukup untuk teks putih di atasnya)
PALETTE = ["#14532D", "#1B6B45", "#2E8B5A", "#C99A2E", "#A97C3F", "#E08A3C", "#5DB187"]

FONT = "Poppins"

# (label, ikon, path file halaman relatif terhadap file entrypoint)
# Sesuaikan path bila struktur folder berbeda.
NAV_ITEMS = [
    ("Beranda", "🏠", "home.py"),
    ("Input", "🟨", "pages/input_user.py"),
    ("Dashboard", "📊", "pages/dashboard.py"),
    ("Budget Example", "🎯", "pages/budget_example.py"),
    ("Edukasi", "📖", "pages/edukasi.py"),
]

SIDEBAR_MENU = [
    ("Beranda", "🏠"),
    ("Pencatatan Keuangan", "🟨"),
    ("Perencanaan Anggaran", "📊"),
    ("Tujuan Keuangan", "🎯"),
    ("Edukasi Keuangan Syariah", "📖"),
    ("Laporan & Visualisasi", "📈"),
]

# ------------------------------------------------------------------- css ----
_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --green-900:#0B3A26; --green-800:#0E4A33; --green-700:#14532D;
  --green-600:#1B6B45; --green-500:#2E8B5A; --green-200:#C9E2D4;
  --green-100:#E8F3EC; --green-50:#F4F9F6;  --gold-400:#F2C94C; --gold-500:#C99A2E;
  --ink:#1F2A24; --muted:#6B7C74; --border:#E3EAE6; --surface:#FFFFFF;
  --danger:#C0483C;
  --font:"Poppins","Plus Jakarta Sans","Segoe UI",system-ui,sans-serif;
}

html, body, [class*="css"], .stApp { font-family: var(--font); color: var(--ink); }
.stApp { background: var(--surface); }
.block-container { max-width: 1040px; padding-top: 1.6rem; }

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] { background: var(--green-800); }
section[data-testid="stSidebar"] * { color: #FFFFFF; }
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
  border-radius: 9px; padding: 6px 12px; font-size: 14px;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
  background: rgba(255,255,255,.10);
}
.ks-brand { padding: 14px 4px 4px; border-top: 1px solid rgba(255,255,255,.14); margin-top: 12px; }
.ks-brand__name { color: var(--gold-400); font-size: 15px; font-weight: 700; }
.ks-brand__sub { color: rgba(255,255,255,.65); font-size: 11.5px; margin-top: 2px; }
.ks-menu { margin-top: 14px; }
.ks-menu__item {
  display: flex; gap: 10px; align-items: center;
  padding: 9px 12px; margin-bottom: 8px; border-radius: 9px;
  font-size: 14px; color: rgba(255,255,255,.88);
}
.ks-menu__item--active { background: var(--green-600); color: #fff; font-weight: 600; }

/* ---------- navbar ---------- */
.ks-nav__brand { color: var(--green-700); font-weight: 700; font-size: 15px;
                 white-space: nowrap; padding-top: 7px; }
.ks-nav__tab--active {
  display: inline-flex; gap: 6px; align-items: center; white-space: nowrap;
  background: var(--green-700); color: #FFFFFF; font-weight: 600;
  padding: 8px 14px; border-radius: 999px; font-size: 13.5px;
}
/* tab non-aktif = st.page_link, dinavigasi router Streamlit (sesi tidak hilang) */
a[data-testid="stPageLink-NavLink"] {
  border-radius: 999px !important; padding: 8px 14px !important;
  justify-content: center; white-space: nowrap;
}
a[data-testid="stPageLink-NavLink"] p {
  font-size: 13.5px !important; font-weight: 500 !important; color: var(--muted) !important;
  margin: 0 !important;
}
a[data-testid="stPageLink-NavLink"]:hover { background: var(--green-50) !important; }
a[data-testid="stPageLink-NavLink"]:hover p { color: var(--green-700) !important; }
.ks-navbox div[data-testid="stHorizontalBlock"] { gap: 4px; align-items: center; }

/* ---------- hero ---------- */
.ks-hero {
  background: linear-gradient(135deg, var(--green-700) 0%, var(--green-600) 100%);
  border-radius: 18px; padding: 42px 46px; margin-bottom: 18px; color: #fff;
}
.ks-hero__eyebrow {
  display: flex; align-items: center; gap: 14px;
  font-size: 12px; font-weight: 600; letter-spacing: .16em; text-transform: uppercase;
  color: rgba(255,255,255,.92); margin-bottom: 18px;
}
.ks-hero__eyebrow::before { content: ""; width: 28px; height: 3px; background: var(--gold-400); }
.ks-hero__title { font-size: 40px; line-height: 1.18; font-weight: 700; margin: 0 0 18px; color: #fff; }
.ks-hero__lead { font-size: 16.5px; line-height: 1.65; color: rgba(255,255,255,.82); max-width: 66ch; margin: 0 0 26px; }
.ks-chips { display: flex; gap: 12px; flex-wrap: wrap; }
.ks-chip { background: rgba(255,255,255,.12); color: #fff; font-size: 12.5px; font-weight: 600; padding: 8px 16px; border-radius: 999px; }

/* ---------- kartu alokasi (dipakai di dalam st.columns) ---------- */
.ks-alloc {
  background: linear-gradient(135deg, var(--green-700) 0%, var(--green-600) 100%);
  border-radius: 14px; padding: 22px 20px; color: #fff; min-height: 196px;
}
.ks-alloc__pct { font-size: 34px; font-weight: 700; color: var(--gold-400); line-height: 1; }
.ks-alloc__bar { height: 4px; border-radius: 999px; background: rgba(255,255,255,.18); margin: 12px 0 14px; overflow: hidden; }
.ks-alloc__bar > span { display: block; height: 100%; background: var(--gold-400); }
.ks-alloc__name { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.ks-alloc__desc { font-size: 13px; line-height: 1.55; color: rgba(255,255,255,.78); }

/* ---------- kartu metrik ---------- */
.ks-metric {
  background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
  padding: 18px 20px; min-height: 132px;
}
.ks-metric--highlight { border-left: 4px solid var(--gold-400); }
.ks-metric__top { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; }
.ks-metric__label { font-size: 13px; color: var(--muted); font-weight: 500; }
.ks-metric__icon {
  width: 34px; height: 34px; border-radius: 10px; background: var(--green-100);
  display: inline-flex; align-items: center; justify-content: center; font-size: 16px; flex: none;
}
.ks-metric__value { font-size: 25px; font-weight: 700; color: var(--green-900); margin: 14px 0 6px; line-height: 1.1; }
.ks-metric__sub { font-size: 12px; font-weight: 600; color: var(--muted); }
.ks-metric__sub--up { color: var(--green-600); }
.ks-metric__sub--down { color: var(--danger); }

/* ---------- panel / kartu isi ---------- */
.ks-panel__title { font-size: 17px; font-weight: 600; color: var(--green-900); }
.ks-panel__sub { font-size: 13px; color: var(--muted); margin-top: 4px; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 14px; }

/* ---------- kartu info ---------- */
.ks-card {
  display: flex; gap: 14px; align-items: flex-start;
  background: var(--green-100); border: 1px solid var(--green-200);
  border-radius: 14px; padding: 20px 24px; margin-bottom: 18px;
}
.ks-card__icon { font-size: 22px; line-height: 1.2; }
.ks-card__title { color: var(--green-700); font-size: 17px; font-weight: 600; margin-bottom: 4px; }
.ks-card__body { color: var(--green-600); font-size: 15px; line-height: 1.6; }

/* ---------- judul seksi ---------- */
.ks-section {
  display: flex; align-items: center; gap: 10px;
  font-size: 20px; font-weight: 700; color: var(--green-900); margin: 26px 0 12px;
}
.ks-section__num {
  width: 26px; height: 26px; border-radius: 8px; background: var(--green-700); color: #fff;
  font-size: 13px; font-weight: 600; display: inline-flex; align-items: center;
  justify-content: center; flex: none;
}
.ks-step { font-size: 12.5px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }

/* ---------- widget Streamlit ---------- */
.stButton > button, .stFormSubmitButton > button, .stLinkButton > a {
  background: var(--green-700); color: #fff !important; border: none; border-radius: 999px;
  padding: 8px 20px; font-weight: 600; font-size: 14px; text-decoration: none !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stLinkButton > a:hover { background: var(--green-600); color: #fff !important; }
.stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible { outline: 2px solid var(--gold-400); outline-offset: 2px; }
div[data-testid="stForm"] { border: 1px solid var(--border); border-radius: 14px; padding: 22px 24px; background: var(--surface); }
div[data-testid="stProgress"] > div > div > div > div { background: var(--green-600); }
span[data-baseweb="tag"] { background-color: var(--green-700) !important; border-radius: 999px !important; font-weight: 500 !important; }
div[data-testid="stMetricValue"] { color: var(--green-900); font-weight: 700; }

@media (max-width: 640px) {
  .ks-hero { padding: 28px 22px; }
  .ks-hero__title { font-size: 28px; }
  .ks-alloc { min-height: auto; }
  .ks-metric { min-height: auto; }
}

@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""


def inject_css() -> None:
    """Suntikkan CSS tema. Baris kosong dibuang agar blok HTML tidak terputus."""
    css = "\n".join(line for line in _CSS.splitlines() if line.strip())
    st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)


# ------------------------------------------------------------ components ----
def sidebar_brand(active: str = "Beranda") -> None:
    items = "".join(
        '<div class="ks-menu__item'
        + (" ks-menu__item--active" if label == active else "")
        + '"><span>' + icon + "</span><span>" + label + "</span></div>"
        for label, icon in SIDEBAR_MENU
    )
    st.markdown(
        '<div class="ks-brand">'
        '<div class="ks-brand__name">🌙 Keuangan Syariah</div>'
        '<div class="ks-brand__sub">SMA Integral Ar-Rohmah · Malang</div>'
        "</div>"
        '<div class="ks-menu">' + items + "</div>",
        unsafe_allow_html=True,
    )


def navbar(active: str = "Beranda") -> None:
    """Navigasi utama.

    Memakai st.page_link, bukan tag <a>, supaya perpindahan halaman ditangani
    router Streamlit. Tautan <a> biasa memuat ulang browser sehingga
    st.session_state (termasuk status login) ikut terhapus.
    """
    st.markdown('<div class="ks-navbox">', unsafe_allow_html=True)
    with st.container(border=True):
        lebar = [2.1] + [len(label) * 0.13 + 0.62 for label, _, _ in NAV_ITEMS]
        kolom = st.columns(lebar, vertical_alignment="center")

        kolom[0].markdown(
            '<span class="ks-nav__brand">🌙 Keuangan Syariah</span>', unsafe_allow_html=True
        )
        for kotak, (label, ikon, path) in zip(kolom[1:], NAV_ITEMS):
            with kotak:
                if label == active:
                    st.markdown(
                        '<span class="ks-nav__tab--active">' + ikon + " " + label + "</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.page_link(path, label=label, icon=ikon)
    st.markdown("</div>", unsafe_allow_html=True)


def hero(eyebrow: str, title: str, lead: str, chips=None) -> None:
    chip_html = ""
    if chips:
        chip_html = (
            '<div class="ks-chips">'
            + "".join('<span class="ks-chip">' + c + "</span>" for c in chips)
            + "</div>"
        )
    st.markdown(
        '<div class="ks-hero">'
        '<div class="ks-hero__eyebrow">' + eyebrow + "</div>"
        '<div class="ks-hero__title">' + title + "</div>"
        '<div class="ks-hero__lead">' + lead + "</div>" + chip_html + "</div>",
        unsafe_allow_html=True,
    )


def alloc_card(pct: int, name: str, desc: str) -> None:
    """Kartu hijau berisi persentase alokasi — dipakai di dalam st.columns()."""
    st.markdown(
        '<div class="ks-alloc">'
        '<div class="ks-alloc__pct">' + str(pct) + "%</div>"
        '<div class="ks-alloc__bar"><span style="width:' + str(pct) + '%"></span></div>'
        '<div class="ks-alloc__name">' + name + "</div>"
        '<div class="ks-alloc__desc">' + desc + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, sub: str = "", icon: str = "",
                tone: str = "neutral", highlight: bool = False) -> None:
    """Kartu angka ringkas. tone: 'neutral' | 'up' | 'down'."""
    icon_html = '<span class="ks-metric__icon">' + icon + "</span>" if icon else ""
    sub_cls = "ks-metric__sub"
    if tone in ("up", "down"):
        sub_cls += " ks-metric__sub--" + tone
    sub_html = '<div class="' + sub_cls + '">' + sub + "</div>" if sub else ""
    st.markdown(
        '<div class="ks-metric' + (" ks-metric--highlight" if highlight else "") + '">'
        '<div class="ks-metric__top"><span class="ks-metric__label">' + label + "</span>"
        + icon_html + "</div>"
        '<div class="ks-metric__value">' + value + "</div>" + sub_html + "</div>",
        unsafe_allow_html=True,
    )


def panel_header(title: str, subtitle: str = "") -> None:
    sub = '<div class="ks-panel__sub">' + subtitle + "</div>" if subtitle else ""
    st.markdown('<div class="ks-panel__title">' + title + "</div>" + sub, unsafe_allow_html=True)


def section_title(text: str, num: str = None) -> None:
    badge = '<span class="ks-section__num">' + num + "</span>" if num else ""
    st.markdown('<div class="ks-section">' + badge + text + "</div>", unsafe_allow_html=True)


def info_card(icon: str, title: str, body: str) -> None:
    st.markdown(
        '<div class="ks-card"><div class="ks-card__icon">' + icon + "</div>"
        '<div><div class="ks-card__title">' + title + "</div>"
        '<div class="ks-card__body">' + body + "</div></div></div>",
        unsafe_allow_html=True,
    )