# Run with Streamlit using the following command:
# streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\systemsprint_NHSL_kiosk_2.py"

import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import json

# ---------- SESSION ----------
if "show_allied" not in st.session_state:
    st.session_state.show_allied = True
if "show_gps" not in st.session_state:
    st.session_state.show_gps = True
if "show_secondary" not in st.session_state:
    st.session_state.show_secondary = True
if "show_managers" not in st.session_state:
    st.session_state.show_managers = True

st.set_page_config(layout="wide")

# ---------- HEADER ----------
col1, col2 = st.columns([4, 2])

with col1:
    st.markdown(
        "<h1 style='color:#1C2747; font-family:\"Yu Gothic UI\";'>Co-designing a<br>Breathlessness Pathway</h1>",
        unsafe_allow_html=True
    )

with col2:
    base_dir = Path(__file__).parent
    st.image(Image.open(base_dir / "assets" / "Logo.png"), width=250)

# ---------- PATHS ----------
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
    return base64.b64encode(open(path, "rb").read()).decode()

base_img = img_to_base64(images["Base"])

# ---------- STATE ----------
state = {
    "ahp": st.session_state.show_allied,
    "gps": st.session_state.show_gps,
    "secondary": st.session_state.show_secondary,
    "managers": st.session_state.show_managers
}
state_json = json.dumps(state)

# ---------- OVERLAYS ----------
overlay_main = "".join([
    f'<img id="{k}" class="overlay" src="data:image/png;base64,{img_to_base64(images[name])}">'
    for k, name in {
        "ahp": "Allied Health",
        "gps": "GPs",
        "secondary": "Secondary Care",
        "managers": "Service Managers"
    }.items()
])

overlay_zoom = overlay_main.replace('"overlay"', '"overlay"')

