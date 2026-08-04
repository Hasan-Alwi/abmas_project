"""
utils/auth.py
Autentikasi Dashboard Keuangan Syariah — SMA Integral Ar-Rohmah, Malang.

Akun dibaca dari tabel Supabase `user_account` (kolom: nis, username).
Kolom lain seperti `password` diabaikan.

Cara pakai di setiap halaman (home.py dan semua file di pages/):

    import streamlit as st
    from utils.theme import inject_css, sidebar_brand, navbar
    from utils.auth import require_login, sidebar_user

    inject_css()
    siswa = require_login()          # berhenti di sini kalau belum masuk
    with st.sidebar:
        sidebar_brand(active="Beranda")
        sidebar_user()
    navbar(active="Beranda")
"""

import streamlit as st

from supabase_client import supabase
from utils.theme import inject_css

# ----------------------------------------------------------------------------
# PENGATURAN — sesuaikan bila nama tabel / kolom berbeda
# ----------------------------------------------------------------------------
TABEL_AKUN = "user_account"

KOLOM_NIS = "nis"
KOLOM_USERNAME = "username"

# NIS di tabel bertipe angka (int8), jadi nilai teks dari form dikonversi dulu.
NIS_BERTIPE_ANGKA = True


# ----------------------------------------------------------------------------
# GAYA HALAMAN MASUK
# ----------------------------------------------------------------------------
_CSS_LOGIN = """
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { padding-top: 3rem; max-width: 1100px; }

.auth-card {
  border-radius: 20px; padding: 34px 34px 28px; color: #F5FBF8; text-align: center;
  background:
    radial-gradient(120% 140% at 88% -10%, rgba(242,201,76,.28), transparent 46%),
    linear-gradient(135deg, var(--green-900) 0%, var(--green-700) 58%, var(--green-500) 130%);
  box-shadow: 0 18px 40px -24px rgba(11,58,38,.65);
}
.auth-card .ayat { font-family: 'Amiri', 'Traditional Arabic', serif; font-size: 1.4rem;
                   color: var(--gold-400); margin-bottom: 12px; }
.auth-card h2 { font-size: 1.34rem; font-weight: 700; margin: 0 0 6px; color: #FFFFFF; }
.auth-card p  { font-size: .88rem; color: #DCEFE7; margin: 0; }

.auth-judul { font-size: 1.05rem; font-weight: 700; color: var(--green-900);
              margin-bottom: 2px; text-align: center; }
.auth-sub   { font-size: .84rem; color: var(--muted); margin-bottom: 12px; text-align: center; }
.auth-nota  { text-align: center; font-size: .86rem; color: var(--muted); margin: 16px 0 4px; }
.auth-nota a, [data-testid="stMarkdownContainer"] .auth-nota a {
  color: var(--green-700) !important; font-weight: 700; text-decoration: none !important;
  border-bottom: 1.5px solid var(--green-200);
}
.auth-nota a:hover { border-bottom-color: var(--green-600); }

/* semua tombol di halaman ini diletakkan di tengah */
div[data-testid="stForm"] { margin-top: 14px; }
div[data-testid="stFormSubmitButton"], .stButton { display: flex; justify-content: center; }
div[data-testid="stFormSubmitButton"] button, .stButton > button { min-width: 190px; }
.stButton > button[kind="secondary"] {
  background: transparent !important; color: var(--green-700) !important;
  border: 1px solid var(--green-200) !important; font-weight: 600;
}
.stButton > button[kind="secondary"]:hover {
  background: var(--green-50) !important; color: var(--green-700) !important;
}

.sb-user {
  display: flex; gap: 10px; align-items: center;
  background: rgba(255,255,255,.10); border-radius: 12px;
  padding: 12px 14px; margin-bottom: 10px; font-size: 13.5px;
}
.sb-user__ikon { font-size: 20px; }
.sb-user__nama { font-weight: 600; }
.sb-user__ket  { opacity: .75; font-size: 12px; }
"""


def _suntik_css_login() -> None:
    """Baris kosong dibuang agar blok <style> tidak terputus parser Markdown."""
    css = "\n".join(b for b in _CSS_LOGIN.splitlines() if b.strip())
    st.markdown("<style>" + css + "</style>", unsafe_allow_html=True)


