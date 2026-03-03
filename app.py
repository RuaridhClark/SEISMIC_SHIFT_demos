# Run with streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\app.py"

import streamlit as st
import simpy
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import graphviz
import pydot
from collections import defaultdict

st.set_page_config(layout="wide")
st.title("🏥 Healthcare Pathway Discrete Event Simulation")

# =========================================================
# Healthcare Pathway Models
# =========================================================

def get_models():
    
    staff_roles_common = {
        "GP appointment": "GP (8B)",

        "Respiratory referral admin": "Administrative",
        "Cardiology referral admin": "Administrative",

        "Respiratory Referral vetting": "Respiratory Consultant",
        "Cardiology Referral vetting": "Cardiology Consultant",

        # Example: two roles costed in one activity
        # If both are present for the entire clinic time, set both to 1.0
        # If the registrar is present for half of it, use 0.5, etc.
        "Respiratory clinic": {
            "Respiratory Consultant": 1.0,
            "Nurse": 1.0  
        },
        "Cardiology clinic": {
            "Cardiology Consultant": 1.0,
            "Nurse": 1.0  
        },

        "Respiratory test admin": "Respiratory Consultant",
        "Cardiology test admin": "Cardiology Consultant",

        "Respiratory tests": "Technician",
        "Cardiology tests": "Technician",

        "Respiratory Review": {
            "Respiratory Consultant": 1.0,
            "Nurse": 1.0  
        },
        "Cardiology Review": {
            "Cardiology Consultant": 1.0,
            "Nurse": 1.0  
        },

        "Respiratory review admin": "Respiratory Consultant",
        "Cardiology review admin": "Cardiology Consultant",
    }

    return {
        "Current pathway": {
            "edges": {
                "Start": [("GP appointment", 1.0)],
                "GP appointment": [("Respiratory referral admin", 0.558),("Cardiology referral admin", 0.442)],
                "Respiratory referral admin": [("Respiratory Referral vetting", 1.0)],
                "Cardiology referral admin": [("Cardiology Referral vetting", 1.0)],
                "Respiratory Referral vetting": [("Respiratory clinic", 1.0)],
                "Cardiology Referral vetting": [("Cardiology clinic", 1.0)],
                "Respiratory clinic": [("Respiratory test admin", 1.0)],
                "Cardiology clinic": [("Cardiology test admin", 1.0)],
                "Respiratory test admin": [("Respiratory tests", 1.0)],
                "Cardiology test admin": [("Cardiology tests", 1.0)],
                "Respiratory tests": [("Respiratory Review", 1.0)],
                "Cardiology tests": [("Cardiology Review", 0.565),("Respiratory referral admin", 0.435)],
                "Respiratory Review": [("Respiratory review admin", 1.0)],
                "Cardiology Review": [("Cardiology review admin", 1.0)],
                "Respiratory review admin": [("End", 0.87),("GP appointment", 0.13)],
                "Cardiology review admin": [("End", 0.931),("GP appointment", 0.069)],
            },
            "durations": {
                "GP appointment": (10, 20),
                "Respiratory referral admin": (5, 15),
                "Cardiology referral admin": (5, 15),
                "Respiratory Referral vetting": (3, 5),
                "Cardiology Referral vetting": (3, 5),
                "Respiratory clinic": (25, 35),
                "Cardiology clinic": (25, 35),
                "Respiratory test admin": (5, 15),
                "Cardiology test admin": (5, 15),
                "Respiratory tests": (15, 25),
                "Cardiology tests": (15, 25),
                "Respiratory Review": (20, 30),
                "Cardiology Review": (20, 30),
                "Respiratory review admin": (6, 10),
                "Cardiology review admin": (6, 10),
            },
            "staff_roles": staff_roles_common,
        },

        "Test of change": {
            "edges": {
                "Start": [("GP appointment", 1.0)],
                "GP appointment": [("Respiratory referral admin", 0.5),("Cardiology referral admin", 0.5)],
                "Respiratory referral admin": [("Respiratory Referral vetting", 1.0)],
                "Cardiology referral admin": [("Cardiology Referral vetting", 1.0)],
                "Respiratory Referral vetting": [("Respiratory clinic", 1.0)],
                "Cardiology Referral vetting": [("Cardiology clinic", 1.0)],
                "Respiratory clinic": [("Respiratory tests", 1.0)],
                "Cardiology clinic": [("Cardiology tests", 1.0)],
                "Respiratory test admin": [("Respiratory tests", 1.0)],
                "Cardiology test admin": [("Cardiology tests", 1.0)],
                "Respiratory tests": [("Respiratory Review", 1.0)],
                "Cardiology tests": [("Cardiology Review", 1.0)],
                "Respiratory Review": [("Respiratory review admin", 1.0)],
                "Cardiology Review": [("Cardiology review admin", 1.0)],
                "Respiratory review admin": [("End", 1.0)],
                "Cardiology review admin": [("End", 1.0)],
            },
            "durations": {
                "GP appointment": (10, 20),
                "Respiratory referral admin": (5, 15),
                "Cardiology referral admin": (5, 15),
                "Respiratory Referral vetting": (3, 5),
                "Cardiology Referral vetting": (3, 5),
                "Respiratory clinic": (25, 35),
                "Cardiology clinic": (25, 35),
                "Respiratory test admin": (5, 15),
                "Cardiology test admin": (5, 15),
                "Respiratory tests": (15, 25),
                "Cardiology tests": (15, 25),
                "Respiratory Review": (20, 30),
                "Cardiology Review": (20, 30),
                "Respiratory review admin": (6, 10),
                "Cardiology review admin": (6, 10),
            },
            "staff_roles": staff_roles_common,
        },

        "Potential pathway": {
            "edges": {
                "Start": [("GP appointment", 1.0)],
                "GP appointment": [("Respiratory referral admin", 0.5),("Cardiology referral admin", 0.5)],
                "Respiratory referral admin": [("Respiratory Referral vetting", 1.0)],
                "Cardiology referral admin": [("Cardiology Referral vetting", 1.0)],
                "Respiratory Referral vetting": [("Respiratory clinic", 1.0)],
                "Cardiology Referral vetting": [("Cardiology clinic", 1.0)],
                "Respiratory clinic": [("Respiratory tests", 1.0)],
                "Cardiology clinic": [("Cardiology tests", 1.0)],
                "Respiratory test admin": [("Respiratory tests", 1.0)],
                "Cardiology test admin": [("Cardiology tests", 1.0)],
                "Respiratory tests": [("Respiratory Review", 1.0)],
                "Cardiology tests": [("Cardiology Review", 1.0)],
                "Respiratory Review": [("Respiratory review admin", 1.0)],
                "Cardiology Review": [("Cardiology review admin", 1.0)],
                "Respiratory review admin": [("End", 1.0)],
                "Cardiology review admin": [("End", 1.0)],
            },
            "durations": {
                "GP appointment": (10, 20),
                "Respiratory referral admin": (5, 15),
                "Cardiology referral admin": (5, 15),
                "Respiratory Referral vetting": (3, 5),
                "Cardiology Referral vetting": (3, 5),
                "Respiratory clinic": (25, 35),
                "Cardiology clinic": (25, 35),
                "Respiratory test admin": (5, 15),
                "Cardiology test admin": (5, 15),
                "Respiratory tests": (15, 25),
                "Cardiology tests": (15, 25),
                "Respiratory Review": (20, 30),
                "Cardiology Review": (20, 30),
                "Respiratory review admin": (6, 10),
                "Cardiology review admin": (6, 10),
            },
            "staff_roles": staff_roles_common,
        },
    }

