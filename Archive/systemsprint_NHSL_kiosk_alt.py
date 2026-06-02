# Run with Streamlit using the following command:
# streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\systemsprint_NHSL_kiosk.py"

import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ---------- HEADER ----------
col1, col2 = st.columns([4, 2])  # wider space for title

with col1:
    st.markdown("<h1 style='color:#1C2747; line-height:1.2; font-family:\"Yu Gothic UI\", sans-serif;'>Co-designing a<br>Breathlessness Pathway</h1>", unsafe_allow_html=True)

with col2:
    base_dir = Path(__file__).parent
    img_path = base_dir / "assets" / "Logo.png"
    img = Image.open(img_path)
    st.image(img, width=250)


# st.markdown("---")

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

# ---------- IMAGE TO BASE64 ----------
def img_to_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

base_img = img_to_base64(images["Base"])

# ---------- CONTROLS ----------
# st.markdown("### Select Stakeholder Overlays")

col1, col2, col3, col4 = st.columns(4)

with col1:
    show_allied = st.checkbox("Allied Health", value=True)  # ✅ default ON
with col2:
    show_gps = st.checkbox("GPs")
with col3:
    show_secondary = st.checkbox("Secondary Care")
with col4:
    show_managers = st.checkbox("Service Managers")

# ---------- BUILD OVERLAYS ----------
overlay_html = ""

if show_allied:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Allied Health"])}" class="overlay">'
if show_gps:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["GPs"])}" class="overlay">'
if show_secondary:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Secondary Care"])}" class="overlay">'
if show_managers:
    overlay_html += f'<img src="data:image/png;base64,{img_to_base64(images["Service Managers"])}" class="overlay">'


# ✅ ---------- DIAGRAM AT TOP ----------

with diagram_placeholder:
    components.html(f"""
    <style>
    body {{
        margin: 0;
    }}

    /* Container */
    .img-container {{
        position: relative;
        width: 100%;
        max-width: 1200px;
        margin: auto;
        cursor: zoom-in;
    }}

    /* Base image */
    .img-container img {{
        width: 100%;
        height: auto;
        display: block;
    }}

    /* Overlay images */
    .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        pointer-events: none;
    }}

    /* Modal */
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
        cursor: grab;
    }}

    #panzoom-content {{
        position: absolute;
        top: 0;
        left: 0;
        transform-origin: 0 0;
    }}
    </style>


    <!-- MAIN DIAGRAM -->
    <div class="img-container" id="diagram">

        <!-- ✅ Instruction overlay -->
        <div style="    
            
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10;

            font-family: 'Yu Gothic UI', sans-serif;
            font-size: 16px;
            font-style: italic;
            color: #009485;
            padding: 10px 16px;
        ">
            Touch to zoom and pan
        </div>

        <img src="data:image/png;base64,{base_img}">
        {overlay_html}
    </div>

    <!-- MODAL -->
    <div id="zoom-modal">

        <button id="zoom-reset"
            style="
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                padding: 10px 16px;
                font-size: 14px;
                font-family: 'Yu Gothic UI', sans-serif;
                background-color: #009485;
                color: #FFFFFF;
                border: none;                 /* ✅ remove grey border */
                border-radius: 6px;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);  /* ✅ nice depth */
            ">
            Zoom out
        </button>

        <div id="viewport">
            <div id="panzoom-content">
                <img src="data:image/png;base64,{base_img}">
                {overlay_html}
            </div>
        </div>

    </div>

    <script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>

    <script>
    const diagram = document.getElementById("diagram");
    const modal = document.getElementById("zoom-modal");
    const viewport = document.getElementById("viewport");
    const content = document.getElementById("panzoom-content");

    const panzoom = Panzoom(content, {{
        maxScale: 6,
        minScale: 1
    }});

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
    """,
    height=700,
    scrolling=False
)

# ---------- ABOUT ----------
# st.markdown("---")

with st.expander("About this diagram"):
    st.markdown("""
    This diagram illustrates an activity with NHS Lanarkshire stakeholders to define the scope of a possible breathlessness pathway.
                
    The comments and suggestions captured were in response to:

    - Which conditions should be covered?  
    - Which parts of the patient journey should be covered?  
    - How far into primary/community care?  
    - Which parts of NHS Lanarkshire?  
    """)

# ---------- FUNDERS ----------
st.markdown("---")

img_path = base_dir / "assets" / "Funders.png"
img = Image.open(img_path)
st.image(img, width=400)