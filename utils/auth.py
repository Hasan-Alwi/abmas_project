"""
utils/auth.py
Autentikasi Dashboard Keuangan Syariah — SMA Integral Ar-Rohmah, Malang.

Login memakai:
    NIS       -> berperan sebagai "username" di streamlit-authenticator
    Username  -> berperan sebagai "password"

Akun dibaca langsung dari file CSV. Tidak perlu file hashed_pw.pkl:
password di-hash otomatis di memori (bcrypt) dan hasilnya di-cache,
jadi hashing hanya berjalan ulang saat isi CSV berubah.

Cara pakai di setiap halaman (home.py dan semua file di pages/):

    from utils.css import load_css
    from utils.auth import require_login

    st.set_page_config(...)
    load_css()
    authenticator = require_login()      # berhenti di sini kalau belum login
"""

from pathlib import Path
import csv

import bcrypt
import streamlit as st
import streamlit_authenticator as stauth

# ----------------------------------------------------------------------------
# PENGATURAN — ubah bagian ini bila nama kolom / lokasi file berbeda
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent

NAMA_FILE_CSV = "Abmas SMA Ar-Rohman.csv"

# Folder yang akan dicari berurutan sampai file CSV ketemu.
FOLDER_CSV = ["data", "document", "assets", "assets/data", "."]

COL_NIS = "NIS"            # wajib — dipakai sebagai identitas login
COL_USERNAME = "Username"  # wajib — dipakai sebagai kata sandi
COL_NAMA = "Nama"          # opsional — untuk sapaan di sidebar
COL_KELAS = "Kelas"        # opsional — untuk keterangan di sidebar

COOKIE_NAME = "arrohmah_keuangan"
COOKIE_EXPIRY_DAYS = 1

try:
    COOKIE_KEY = st.secrets["auth"]["cookie_key"]
except Exception:
    COOKIE_KEY = "arrohmah_dev_key_ganti_saat_produksi"

print("AUTH FILE =", __file__)
print("COOKIE_KEY =", COOKIE_KEY)

FIELDS = {
    "Form name": "Masuk ke Dashboard",
    "Username": "NIS",
    "Password": "Username",
    "Login": "Masuk",
}


# ----------------------------------------------------------------------------
# PEMBACAAN CSV
# ----------------------------------------------------------------------------
def _cari_csv() -> Path:
    for folder in FOLDER_CSV:
        kandidat = (ROOT / folder / NAMA_FILE_CSV).resolve()
        if kandidat.is_file():
            return kandidat
    dicari = "\n".join(f"• {(ROOT / f / NAMA_FILE_CSV)}" for f in FOLDER_CSV)
    st.error(
        f"File akun **{NAMA_FILE_CSV}** tidak ditemukan.\n\n"
        f"Letakkan file tersebut di salah satu lokasi berikut:\n\n{dicari}"
    )
    st.stop()


def _ambil(baris: dict, kolom: str):
    """Ambil nilai kolom tanpa peduli huruf besar/kecil dan spasi berlebih."""
    for k, v in baris.items():
        if k and k.strip().lower() == kolom.strip().lower():
            return v
    return None


@st.cache_data(show_spinner=False)
def _baca_baris(path_csv: str, _cap_waktu: float):
    with open(path_csv, newline="", encoding="utf-8-sig") as f:
        contoh = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel
        pembaca = csv.DictReader(f, dialect=dialect)
        return [dict(r) for r in pembaca], list(pembaca.fieldnames or [])


@st.cache_data(show_spinner="Menyiapkan data akun…")
def _bangun_kredensial(path_csv: str, _cap_waktu: float):
    baris, kolom_tersedia = _baca_baris(path_csv, _cap_waktu)

    if not baris:
        return {"usernames": {}}, {}, kolom_tersedia

    contoh = baris[0]
    if _ambil(contoh, COL_NIS) is None or _ambil(contoh, COL_USERNAME) is None:
        return None, None, kolom_tersedia

    kredensial = {"usernames": {}}
    profil = {}

    for b in baris:
        nis = str(_ambil(b, COL_NIS) or "").strip()
        username = str(_ambil(b, COL_USERNAME) or "").strip()
        if not nis or not username or nis in kredensial["usernames"]:
            continue

        nama = str(_ambil(b, COL_NAMA) or username).strip()
        kelas = str(_ambil(b, COL_KELAS) or "").strip()

        kredensial["usernames"][nis] = {
            "name": nama,
            "email": f"{nis}@arrohmah.sch.id",
            "password": bcrypt.hashpw(username.encode(), bcrypt.gensalt()).decode(),
        }
        profil[nis] = {"nama": nama, "kelas": kelas, "nis": nis}

    return kredensial, profil, kolom_tersedia


