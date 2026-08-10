import base64
import re
from pathlib import Path

import streamlit as st

from utils.theme import inject_css, sidebar_brand, navbar, hero, info_card, section_title
from utils.auth import require_login, sidebar_user

# ------------------------------------------------------------
# Tema + gerbang login
# ------------------------------------------------------------
inject_css()

siswa = require_login()

with st.sidebar:
    sidebar_brand(active="Edukasi Keuangan Syariah")
    sidebar_user()

navbar(active="Edukasi")

HALAMAN_INPUT = "pages/input_user.py"

# Folder akar proyek. File ini ada di pages/, jadi naik satu tingkat.
AKAR_PROYEK = Path(__file__).resolve().parent.parent


# ============================================================
#  >>>>>>>>>>  TEMPAT MENGISI BERKAS PANDUAN  <<<<<<<<<<
#
#  Tulis path PDF relatif terhadap folder akar proyek.
# ============================================================
PANDUAN = {
    "judul": "Panduan Penggunaan Dashboard Keuangan Syariah",
    "keterangan": (
        "Panduan lengkap cara memakai website ini, mulai dari mendaftar akun, "
        "mencatat pemasukan, membagi ke lima pos alokasi, sampai membaca grafik "
        "pada halaman Dashboard."
    ),
    "penerbit": "Kelompok Studi Pasar Modal Vokasi ITS",

    # ↓↓↓ ISI DI SINI — path file PDF ↓↓↓
    "file_pdf": "data/Panduan Dashboard.pdf",
    # ↑↑↑ ISI DI SINI ↑↑↑
}


# ============================================================
#  >>>>>>>>>>  TEMPAT MENGISI VIDEO  <<<<<<<<<<
#
#  Cukup satu yang perlu diisi: tautan YouTube.
#  Bentuk tautan apa pun bisa dipakai:
#      https://youtu.be/xxxxxxxxxxx
#      https://www.youtube.com/watch?v=xxxxxxxxxxx
#      https://www.youtube.com/shorts/xxxxxxxxxxx
#
#  Thumbnail diambil otomatis dari YouTube berdasarkan tautan tersebut,
#  jadi tidak perlu menyiapkan gambar sampul sendiri.
# ============================================================
VIDEO = {
    "id": "v1",
    "judul": "Budgeting",
    "kategori": "Dasar Keuangan",
    "durasi": "3:45",
    "pemateri": "Bu Dini Safitri",
    "ringkasan": "Alasan kenapa kita harus mulai melakukan budgeting.",

    # ↓↓↓ ISI DI SINI — tautan YouTube ↓↓↓
    "link_youtube": "https://youtu.be/_uII1cb4MbY",
    # ↑↑↑ ISI DI SINI ↑↑↑
}

WARNA_KATEGORI = {"Dasar Keuangan": "#14532D", "Prinsip Syariah": "#1B6B45"}
WARNA_DEFAULT = "#2E8B5A"


# ------------------------------------------------------------
# Pembantu
# ------------------------------------------------------------
def kandidat_path(path_relatif: str):
    """Daftar lokasi yang dicoba saat mencari berkas."""
    nama = Path(path_relatif).name
    return [
        AKAR_PROYEK / path_relatif,
        Path(__file__).resolve().parent / path_relatif,
        Path.cwd() / path_relatif,
        AKAR_PROYEK / "data" / nama,
        AKAR_PROYEK / "assets" / nama,
        AKAR_PROYEK / nama,
    ]


def cari_berkas(path_relatif: str):
    if not path_relatif:
        return None
    for kandidat in kandidat_path(path_relatif):
        if kandidat.is_file():
            return kandidat
    return None


def id_youtube(tautan: str) -> str:
    """Ambil ID video dari berbagai bentuk tautan YouTube."""
    if not tautan:
        return ""
    pola = [
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"[?&]v=([A-Za-z0-9_-]{11})",
        r"/embed/([A-Za-z0-9_-]{11})",
        r"/shorts/([A-Za-z0-9_-]{11})",
    ]
    for p in pola:
        cocok = re.search(p, tautan)
        if cocok:
            return cocok.group(1)
    return ""


