import streamlit as st
from supabase_client import supabase
from utils.theme import inject_css, sidebar_brand, navbar, hero, alloc_card, section_title
from utils.auth import require_login, sidebar_user

# ------------------------------------------------------------
# Tema + gerbang login
# require_login() menghentikan halaman selama siswa belum masuk,
# sekaligus menyediakan identitas yang dipakai saat menyimpan data.
# ------------------------------------------------------------
inject_css()

siswa = require_login()

with st.sidebar:
    sidebar_brand(active="Pencatatan Keuangan")
    sidebar_user()

navbar(active="Input")

# ------------------------------------------------------------
# Kategori alokasi
# Kunci dict HARUS sama persis dengan nama kolom di tabel user_data.
# ------------------------------------------------------------
KATEGORI_ALOKASI = {
    "kebutuhan_pribadi": ("Kebutuhan Pribadi", "Sabun, alat tulis, pulsa, kuota, dan keperluan diri sendiri."),
    "urunan": ("Urunan", "Patungan kelas, kado, iuran kegiatan, atau hadiah bersama teman."),
    "konsumsi": ("Konsumsi", "Makan, minum, dan jajan sehari-hari."),
    "investment": ("Investment", "Tabungan, dana darurat, emas, atau reksa dana syariah."),
    "lain-lain": ("Lain-lain", "Pengeluaran di luar empat pos di atas — wajib diberi keterangan."),
}
KATEGORI_KOLOM = list(KATEGORI_ALOKASI.keys())

KOLOM_LAIN = "lain-lain"          # kolom yang butuh keterangan
KOLOM_KETERANGAN = "keterangan"   # kolom teks penjelasan "Lain-lain"

# Kolom identitas pemilik catatan di tabel user_data
KOLOM_NIS_SISWA = "nis_siswa"
KOLOM_USERNAME = "username"
NIS_BERTIPE_ANGKA = True          # kolom nis_siswa bertipe int8

HALAMAN_DASHBOARD = "pages/dashboard.py"  # sesuaikan jika letak file berbeda

# ------------------------------------------------------------
# Identitas siswa yang sedang masuk — ikut disimpan di setiap catatan
# ------------------------------------------------------------
NIS_SISWA = str(siswa.get("nis", "")).strip()
USERNAME_SISWA = str(siswa.get("username", "")).strip()


def nis_nilai():
    """Samakan tipe NIS dengan kolom di database."""
    if NIS_BERTIPE_ANGKA and NIS_SISWA.isdigit():
        return int(NIS_SISWA)
    return NIS_SISWA


# Hanya untuk ditampilkan sebagai contoh teori — tidak dipakai saat menyimpan
CONTOH_PEMBAGIAN = [
    (50, "Kebutuhan", "Kebutuhan pribadi, konsumsi harian, dan urunan yang sudah pasti."),
    (30, "Keinginan", "Jajan tambahan, hobi, hiburan, dan hal yang bisa ditunda."),
    (20, "Tabungan & Investasi", "Dana darurat, tabungan tujuan, emas, atau reksa dana syariah."),
]

# ------------------------------------------------------------
# Banner judul + prakata
# ------------------------------------------------------------
hero(
    eyebrow="Pencatatan Keuangan",
    title="Catat Pemasukan, Lalu Bagi Sesuai Porsinya",
    lead=(
        "Uang yang tercatat jauh lebih mudah dikendalikan. Isi dulu berapa pemasukanmu, "
        "lalu bagi ke lima pos alokasi. Hanya dua langkah, dan catatanmu langsung tersimpan."
    ),
    chips=["2 langkah pengisian", "Tersimpan otomatis", "Sesuai prinsip syariah"],
)

# ------------------------------------------------------------
# Contoh pembagian berdasarkan aturan 50/30/20
# ------------------------------------------------------------
section_title("Contoh pembagian: aturan 50/30/20")
st.caption(
    "Aturan 50/30/20 dipopulerkan Elizabeth Warren dalam buku *All Your Worth* — "
    "separuh pemasukan untuk kebutuhan, sepertiganya untuk keinginan, sisanya disimpan. "
    "Pakai sebagai patokan awal, lalu sesuaikan dengan kondisimu. "
    "Sisihkan sedekah atau infak lebih dulu sebelum membagi ke pos-pos ini."
)

kolom_contoh = st.columns(3, gap="medium")
for kolom, (pct, nama, desc) in zip(kolom_contoh, CONTOH_PEMBAGIAN):
    with kolom:
        alloc_card(pct, nama, desc)

st.divider()

# Catatan: kolom "date" TIDAK diisi dari kode ini — dibiarkan kosong
# supaya Postgres otomatis mengisi dengan default now().


# ------------------------------------------------------------
# State management untuk alur 2 langkah
# ------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 1
if "pemasukan_data" not in st.session_state:
    st.session_state.pemasukan_data = {}


def reset_flow():
    st.session_state.step = 1
    st.session_state.pemasukan_data = {}
    for kat in KATEGORI_KOLOM:
        st.session_state.pop(f"alokasi_{kat}", None)
    st.session_state.pop("keterangan_lain", None)


