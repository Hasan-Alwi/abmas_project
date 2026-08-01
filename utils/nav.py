import streamlit as st

MENU = [
    ("🏠", "Beranda",        "/"),
    ("📒", "Input",     "/input_user"),
    ("🧮", "Dashboard",       "/dashboard"),
    ("🎯", "Budget Example", "/budget_example"),
    ("📖", "Edukasi",        "/financial_education"),
]


def top_nav(active: str = "/"):
    """Navbar atas. `active` diisi href halaman yang sedang dibuka."""
    items = "".join(
        f'<a class="nav-item{" active" if href == active else ""}" '
        f'href="{href}" target="_self">{icon}&nbsp;&nbsp;{label}</a>'
        for icon, label, href in MENU
    )
    st.markdown(
        '<div class="topnav">'
        '<a class="brand" href="/" target="_self">🌙 Keuangan Syariah</a>'
        f'<nav class="nav-links">{items}</nav>'
        '</div>',
        unsafe_allow_html=True,
    )