def thumbnail_youtube(tautan: str) -> str:
    """Alamat gambar sampul dari YouTube. hqdefault selalu tersedia."""
    vid = id_youtube(tautan)
    return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else ""


def warna(video) -> str:
    return WARNA_KATEGORI.get(video["kategori"], WARNA_DEFAULT)


def lencana(teks: str, bg: str = "#14532D") -> str:
    return (
        f'<span style="display:inline-block;background:{bg};color:#FFFFFF;font-size:11.5px;'
        f'font-weight:600;padding:4px 11px;border-radius:999px">{teks}</span>'
    )


def sampul(video, tinggi: int = 280) -> str:
    """Bingkai pengganti bila tautan YouTube belum diisi."""
    return (
        f'<svg viewBox="0 0 400 225" style="width:100%;height:{tinggi}px;display:block;'
        'border-radius:12px" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Sampul video {video["judul"]}">'
        f'<defs><linearGradient id="grad-{video["id"]}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{warna(video)}"/><stop offset="100%" stop-color="#0B3A26"/>'
        "</linearGradient></defs>"
        f'<rect width="400" height="225" fill="url(#grad-{video["id"]})"/>'
        '<circle cx="342" cy="46" r="58" fill="#FFFFFF" opacity="0.05"/>'
        '<circle cx="58" cy="196" r="42" fill="#FFFFFF" opacity="0.05"/>'
        '<path d="M356 34a17 17 0 1 0 13 27 21 21 0 1 1-13-27z" fill="#F2C94C" opacity="0.85"/>'
        '<circle cx="200" cy="112" r="36" fill="#FFFFFF" opacity="0.18"/>'
        '<circle cx="200" cy="112" r="35" fill="none" stroke="#FFFFFF" '
        'stroke-opacity="0.5" stroke-width="2"/>'
        '<path d="M190 95 L219 112 L190 129 Z" fill="#FFFFFF"/>'
        '<rect x="16" y="188" width="86" height="24" rx="12" fill="#0B3A26" opacity="0.55"/>'
        '<text x="59" y="204" fill="#FFFFFF" font-size="13" font-weight="600" '
        f'font-family="Poppins, sans-serif" text-anchor="middle">{video["durasi"]}</text>'
        "</svg>"
    )


# ------------------------------------------------------------
# Banner
# ------------------------------------------------------------
hero(
    eyebrow="Edukasi Keuangan Syariah",
    title="Belajar Mengelola Uang, Sedikit Demi Sedikit",
    lead=(
        "Dua bekal untukmu di halaman ini: panduan lengkap cara memakai website, "
        "dan video singkat tentang mengatur uang saku sesuai prinsip syariah."
    ),
    chips=["1 buku panduan", "1 video", "Gratis diunduh"],
)

# ============================================================
# BAGIAN 1 — PANDUAN PENGGUNAAN (PDF)
# ============================================================
section_title("Panduan Penggunaan Website", num="1")

berkas_panduan = cari_berkas(PANDUAN["file_pdf"])