def build_positions(pathway_name):

    if pathway_name == "Current pathway":
        return {
            "Start": (0, 0),
            "GP appointment": (1, 0),

            "Respiratory referral admin": (2, .5), "Respiratory Referral vetting": (2, 1),
            "Cardiology referral admin": (2, -.5), "Cardiology Referral vetting": (2, -1),

            "Respiratory clinic": (3, .75),
            "Cardiology clinic": (3, -.75),

            "Respiratory test admin": (4, 1), "Respiratory tests": (4, .5),
            "Cardiology test admin": (4, -1), "Cardiology tests": (4, -.5),

            "Respiratory Review": (5, 1), "Respiratory review admin": (5, .5),
            "Cardiology Review": (5, -1), "Cardiology review admin": (5, -.5),

            "End": (6, 0),
        }

    elif pathway_name == "Test of change":
        # No GP loop-back → cleaner straight flow
        return {
            "Start": (0, 0),
            "GP appointment": (1, 0),

            "Respiratory referral admin": (2, 1),
            "Cardiology referral admin": (2, -1),

            "Respiratory Referral vetting": (3, 1),
            "Cardiology Referral vetting": (3, -1),

            "Respiratory clinic": (4, 1),
            "Cardiology clinic": (4, -1),

            "Respiratory tests": (5, 1),
            "Cardiology tests": (5, -1),

            "Respiratory Review": (6, 1),
            "Cardiology Review": (6, -1),

            "Respiratory review admin": (7, 1),
            "Cardiology review admin": (7, -1),

            "End": (8, 0),
        }

    elif pathway_name == "Potential pathway":
        # Example: compress branches closer together
        return {
            "Start": (0, 0),
            "GP appointment": (1, 0),

            "Respiratory referral admin": (2, 0.8),
            "Cardiology referral admin": (2, -0.8),

            "Respiratory Referral vetting": (2, 0.8),
            "Cardiology Referral vetting": (2, -0.8),

            "Respiratory clinic": (4, 0.8),
            "Cardiology clinic": (4, -0.8),

            "Respiratory test admin": (5, 2),
            "Cardiology test admin": (5, -2),

            "Respiratory tests": (5, 0.8),
            "Cardiology tests": (5, -0.8),

            "Respiratory Review": (6, 0.8),
            "Cardiology Review": (6, -0.8),

            "Respiratory review admin": (7, 0.8),
            "Cardiology review admin": (7, -0.8),

            "End": (8, 0),
        }

