# Run with Streamlit using the following command:
# streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\systemsprint_NHSL_kiosk.py"

import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import json
import streamlit.components.v1 as components

if "show_allied" not in st.session_state:
    st.session_state.show_allied = True

if "show_gps" not in st.session_state:
    st.session_state.show_gps = False

if "show_secondary" not in st.session_state:
    st.session_state.show_secondary = False

if "show_managers" not in st.session_state:
    st.session_state.show_managers = False

st.set_page_config(layout="wide")

# ---------- HEADER ----------
col1, col2 = st.columns([4, 2])

with col1:
    st.markdown(
        "<h1 style='color:#1C2747; font-family:\"Yu Gothic UI\", sans-serif;'>"
        "Co-designing a<br>Breathlessness Pathway</h1>",
        unsafe_allow_html=True
    )

with col2:
    base_dir = Path(__file__).parent
    img = Image.open(base_dir / "assets" / "Logo.png")
    st.image(img, width=250)

diagram_placeholder = st.empty()

# ---------- IMAGE PATHS ----------
base_dir = Path(__file__).parent

images = {
    "Base": base_dir / "assets" / "SysSprint_Base.png",
    "Allied Health": base_dir / "assets" / "SysSprint_AHP.png",
    "GPs": base_dir / "assets" / "SysSprint_GP.png",
    "Secondary Care": base_dir / "assets" / "SysSprint_SC.png",
    "Service Managers": base_dir / "assets" / "SysSprint_SM.png",
}

# ---------- BASE64 ----------
@st.cache_data
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

base_img = img_to_base64(images["Base"])

# ---------- CONTROLS ----------
show_allied = st.session_state.get("show_allied", True)
show_gps = st.session_state.get("show_gps", False)
show_secondary = st.session_state.get("show_secondary", False)
show_managers = st.session_state.get("show_managers", False)

# ---------- STATE ----------
import json

# state = {
#     "ahp": show_allied,
#     "gps": show_gps,
#     "secondary": show_secondary,
#     "managers": show_managers
# }

# state_json = json.dumps(state)

state = {
    "ahp": st.session_state.show_allied,
    "gps": st.session_state.show_gps,
    "secondary": st.session_state.show_secondary,
    "managers": st.session_state.show_managers
}

state_json = json.dumps(state)

# ---------- STATIC OVERLAYS ----------
overlay_html_main = f"""
<img id="ahp" class="overlay" src="data:image/png;base64,{img_to_base64(images["Allied Health"])}">
<img id="gps" class="overlay" src="data:image/png;base64,{img_to_base64(images["GPs"])}">
<img id="secondary" class="overlay" src="data:image/png;base64,{img_to_base64(images["Secondary Care"])}">
<img id="managers" class="overlay" src="data:image/png;base64,{img_to_base64(images["Service Managers"])}">
"""

overlay_html_zoom = f"""
<img id="ahp-zoom" class="overlay" src="data:image/png;base64,{img_to_base64(images["Allied Health"])}">
<img id="gps-zoom" class="overlay" src="data:image/png;base64,{img_to_base64(images["GPs"])}">
<img id="secondary-zoom" class="overlay" src="data:image/png;base64,{img_to_base64(images["Secondary Care"])}">
<img id="managers-zoom" class="overlay" src="data:image/png;base64,{img_to_base64(images["Service Managers"])}">
"""

# ---------- HTML ----------
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{ margin:0; }}

.img-container {{
    position: relative;
    width: 100%;
    max-width: 1200px;
    margin: auto;
}}

.img-container img {{
    width: 100%;
}}

.overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    display: none;
}}

#zoom-modal {{
    display: none;
    position: fixed;
    inset: 0;
    background: white;
    z-index: 9999;
}}

#viewport {{
    position: absolute;
    inset: 0;
    overflow: hidden;
}}

#panzoom-content {{
    position: absolute;
    transform-origin: 0 0;
}}
</style>
</head>

<body>

<div class="img-container" id="diagram">

    <!-- Instruction -->
    <div style="
        position:absolute;
        top:20px;
        left:50%;
        transform:translateX(-50%);
        font-family:'Yu Gothic UI';
        font-style:italic;
        color:#009485;
        font-size:15px;">
        Touch to zoom and pan
    </div>

    <img src="data:image/png;base64,{base_img}">
    {overlay_html_main}
</div>

<div id="zoom-modal">
    <div id="viewport">
        <div id="panzoom-content">
            <img src="data:image/png;base64,{base_img}">
            {overlay_html_zoom}
        </div>
    </div>
</div>

<script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>

<script>

// ---------- overlay state ----------
const overlayState = {state_json};

