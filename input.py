import streamlit as st
from supabase_client import supabase

KATEGORI_KOLOM = ["alocation_1", "alocation_2", "investment"]

st.title("📝 Input Keuangan")

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


st.caption(f"Langkah {st.session_state.step} dari 2")
st.progress(st.session_state.step / 2)

# ============================================================
# LANGKAH 1 — Input Pemasukan
# ============================================================
if st.session_state.step == 1:
    st.subheader("1️⃣ Masukkan Pemasukan Kamu")

    with st.form("form_pemasukan"):
        jumlah = st.number_input(
            "Jumlah Pemasukan (Rp)",
            min_value=0,
            step=1000,
            value=st.session_state.pemasukan_data.get("money", 0),
        )
        # sumber = st.text_input(
        #     "Sumber (misal: uang saku, gaji part-time, bonus)",
        #     value=st.session_state.pemasukan_data.get("sumber", ""),
        # )
        # catatan = st.text_area(
        #     "Catatan (opsional)",
        #     value=st.session_state.pemasukan_data.get("catatan", ""),
        # )

        lanjut = st.form_submit_button("Lanjut ke Alokasi →")

        if lanjut:
            if jumlah <= 0:
                st.warning("Jumlah harus lebih dari 0.")
            else:
                st.session_state.pemasukan_data = {
                    "money": jumlah,
                    # "sumber": sumber,
                    # "catatan": catatan,
                }
                st.session_state.step = 2
                st.rerun()

# ============================================================
# LANGKAH 2 — Alokasi Pemasukan ke Kategori
# ============================================================
elif st.session_state.step == 2:
    data = st.session_state.pemasukan_data
    total = data["money"]

    st.subheader("2️⃣ Alokasikan Pemasukan Kamu")
    st.info(f"Total pemasukan yang akan dialokasikan: **Rp {total:,.0f}**")

    with st.form("form_alokasi"):
        alokasi_input = {}
        for kat in KATEGORI_KOLOM:
            alokasi_input[kat] = st.number_input(
                f"{kat.capitalize()} (Rp)",
                min_value=0,
                step=1000,
                key=f"alokasi_{kat}",
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
            else:
                try:
                    # Gabungkan pemasukan + alokasi jadi SATU baris di tabel user_data.
                    # Kolom "date" sengaja TIDAK disertakan -> otomatis diisi now() oleh Supabase.
                    row = {
                        "money": data["money"],
                        # "sumber": data["sumber"],
                        # "catatan": data["catatan"],
                    }
                    row.update(alokasi_input)

                    supabase.table("user_data").insert(row).execute()

                    st.success("Pemasukan & alokasi berhasil disimpan!")
                    reset_flow()
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menyimpan data: {e}")

    if st.button("🔄 Mulai Ulang dari Awal"):
        reset_flow()
        st.rerun()

# ============================================================
# Kelola Data — lihat & hapus data yang sudah tersimpan
# ============================================================
st.divider()
st.subheader("Kelola Data")

try:
    response = (
        supabase.table("user_data")
        .select("*")
        .order("date", desc=True)
        .execute()
    )
    data_list = response.data

    if data_list:
        for row in data_list:
            col1, col2, col3, col4 = st.columns([2, 2, 3, 1])
            col1.write(row.get("date", ""))
            col2.write(f"Rp {row['money']:,.0f}")
            # col3.write(row.get("sumber", ""))
            if col4.button("🗑️", key=f"del_{row['id_input']}"):
                supabase.table("user_data").delete().eq("id_input", row["id_input"]).execute()
                st.rerun()
    else:
        st.info("Belum ada data.")
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")