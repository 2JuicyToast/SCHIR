# SCHIR
An active sim for the SIR+ model, including Carrier(C) and Hybrid (H).

The SIR model (Susceptible, Infected, and Removed or Recovered) is a model used to simulate a Zombie Apocalypse. The SCHIR model is a SIR+ model with the added states Carrier and Hybrid.
To define each state:
-----
# Susceptible:
Susceptibles are normal people who aren't infected. From this state, they can go to Carrier, Hybrid, Infected, and Removed. This is the state with the most transitions.

# Carrier 
Carriers are infected, yet do not show symptoms. They can infect Susceptibles, but can only transition to removed. When their progression reaches 10, they die immediately. They also have a chance of dying randomly based on their transition rate.

# Hybrid 
Hybrids are in a middle state between Susceptible and Infected. They have a chance of recovering, but if they don't recover, they move closer to becoming infected. This State was added to introduce more movement into the SIR model, and also provide a means of recovery while keeping the Removed state.

# Infected
Infected is a state from the original SIR model. They represent those who have caught the "virus" in the model. They infect others, and before could only die. However, with the added Hybrid class, they have a small chance of becoming Hybrid, and from there, they can recover to Susceptible.

# Removed
For this model, R was chosen to represent Removed. Anyone who dies within the simulation will be removed, and they will no longer be part of the simulation. This end-state is where everyone in the simulation will eventually end up.

# Susceptible Transitions
The following transitions and rates are listed below

**Aalpha (S-I)**: 0.018  
**Theta (S-C)**: 0.006   
**Omega (S-H)**: 0.010   
**Gamma (S-R)** 0.001

# Carrier Transitions
The transitions and rates are listed below

**Iota (C-R)**: 0.003

# Hybrid Transitions
The transitions and rates are listed below

**Delta (H-S)**: 0.020  
**Eta (H-I)**: 0.012  
**Zeta (H-R)**: 0.005

# Infected Transitions
The transitions and rates are listed below

**Epsilon (I-H)**: 0.003  
**Beta (I-R)**: 0.008   