# ----------------------------------------------------------------------------
# AUTHENTICATOR
# ----------------------------------------------------------------------------
def get_authenticator():
    path_csv = _cari_csv()
    kredensial, profil, kolom = _bangun_kredensial(str(path_csv), path_csv.stat().st_mtime)

    if kredensial is None:
        st.error(
            f"Kolom **{COL_NIS}** dan/atau **{COL_USERNAME}** tidak ada di {NAMA_FILE_CSV}.\n\n"
            f"Kolom yang terbaca: {', '.join(kolom) if kolom else '(kosong)'}\n\n"
            "Sesuaikan konstanta `COL_NIS` dan `COL_USERNAME` di `utils/auth.py`."
        )
        st.stop()

    if not kredensial["usernames"]:
        st.error(f"Tidak ada baris akun yang valid di {NAMA_FILE_CSV}.")
        st.stop()

    st.session_state["_profil_siswa"] = profil

    try:  # streamlit-authenticator >= 0.3.2
        return stauth.Authenticate(
            kredensial, COOKIE_NAME, COOKIE_KEY, COOKIE_EXPIRY_DAYS, auto_hash=False
        )
    except TypeError:  # versi lama
        return stauth.Authenticate(kredensial, COOKIE_NAME, COOKIE_KEY, COOKIE_EXPIRY_DAYS)


# ----------------------------------------------------------------------------
# TAMPILAN HALAMAN MASUK
# ----------------------------------------------------------------------------
_CSS_LOGIN = """
<style>
  section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"]{ display:none; }
  .block-container{ padding-top:3.2rem; max-width:1180px; }

  .login-card{ border-radius:22px; padding:34px 34px 26px; color:#F5FBF8; overflow:hidden;
    position:relative; text-align:center;
    background:
      radial-gradient(120% 140% at 88% -10%, rgba(201,162,39,.30), transparent 46%),
      linear-gradient(135deg, var(--green-900) 0%, var(--green-700) 58%, var(--green-500) 130%);
    box-shadow:0 18px 40px -22px rgba(11,79,62,.65); }
  .login-card .ar{ font-family:'Amiri', serif; font-size:1.35rem; color:var(--gold-soft); margin-bottom:10px; }
  .login-card h2{ font-size:1.32rem; font-weight:800; margin:0 0 6px; letter-spacing:-.02em; }
  .login-card p{ font-size:.88rem; color:#DCEFE7; margin:0; }

  /* form bawaan streamlit-authenticator */
  [data-testid="stForm"]{ background:var(--card); border:1px solid var(--line);
    border-radius:18px; padding:22px 24px 8px; margin-top:-14px;
    box-shadow:0 16px 34px -26px rgba(11,79,62,.6); }
  [data-testid="stForm"] h1, [data-testid="stForm"] h2, [data-testid="stForm"] h3{
    font-size:1rem !important; font-weight:700 !important; color:var(--green-900) !important;
    margin:0 0 10px !important; }
  [data-testid="stForm"] label p{ font-size:.82rem !important; font-weight:600; color:var(--muted); }
  [data-testid="stForm"] input{ border-radius:10px !important; }
  [data-testid="stForm"] button{ width:100%; border-radius:999px !important; font-weight:700 !important;
    border:none !important; color:#F5FBF8 !important;
    background:linear-gradient(135deg,var(--green-900),var(--green-700)) !important; }

  .login-note{ text-align:center; font-size:.8rem; color:var(--muted); margin-top:14px; }
  .login-note b{ color:var(--green-900); }
</style>
"""


def _kepala_login():
    st.markdown(_CSS_LOGIN, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="login-card">
          <div class="ar">وَأَنفِقُوا۟ فِى سَبِيلِ ٱللَّهِ</div>
          <h2>Dashboard Keuangan Syariah</h2>
          <p>SMA Integral Ar-Rohmah · Malang</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def require_login():
    """Tampilkan halaman masuk bila belum login. Kembalikan objek authenticator."""
    authenticator = get_authenticator()

    if st.session_state.get("authentication_status"):
        return authenticator

    _kiri, tengah, _kanan = st.columns([1, 1.25, 1])
    with tengah:
        # Diisi belakangan: bila cookie masih berlaku, form tidak perlu muncul.
        slot_kepala = st.empty()

        try:  # streamlit-authenticator >= 0.4
            authenticator.login(location="main", fields=FIELDS)
        except TypeError:  # versi lama
            authenticator.login("Masuk ke Dashboard", "main")

        status = st.session_state.get("authentication_status")
        if not status:
            with slot_kepala:
                _kepala_login()

        if status is False:
            st.error("NIS atau Username belum cocok. Periksa kembali penulisannya.")
        elif status is None:
            st.markdown(
                '<div class="login-note">Masuk memakai <b>NIS</b> dan '
                '<b>Username</b> yang terdaftar di sekolah.</div>',
                unsafe_allow_html=True,
            )

    if not st.session_state.get("authentication_status"):
        st.stop()

    return authenticator


def user_aktif() -> dict:
    """Data siswa yang sedang login: nama, nis, kelas."""
    nis = st.session_state.get("username", "")
    profil = st.session_state.get("_profil_siswa", {})
    return profil.get(nis, {"nama": st.session_state.get("name", ""), "nis": nis, "kelas": ""})


def sidebar_user(authenticator):
    """Kartu identitas + tombol keluar di sidebar."""
    u = user_aktif()
    keterangan = f"Kelas {u['kelas']}" if u.get("kelas") else f"NIS {u.get('nis', '')}"
    st.sidebar.markdown(
        f"""
        <div class="sb-user">
          <div>👤</div>
          <div><b>{u.get('nama', '')}</b><br>
          <span style="opacity:.75">{keterangan}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    authenticator.logout("Keluar", location="sidebar")
