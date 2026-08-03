import streamlit as st
import pandas as pd
import altair as alt
from supabase_client import supabase
from utils.theme import (
    inject_css,
    sidebar_brand,
    navbar,
    hero,
    metric_card,
    panel_header,
    section_title,
    info_card,
    PALETTE,
    COLORS,
    FONT,
)

# ------------------------------------------------------------
# Tema (sama dengan halaman lain)
# ------------------------------------------------------------
inject_css()

with st.sidebar:
    sidebar_brand(active="Laporan & Visualisasi")

navbar(active="Dashboard")

# ------------------------------------------------------------
# Kategori alokasi — kunci = nama kolom di tabel user_data
# ------------------------------------------------------------
KATEGORI_ALOKASI = {
    "kebutuhan_pribadi": "Kebutuhan Pribadi",
    "urunan": "Urunan",
    "konsumsi": "Konsumsi",
    "investment": "Investasi",
    "lain_lain": "Lain-lain",
}
KATEGORI_KOLOM = list(KATEGORI_ALOKASI.keys())
LABEL_KATEGORI = list(KATEGORI_ALOKASI.values())

KOLOM_INVESTASI = "investment"
LABEL_INVESTASI = KATEGORI_ALOKASI[KOLOM_INVESTASI]
KOLOM_KETERANGAN = "keterangan"
HALAMAN_INPUT = "pages/input_user.py"

WARNA = dict(zip(LABEL_KATEGORI, PALETTE))


def rupiah(nilai) -> str:
    return "Rp {:,.0f}".format(nilai or 0).replace(",", ".")


def rapikan(chart, grid_y: bool = False):
    """Konfigurasi visual seragam untuk semua grafik."""
    chart = (
        chart.configure_view(strokeWidth=0)
        .configure_axis(
            labelFont=FONT,
            titleFont=FONT,
            labelColor=COLORS["muted"],
            titleColor=COLORS["muted"],
            labelFontSize=12,
            domainColor=COLORS["border"],
            tickColor=COLORS["border"],
            grid=False,
        )
        .configure_legend(
            labelFont=FONT,
            titleFont=FONT,
            labelColor=COLORS["ink"],
            labelFontSize=12,
            symbolType="circle",
        )
    )
    if grid_y:
        chart = chart.configure_axisY(
            grid=True, gridColor=COLORS["border"], gridDash=[3, 4], domain=False, ticks=False
        )
    return chart


# ------------------------------------------------------------
# Banner
# ------------------------------------------------------------
hero(
    eyebrow="Laporan & Visualisasi",
    title="Pantau Ke Mana Uangmu Pergi",
    lead=(
        "Ringkasan seluruh catatan keuanganmu: berapa yang masuk, ke mana saja dibagi, "
        "dan sejauh mana investasimu bertumbuh dari waktu ke waktu."
    ),
)

# ------------------------------------------------------------
# Ambil & siapkan data
# ------------------------------------------------------------
try:
    response = supabase.table("user_data").select("*").execute()
    data = response.data
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

if not data:
    info_card(
        "📭",
        "Belum ada data untuk ditampilkan",
        "Yuk mulai catat pemasukan dan alokasimu dulu, nanti grafiknya muncul di sini.",
    )
    st.page_link(HALAMAN_INPUT, label="Input Sekarang", icon="📝")
    st.stop()

df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"]).sort_values("date")

df["money"] = pd.to_numeric(df.get("money", 0), errors="coerce").fillna(0)
for kol in KATEGORI_KOLOM:
    if kol not in df.columns:
        df[kol] = 0
    df[kol] = pd.to_numeric(df[kol], errors="coerce").fillna(0)

total_pemasukan = df["money"].sum()
ringkasan = df[KATEGORI_KOLOM].sum()
ringkasan.index = [KATEGORI_ALOKASI[k] for k in ringkasan.index]
total_alokasi = ringkasan.sum()
total_investasi = ringkasan.get(LABEL_INVESTASI, 0)

terbesar_label = ringkasan.idxmax() if total_alokasi else "—"
terbesar_nilai = ringkasan.max() if total_alokasi else 0
terkecil_label = ringkasan.idxmin() if total_alokasi else "—"
terkecil_nilai = ringkasan.min() if total_alokasi else 0


def persen(bagian, total):
    return (bagian / total * 100) if total else 0


# ------------------------------------------------------------
# Kartu ringkasan
# ------------------------------------------------------------
section_title("Ringkasan Keuangan")

k1, k2, k3, k4 = st.columns(4, gap="medium")
with k1:
    metric_card(
        "Total Pemasukan",
        rupiah(total_pemasukan),
        f"{len(df)} catatan tersimpan",
        icon="💰",
    )
with k2:
    metric_card(
        "Total Teralokasi",
        rupiah(total_alokasi),
        f"{persen(total_alokasi, total_pemasukan):,.0f}% dari pemasukan",
        icon="🛒",
    )
