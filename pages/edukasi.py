from pathlib import Path

import streamlit as st

from utils.theme import inject_css, sidebar_brand, navbar, hero, info_card, section_title

# ------------------------------------------------------------
# Tema (sama dengan halaman lain)
# ------------------------------------------------------------
inject_css()

with st.sidebar:
    sidebar_brand(active="Edukasi Keuangan Syariah")

navbar(active="Edukasi")

HALAMAN_INPUT = "pages/input_user.py"

# ============================================================
#  >>>>>>>>>>  TEMPAT MENGISI VIDEO  <<<<<<<<<<
#
#  Tiap video punya DUA tempat yang perlu diisi:
#
#  1. "file_video"   -> path file video di dalam repositori.
#                       Contoh: "assets/video/edukasi_1.mp4"
#                       Simpan filenya di folder assets/video/.
#                       Biarkan "" kalau videonya hanya ada di YouTube.
#
#  2. "link_youtube" -> tautan lengkap video di YouTube.
#                       Contoh: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
#                       Dipakai untuk tombol "Buka di YouTube",
#                       dan jadi pemutar cadangan kalau file_video kosong.
#
#  Urutan yang dipakai halaman ini:
#     file_video ada  -> putar dari file
#     file_video kosong tapi link_youtube ada -> putar dari YouTube
#     dua-duanya kosong -> tampil bingkai contoh + keterangan
# ============================================================
VIDEO = [
    {
        "id": "v1",
        "judul": "Kenapa Uang Saku Selalu Habis Sebelum Akhir Bulan?",
        "kategori": "Dasar Keuangan",
        "durasi": "6:42",
        "pemateri": "Tim GI BEI Vokasi ITS",
        "ringkasan": (
            "Membedah kebiasaan belanja harian yang tidak terasa tapi menggerus uang saku, "
            "lalu cara sederhana melacaknya lewat pencatatan."
        ),
        "poin": [
            "Beda antara kebutuhan, keinginan, dan kebiasaan",
            "Efek jajan kecil yang berulang setiap hari",
            "Langkah pertama mencatat tanpa ribet",
        ],
        # ↓↓↓ ISI DI SINI ↓↓↓
        "file_video": "",     # contoh: "assets/video/edukasi_1.mp4"
        "link_youtube": "",   # contoh: "https://www.youtube.com/watch?v=xxxxxxxxxxx"
        # ↑↑↑ ISI DI SINI ↑↑↑
    },
    {
        "id": "v2",
        "judul": "Bagi Uang Sakumu: Aturan 50/30/20 untuk Anak Sekolah",
        "kategori": "Prinsip Syariah",
        "durasi": "8:15",
        "pemateri": "Tim GI BEI Vokasi ITS",
        "ringkasan": (
            "Cara membagi uang saku ke pos kebutuhan, keinginan, dan tabungan, "
            "serta menempatkan sedekah sebelum pembagian dilakukan."
        ),
        "poin": [
            "Asal-usul aturan 50/30/20",
            "Menyesuaikan porsi saat uang saku pas-pasan",
            "Mendahulukan sedekah dari pemasukan",
        ],
        # ↓↓↓ ISI DI SINI ↓↓↓
        "file_video": "",     # contoh: "assets/video/edukasi_2.mp4"
        "link_youtube": "",   # contoh: "https://www.youtube.com/watch?v=xxxxxxxxxxx"
        # ↑↑↑ ISI DI SINI ↑↑↑
    },
]

WARNA_KATEGORI = {"Dasar Keuangan": "#14532D", "Prinsip Syariah": "#1B6B45"}
WARNA_DEFAULT = "#2E8B5A"

AKAR_PROYEK = Path(__file__).resolve().parent.parent


def warna(video) -> str:
    return WARNA_KATEGORI.get(video["kategori"], WARNA_DEFAULT)


def path_video(video):
    """Kembalikan path file video kalau ada dan benar-benar ditemukan."""
    if not video.get("file_video"):
        return None
    for kandidat in (AKAR_PROYEK / video["file_video"], Path(video["file_video"])):
        if kandidat.exists():
            return kandidat
    return None


def sumber_video(video):
    """('file', path) | ('youtube', url) | (None, None)"""
    berkas = path_video(video)
    if berkas:
        return "file", berkas
    if video.get("link_youtube"):
        return "youtube", video["link_youtube"]
    return None, None


# ------------------------------------------------------------
# State
# ------------------------------------------------------------
if "edu_terpilih" not in st.session_state:
    st.session_state.edu_terpilih = None
