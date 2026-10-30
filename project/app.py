"""Run with: streamlit run app.py"""
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Coffee Shop Sales | OSB", page_icon="☕", layout="wide")
st.markdown("<style>.block-container{padding:0;max-width:1120px}</style>", unsafe_allow_html=True)


@st.cache_data
def load_dashboard(html_modified, data_modified, logo_modified):
    # Timestamps invalidate the cache when prepared data, HTML or the logo changes.
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    rows = json.loads((ROOT / "public" / "agg.json").read_text(encoding="utf-8"))
    # components.html runs in an iframe. Embed the local JSON instead of fetching
    # a static URL that Streamlit does not serve from this directory.
    original = "fetch('agg.json').then(r=>{if(!r.ok)throw Error('agg.json could not be loaded');return r.json();})"
    assert original in html, "Dashboard data loader changed; update app.py to match."
    payload = json.dumps(rows, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace(original, f"Promise.resolve({payload})")
    logo = ROOT / "public" / "assets" / "osb-logo.png"
    if logo.exists():
        import base64
        image = base64.b64encode(logo.read_bytes()).decode("ascii")
        html = html.replace('src="assets/osb-logo.png"', f'src="data:image/png;base64,{image}"')
    else:
        # No request for a nonexistent asset inside the Streamlit iframe.
        html = html.replace('src="assets/osb-logo.png"', '')
    return html


if not (ROOT / "public" / "agg.json").exists():
    st.error("Prepared data is missing. Run python prepare.py, then reload this page.")
    st.stop()

logo_path = ROOT / "public" / "assets" / "osb-logo.png"
dashboard = load_dashboard(
    (ROOT / "public" / "index.html").stat().st_mtime_ns,
    (ROOT / "public" / "agg.json").stat().st_mtime_ns,
    logo_path.stat().st_mtime_ns if logo_path.exists() else 0,
)
# Scrolling preserves mobile layouts and keeps the dashboard filter bar sticky.
components.html(dashboard, height=1600, scrolling=True)