# =========================================================
# Simulation Engine
# =========================================================

class HealthcareDES:
    def __init__(self, env, edges, durations, staff_roles, staff_rates_per_min, counters):
        self.env = env
        self.edges = edges
        self.durations = durations
        self.staff_roles = staff_roles
        self.staff_rates_per_min = staff_rates_per_min  # e.g., {"GP": 2.00, "Administrative": 0.60, ...}
        self.counters = counters

        # Tracking time and cost
        self.time_per_node = defaultdict(float)  # minutes
        self.cost_per_node = defaultdict(float)  # currency
        self.total_cost = 0.0

    def patient(self, name):
        node = "Start"

        while node != "End":
            next_nodes, probs = zip(*self.edges[node])
            node = random.choices(next_nodes, probs)[0]

            # Count the visit to the node (including End)
            self.counters[node] += 1

            # If the node has a duration, simulate time and compute cost
            if node in self.durations:
                t_min, t_max = self.durations[node]
                dur = random.uniform(t_min, t_max)  # minutes
                yield self.env.timeout(dur)

                # Get role mix for this node
            mix = self.staff_roles.get(node, None)

            # Normalize to a list of (role, weight) pairs
            if isinstance(mix, str):
                role_pairs = [(mix, 1.0)]
            elif isinstance(mix, dict):
                role_pairs = list(mix.items())
            else:
                role_pairs = []

            # Accumulate time and cost
            self.time_per_node[node] += dur

            node_cost = 0.0
            for role, weight in role_pairs:
                rate = self.staff_rates_per_min.get(role, 0.0)
                # weight is the fraction of the node duration that role is engaged
                node_cost += dur * weight * rate

            self.cost_per_node[node] += node_cost
            self.total_cost += node_cost

# =========================================================
# Run Simulation
# =========================================================

def run_sim(model, num_patients, staff_rates_per_min):
    edges = model["edges"]
    durations = model["durations"]
    staff_roles = model["staff_roles"]

    counters = {n: 0 for n in edges.keys()}
    counters["End"] = 0  # ensure present

    env = simpy.Environment()
    system = HealthcareDES(env, edges, durations, staff_roles, staff_rates_per_min, counters)

    def Starts():
        for i in range(1, num_patients + 1):
            env.process(system.patient(f"P{i}"))
            # Optional: small fixed inter-arrival time to avoid simultaneous starts
            yield env.timeout(1)  # 1 minute between patients (adjust if needed)

    env.process(Starts())
    
    # Run until all patients have finished
    env.run()

    # Return counters, time, and costs
    results = {
        "counts": system.counters,
        "time_per_node": dict(system.time_per_node),
        "cost_per_node": dict(system.cost_per_node),
        "total_cost": system.total_cost,
    }
    return results

