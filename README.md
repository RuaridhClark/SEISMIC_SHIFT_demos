# SEISMIC SHIFT Breathlessness Pathway Simulator

A **Streamlit app** for modelling and comparing different configurations of a breathlessness diagnostic pathway.

This tool was developed as part of the **SEISMIC SHIFT project** in collaboration with **NHS Lanarkshire** to explore how pathway redesign may affect **staff workload and cost**.

---

## Overview

This application simulates various pathways for patients presenting with breathlessness in NHS Lanarkshire.

A **Discrete Event Simulation (DES)** model is used to compare potential service configurations with users able to modify staff bands and activity durations.

---

## Features

- Simulate patient flow through a breathlessness pathway  
- Adjust **activity durations** (min–max time ranges)  
- Assign **staff roles to NHS pay bands**  
- Estimate **staff time and cost per activity**  
- Compare **previous simulation runs**  

---

## How the Simulation Works

This app uses **discrete-event simulation (DES)** to model resources in a patient pathway.

- Each patient is simulated individually, moving through the pathway according to defined transitions and durations.
- Transitions follow probabilities that a given patient will move from one activity to another. These probabilities are based on findings from a test of change run in NHS Lanarkshire (2024).
- Each activity takes a variable amount of time within bounds set as a defined minimum and maximum duration.
- Each activity is linked to a staff role with their associated cost per minute.
- Ten simulations are run before reporting on simulated patient journeys, time at each activity, and cost

---
