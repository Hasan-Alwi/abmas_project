import streamlit as st
import plotly.graph_objects as go
from utils.css import load_css
from utils.nav import top_nav
from utils.page import setup


# Import CSS
load_css()
top_nav("/budget_example")
setup("/budget_example")

# ----------------------------------------------------------------------------
# DATA EXAMPLE
# ----------------------------------------------------------------------------
PEMASUKAN = 1_500_000

# Total pengeluaran contoh. Nominal tiap kategori dihitung otomatis dari persen.
TOTAL_PENGELUARAN = 1_500_000

# 9 kategori pengeluaran (contoh alokasi). Cukup ubah "persen" di sini —
# kartu, donat, dan bar chart akan ikut menyesuaikan secara otomatis.
KATEGORI = [
    {"nama": "Makan & minum",     "persen": 30, "icon": "🍽️", "warna": "#0B4F3E"},
    {"nama": "Sekolah",           "persen": 12, "icon": "📚", "warna": "#14764F"},
    {"nama": "Sosial & Hiburan",  "persen": 11, "icon": "🎬", "warna": "#1F8A5F"},
    {"nama": "Sedekah / Amal",    "persen": 10, "icon": "🤲", "warna": "#C9A227"},
    {"nama": "Kebutuhan pribadi", "persen": 10, "icon": "🧴", "warna": "#3FA877"},
    {"nama": "Transportasi",      "persen":  9, "icon": "🚌", "warna": "#57B894"},
    {"nama": "Olahraga",          "persen":  7, "icon": "🏃", "warna": "#7BC9A8"},
    {"nama": "Investasi",         "persen":  6, "icon": "📈", "warna": "#D98E3A"},
    {"nama": "Acara / kegiatan",  "persen":  5, "icon": "🎉", "warna": "#B5894A"},
]

# Nominal tiap kategori (turunan dari persen) + total pengeluaran sebenarnya
for k in KATEGORI:
    k["nominal"] = round(TOTAL_PENGELUARAN * k["persen"] / 100)
PENGELUARAN = sum(k["nominal"] for k in KATEGORI)

# Kategori terbesar & terkecil (untuk kartu metrik)
terbesar = max(KATEGORI, key=lambda k: k["nominal"])
terkecil = min(KATEGORI, key=lambda k: k["nominal"])


def rupiah(n: int) -> str:
    return "Rp " + f"{int(n):,}".replace(",", ".")


# ----------------------------------------------------------------------------
# BUDGETING EXAMPLE
# ----------------------------------------------------------------------------
st.markdown('<div class="sec-title"><h3>Budgeting Example</h3><div class="rule"></div></div>',
            unsafe_allow_html=True)


def metric_card(label, value, icon, bg, *, delta=None, direction="up", caption=None, gold=False):
    cls = "metric sedekah" if gold else "metric"
    if caption is not None:
        bottom = f'<div class="delta up">{caption}</div>'
    else:
        arrow = "↑" if direction == "up" else "↓"
        bottom = f'<div class="delta {direction}">{arrow} {delta} dari bulan lalu</div>'
    return f"""
    <div class="{cls}">
      <div class="top">
        <div class="label">{label}</div>
        <div class="dot" style="background:{bg}">{icon}</div>
      </div>
      <div class="val">{value}</div>
      {bottom}
    </div>"""


c1, c2, c3, c4 = st.columns(4)
c1.markdown(
    metric_card("Total Pemasukan", rupiah(PEMASUKAN), "💰", "#E2F1EA", delta="12%", direction="up"),
    unsafe_allow_html=True)
c2.markdown(
    metric_card("Total Pengeluaran", rupiah(PENGELUARAN), "🛒", "#FBE7E5", delta="8%", direction="down"),
    unsafe_allow_html=True)