import re

# =========================================================
# UI Controls
# =========================================================

models = get_models()
model_name = st.selectbox("Select Healthcare Pathway Model", list(models.keys()))
model = models[model_name]

# include image based on model selection (optional)
image_location = "C:\\Users\\pxb08145\\OneDrive - University of Strathclyde\\Documents\\Research\\SEISMIC\\Innovation Partnership\\WS1\\Breathlessness Pathway Modelling\\Models"
if model_name == "Current pathway":
    # add image from image_location
    st.image(image_location + "\\Current_pathway_model.png", caption="Current Pathway Diagram")
elif model_name == "Test of change":
    st.image(image_location + "\\ToC_pathway_model.png", caption="Test of Change Pathway Diagram")
elif model_name == "Potential pathway":
    st.image(image_location + "\\Proposed_pathway_model.png", caption="Potential Pathway Diagram")

# Allow user to select exactly how many patients enter
num_patients = st.slider("Number of Patients", 1, 500, 100, step=1)

# --- Helper: extract unique roles from staff_roles (string or dict) ---
def extract_roles_from_staff_map(staff_map):
    roles = set()
    for v in staff_map.values():
        if isinstance(v, str):
            roles.add(v)
        elif isinstance(v, dict):
            roles.update(v.keys())
    return sorted(roles)

# --- Band → £/min (given) ---
band_rates = {
    "Band 2": 0.39,
    "Band 3": 0.43,
    "Band 4": 0.47,
    "Band 5": 0.59,
    "Band 6": 0.72,
    "Band 7": 0.85,
    "Band 8A": 0.96,
    "Band 8B": 1.13,
    "Band 8C": 1.34,
    "Band 8D": 1.55,
    "Band 9": 1.83,
}

# --- Optional mapping to suggest default band for common roles (fallbacks) ---
role_default_band_hint = {
    # add/adjust to taste
    "GP": "Band 8B",
    "Administrative": "Band 3",
    "Technician": "Band 4",
    "Nurse": "Band 6",
    "Cardiology Consultant": "Band 8B",
    "Respiratory Consultant": "Band 8B",
}

# --- Try to parse a band from role name, e.g. "Admin Band 3", "GP (8B)", "Nurse" ---
band_token_to_full = {
    "2": "Band 2", "3": "Band 3", "4": "Band 4", "5": "Band 5", "6": "Band 6", "7": "Band 7",
    "8A": "Band 8A", "8B": "Band 8B", "8C": "Band 8C", "8D": "Band 8D", "9": "Band 9",
}

band_options = list(band_rates.keys())  # for dropdowns, keeps order as defined above

def infer_default_band(role_name: str) -> str:
    # 1) Look for patterns like "Band 3" directly
    m = re.search(r"\bBand\s*(2|3|4|5|6|7|8A|8B|8C|8D|9)\b", role_name, re.IGNORECASE)
    if m:
        token = m.group(1).upper()
        return band_token_to_full.get(token, "Band 6")

    # 2) Look for bracketed band notation, e.g. "(8B)", "(7)", "(6)"
    m2 = re.search(r"\((2|3|4|5|6|7|8A|8B|8C|8D|9)\)", role_name, re.IGNORECASE)
    if m2:
        token = m2.group(1).upper()
        return band_token_to_full.get(token, "Band 6")

    # 3) Use keyword hints (e.g., "Consultant", "Registrar", "Admin", etc.)
    # Try the longest matching hint to avoid generic matches overshadowing specific ones
    for hint, band in sorted(role_default_band_hint.items(), key=lambda x: -len(x[0])):
        if hint.lower() in role_name.lower():
            return band

    # 4) Final fallback
    return "Band 6"

st.subheader("💷 Staff Cost by role")
roles = extract_roles_from_staff_map(model["staff_roles"])

# Let user pick Band per role, compute rate from band_rates
selected_band_for_role = {}
staff_rates_per_min = {}

