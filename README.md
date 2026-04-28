# SCHIR

An active simulation of the SIR+ model, including the Carrier (C) and Hybrid (H) states.

**Please Note:** This project requires **NumPy** and **Matplotlib** to run properly. Make sure to install these packages using your preferred console or environment (such as Anaconda Prompt, PowerShell, or Terminal). If you prefer not to install these packages, you may comment out the NumPy/Matplotlib import lines and any code that depends on them.

---

## Overview

The traditional SIR model (Susceptible, Infected, Removed/Recovered) is often used to simulate disease spread — including fictional scenarios like a zombie outbreak.  
The **SCHIR** model extends SIR by adding two additional states:

- Carrier (C)  
- Hybrid (H)

These states introduce more realistic movement, partial recovery, and multi‑stage infection behavior.

---

## State Definitions

### Susceptible (S)
Normal individuals who are not infected. They can transition into Carrier, Hybrid, Infected, or Removed. This state has the most possible transitions.

### Carrier (C)
Individuals who are infected but asymptomatic. They can infect Susceptibles but can only transition to Removed. Carriers die immediately when their progression reaches 10, and they also have a random chance of dying based on their transition rate.

### Hybrid (H)
A middle state between Susceptible and Infected. Hybrids may recover back to Susceptible or progress toward becoming Infected. This state adds more movement and recovery dynamics to the model while preserving the Removed state.

### Infected (I)
A state from the original SIR model. Infected individuals spread the “virus.” With the addition of Hybrids, they now have a small chance of transitioning into a Hybrid before potentially recovering.

### Removed (R)
Represents individuals who have died or otherwise left the simulation. All individuals eventually end up in this state.

---

<img width="829" height="686" alt="Screenshot 2026-04-28 140909" src="https://github.com/user-attachments/assets/05664b9b-7ac6-4029-b213-49becbfd9b4e" />


## Transition Rates

### Susceptible Transitions
**Alpha (S → I):** 0.018  
**Theta (S → C):** 0.006  
**Omega (S → H):** 0.010  
**Gamma (S → R):** 0.001  

### Carrier Transitions
**Iota (C → R):** 0.003  

### Hybrid Transitions
**Delta (H → S):** 0.020  
**Eta (H → I):** 0.012  
**Zeta (H → R):** 0.005  

### Infected Transitions
**Epsilon (I → H):** 0.003  
**Beta (I → R):** 0.008  

## Features

- Full SCHIR (Susceptible–Carrier–Hybrid–Infected–Removed) simulation model  
- Agent-based movement with Manhattan-distance interactions  
- Randomized infection, recovery, and death events  
- Daily population tracking and graph generation  
- Deterministic “Expected Statistics” model for comparison  
- Adjustable simulation length and transition rates  
- Modular class-based design for easy modification  