with k3:
    metric_card(
        "Alokasi Terbesar",
        rupiah(terbesar_nilai),
        f"{terbesar_label} · {persen(terbesar_nilai, total_alokasi):,.0f}%",
        icon="📌",
        highlight=True,
    )
with k4:
    metric_card(
        "Total Investasi",
        rupiah(total_investasi),
        f"{persen(total_investasi, total_pemasukan):,.1f}% dari pemasukan",
        icon="🌱",
        tone="up",
    )

st.write("")

# ------------------------------------------------------------
# Donat alokasi + perbandingan antar kategori
# ------------------------------------------------------------
donut_df = pd.DataFrame(
    {
        "kategori": ringkasan.index,
        "nilai": ringkasan.values,
    }
)
donut_df["persen"] = donut_df["nilai"].apply(lambda v: persen(v, total_alokasi))
donut_df["label"] = donut_df["persen"].apply(lambda p: f"{p:,.0f}%" if p >= 4 else "")
donut_df["nominal"] = donut_df["nilai"].apply(rupiah)

kiri, kanan = st.columns([5, 7], gap="medium")

with kiri:
    with st.container(border=True):
        panel_header("Alokasi Keuangan", "Pembagian dari total alokasi tercatat")

        skala = alt.Scale(domain=LABEL_KATEGORI, range=PALETTE[: len(LABEL_KATEGORI)])
        dasar = alt.Chart(donut_df).encode(
            theta=alt.Theta("nilai:Q", stack=True),
            color=alt.Color(
                "kategori:N",
                scale=skala,
                legend=alt.Legend(orient="bottom", title=None, columns=2),
            ),
            tooltip=[
                alt.Tooltip("kategori:N", title="Pos"),
                alt.Tooltip("nominal:N", title="Nilai"),
                alt.Tooltip("persen:Q", title="Porsi", format=".1f"),
            ],
        )
        arc = dasar.mark_arc(innerRadius=78, outerRadius=126, stroke="#FFFFFF", strokeWidth=2)
        label_persen = dasar.mark_text(radius=102, fill="#FFFFFF", fontSize=12, fontWeight="bold").encode(
            text=alt.Text("label:N"), color=alt.value("#FFFFFF")
        )
        pusat_nilai = (
            alt.Chart(pd.DataFrame({"x": [0]}))
            .mark_text(dy=-8, fontSize=17, fontWeight="bold", color=COLORS["green_900"])
            .encode(text=alt.value(rupiah(total_alokasi)))
        )
        pusat_label = (
            alt.Chart(pd.DataFrame({"x": [0]}))
            .mark_text(dy=14, fontSize=12, color=COLORS["muted"])
            .encode(text=alt.value("Teralokasi"))
        )
        st.altair_chart(
            rapikan(alt.layer(arc, label_persen, pusat_nilai, pusat_label).properties(height=340)),
            use_container_width=True,
        )

with kanan:
    with st.container(border=True):
        panel_header("Perbandingan Alokasi", "Pilih pos yang ingin kamu tampilkan & bandingkan")
        pilihan = st.multiselect(
            "Kategori",
            options=LABEL_KATEGORI,
            default=LABEL_KATEGORI,
            label_visibility="collapsed",
        )

        if not pilihan:
            st.caption("Pilih minimal satu kategori untuk menampilkan grafik.")
        else:
            banding_df = donut_df[donut_df["kategori"].isin(pilihan)]
            batang = (
                alt.Chart(banding_df)
                .mark_bar(cornerRadiusEnd=5, size=22)
                .encode(
                    y=alt.Y("kategori:N", sort="-x", title=None,
                            axis=alt.Axis(domain=False, ticks=False, labelPadding=8)),
                    x=alt.X("nilai:Q", title=None, axis=None,
                            scale=alt.Scale(domainMax=float(banding_df["nilai"].max()) * 1.28 or 1)),
                    color=alt.Color("kategori:N", scale=skala, legend=None),
                    tooltip=[
                        alt.Tooltip("kategori:N", title="Pos"),
                        alt.Tooltip("nominal:N", title="Nilai"),
                    ],
                )
            )
            teks = batang.mark_text(align="left", dx=8, fontSize=12,
                                    color=COLORS["ink"], fontWeight="bold").encode(
                text=alt.Text("nominal:N")
            )
            st.altair_chart(
                rapikan(alt.layer(batang, teks).properties(height=max(210, 44 * len(banding_df)))),
                use_container_width=True,
            )

st.write("")

# ------------------------------------------------------------
# Perkembangan tiap alokasi dari waktu ke waktu
# ------------------------------------------------------------
harian = (
    df.groupby(df["date"].dt.date)[["money"] + KATEGORI_KOLOM].sum().sort_index()
)
kumulatif = harian.cumsum().reset_index().rename(columns={"index": "date"})
kumulatif.columns = ["date"] + list(kumulatif.columns[1:])
kumulatif["date"] = pd.to_datetime(kumulatif["date"])
harian = harian.reset_index()
harian.columns = ["date"] + list(harian.columns[1:])
harian["date"] = pd.to_datetime(harian["date"])