cols = st.columns(3)
for idx, role in enumerate(roles):
    with cols[idx % 3]:
        default_band = infer_default_band(role)
        chosen_band = st.selectbox(
            f"{role} — Band",
            options=band_options,
            index=band_options.index(default_band) if default_band in band_options else 4,  # default to Band 6
            key=f"band_{role}",
        )
        selected_band_for_role[role] = chosen_band
        staff_rates_per_min[role] = band_rates[chosen_band]

# # (Optional) show a small note with the rate derived from the band
# st.caption("Rates are derived from selected Band: " + ", ".join(
#     [f"{r}: £{staff_rates_per_min[r]:.2f}/min" for r in roles[:5]]
# ) + (" …" if len(roles) > 5 else ""))

def format_role_mix(val):
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        return ", ".join([f"{r}×{w:g}" for r, w in val.items()])
    return ""

def staff_role_costs(df, staff_roles):
    expanded_rows = []

    for _, row in df.iterrows():
        activity = row.name  # because Node is index
        minutes = row["Total Minutes"]
        cost = row["Total Cost (£)"]

        roles = staff_roles.get(activity)

        # Skip if no staff role defined
        if roles is None:
            continue

        # Single role (string)
        if isinstance(roles, str):
            expanded_rows.append({
                "Staff Role": roles,
                "Total Minutes": minutes,
                "Total Cost (£)": cost
            })

        # Multiple roles (dict)
        elif isinstance(roles, dict):
            for role, multiplier in roles.items():
                expanded_rows.append({
                    "Staff Role": role,
                    "Total Minutes": minutes * multiplier,
                    "Total Cost (£)": cost * multiplier
                })

    df_roles = pd.DataFrame(expanded_rows)

    # Aggregate by role
    role_summary = (
        df_roles
        .groupby("Staff Role", as_index=False)
        .agg({
            "Total Minutes": "sum",
            "Total Cost (£)": "sum"
        })
        .sort_values("Total Cost (£)", ascending=False)
    )

    return role_summary

def image_overlay_results(df,image_location, model_name):
    import streamlit as st
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import pandas as pd

    image_path = image_location + "\\Current_pathway_model.png"
    img = mpimg.imread(image_path)

    # Fixed x, y positions for each node (dummy example, in pixels)
    positions = {
        "Start": (120, 250),
        "GP appointment": (700, 450),
        "Respiratory referral admin": (1350, 550),
        "Cardiology referral admin": (1350, 600),
        "Respiratory Referral vetting": (1450, 550),
        "Cardiology Referral vetting": (1450, 600),
        "Respiratory clinic": (1850, 225),
        "Cardiology clinic": (1850, 925),
        "Respiratory test admin": (2600, 225),
        "Cardiology test admin": (2600, 925),
        "Respiratory tests": (2700, 225),
        "Cardiology tests": (2700, 925),
        "Respiratory Review": (3385, 225),
        "Cardiology Review": (3385, 925),
        "Respiratory review admin": (3485, 225),
        "Cardiology review admin": (3485, 925),
        "End": (3700, 250),
    }

    # Add x and y columns based on positions dictionary
    df['x'] = [positions[node][0] for node in df.index]
    df['y'] = [positions[node][1] for node in df.index]

    # # Reset index to have a column for node names
    # df = df.reset_index().rename(columns={"index": "Node"})
    df = df.reset_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(30, 18))

    # Show the image
    ax.imshow(img)

    # Remove axes if desired
    ax.axis('off')

    bar_width = 75  # width of each bar in pixels

    for _, row in df.iterrows():
        height = row['Total Cost (£)']
    
        # Flip sign for specific nodes
        if row['Node'] in ["GP appointment","Respiratory referral admin","Respiratory Referral vetting","Respiratory review admin","Respiratory Review","Respiratory clinic","Respiratory test admin","Respiratory tests"]:
            height = -height  # will extend downwards

        ax.bar(
            x=row['x'], 
            height=height*0.035,  # scale cost to pixels
            width=bar_width, 
            bottom=row['y'],  # start from y coordinate
            color='red', 
            alpha=0.7
        )
        # # optional: label each node
        # ax.text(row['x'], row['y'] + row['Total Cost (£)'] + 5, row['Node'],
        #         ha='center', va='bottom', fontsize=10, color='black')

    st.pyplot(fig)

    return

