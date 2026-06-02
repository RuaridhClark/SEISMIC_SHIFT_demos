# Run with Streamlit using the following command:
# streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\systemsprint_NHSL.py"

import streamlit as st
from pathlib import Path
from PIL import Image
import base64
import streamlit.components.v1 as components

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
# st.markdown(
#     f"""
#     <style>
#     .img-container {{
#         position: relative;
#         width: 100%;
#         max-width: 1200px;
#     }}

#     .img-container img {{
#         width: 100%;
#     }}

#     .overlay {{
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 100%;
#     }}
#     </style>

#     <div class="img-container zoomable">
#         <img src="data:image/png;base64,{base_img}">
#         {overlay_html}
#     </div>
#     """,
#     unsafe_allow_html=True
# )
import streamlit.components.v1 as components

components.html(
    f"""
    <style>
    /* --- Base diagram --- */
    .img-container {{
        position: relative;
        width: 100%;
        max-width: 1200px;
        cursor: zoom-in;
    }}

    .img-container img {{
        width: 100%;
        display: block;
    }}

    .overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        pointer-events: none;
    }}

    /* --- Modal --- */
    #zoom-modal {{
        display: none;
        position: fixed;
        inset: 0;
        background: white;   /* ✅ solid white background */
        z-index: 9999;
    }}

    /* This is the viewport (clips edges only) */
    #viewport {{
        position: absolute;
        inset: 0;
        overflow: hidden;
        cursor: grab;
    }}

    #viewport:active {{
        cursor: grabbing;
    }}

    /* THIS is what panzoom transforms */
    #panzoom-content {{
        position: absolute;
        top: 0;
        left: 0;
        transform-origin: 0 0;
    }}
    </style>

    <!-- Main page diagram -->
    <div class="img-container" id="diagram">
        <img src="data:image/png;base64,{base_img}">
        {overlay_html}
    </div>

    <!-- Modal -->
    <div id="zoom-modal">

        <!-- ✅ Reset Zoom Button -->
        <button id="zoom-reset"
            style="
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                padding: 8px 14px;
                font-size: 14px;
                background: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                cursor: pointer;">
            Zoom out
        </button>

        <div id="viewport">
            <div id="panzoom-content">
                <img src="data:image/png;base64,{base_img}">
                {overlay_html}
            </div>
        </div>

    </div>

    <!-- Panzoom JS -->
    <script src="https://unpkg.com/@panzoom/panzoom/dist/panzoom.min.js"></script>

    
    <script>
    const diagram = document.getElementById("diagram");
    const modal = document.getElementById("zoom-modal");
    const viewport = document.getElementById("viewport");
    const content = document.getElementById("panzoom-content");

    const panzoom = Panzoom(content, {{
        maxScale: 6,
        minScale: 1,
        contain: false
    }});

    // Enable wheel zoom
    viewport.addEventListener("wheel", panzoom.zoomWithWheel);

    // ✅ OPEN modal and centre near click position
    diagram.onclick = function (event) {{
        modal.style.display = "block";

        // Reset scale & pan
        panzoom.reset();

        requestAnimationFrame(function () {{
            // Viewport size
            const vw = viewport.clientWidth;
            const vh = viewport.clientHeight;

            // Image size
            const cw = content.clientWidth;
            const ch = content.clientHeight;

            // Click position relative to the diagram
            const rect = diagram.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const clickY = event.clientY - rect.top;

            // Convert click position to image space
            const imgX = (clickX / rect.width) * cw;
            const imgY = (clickY / rect.height) * ch;

            // Pan so clicked point moves near centre of viewport
            const x = vw / 2 - imgX;
            const y = vh / 2 - imgY;

            panzoom.pan(x, y);
        }});
    }};

    document.getElementById("zoom-reset").onclick = function () {{
        panzoom.reset();
    }};

    // ✅ CLOSE only when clicking the backdrop (not the image)
    modal.addEventListener("click", () => {{
        modal.style.display = "none";
    }});

    // ✅ PREVENT clicks inside viewport from closing modal
    viewport.addEventListener("click", (e) => {{
        e.stopPropagation();
    }});
    </script>
    
    """,
    height=850,
    scrolling=False
)

# ---------- FUNDERS ----------
st.markdown("---")

base_dir = Path(__file__).parent
img_path = base_dir / "assets" / "Funders.png"

img = Image.open(img_path)
st.image(img, width=400)