def _kepala_login() -> None:
    st.markdown(
        '<div class="auth-card">'
        '<div class="ayat">وَأَنفِقُوا۟ فِى سَبِيلِ ٱللَّهِ</div>'
        "<h2>Dashboard Keuangan Syariah</h2>"
        "<p>SMA Integral Ar-Rohmah · Malang</p>"
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# AKSES DATABASE
# ----------------------------------------------------------------------------
def _nilai_nis(nis: str):
    """Samakan tipe dengan kolom di database."""
    nis = str(nis).strip()
    if NIS_BERTIPE_ANGKA and nis.isdigit():
        return int(nis)
    return nis


def _cari_akun(kolom: str, nilai):
    hasil = supabase.table(TABEL_AKUN).select("*").eq(kolom, nilai).limit(1).execute()
    return hasil.data[0] if hasil.data else None


def _tabel_terbaca() -> bool:
    """Deteksi RLS: True bila minimal satu baris bisa dibaca kunci anon."""
    try:
        return bool(supabase.table(TABEL_AKUN).select(KOLOM_NIS).limit(1).execute().data)
    except Exception:
        return False


def _cek_masuk(username: str, nis: str):
    """Cocokkan username & NIS. Username tidak peka huruf besar/kecil."""
    akun = _cari_akun(KOLOM_NIS, _nilai_nis(nis))
    if not akun:
        return None
    tersimpan = str(akun.get(KOLOM_USERNAME, "")).strip().lower()
    return akun if tersimpan == username.strip().lower() else None


def _buat_akun(username: str, nis: str) -> None:
    supabase.table(TABEL_AKUN).insert(
        {KOLOM_NIS: _nilai_nis(nis), KOLOM_USERNAME: username.strip()}
    ).execute()


def _simpan_sesi(akun: dict) -> None:
    st.session_state.auth_masuk = True
    st.session_state.auth_user = {
        "nis": str(akun.get(KOLOM_NIS, "")),
        "username": str(akun.get(KOLOM_USERNAME, "")),
        "nama": str(akun.get(KOLOM_USERNAME, "")),
    }


def _ke_mode(mode: str) -> None:
    st.query_params["mode"] = mode


# ----------------------------------------------------------------------------
# FORM MASUK & DAFTAR
# ----------------------------------------------------------------------------
def _form_masuk() -> None:
    st.markdown(
        '<div class="auth-judul">Masuk ke Dashboard</div>'
        '<div class="auth-sub">Gunakan Username dan NIS yang terdaftar di sekolah.</div>',
        unsafe_allow_html=True,
    )

    with st.form("form_masuk"):
        username = st.text_input("Username", placeholder="Contoh: Fulan bin Abdullah")
        nis = st.text_input("NIS", placeholder="Contoh: 1")
        masuk = st.form_submit_button("Masuk")

    if masuk:
        if not username.strip() or not nis.strip():
            st.warning("Username dan NIS harus diisi.")
        else:
            try:
                akun = _cek_masuk(username, nis)
            except Exception as e:
                st.error(f"Gagal menghubungi database: {e}")
                akun = None
            else:
                if akun:
                    _simpan_sesi(akun)
                    st.rerun()
                elif not _tabel_terbaca():
                    st.error(
                        f"Tabel **{TABEL_AKUN}** tidak bisa dibaca. Kemungkinan besar RLS "
                        "aktif tanpa policy SELECT. Jalankan perintah SQL yang ada di "
                        "catatan bawah halaman ini."
                    )
                else:
                    st.error("Username atau NIS belum cocok. Periksa kembali penulisannya.")

    st.markdown(
        '<div class="auth-nota">Belum punya akun? '
        '<a href="?mode=daftar" target="_self">Daftar di sini</a></div>',
        unsafe_allow_html=True,
    )


def _form_daftar() -> None:
    st.markdown(
        '<div class="auth-judul">Daftar Akun Baru</div>'
        '<div class="auth-sub">Cukup isi Username dan NIS. Keduanya dipakai untuk masuk.</div>',
        unsafe_allow_html=True,
    )

    with st.form("form_daftar"):
        username = st.text_input("Username", placeholder="Pilih nama pengguna, tanpa spasi")
        nis = st.text_input("NIS", placeholder="Nomor Induk Siswa")
        daftar = st.form_submit_button("Daftar Sekarang")

    if daftar:
        username, nis = username.strip(), nis.strip()

        if not username or not nis:
            st.warning("Username dan NIS wajib diisi.")
        elif " " in username:
            st.warning("Username tidak boleh mengandung spasi.")
        elif NIS_BERTIPE_ANGKA and not nis.isdigit():
            st.warning("NIS hanya boleh berisi angka.")
        else:
            try:
                if _cari_akun(KOLOM_NIS, _nilai_nis(nis)):
                    st.error("NIS ini sudah terdaftar. Silakan masuk memakai akun tersebut.")
                elif _cari_akun(KOLOM_USERNAME, username):
                    st.error("Username ini sudah dipakai. Coba nama pengguna lain.")
                else:
                    _buat_akun(username, nis)
                    st.success("Akun berhasil dibuat. Silakan masuk dengan Username dan NIS tadi.")
            except Exception as e:
                st.error(f"Gagal mendaftarkan akun: {e}")

    st.markdown(
        '<div class="auth-nota">Sudah punya akun? '
        '<a href="?mode=masuk" target="_self">Masuk di sini</a></div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# API UTAMA
# ----------------------------------------------------------------------------
def require_login() -> dict:
    """Tampilkan halaman masuk bila belum login. Kembalikan data siswa aktif."""
    if st.session_state.get("auth_masuk"):
        return st.session_state.get("auth_user", {})

    inject_css()
    _suntik_css_login()

    mode = st.query_params.get("mode", "masuk")

    _kiri, tengah, _kanan = st.columns([1, 1.3, 1])
    with tengah:
        _kepala_login()
        if mode == "daftar":
            _form_daftar()
        else:
            _form_masuk()

    st.stop()


def user_aktif() -> dict:
    """Data siswa yang sedang masuk: username, nis."""
    return st.session_state.get("auth_user", {})


def keluar() -> None:
    for kunci in ("auth_masuk", "auth_user"):
        st.session_state.pop(kunci, None)
    st.query_params.clear()
    st.rerun()


def sidebar_user() -> None:
    """Kartu identitas + tombol keluar. Panggil di dalam `with st.sidebar:`."""
    u = user_aktif()
    st.markdown(
        '<div class="sb-user"><div class="sb-user__ikon">👤</div><div>'
        f'<div class="sb-user__nama">{u.get("username", "")}</div>'
        f'<div class="sb-user__ket">NIS {u.get("nis", "")}</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )
    if st.button("Keluar", key="tombol_keluar"):
        keluar()