if st.button("Run Simulation"):
    sim_results = run_sim(model, num_patients, staff_rates_per_min)

    counts = sim_results["counts"]
    time_per_node = sim_results["time_per_node"]
    cost_per_node = sim_results["cost_per_node"]
    total_cost = sim_results["total_cost"]

    # Prepare results DataFrame (nodes with any counts or any time/cost)
    all_nodes = sorted(set(list(counts.keys()) + list(time_per_node.keys()) + list(cost_per_node.keys())))
    data = []
    for n in all_nodes:
        if n in ["Start"]:  # usually we don't report Start as an activity
            continue
        data.append({
            "Node": n,
            "Patients": counts.get(n, 0),
            "Total Minutes": round(time_per_node.get(n, 0.0), 2),
            "Total Cost (£)": round(cost_per_node.get(n, 0.0), 2),
            # "Role": model["staff_roles"].get(n, ""),
            "Roles": format_role_mix(model["staff_roles"].get(n, ""))
        })
    df = pd.DataFrame(data).set_index("Node").sort_index()

    # Summary metrics
    Endd = counts.get("End", 0)
    avg_cost_per_patient = (total_cost / Endd) if Endd > 0 else 0.0

    c1, c2 = st.columns(2)
    c1.metric("Total Cost (£)", f"{total_cost:,.2f}")
    c2.metric("Avg Cost per Patient (£)", f"{avg_cost_per_patient:,.2f}")

    ### Overlay results on pathway image
    image_overlay_results(df, image_location, model_name)

    df_sorted = df.sort_values(by="Total Cost (£)", ascending=False)
    st.subheader("📊 Activity-Level Results")
    st.dataframe(df_sorted, use_container_width=True)

    # # Optional: bar charts for cost and time
    # st.bar_chart(df["Total Cost (£)"])
    # st.bar_chart(df["Total Minutes"])

    role_summary = staff_role_costs(df, model["staff_roles"])
    st.subheader("💷 Cost by Staff Role")
    st.bar_chart(
        role_summary.set_index("Staff Role")["Total Cost (£)"]
    )

    # =========================================================
    # Pathway Visualization
    # =========================================================

    st.subheader("🧭 Pathway Structure")

    # G = nx.DiGraph()
    # for u in model["edges"]:
    #     for v, p in model["edges"][u]:
    #         G.add_edge(u, v, weight=p)

    # # pos = nx.nx_pydot.graphviz_layout(G, prog="dot") 
    # pos = nx.spring_layout(G) 
    # pos = build_positions(model_name)  

    # plt.figure(figsize=(15, 15))
    # nx.draw(G, pos, with_labels=True, node_size=2200, node_color="lightgreen")

    # labels = {(u, v): f"{p:.2f}" for u, v, p in G.edges(data="weight")}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    # st.pyplot(plt)

    G = nx.DiGraph()
    for u in model["edges"]:
        for v, p in model["edges"][u]:
            G.add_edge(u, v, weight=p)

    # pos = nx.nx_pydot.graphviz_layout(G, prog="dot") 
    pos = nx.spring_layout(G)
    pos = build_positions(model_name)

    plt.figure(figsize=(15, 15))

    # ---- Scale edge widths by weight ----
    min_width = 0.5
    max_width = 8

    edge_weights = [G[u][v]["weight"] for u, v in G.edges()]
    edge_widths = [
        min_width + w * (max_width - min_width)
        for w in edge_weights
    ]

    # Draw graph with variable edge widths
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2200,
        node_color="lightgreen",
        width=edge_widths
    )

    # Edge labels
    labels = {(u, v): f"{p:.2f}" for u, v, p in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    st.pyplot(plt)

# =========================================================
# Model Explanation
# =========================================================

with st.expander("ℹ️ How This Simulation Works"):
    st.markdown("""
    This app uses **discrete-event simulation (DES)** to model patient flow.

    - Starts are stochastic (exponential inter-Start time).
    - Transitions follow **probabilities on edges**.
    - Each activity (node) has a **stochastic duration** (uniform between min and max).
    - Each activity is linked to a **staff role** with a **cost per minute**.
    - We track **patients, minutes, and cost per node**, plus **total cost** and **average cost per Endd patient**.

    """)