function setOverlay(id, visible) {{
    const el = document.getElementById(id);
    if (el) {{
        el.style.display = visible ? "block" : "none";
    }}
}}

function updateOverlays() {{

    setOverlay("ahp", overlayState.ahp);
    setOverlay("gps", overlayState.gps);
    setOverlay("secondary", overlayState.secondary);
    setOverlay("managers", overlayState.managers);

    setOverlay("ahp-zoom", overlayState.ahp);
    setOverlay("gps-zoom", overlayState.gps);
    setOverlay("secondary-zoom", overlayState.secondary);
    setOverlay("managers-zoom", overlayState.managers);
}}

updateOverlays();

// ---------- zoom ----------
const diagram = document.getElementById("diagram");
const modal = document.getElementById("zoom-modal");
const viewport = document.getElementById("viewport");
const content = document.getElementById("panzoom-content");

const panzoom = Panzoom(content, {{
    maxScale: 6,
    minScale: 1,
    exclude: ["#zoom-reset"]
}});

viewport.addEventListener("wheel", panzoom.zoomWithWheel);

// ✅ Fix button interaction
const resetBtn = document.getElementById("zoom-reset");
resetBtn.addEventListener("mousedown", (e) => e.stopPropagation());
resetBtn.addEventListener("touchstart", (e) => e.stopPropagation());


viewport.addEventListener("wheel", panzoom.zoomWithWheel);

diagram.onclick = function (event) {{
    modal.style.display = "block";
    panzoom.reset();

    requestAnimationFrame(function () {{
        const vw = viewport.clientWidth;
        const vh = viewport.clientHeight;

        const cw = content.clientWidth;
        const ch = content.clientHeight;

        const rect = diagram.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const clickY = event.clientY - rect.top;

        const imgX = (clickX / rect.width) * cw;
        const imgY = (clickY / rect.height) * ch;

        const x = vw / 2 - imgX;
        const y = vh / 2 - imgY;

        panzoom.pan(x, y);
    }});
}};

document.getElementById("zoom-reset").onclick = function () {{
    panzoom.reset();
}};

modal.addEventListener("click", () => {{
        modal.style.display = "none";
    }});

    viewport.addEventListener("click", (e) => {{
        e.stopPropagation();
    }});

</script>

</body>
</html>
"""

# ✅ ---------- RENDER ----------
st.iframe(html, height=700)


# ---------- CONTROLS ----------
col1, col2, col3, col4 = st.columns(4)

# with col1:
#     st.checkbox(
#         "Allied Health",
#         value=True,
#         key="show_allied"
#     )

# with col2:
#     st.checkbox(
#         "GPs",
#         key="show_gps"
#     )

# with col3:
#     st.checkbox(
#         "Secondary Care",
#         key="show_secondary"
#     )

# with col4:
#     st.checkbox(
#         "Service Managers",
#         key="show_managers"
#     )
if "show_allied" not in st.session_state:
    st.session_state.show_allied = True  # initially ON

if "show_gps" not in st.session_state:
    st.session_state.show_gps = False

if "show_secondary" not in st.session_state:
    st.session_state.show_secondary = False

if "show_managers" not in st.session_state:
    st.session_state.show_managers = False

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(
        "Allied Health ✓" if st.session_state.show_allied else "Allied Health",
        use_container_width=True
    ):
        st.session_state.show_allied = not st.session_state.show_allied
        st.rerun()

with col2:
    if st.button(
        "GPs ✓" if st.session_state.show_gps else "GPs",
        use_container_width=True
    ):
        st.session_state.show_gps = not st.session_state.show_gps
        st.rerun()

with col3:
    if st.button(
        "Secondary Care ✓" if st.session_state.show_secondary else "Secondary Care",
        use_container_width=True
    ):
        st.session_state.show_secondary = not st.session_state.show_secondary
        st.rerun()

with col4:
    if st.button(
        "Service Managers ✓" if st.session_state.show_managers else "Service Managers",
        use_container_width=True
    ):
        st.session_state.show_managers = not st.session_state.show_managers
        st.rerun()


# Add whitespace below
st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# ---------- ABOUT ----------
with st.expander("About this diagram"):
    st.markdown("""
    This diagram illustrates an output from the System Sprint run with NHS Lanarkshire to define the scope of a future breathlessness pathway.
                
    The comments and suggestions captured were in response to a series of prompts:​

    - Which conditions should be covered?​
    - Which parts of the patient journey should be covered?​
    - How far into primary/community care, and else?​
    - Which parts of NHS Lanarkshire? 

    """)

# ---------- FOOTER ----------
st.markdown("---")
img = Image.open(base_dir / "assets" / "Funders.png")
st.image(img, width=400)