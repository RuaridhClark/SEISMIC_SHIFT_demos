# Run with Streamlit using the following command:
# streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\Research\SEISMIC\Innovation Partnership\Apps\SEISMIC_SHIFT_apps\systemsprint_NHSL.py"

import streamlit as st
from pathlib import Path
from PIL import Image
import base64

st.set_page_config(layout="wide")

# ---------- HEADER ----------
col1, col2 = st.columns([3, 1])

with col2:
    base_dir = Path(__file__).parent
    img_path = base_dir / "assets" / "Logo.png"
    img = Image.open(img_path)
    st.image(img, width=500)

st.title("NHSL System Sprint to co-design a Breathlessness Pathway")

# =========================================================
# Model Explanation
# =========================================================

with st.expander("About this diagram"):
    st.markdown("""
    This diagram illustrates an activity with NHS Lanarkshire stakeholders to define the scope of a possible breathlessness pathway.
                
    The comments and suggestions captured were in response to a series of prompts:​

    - Which conditions should be covered?​
    - Which parts of the patient journey should be covered?​
    - How far into primary/community care, and else?​
    - Which parts of NHS Lanarkshire? 

    """)

# ---------- IMAGE PATHS ----------
base_dir = Path(__file__).parent

images = {
    "Base": base_dir / "assets" / "SysSprint_Base.png",
    "Allied Health": base_dir / "assets" / "SysSprint_AHP.png",
    "GPs": base_dir / "assets" / "SysSprint_GP.png",
    "Secondary Care": base_dir / "assets" / "SysSprint_SC.png",
    "Service Managers": base_dir / "assets" / "SysSprint_SM.png",
}

# ---------- STAKEHOLDER CONTROLS ----------
st.markdown("### Select Stakeholder Overlays")
col1, col2, col3, col4 = st.columns(4)

with col1:
    show_allied = st.checkbox("Allied Health")
with col2:
    show_gps = st.checkbox("GPs")
with col3:
    show_secondary = st.checkbox("Secondary Care")
with col4:
    show_managers = st.checkbox("Service Managers")

st.markdown("---")

# ---------- IMAGE TO BASE64 FUNCTION ----------
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

base_img = img_to_base64(images["Base"])

overlay_html = ""

if show_allied:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Allied Health"])}" class="overlay">'
if show_gps:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["GPs"])}" class="overlay">'
if show_secondary:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Secondary Care"])}" class="overlay">'
if show_managers:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Service Managers"])}" class="overlay">'

# ---------- DISPLAY LAYERED IMAGE ----------
st.markdown(
    f"""
    <style>
    .img-container {{
        position: relative;
        width: 100%;
        max-width: 1200px;
    }}

    .img-container img {{
        width: 100%;
    }}

    .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
    }}
    </style>

    <div class="img-container">
        <img src="data:image/png;base64,{base_img}">
        {overlay_html}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- FUNDERS ----------
st.markdown("---")

base_dir = Path(__file__).parent
img_path = base_dir / "assets" / "Funders.png"

img = Image.open(img_path)
st.image(img, width=400)