c3.markdown(
    metric_card("Pengeluaran Terbesar", rupiah(terbesar["nominal"]), terbesar["icon"], "#F7EFD3",
                caption=f"{terbesar['nama']} · {terbesar['persen']}%", gold=True),
    unsafe_allow_html=True)
c4.markdown(
    metric_card("Pengeluaran Terkecil", rupiah(terkecil["nominal"]), terkecil["icon"], "#E4EEFB",
                caption=f"{terkecil['nama']} · {terkecil['persen']}%"),
    unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Donut Alokasi (semua kategori) + Bar Chart Adaptif (kategori pilihan user)
# ----------------------------------------------------------------------------
left, right = st.columns([1, 1], gap="medium")

with left:
    st.markdown('<div class="panel"><h4>Alokasi Keuangan</h4>'
                '<p class="sub">Pembagian dari total pengeluaran bulan ini</p></div>',
                unsafe_allow_html=True)
    fig = go.Figure(go.Pie(
        labels=[k["nama"] for k in KATEGORI],
        values=[k["nominal"] for k in KATEGORI],
        hole=0.62, sort=False, direction="clockwise",
        marker=dict(colors=[k["warna"] for k in KATEGORI], line=dict(color="#FFFFFF", width=2)),
        textinfo="percent", textfont=dict(size=11, family="Plus Jakarta Sans", color="#fff"),
        hovertemplate="%{label}: Rp %{value:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.02, x=0.5, xanchor="center",
                    font=dict(family="Plus Jakarta Sans", size=10, color="#1E2A28")),
        margin=dict(t=10, b=10, l=10, r=10), height=400,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(text=f"<b>{rupiah(PENGELUARAN)}</b><br>Pengeluaran", x=0.5, y=0.5,
                          showarrow=False,
                          font=dict(family="Plus Jakarta Sans", size=13, color="#0B4F3E"))],
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with right:
    st.markdown('<div class="panel"><h4>Perbandingan Pengeluaran</h4>'
                '<p class="sub">Centang kategori yang ingin kamu tampilkan & bandingkan</p></div>',
                unsafe_allow_html=True)

    semua_nama = [k["nama"] for k in KATEGORI]
    pilihan = st.multiselect(
        "Pilih kategori pengeluaran",
        options=semua_nama,
        default=semua_nama,
        label_visibility="collapsed",
        placeholder="Pilih kategori pengeluaran…",
    )

    # hanya kategori yang dicentang yang ditampilkan, diurutkan kecil -> besar
    terpilih = [k for k in KATEGORI if k["nama"] in pilihan]
    terpilih.sort(key=lambda k: k["nominal"])

    if not terpilih:
        st.info("Centang minimal satu kategori untuk menampilkan grafik.")
    else:
        maxv = max(k["nominal"] for k in terpilih)
        bar = go.Figure(go.Bar(
            x=[k["nominal"] for k in terpilih],
            y=[k["nama"] for k in terpilih],
            orientation="h",
            marker=dict(color=[k["warna"] for k in terpilih], line=dict(color="#FFFFFF", width=1)),
            text=[rupiah(k["nominal"]) for k in terpilih],
            textposition="outside",
            textfont=dict(family="Plus Jakarta Sans", size=11, color="#1E2A28"),
            customdata=[k["persen"] for k in terpilih],
            hovertemplate="%{y}<br>Rp %{x:,.0f} · %{customdata}%<extra></extra>",
            cliponaxis=False,
        ))
        bar.update_layout(
            margin=dict(t=10, b=10, l=10, r=40), height=400,
            paper_bgcolor="rgba(255, 255, 255, 1)", plot_bgcolor="rgba(255, 255, 255, 1)",
            font=dict(family="Plus Jakarta Sans"),
            bargap=0.35,
            xaxis=dict(range=[0, maxv * 1.25], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(tickfont=dict(family="Plus Jakarta Sans", size=11, color="#1E2A28")),
        )
        st.plotly_chart(bar, use_container_width=True, config={"displayModeBar": False})