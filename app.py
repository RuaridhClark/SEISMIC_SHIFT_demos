import streamlit as st
import simpy
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🏥 Healthcare Pathway Discrete Event Simulation")

# =========================================================
# Healthcare Pathway Models
# =========================================================

def get_models():
    return {
        "Emergency Department": {
            "edges": {
                "Arrival": [("Triage", 1.0)],
                "Triage": [("Assessment", 0.85), ("Discharge", 0.15)],
                "Assessment": [("Treatment", 0.7), ("Admit", 0.3)],
                "Treatment": [("Discharge", 1.0)],
                "Admit": [("Inpatient Care", 1.0)],
                "Inpatient Care": [("Discharge", 1.0)]
            },
            "durations": {
                "Triage": (3, 6),
                "Assessment": (10, 20),
                "Treatment": (20, 40),
                "Inpatient Care": (300, 600)
            }
        },

        "Cancer Diagnostic Pathway": {
            "edges": {
                "Arrival": [("GP Referral", 1.0)],
                "GP Referral": [("Imaging", 0.6), ("Blood Test", 0.4)],
                "Imaging": [("Biopsy", 0.7), ("Discharge", 0.3)],
                "Blood Test": [("Imaging", 0.5), ("Discharge", 0.5)],
                "Biopsy": [("MDT Review", 1.0)],
                "MDT Review": [("Treatment", 0.8), ("Discharge", 0.2)],
                "Treatment": [("Discharge", 1.0)]
            },
            "durations": {
                "GP Referral": (60, 120),
                "Imaging": (30, 90),
                "Blood Test": (15, 30),
                "Biopsy": (45, 90),
                "MDT Review": (60, 180),
                "Treatment": (300, 900)
            }
        }
    }


# =========================================================
# Simulation Engine
# =========================================================

class HealthcareDES:
    def __init__(self, env, edges, durations, counters):
        self.env = env
        self.edges = edges
        self.durations = durations
        self.counters = counters

    def patient(self, name):
        node = "Arrival"

        while node != "Discharge":
            next_nodes, probs = zip(*self.edges[node])
            node = random.choices(next_nodes, probs)[0]

            self.counters[node] += 1

            if node in self.durations:
                t_min, t_max = self.durations[node]
                yield self.env.timeout(random.uniform(t_min, t_max))


# =========================================================
# Run Simulation
# =========================================================

def run_sim(model, sim_time, arrival_rate):

    edges = model["edges"]
    durations = model["durations"]

    counters = {n: 0 for n in edges.keys()}
    counters["Discharge"] = 0

    env = simpy.Environment()
    system = HealthcareDES(env, edges, durations, counters)

    def arrivals():
        i = 0
        while env.now < sim_time:
            i += 1
            env.process(system.patient(f"P{i}"))
            yield env.timeout(random.expovariate(arrival_rate))

    env.process(arrivals())
    env.run(until=sim_time)

    return counters


# =========================================================
# UI Controls
# =========================================================

model_name = st.selectbox("Select Healthcare Pathway Model", list(get_models().keys()))
model = get_models()[model_name]

sim_time = st.slider("Simulation Duration (minutes)", 500, 5000, 2000, step=100)
arrival_rate = st.slider("Arrival Rate (patients per minute)", 0.01, 0.3, 0.08, step=0.01)

if st.button("Run Simulation"):
    results = run_sim(model, sim_time, arrival_rate)

    st.subheader("📊 Patient Counts at Each Activity")

    df = pd.DataFrame.from_dict(results, orient="index", columns=["Patients"])
    st.dataframe(df, use_container_width=True)

    st.bar_chart(df)

    # =========================================================
    # Pathway Visualization
    # =========================================================

    st.subheader("🧭 Pathway Structure")

    G = nx.DiGraph()

    for u in model["edges"]:
        for v, p in model["edges"][u]:
            G.add_edge(u, v, weight=p)

    pos = nx.spring_layout(G, seed=5)

    plt.figure(figsize=(9, 6))

    nx.draw(G, pos, with_labels=True, node_size=2200, node_color="lightgreen")

    labels = {(u, v): f"{p:.2f}" for u, v, p in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

    st.pyplot(plt)

# =========================================================
# Model Explanation
# =========================================================

with st.expander("ℹ️ How This Simulation Works"):
    st.markdown("""
    This app uses **discrete-event simulation (DES)** to model patient flow.
    
    - Each patient arrives stochastically.
    - They move through activities based on **transition probabilities**.
    - Each activity takes a **random amount of time**.
    - The model tracks **how many patients reach each activity**.
    
    This is ideal for:
    - Pathway redesign
    - Service planning
    - Bottleneck analysis
    - Demand modelling
    """)