# ------------------------------------------------------------
# Pesan sukses + tombol lanjut ke Dashboard (muncul setelah menyimpan)
# ------------------------------------------------------------
if st.session_state.get("baru_disimpan"):
    st.success("Pemasukan & alokasi berhasil disimpan!")
    if st.button("📊 Lanjut ke Dashboard"):
        st.session_state.baru_disimpan = False
        st.switch_page(HALAMAN_DASHBOARD)

st.caption(f"Langkah {st.session_state.step} dari 2")
st.progress(st.session_state.step / 2)

# ============================================================
# LANGKAH 1 — Input Pemasukan
# ============================================================
if st.session_state.step == 1:
    section_title("Masukkan Pemasukan Kamu", num="1")

    with st.form("form_pemasukan"):
        jumlah = st.number_input(
            "Jumlah Pemasukan (Rp)",
            min_value=0,
            step=1000,
            value=st.session_state.pemasukan_data.get("money", 0),
        )

        lanjut = st.form_submit_button("Lanjut ke Alokasi →")

        if lanjut:
            if jumlah <= 0:
                st.warning("Jumlah harus lebih dari 0.")
            else:
                st.session_state.pemasukan_data = {"money": jumlah}
                st.session_state.step = 2
                st.session_state.baru_disimpan = False
                st.rerun()

# ============================================================
# LANGKAH 2 — Alokasi Pemasukan ke Kategori
# ============================================================
elif st.session_state.step == 2:
    data = st.session_state.pemasukan_data
    total = data["money"]

    section_title("Alokasikan Pemasukan Kamu", num="2")
    st.info(f"Total pemasukan yang akan dialokasikan: **Rp {total:,.0f}**")

    with st.form("form_alokasi"):
        alokasi_input = {}
        for kat in KATEGORI_KOLOM:
            label, bantuan = KATEGORI_ALOKASI[kat]
            alokasi_input[kat] = st.number_input(
                f"{label} (Rp)",
                min_value=0,
                step=1000,
                key=f"alokasi_{kat}",
                help=bantuan,
            )

        keterangan = st.text_input(
            "Keterangan Lain-lain",
            key="keterangan_lain",
            placeholder="Contoh: beli kado ulang tahun teman, servis sepeda",
            help="Wajib diisi kalau pos Lain-lain lebih dari 0.",
        )

        total_alokasi = sum(alokasi_input.values())
        sisa = total - total_alokasi

        if sisa < 0:
            st.error(f"Alokasi melebihi pemasukan sebesar Rp {abs(sisa):,.0f}")
        elif sisa > 0:
            st.warning(f"Masih ada sisa belum dialokasikan: Rp {sisa:,.0f}")
        else:
            st.success("Alokasi sudah pas dengan total pemasukan ✅")

        col_back, col_save = st.columns(2)
        kembali = col_back.form_submit_button("← Kembali / Edit Pemasukan")
        simpan = col_save.form_submit_button("💾 Simpan Semua")

        if kembali:
            st.session_state.step = 1
            st.rerun()

        if simpan:
            if total_alokasi != total:
                st.error("Total alokasi harus sama persis dengan total pemasukan sebelum disimpan.")
            elif alokasi_input[KOLOM_LAIN] > 0 and not keterangan.strip():
                st.error("Isi dulu keterangan untuk pos Lain-lain sebelum menyimpan.")
            elif not NIS_SISWA:
                st.error("Identitas siswa tidak terbaca. Coba keluar lalu masuk kembali.")
            else:
                try:
                    # Gabungkan identitas + pemasukan + alokasi jadi SATU baris.
                    # Kolom "date" sengaja TIDAK disertakan -> diisi now() oleh Supabase.
                    row = {
                        KOLOM_NIS_SISWA: nis_nilai(),
                        KOLOM_USERNAME: USERNAME_SISWA,
                        "money": data["money"],
                    }
                    row.update(alokasi_input)
                    row[KOLOM_KETERANGAN] = (
                        keterangan.strip() if alokasi_input[KOLOM_LAIN] > 0 else ""
                    )

                    supabase.table("user_data").insert(row).execute()

                    reset_flow()
                    st.session_state.baru_disimpan = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menyimpan data: {e}")

    if st.button("🔄 Mulai Ulang dari Awal"):
        reset_flow()
        st.rerun()

# ============================================================
# Kelola Data — hanya catatan milik siswa yang sedang masuk
# ============================================================
st.divider()
section_title("Kelola Data")
st.caption(f"Catatan atas nama {USERNAME_SISWA} · NIS {NIS_SISWA}")

try:
    response = (
        supabase.table("user_data")
        .select("*")
        .eq(KOLOM_NIS_SISWA, nis_nilai())
        .order("date", desc=True)
        .execute()
    )
    data_list = response.data

    if data_list:
        for row in data_list:
            col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
            col1.write(row.get("date", ""))
            col2.write(f"Rp {row['money']:,.0f}")
            col3.write(row.get(KOLOM_KETERANGAN, "") or "")
            if col4.button("🗑️", key=f"del_{row['id_input']}"):
                (
                    supabase.table("user_data")
                    .delete()
                    .eq("id_input", row["id_input"])
                    .eq(KOLOM_NIS_SISWA, nis_nilai())
                    .execute()
                )
                st.rerun()
    else:
        st.info("Belum ada data.")
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")