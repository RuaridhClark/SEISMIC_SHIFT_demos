# Run with streamlit run "C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\GitHub\SEISMIC_SHIFT_demos\SEISMIC_SHIFT_demos\app.py"

import streamlit as st
import simpy
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

st.set_page_config(layout="wide")

# Add image right aligned in the header (optional)
col1, col2 = st.columns([3, 1])
img_location = r"C:\Users\pxb08145\OneDrive - University of Strathclyde\Documents\Research\SEISMIC\Development Phase\Communication\Logo"
with col2:
    st.image(img_location + "\\Logo_concepts_update2.png", width=500)

st.title("NHSL Breathlessness Pathway")

# =========================================================
# Healthcare Pathway Models
# =========================================================

def get_models():

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
            "staff_roles": {
                "GP appointment": "GP",

                "Respiratory referral admin": "Administrative",
                "Cardiology referral admin": "Administrative",

                "Respiratory Referral vetting": "Respiratory Consultant",
                "Cardiology Referral vetting": "Cardiology Consultant",

                "Respiratory clinic": {
                    "Respiratory Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },
                "Cardiology clinic": {
                    "Cardiology Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },

                "Respiratory test admin": "Respiratory Consultant",
                "Cardiology test admin": "Cardiology Consultant",

                "Respiratory tests": "Technician",
                "Cardiology tests": "Technician",

                "Respiratory Review": {
                    "Respiratory Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },
                "Cardiology Review": {
                    "Cardiology Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },

                "Respiratory review admin": "Respiratory Consultant",
                "Cardiology review admin": "Cardiology Consultant",
            },
        },

        "Test of change": {
            "edges": {
                "Start": [("GP appointment", 1.0)],
                "GP appointment": [("Respiratory referral admin", 0.558),("Cardiology referral admin", 0.442)],
                "Respiratory referral admin": [("Respiratory Referral vetting", 1.0)],
                "Cardiology referral admin": [("Cardiology Referral vetting", 1.0)],
                "Respiratory Referral vetting": [("Patient identification", 1.0)],
                "Cardiology Referral vetting": [("Patient identification", 1.0)],
                "Patient identification": [("Breathlessness MDT onboarding", 1.0)],
                "Breathlessness MDT onboarding": [("MDT review", 1.0)],
                "MDT review": [("Test admin", 0.5)],
                "Test admin": [("Diagnostic tests", 1.0)],
                "Diagnostic tests": [("Test review", 1.0)],
                "Test review": [("Patient follow-up", 1.0)],
                "Patient follow-up": [("Respiratory Review", 12/42),("Cardiology Review", 8/42),("Pulmonary rehab", 1/42),("Respiratory physiotherapy", 4/42),("GP practice nurse", 6/42),("End", 10/42)],
                "Respiratory Review": [("Respiratory review admin", 1.0)],
                "Cardiology Review": [("Cardiology review admin", 1.0)],
                "Respiratory review admin": [("End", 1.0)],
                "Cardiology review admin": [("End", 1.0)],
                "Pulmonary rehab": [("End", 1.0)],
                "Respiratory physiotherapy": [("End", 1.0)],
                "GP practice nurse": [("End", 1.0)],
            },
            "durations": {
                "GP appointment": (10, 20),
                "Respiratory referral admin": (5, 15),
                "Cardiology referral admin": (5, 15),
                "Respiratory Referral vetting": (3, 5),
                "Cardiology Referral vetting": (3, 5),
                "Patient identification": (213, 321),
                "Breathlessness MDT onboarding": (18, 28),
                "MDT review": (13, 17),
                "Test admin": (4, 8),
                "Diagnostic tests": (15, 25),
                "Test review": (4, 8),
                "Patient follow-up": (14, 18),
                "Respiratory Review": (20, 30),
                "Cardiology Review": (20, 30),
                "Respiratory review admin": (6, 10),
                "Cardiology review admin": (6, 10),
                "Pulmonary rehab": (10, 20),
                "Respiratory physiotherapy": (10, 20),
                "GP practice nurse": (10, 20),
            },
            "staff_roles": {
                "GP appointment": "GP",

                "Respiratory referral admin": "Administrative",
                "Cardiology referral admin": "Administrative",

                "Respiratory Referral vetting": "Respiratory Consultant",
                "Cardiology Referral vetting": "Cardiology Consultant",

                "Patient identification": "Nurse coordinator",
                "Breathlessness MDT onboarding": "Nurse coordinator",

                "MDT review": {
                    "Respiratory Consultant": 1,
                    "Cardiology Consultant": 1,
                    "Nurse coordinator": 1,
                },

                "Test admin": "Nurse coordinator",
                "Diagnostic tests": "Technician",
                "Test review": {
                    "Respiratory Consultant": 17/(17+8),
                    "Cardiology Consultant": 8/(17+8)
                },

                "Patient follow-up": "Nurse coordinator",

                "Respiratory Review": {
                    "Respiratory Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },
                "Cardiology Review": {
                    "Cardiology Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },

                "Respiratory review admin": "Respiratory Consultant",
                "Cardiology review admin": "Cardiology Consultant",

                "Pulmonary rehab": "Rehabilitation nurse",
                "Respiratory physiotherapy": "Respiratory Physiotherapist",
                "GP practice nurse": "GP practice nurse",
            },
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
            "staff_roles": {
                "GP appointment": "GP",

                "Respiratory referral admin": "Administrative",
                "Cardiology referral admin": "Administrative",

                "Respiratory Referral vetting": "Respiratory Consultant",
                "Cardiology Referral vetting": "Cardiology Consultant",

                "Patient identification": "Nurse coordinator",
                "Breathlessness MDT onboarding": "Nurse coordinator",

                "MDT review": {
                    "Respiratory Consultant": 1,
                    "Cardiology Consultant": 1,
                    "Nurse coordinator": 1,
                },

                "Test admin": "Nurse coordinator",
                "Diagnostic tests": "Technician",
                "Test review": {
                    "Respiratory Consultant": 17/(17+8),
                    "Cardiology Consultant": 8/(17+8)
                },

                "Patient follow-up": "Nurse coordinator",

                "Respiratory Review": {
                    "Respiratory Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },
                "Cardiology Review": {
                    "Cardiology Consultant": 1.0,
                    "Speciality Nurse": 1.0  
                },

                "Respiratory review admin": "Respiratory Consultant",
                "Cardiology review admin": "Cardiology Consultant",

                "Pulmonary rehab": "Rehabilitation nurse",
                "Respiratory physiotherapy": "Respiratory Physiotherapist",
                "GP practice nurse": "GP practice nurse",
            },
        },
    }

def build_positions_nx(pathway_name):

    if pathway_name == "Current pathway":
        return {
            "Start": (-8, 0),
            "GP appointment": (0, 0),

            "Respiratory referral admin": (4, .025), "Respiratory Referral vetting": (4, .05),
            "Cardiology referral admin": (4, -.025), "Cardiology Referral vetting": (4, -.05),

            "Respiratory clinic": (8, .0325),
            "Cardiology clinic": (8, -.0325),

            "Respiratory test admin": (12, .05), "Respiratory tests": (12, .025),
            "Cardiology test admin": (12, -.05), "Cardiology tests": (12, -.025),

            "Respiratory Review": (20, .05), "Respiratory review admin": (20, .025),
            "Cardiology Review": (20, -.05), "Cardiology review admin": (20, -.025),

            "End": (26, 0),
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
            "GP appointment": (5, 0),

            "Respiratory referral admin": (7, 0.8),
            "Cardiology referral admin": (7, -0.8),

            "Respiratory Referral vetting": (7, 0.8),
            "Cardiology Referral vetting": (7, -0.8),

            "Respiratory clinic": (9, 0.8),
            "Cardiology clinic": (9, -0.8),

            "Respiratory test admin": (10, 2),
            "Cardiology test admin": (10, -2),

            "Respiratory tests": (10, 0.8),
            "Cardiology tests": (10, -0.8),

            "Respiratory Review": (11, 0.8),
            "Cardiology Review": (11, -0.8),

            "Respiratory review admin": (12, 0.8),
            "Cardiology review admin": (12, -0.8),

            "End": (13, 0),
        }
    
def build_positions(pathway_name):
    if pathway_name == "Current pathway":
        return {
            "Start": (120, 250),
            "GP appointment": (700, 450),
            "Respiratory referral admin": (1350, 550),
            "Cardiology referral admin": (1350, 600),
            "Respiratory Referral vetting": (1450, 550),
            "Cardiology Referral vetting": (1450, 600),
            "Respiratory clinic": (1850, 225),
            "Cardiology clinic": (1850, 925),
            "Respiratory test admin": (2590, 225),
            "Cardiology test admin": (2590, 925),
            "Respiratory tests": (2710, 225),
            "Cardiology tests": (2710, 925),
            "Respiratory Review": (3370, 225),
            "Cardiology Review": (3370, 925),
            "Respiratory review admin": (3500, 225),
            "Cardiology review admin": (3500, 925),
            "End": (3700, 250),
        }

    elif pathway_name == "Test of change":
        # No GP loop-back → cleaner straight flow
        return {
            "Start": (120, 250),
            "GP appointment": (825, 625),
            "Patient identification": (1550, 625),
            "Breathlessness MDT onboarding": (2280, 625),
            "MDT review": (3025, 430),
            "Test admin": (2900, 790),
            "Diagnostic tests": (3025, 1120),
            "Test review": (3025, 790),
            "Patient follow-up": (3150, 790),
            "Respiratory referral admin": (3750, 225),
            "Cardiology referral admin": (3750, 535),
            "Respiratory Referral vetting": (3850, 225),
            "Cardiology Referral vetting": (3850, 535),
            "Respiratory Review": (3950, 225),
            "Cardiology Review": (3950, 535),
            "Respiratory review admin": (4050, 225),
            "Cardiology review admin": (4050, 535),
            "Pulmonary rehab": (3850, 780),
            "Respiratory physiotherapy": (3950, 780),
            "GP practice nurse": (3900, 1030),
            "End": (3700, 250),
        }

    elif pathway_name == "Potential pathway":
        # Example: compress branches closer together
        return {
            "Start": (120, 250),
            "GP appointment": (700, 450),
            "Respiratory referral admin": (1350, 550),
            "Cardiology referral admin": (1350, 600),
            "Respiratory Referral vetting": (1450, 550),
            "Cardiology Referral vetting": (1450, 600),
            "Respiratory clinic": (1850, 225),
            "Cardiology clinic": (1850, 925),
            "Respiratory test admin": (2590, 225),
            "Cardiology test admin": (2590, 925),
            "Respiratory tests": (2710, 225),
            "Cardiology tests": (2710, 925),
            "Respiratory Review": (3370, 225),
            "Cardiology Review": (3370, 925),
            "Respiratory review admin": (3500, 225),
            "Cardiology review admin": (3500, 925),
            "End": (3700, 250),
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


import pandas as pd

def run_multiple_sims(model, num_patients, staff_rates_per_min, n_sims=10):
    """Run the simulation multiple times and return average results."""
    
    # Lists to store results
    counts_list = []
    time_list = []
    cost_list = []
    total_cost_list = []
    
    for i in range(n_sims):
        sim_results = run_sim(model, num_patients, staff_rates_per_min)
        
        counts_list.append(sim_results["counts"])
        time_list.append(sim_results["time_per_node"])
        cost_list.append(sim_results["cost_per_node"])
        total_cost_list.append(sim_results["total_cost"])
    
    # Convert lists of dicts to DataFrames for easy averaging
    counts_df = pd.DataFrame(counts_list).fillna(0)
    time_df = pd.DataFrame(time_list).fillna(0)
    cost_df = pd.DataFrame(cost_list).fillna(0)
    
    # Compute mean across simulations
    avg_counts = counts_df.mean().to_dict()
    avg_time = time_df.mean().to_dict()
    avg_cost = cost_df.mean().to_dict()
    avg_total_cost = sum(total_cost_list) / n_sims
    
    # Return aggregated results
    avg_results = {
        "counts": avg_counts,
        "time_per_node": avg_time,
        "cost_per_node": avg_cost,
        "total_cost": avg_total_cost,
    }
    
    return avg_results

import re

# =========================================================
# UI Controls
# =========================================================

models = get_models()
model_name = st.selectbox("Select NHSL Breathlessness Pathway Model", list(models.keys()))
model = models[model_name]

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
    "GP": "Band 8B",
    "Administrative": "Band 3",
    "Technician": "Band 4",
    "Speciality nurse": "Band 6",
    "Nurse coordinator": "Band 7",
    "Cardiology Consultant": "Band 8B",
    "Respiratory Consultant": "Band 8B",
    "Rehabilitation nurse": "Band 7",
    "Respiratory Physiotherapist": "Band 7",
    "GP practice nurse": "Band 7",
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

st.subheader("Staff Cost by role")
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
        activity = row.name  # Node
        minutes = row["Total Minutes"]
        cost = row["Total Cost (£)"]

        roles = staff_roles.get(activity)
        if roles is None:
            continue

        if isinstance(roles, str):
            expanded_rows.append({
                "Staff Role": roles,
                "Total Minutes": minutes,
                "Total Cost (£)": cost
            })
        elif isinstance(roles, dict):
            for role, multiplier in roles.items():
                expanded_rows.append({
                    "Staff Role": role,
                    "Total Minutes": minutes * multiplier,
                    "Total Cost (£)": cost * multiplier
                })

    df_roles = pd.DataFrame(expanded_rows)

    # If empty, create empty DataFrame with expected columns
    if df_roles.empty:
        df_roles = pd.DataFrame(columns=["Staff Role", "Total Minutes", "Total Cost (£)"])

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

def image_overlay_results(df, df_roles, image_location, model_name, image_placeholder):
    import streamlit as st
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import pandas as pd
    from matplotlib.patches import Patch

    # Path to the pathway image
    if model_name == "Current pathway":
        image_path = image_location + "\\Current_pathway_model.png"
    elif model_name == "Test of change":
        image_path = image_location + "\\ToC_pathway_model.png"
    elif model_name == "Potential pathway":
        image_path = image_location + "\\Potential_pathway_model.png"

    img = mpimg.imread(image_path)

    # Fixed x, y positions for each node (in pixels)
    positions = build_positions(model_name)

    # Flatten the role-level data into one DataFrame with Node, x, y
    all_roles_df = []
    for node, node_df in df_roles.items():
        node_df = node_df.copy()
        node_df['Node'] = node
        node_df['x'] = positions.get(node, (0, 0))[0]
        node_df['y'] = positions.get(node, (0, 0))[1]
        all_roles_df.append(node_df)

    # Plotting setup
    fig, ax = plt.subplots(figsize=(50, 25))
    ax.imshow(img)
    ax.axis('off')

    bar_width = 75  # width in pixels
    scale = 0.045   # cost-to-pixels scale

    role_color_map = { 
        "Administrative": "#E3D200",  
        "Speciality Consultant": "#F9A664", 
        "GP": "#E6829E",   
        "Speciality Nurse": "#00D2A8",    
        "Nurse coordinator": "#067A63",  
        "GP practice nurse": "#1D7A06",              
        # "Respiratory Consultant": "#F9A664", # "#F99D64", 
        # "Cardiology Consultant": "#F97A64",  # "#F99D64",  
        "Technician": "#20A5CD",                  
    }

    # Loop over each node in df to overlay stacked bars
    for node in df.index:
        bottom_y = positions[node][1]

        # Flip sign for specific nodes (optional)
        if model_name == "Current pathway":
            sign = -1 if node in [
                "GP appointment", "Respiratory referral admin", "Respiratory Referral vetting",
                "Respiratory review admin", "Respiratory Review", "Respiratory clinic",
                "Respiratory test admin", "Respiratory tests"
            ] else 1
        elif model_name == "Test of change" or model_name == "Potential pathway":
            sign = 1 if node in [
                "Diagnostic tests"
            ] else -1

        # Get role-level costs for this node
        role_costs = df_roles.get(node)
        # # Combine respiratory and cardiology consultant into "Speciality Consultant"
        role_costs['Staff Role'] = role_costs['Staff Role'].replace({
            "Respiratory Consultant": "Speciality Consultant",
            "Cardiology Consultant": "Speciality Consultant"
        })
        # if role_costs is None or role_costs.empty:
        #     continue  # skip if no staff role data

        # Aggregate costs by the new Staff Role
        role_costs = role_costs.groupby('Staff Role', as_index=False)['Total Cost (£)'].sum()

        # Stack bars by staff role
        for _, r in role_costs.iterrows():
            height = r['Total Cost (£)'] * scale * sign
            ax.bar(
                x=positions[node][0],
                height=height,
                width=bar_width,
                bottom=bottom_y,
                color=role_color_map.get(r['Staff Role'], 'gray'),
                alpha=1,
                edgecolor = '#1C2747',   # outline color
                linewidth = 4.5        # thickness of the outline
            )
            bottom_y += height

    # Create legend handles
    legend_handles = [Patch(color=color, label=role) for role, color in role_color_map.items()]

    # Place legend below the plot, horizontally
    leg = ax.legend(
        handles=legend_handles,
        loc='upper center',       # anchor point of legend
        bbox_to_anchor=(0.5, -0.05),  # 0.5 = center, -0.05 = below axes
        ncol=len(role_color_map), # number of columns = number of roles
        fontsize=35,
        frameon=True,
        framealpha=0.9
    )
    for text in leg.get_texts():
        text.set_color('#1C2747')  # replace with your desired color

    # ax.set_title(str(model_name), fontsize=80, loc='left')

    # Show the figure in Streamlit
    image_placeholder.pyplot(fig,width="content")

    return

def role_cost_barchart(df, model_staff_roles):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    # Compute role-level costs
    role_summary = staff_role_costs(df, model_staff_roles)

    # Sort by cost for better visualization
    role_summary = role_summary.sort_values("Total Cost (£)", ascending=False)

    # Updated color map
    role_color_map = {
        "Nurse": "#00D2A8",                 
        "Respiratory Consultant": "#F9A664",
        "Cardiology Consultant": "#F97A64",  
        "Administrative": "#E3D200",        
        "Technician": "#20A5CD",            
        "GP": "#E6829E",                     
    }

    edge_col = '#1C2747'  # dark blue for axes and bar outlines

    # Map colors to the roles in role_summary
    colors = [role_color_map.get(role, "gray") for role in role_summary["Staff Role"]]

    # Plot using Matplotlib
    fig, ax = plt.subplots(figsize=(20,6))
    bars = ax.bar(role_summary["Staff Role"], 
                  role_summary["Total Cost (£)"], 
                  color=colors,
                  edgecolor = edge_col,   # outline color
                  linewidth = 1        # thickness of the outline
                )

    # Rotate x-axis labels to avoid overlap
    plt.xticks(rotation=45, ha='right', fontsize=16, color=edge_col)
    plt.yticks(fontsize=14, color=edge_col)

    # Customize axis lines (spines) color
    for spine in ax.spines.values():
        spine.set_color(edge_col)
        spine.set_linewidth(1.5)
        
    # Customize axes and title
    ax.set_ylabel("Total Cost (£)", fontsize=16, color=edge_col)
    ax.set_xlabel("Staff Role", fontsize=16, color=edge_col)
    # ax.set_title("Cost by Staff Role", fontsize=14, loc='center')

    # axis box off
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # # Create legend
    # legend_handles = [Patch(color=color, label=role) for role, color in role_color_map.items() if role in role_summary["Staff Role"].values]
    # ax.legend(handles=legend_handles, loc='upper right', fontsize=12)

    # Show in Streamlit
    st.pyplot(fig, width="content")
    return

# Define the button first
run_sim_clicked = st.button("Run Simulation")

st.subheader(model_name)

# Create a placeholder for the image / plot
image_placeholder = st.empty()  

# include image based on model selection (optional)
image_location = "C:\\Users\\pxb08145\\OneDrive - University of Strathclyde\\Documents\\Research\\SEISMIC\\Innovation Partnership\\WS1\\Breathlessness Pathway Modelling\\Models"
if model_name == "Current pathway":
    # add image from image_location
    image_placeholder.image(image_location + "\\Current_pathway_model.png", caption="Current Pathway Diagram")
elif model_name == "Test of change":
    image_placeholder.image(image_location + "\\ToC_pathway_model.png", caption="Test of Change Pathway Diagram")
elif model_name == "Potential pathway":
    image_placeholder.image(image_location + "\\Proposed_pathway_model.png", caption="Potential Pathway Diagram")

if run_sim_clicked:
    # sim_results = run_sim(model, num_patients, staff_rates_per_min)
    sim_results = run_multiple_sims(model, num_patients, staff_rates_per_min, n_sims=10)

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

    # Node-level staff role cost breakdown

    # df is the node-level summary, staff_roles is a dict of roles per node
    df_roles = {}

    for node in df.index:
        node_df = df.loc[[node]]
        node_role_summary = staff_role_costs(node_df, model["staff_roles"])
        df_roles[node] = node_role_summary

    ### Overlay results on pathway image
    image_overlay_results(df, df_roles, image_location, model_name, image_placeholder)

    role_cost_barchart(df, model["staff_roles"])

    df_sorted = df.sort_values(by="Total Cost (£)", ascending=False)
    st.subheader("Activity-Level Results")
    st.dataframe(df_sorted, use_container_width=True)

    # =========================================================
    # Pathway Visualization
    # =========================================================

    st.subheader("Technical Pathway Model")

    from matplotlib.patches import FancyBboxPatch

    G = nx.DiGraph()
    for u in model["edges"]:
        for v, p in model["edges"][u]:
            G.add_edge(u, v, weight=p)

    pos = build_positions_nx(model_name)

    fig, ax = plt.subplots(figsize=(15, 15))

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
        with_labels=False,
        node_size=3000,
        width=edge_widths,
        edge_color='#1C2747',
        node_color='lightgray',
        arrows=True,          
        arrowsize=25 
    )

    # Adjust node labels to use linebreaks if too long
    for node, (x, y) in pos.items():
        label = node
        if len(label) > 13:
            # Insert linebreaks for long labels
            label = "\n".join(label.split())
        ax.text(x, y, label, ha="center", va="center", fontsize=10, color="#1C2747")

    # Edge labels
    labels = {(u, v): f"{p:.2f}" for u, v, p in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    # # Draw custom nodes as rounded rectangles
    # for node, (x, y) in pos.items():
    #     width = 1
    #     height = 0.08
    #     boxstyle = "round,pad=0.02,rounding_size=0.05"
    #     node_color = '#1C2747'  # customize per node if needed
        
    #     bbox = FancyBboxPatch(
    #         (x - width/2, y - height/2), width, height,
    #         boxstyle=boxstyle,
    #         linewidth=2,
    #         facecolor=node_color,
    #         edgecolor="#1C2747",
    #         mutation_aspect=1.0
    #     )
    #     ax.add_patch(bbox)
        
    #     # Add node label
    #     ax.text(x, y, node, ha="center", va="center", fontsize=12, color="white")
        
    st.pyplot(plt, width="content")

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