with st.container(border=True):
    st.markdown(
        '<div style="display:flex;gap:16px;align-items:flex-start">'
        '<div style="width:46px;height:46px;border-radius:12px;background:#E8F3EC;'
        'display:inline-flex;align-items:center;justify-content:center;font-size:22px;'
        'flex:none">📕</div><div>'
        f'<div style="font-size:17px;font-weight:600;color:#0B3A26;margin-bottom:4px">{PANDUAN["judul"]}</div>'
        f'<div style="font-size:14px;line-height:1.6;color:#6B7C74">{PANDUAN["keterangan"]}</div>'
        f'<div style="font-size:12px;color:#6B7C74;margin-top:8px">{PANDUAN["penerbit"]}</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )

    if berkas_panduan:
        isi_pdf = berkas_panduan.read_bytes()
        ukuran_mb = len(isi_pdf) / 1_048_576

        st.write("")
        st.download_button(
            "⬇️ Unduh Panduan (PDF)",
            data=isi_pdf,
            file_name=berkas_panduan.name,
            mime="application/pdf",
        )
        st.caption(f"Ukuran berkas {ukuran_mb:.1f} MB")

        if ukuran_mb <= 8:
            with st.expander("Baca langsung di halaman ini"):
                b64 = base64.b64encode(isi_pdf).decode()
                st.markdown(
                    f'<iframe src="data:application/pdf;base64,{b64}" width="100%" '
                    'height="620" style="border:1px solid #E3EAE6;border-radius:12px">'
                    "</iframe>",
                    unsafe_allow_html=True,
                )
                st.caption(
                    "Bila pratinjau tidak muncul di telepon genggam, "
                    "gunakan tombol unduh di atas."
                )
        else:
            st.caption("Berkas terlalu besar untuk dipratinjau. Silakan diunduh saja.")
    else:
        st.write("")
        st.warning(f"Berkas panduan belum ditemukan pada `{PANDUAN['file_pdf']}`.")
        with st.expander("Lokasi yang sudah dicoba"):
            st.code("\n".join(str(p) for p in kandidat_path(PANDUAN["file_pdf"])))
            st.caption(
                "Pastikan nama file sama persis, termasuk huruf besar-kecilnya, "
                "dan folder data/ tidak tercantum di .gitignore."
            )

st.write("")

# ============================================================
# BAGIAN 2 — VIDEO EDUKASI (YouTube)
# ============================================================
section_title("Video Edukasi Keuangan", num="2")
st.caption(
    "Tekan gambar sampulnya untuk menonton langsung di halaman ini, "
    "atau buka di YouTube lewat tombol di sebelahnya."
)

if "edu_putar" not in st.session_state:
    st.session_state.edu_putar = False

tautan = VIDEO.get("link_youtube", "")
gambar_sampul = thumbnail_youtube(tautan)

with st.container(border=True):
    st.markdown(
        '<div style="margin-bottom:12px">'
        + lencana(VIDEO["kategori"], warna(VIDEO))
        + ("" if tautan else "&nbsp;" + lencana("Belum ada video", "#6B7C74"))
        + f'<div style="font-size:18px;font-weight:600;color:#0B3A26;line-height:1.35;'
        f'margin:10px 0 4px">{VIDEO["judul"]}</div>'
        f'<div style="font-size:12.5px;color:#6B7C74">{VIDEO["pemateri"]} · {VIDEO["durasi"]} menit</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    if not tautan:
        st.markdown(sampul(VIDEO), unsafe_allow_html=True)
        st.caption(
            "Video belum tersedia. Isi `link_youtube` pada bagian VIDEO "
            "di atas file `edukasi.py`."
        )
    elif st.session_state.edu_putar:
        st.video(tautan)
    else:
        if gambar_sampul:
            st.image(gambar_sampul, use_container_width=True)
        else:
            st.markdown(sampul(VIDEO), unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:14.5px;line-height:1.65;color:#1F2A24;margin:12px 0 8px">'
        f'{VIDEO["ringkasan"]}</div>',
        unsafe_allow_html=True,
    )

    if tautan:
        tombol_kiri, tombol_kanan, _sisa = st.columns([1.6, 1.6, 2])
        with tombol_kiri:
            if st.session_state.edu_putar:
                if st.button("✕ Tutup pemutar", key="tutup_video"):
                    st.session_state.edu_putar = False
                    st.rerun()
            else:
                if st.button("▶ Tonton di sini", key="putar_video"):
                    st.session_state.edu_putar = True
                    st.rerun()
        with tombol_kanan:
            st.link_button("↗ Buka di YouTube", tautan)
    else:
        st.button(
            "↗ Buka di YouTube",
            disabled=True,
            key="yt_kosong",
            help="Tautan YouTube belum diisi pada bagian VIDEO.",
        )

st.write("")

# ------------------------------------------------------------
# Ajakan praktik
# ------------------------------------------------------------
info_card(
    "🎯",
    "Sudah belajar? Langsung praktikkan",
    "Ilmu keuangan baru terasa manfaatnya kalau dipakai. Catat uang sakumu bulan ini "
    "dan bagi ke pos-pos alokasi sesuai yang kamu pelajari.",
)
st.page_link(HALAMAN_INPUT, label="Buka Halaman Pencatatan", icon="📝")