if "edu_ditonton" not in st.session_state:
    st.session_state.edu_ditonton = []


def buka_video(video_id: str):
    st.session_state.edu_terpilih = video_id


def kembali_ke_daftar():
    st.session_state.edu_terpilih = None


# ------------------------------------------------------------
# Sampul video — digambar dengan SVG, tanpa file gambar
# ------------------------------------------------------------
def sampul(video, tinggi: int = 190) -> str:
    return (
        f'<svg viewBox="0 0 400 225" style="width:100%;height:{tinggi}px;display:block;border-radius:12px" '
        f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Sampul video {video["judul"]}">'
        f'<defs><linearGradient id="grad-{video["id"]}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{warna(video)}"/><stop offset="100%" stop-color="#0B3A26"/>'
        "</linearGradient></defs>"
        f'<rect width="400" height="225" fill="url(#grad-{video["id"]})"/>'
        '<circle cx="342" cy="46" r="58" fill="#FFFFFF" opacity="0.05"/>'
        '<circle cx="58" cy="196" r="42" fill="#FFFFFF" opacity="0.05"/>'
        '<path d="M356 34a17 17 0 1 0 13 27 21 21 0 1 1-13-27z" fill="#F2C94C" opacity="0.85"/>'
        '<circle cx="200" cy="112" r="36" fill="#FFFFFF" opacity="0.18"/>'
        '<circle cx="200" cy="112" r="35" fill="none" stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="2"/>'
        '<path d="M190 95 L219 112 L190 129 Z" fill="#FFFFFF"/>'
        '<rect x="16" y="188" width="86" height="24" rx="12" fill="#0B3A26" opacity="0.55"/>'
        '<text x="59" y="204" fill="#FFFFFF" font-size="13" font-weight="600" '
        f'font-family="Poppins, sans-serif" text-anchor="middle">{video["durasi"]}</text>'
        "</svg>"
    )


def lencana(teks: str, bg: str = "#14532D") -> str:
    return (
        f'<span style="display:inline-block;background:{bg};color:#FFFFFF;font-size:11.5px;'
        f'font-weight:600;padding:4px 11px;border-radius:999px">{teks}</span>'
    )


terpilih = next((v for v in VIDEO if v["id"] == st.session_state.edu_terpilih), None)