# ---------- HTML ----------
html = f"""
<!DOCTYPE html>
<html>
<head>
<style>

body {{ margin:0; }}

.overlay {{
    position:absolute;
    top:0;
    left:0;
    width:100%;
    display:none;
}}

#zoom-modal {{
    display:block;   /* ✅ DEFAULT OPEN */
    position:fixed;
    inset:0;
    background:white;
    z-index:9999;
}}

#viewport {{
    position:absolute;
    top:0;
    left:0;
    right:0;
    bottom:0;
    overflow:hidden;
}}

#panzoom-content {{
    position:absolute;
    transform-origin:0 0;
}}

#minimap {{
    position:absolute;
    bottom:0px;
    right:0px;
    width:320px;      /* ✅ BIGGER */
    border:2px solid #009485;
    background:white;
    z-index:10000;
}}

#minimap img {{
    width:100%;
}}


#minimap-viewport {{
    display: block;
    position: absolute;
    border: 2px solid #FF6B35;
    background: rgba(255, 107, 53, 0.2);
    cursor: grab;
    box-sizing: border-box;
}}


#zoom-reset {{
    position:fixed;
    top:20px;
    right:20px;
    z-index:10000;
    padding:10px 16px;
    background:#009485;
    color:white;
    border:none;
    border-radius:6px;
    cursor:pointer;
}}

</style>
</head>

<body>

<div id="zoom-modal">

<button id="zoom-reset">Reset</button>

<div id="viewport">
    <div id="panzoom-content">
        <img src="data:image/png;base64,{base_img}">
        {overlay_zoom}
    </div>
</div>

<div id="minimap">
    <img id="minimap-img" src="data:image/png;base64,{base_img}">
    <div id="minimap-viewport"></div>
</div>

</div>

<script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>

<script>

// ---------- overlays ----------
const overlayState = {state_json};

function setOverlay(id, visible) {{
    const el = document.getElementById(id);
    if (el) el.style.display = visible ? "block" : "none";
}}

function updateOverlays() {{
    ["ahp","gps","secondary","managers"].forEach(k => {{
        setOverlay(k, overlayState[k]);
    }});
}}
updateOverlays();

// ---------- panzoom ----------
const viewport = document.getElementById("viewport");
const content = document.getElementById("panzoom-content");

const minimapImg = document.getElementById("minimap-img");
const minimapViewport = document.getElementById("minimap-viewport");

const panzoom = Panzoom(content, {{
    maxScale: 6,
    minScale: 0.2,
    step: 0.05
}});

// ---------- smooth wheel zoom ----------
viewport.addEventListener(
    "wheel",
    function (e) {{

        e.preventDefault();

        const currentScale = panzoom.getScale();

        const newScale =
            e.deltaY < 0
                ? currentScale * 1.05
                : currentScale * 0.95;

        panzoom.zoomToPoint(
            newScale,
            {{
                clientX: e.clientX,
                clientY: e.clientY
            }},
            {{
                animate: false
            }}
        );

        updateMinimap();
    }},
    {{ passive: false }}
);


// ---------- helper ----------
function fitToScreen(animated = false) {{

    const img = content.querySelector("img");

    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;

    const iw = img.naturalWidth;
    const ih = img.naturalHeight;

    const fitScale = Math.min(
        vw / iw,
        vh / ih
    );

    panzoom.zoom(fitScale, {{
        animate: animated,
        duration: 400
    }});

    panzoom.pan(
        (vw - iw * fitScale) / 2,
        (vh - ih * fitScale) / 2,
        {{
            animate: animated,
            duration: 400
        }}
    );

    updateMinimap();
}}

function updateMinimap() {{

    const scale = panzoom.getScale();
    const pan = panzoom.getPan();

    const img = content.querySelector("img");

    const contentWidth = img.naturalWidth;
    const contentHeight = img.naturalHeight;

    const minimapRect = minimapImg.getBoundingClientRect();

    // ✅ Determine actual minimap dimensions (respect aspect ratio)
    const actualMinimapWidth = minimapRect.width;
    const actualMinimapHeight = minimapRect.height;

    if (!actualMinimapWidth || !actualMinimapHeight) {{
        return;
    }}

    // ✅ Scale factors from image → minimap (using actual dimensions)
    const ratioX = actualMinimapWidth / contentWidth;
    const ratioY = actualMinimapHeight / contentHeight;

    // ✅ Size of visible area in image coordinates, clamped to image bounds
    const visibleWidth = Math.min(viewport.clientWidth / scale, contentWidth);
    const visibleHeight = Math.min(viewport.clientHeight / scale, contentHeight);

    // ✅ Top-left corner in image coordinates, clamped to image bounds
    const offsetX = -pan.x / scale // Math.max(0, Math.min(-pan.x / scale, contentWidth - visibleWidth));
    const offsetY = -pan.y / scale // Math.max(0, Math.min(-pan.y / scale, contentHeight - visibleHeight));

    const boxWidth = visibleWidth * ratioX;
    const boxHeight = visibleHeight * ratioY;
    const left = offsetX * ratioX;
    const top = offsetY * ratioY;

    minimapViewport.style.width = boxWidth + "px";
    minimapViewport.style.height = boxHeight + "px";
    minimapViewport.style.left = left + "px";
    minimapViewport.style.top = top + "px";
}}

content.addEventListener("panzoomchange", updateMinimap);

// ---------- DEFAULT LOAD (SLIGHTLY ZOOMED OUT) ----------
requestAnimationFrame(() => {{

    const img = content.querySelector("img");

    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;

    const iw = img.naturalWidth;
    const ih = img.naturalHeight;

    const scale = 1;

    panzoom.zoom(scale, {{ animate:false }});

    panzoom.pan(
        (vw - iw * scale) / 2,
        (vh - ih * scale) / 2
    );

    updateMinimap();
}});

// ---------- RESET ----------
document.getElementById("zoom-reset").onclick = function() {{
    const img = content.querySelector("img");

    const vw = viewport.clientWidth;
    const vh = viewport.clientHeight;

    const iw = img.naturalWidth;
    const ih = img.naturalHeight;

    const scale = 1;

    panzoom.zoom(scale, {{ animate:false }});

    panzoom.pan(
        (vw - iw * scale) / 2,
        (vh - ih * scale) / 2
    );
    updateMinimap();
}};

</script>

</body>
</html>
"""

st.components.v1.html(html, height=1200)

# ---------- CONTROLS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Allied Health ✓" if st.session_state.show_allied else "Allied Health", use_container_width=True):
        st.session_state.show_allied = not st.session_state.show_allied
        st.rerun()

with col2:
    if st.button("GPs ✓" if st.session_state.show_gps else "GPs", use_container_width=True):
        st.session_state.show_gps = not st.session_state.show_gps
        st.rerun()

with col3:
    if st.button("Secondary Care ✓" if st.session_state.show_secondary else "Secondary Care",use_container_width=True):
        st.session_state.show_secondary = not st.session_state.show_secondary
        st.rerun()

with col4:
    if st.button("Service Managers ✓" if st.session_state.show_managers else "Service Managers", use_container_width=True):
        st.session_state.show_managers = not st.session_state.show_managers
        st.rerun()

st.markdown("---")
st.image(Image.open(base_dir / "assets" / "Funders.png"), width=400)