with st.container(border=True):
    panel_header(
        "Perkembangan Tiap Alokasi",
        "Garis tebal menandai pos Investasi — pantau apakah tren-nya terus naik",
    )

    mode = st.radio(
        "Tampilan",
        ["Kumulatif", "Per tanggal"],
        horizontal=True,
        label_visibility="collapsed",
    )
    sumber = kumulatif if mode == "Kumulatif" else harian

    tren_long = sumber.melt(
        id_vars="date", value_vars=KATEGORI_KOLOM, var_name="kolom", value_name="nilai"
    )
    tren_long["kategori"] = tren_long["kolom"].map(KATEGORI_ALOKASI)
    tren_long["nominal"] = tren_long["nilai"].apply(rupiah)

    garis = (
        alt.Chart(tren_long)
        .mark_line(point=True, interpolate="monotone")
        .encode(
            x=alt.X("date:T", title=None, axis=alt.Axis(format="%d %b", labelAngle=0)),
            y=alt.Y("nilai:Q", title=None, axis=alt.Axis(format="~s")),
            color=alt.Color(
                "kategori:N",
                scale=alt.Scale(domain=LABEL_KATEGORI, range=PALETTE[: len(LABEL_KATEGORI)]),
                legend=alt.Legend(orient="bottom", title=None, columns=3),
            ),
            strokeWidth=alt.condition(
                alt.datum.kategori == LABEL_INVESTASI, alt.value(3.6), alt.value(1.8)
            ),
            opacity=alt.condition(
                alt.datum.kategori == LABEL_INVESTASI, alt.value(1.0), alt.value(0.75)
            ),
            tooltip=[
                alt.Tooltip("date:T", title="Tanggal", format="%d %b %Y"),
                alt.Tooltip("kategori:N", title="Pos"),
                alt.Tooltip("nominal:N", title="Nilai"),
            ],
        )
        .properties(height=330)
    )
    st.altair_chart(rapikan(garis, grid_y=True), use_container_width=True)

st.write("")

# ------------------------------------------------------------
# Fokus: perkembangan investasi
# ------------------------------------------------------------
with st.container(border=True):
    inv_df = kumulatif[["date", KOLOM_INVESTASI]].rename(columns={KOLOM_INVESTASI: "nilai"})
    inv_df["nominal"] = inv_df["nilai"].apply(rupiah)

    pertumbuhan = ""
    if len(inv_df) >= 2 and inv_df["nilai"].iloc[-2]:
        naik = inv_df["nilai"].iloc[-1] - inv_df["nilai"].iloc[-2]
        pertumbuhan = f" Penambahan terakhir {rupiah(naik)}."

    panel_header(
        "Fokus: Perkembangan Investasi",
        "Akumulasi dana yang kamu sisihkan untuk tabungan dan investasi." + pertumbuhan,
    )

    area = (
        alt.Chart(inv_df)
        .mark_area(interpolate="monotone", opacity=0.16, color=COLORS["green_600"])
        .encode(
            x=alt.X("date:T", title=None, axis=alt.Axis(format="%d %b", labelAngle=0)),
            y=alt.Y("nilai:Q", title=None, axis=alt.Axis(format="~s")),
        )
    )
    garis_inv = (
        alt.Chart(inv_df)
        .mark_line(interpolate="monotone", strokeWidth=3, color=COLORS["green_700"],
                   point=alt.OverlayMarkDef(color=COLORS["gold_500"], size=60, filled=True))
        .encode(
            x=alt.X("date:T", title=None),
            y=alt.Y("nilai:Q", title=None),
            tooltip=[
                alt.Tooltip("date:T", title="Tanggal", format="%d %b %Y"),
                alt.Tooltip("nominal:N", title="Akumulasi"),
            ],
        )
    )
    st.altair_chart(
        rapikan(alt.layer(area, garis_inv).properties(height=280), grid_y=True),
        use_container_width=True,
    )

# ------------------------------------------------------------
# Riwayat data
# ------------------------------------------------------------
section_title("Riwayat Data")

tampil = df.sort_values("date", ascending=False).copy()
kolom_tampil = ["date", "money"] + KATEGORI_KOLOM
if KOLOM_KETERANGAN in tampil.columns:
    kolom_tampil.append(KOLOM_KETERANGAN)

tampil = tampil[kolom_tampil]
tampil["date"] = tampil["date"].dt.strftime("%d %b %Y %H:%M")
for kol in ["money"] + KATEGORI_KOLOM:
    tampil[kol] = tampil[kol].apply(rupiah)

nama_kolom = {"date": "Tanggal", "money": "Pemasukan", KOLOM_KETERANGAN: "Keterangan"}
nama_kolom.update(KATEGORI_ALOKASI)
tampil = tampil.rename(columns=nama_kolom)

st.dataframe(tampil, use_container_width=True, hide_index=True)