# ============================================================
# TAMPILAN DETAIL
# ============================================================
if terpilih:
    st.button("← Kembali ke daftar video", on_click=kembali_ke_daftar, key="kembali_atas")

    st.markdown(
        '<div style="margin:14px 0 12px">'
        + lencana(terpilih["kategori"], warna(terpilih))
        + f'<div style="font-size:26px;font-weight:700;color:#0B3A26;line-height:1.25;margin:12px 0 6px">{terpilih["judul"]}</div>'
        + f'<div style="font-size:13px;color:#6B7C74">{terpilih["pemateri"]} · {terpilih["durasi"]} menit</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    jenis, sumber = sumber_video(terpilih)

    if jenis == "file":
        st.video(str(sumber))
    elif jenis == "youtube":
        st.video(sumber)
    else:
        # Belum ada video: tampilkan bingkai contoh supaya halaman tetap rapi.
        st.markdown(sampul(terpilih, tinggi=340), unsafe_allow_html=True)
        st.caption(
            "Video belum tersedia. Isi `file_video` atau `link_youtube` pada daftar VIDEO "
            "di bagian atas file `edukasi.py`, lalu pemutarnya akan muncul di sini."
        )

    st.write("")

    aksi = st.columns([1.5, 1.5, 2])
    with aksi[0]:
        if terpilih.get("link_youtube"):
            st.link_button("▶ Buka di YouTube", terpilih["link_youtube"])
        else:
            st.button("▶ Buka di YouTube", disabled=True, key="yt_kosong",
                      help="Tautan YouTube belum diisi pada daftar VIDEO.")
    with aksi[1]:
        sudah = terpilih["id"] in st.session_state.edu_ditonton
        if sudah:
            if st.button("✓ Sudah ditonton", key="batal_tonton"):
                st.session_state.edu_ditonton.remove(terpilih["id"])
                st.rerun()
        else:
            if st.button("Tandai sudah ditonton", key="tandai_tonton"):
                st.session_state.edu_ditonton.append(terpilih["id"])
                st.rerun()

    st.write("")
    with st.container(border=True):
        st.markdown(
            '<div style="font-size:17px;font-weight:600;color:#0B3A26;margin-bottom:8px">Ringkasan</div>'
            f'<div style="font-size:15px;line-height:1.65;color:#1F2A24">{terpilih["ringkasan"]}</div>'
            '<div style="font-size:17px;font-weight:600;color:#0B3A26;margin:18px 0 8px">Yang akan kamu pelajari</div>'
            + "".join(
                '<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px">'
                '<span style="color:#C99A2E;font-weight:700">•</span>'
                f'<span style="font-size:15px;line-height:1.6;color:#1F2A24">{p}</span></div>'
                for p in terpilih["poin"]
            ),
            unsafe_allow_html=True,
        )

    urutan = [v["id"] for v in VIDEO]
    posisi = urutan.index(terpilih["id"])

    st.write("")
    nav_kiri, nav_tengah, nav_kanan = st.columns([2, 1, 2])
    with nav_kiri:
        if posisi > 0:
            st.button("← Video sebelumnya", on_click=buka_video,
                      args=(VIDEO[posisi - 1]["id"],), key="video_sebelumnya")
    with nav_tengah:
        st.markdown(
            f'<div style="text-align:center;font-size:13px;color:#6B7C74;padding-top:8px">'
            f"Video {posisi + 1} dari {len(VIDEO)}</div>",
            unsafe_allow_html=True,
        )
    with nav_kanan:
        if posisi < len(VIDEO) - 1:
            st.button("Video berikutnya →", on_click=buka_video,
                      args=(VIDEO[posisi + 1]["id"],), key="video_berikutnya")

    st.divider()
    st.button("← Kembali ke daftar video", on_click=kembali_ke_daftar, key="kembali_bawah")

# ============================================================
# TAMPILAN DAFTAR
# ============================================================
else:
    hero(
        eyebrow="Edukasi Keuangan Syariah",
        title="Belajar Mengelola Uang, Sedikit Demi Sedikit",
        lead=(
            "Video singkat tentang mengatur uang saku dan membaginya sesuai prinsip syariah. "
            "Tonton dulu, lalu langsung praktikkan di halaman pencatatan."
        ),
        chips=[f"{len(VIDEO)} video", "Rata-rata 7 menit", "Gratis"],
    )

    selesai = len(st.session_state.edu_ditonton)
    with st.container(border=True):
        st.markdown(
            '<div style="font-size:15px;font-weight:600;color:#0B3A26">Progres belajarmu</div>'
            f'<div style="font-size:13px;color:#6B7C74;margin-top:2px">{selesai} dari {len(VIDEO)} video sudah ditandai selesai</div>',
            unsafe_allow_html=True,
        )
        st.progress(selesai / len(VIDEO))
        if selesai == len(VIDEO):
            st.caption("Semua video sudah kamu tonton. Saatnya praktik di halaman pencatatan.")

    st.write("")
    section_title("Daftar Video")

    kolom = st.columns(2, gap="medium")
    for kartu, video in zip(kolom, VIDEO):
        with kartu:
            with st.container(border=True):
                st.markdown(sampul(video), unsafe_allow_html=True)
                sudah = video["id"] in st.session_state.edu_ditonton
                jenis, _ = sumber_video(video)
                penanda = "" if jenis else "&nbsp;" + lencana("Belum ada video", "#6B7C74")
                st.markdown(
                    '<div style="margin-top:12px">'
                    + lencana(video["kategori"], warna(video))
                    + ("&nbsp;" + lencana("✓ Selesai", "#1B6B45") if sudah else "")
                    + penanda
                    + f'<div style="font-size:16px;font-weight:600;color:#0B3A26;line-height:1.4;margin:10px 0 6px;min-height:46px">{video["judul"]}</div>'
                    + f'<div style="font-size:13.5px;line-height:1.6;color:#6B7C74;min-height:66px">{video["ringkasan"]}</div>'
                    + f'<div style="font-size:12px;color:#6B7C74;margin-top:8px">{video["pemateri"]} · {video["durasi"]} menit</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.button("▶ Tonton", key=f"tonton_{video['id']}",
                          on_click=buka_video, args=(video["id"],))

    st.write("")
    info_card(
        "🎯",
        "Sudah menonton? Langsung praktikkan",
        "Ilmu keuangan baru terasa manfaatnya kalau dipakai. Catat uang sakumu bulan ini "
        "dan bagi ke pos-pos alokasi sesuai yang kamu pelajari.",
    )
    st.page_link(HALAMAN_INPUT, label="Buka Halaman Pencatatan", icon="📝")