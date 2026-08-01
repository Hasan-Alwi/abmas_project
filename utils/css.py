# ----------------------------------------------------------------------------
# DESAIN VISUAL
#   Identitas: emerald pesantren + emas (barakah/sedekah) + kertas hangat.
#   Font: Plus Jakarta Sans (buatan Indonesia) + Amiri untuk kutipan.
# ----------------------------------------------------------------------------

from pathlib import Path
import streamlit as st

def load_css():
    css_file = Path(__file__).parent.parent / "assets" / "css" / "style.css"

    with open(css_file, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )