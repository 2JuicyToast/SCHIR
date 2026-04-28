# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:11:07 2026

@author: Bacon
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import time

susceptible_list = []
carrier_list = []
hybrid_list = []
infected_list = []
removed_list = []

'''
function expected_statistics(S, C, H, I, R, Time)
    define transition rates:
        
        rate_S_to_I, rate_S_to_R, rate_S_to_H, rate_S_to_C
        rate_I_to_R, rate_I_to_H
        rate_H_to_S, rate_H_to_I, rate_H_to_R
        rate_C_to_R
        
    current_time = []
    s_count = [S]
    c_count = [C]
    h_count = [H]
    i_count = [I]
    r_count = [R]
    
    for each unit of time from 0 including Time:
        transitioned_S_to_I = S * rate_S_to_I
        transitioned_I_to_R = I * rate_I_to_R
        transitioned_S_to_R = S * rate_S_to_R

        transitioned_S_to_H = S * rate_S_to_H
        transitioned_I_to_H = I * rate_I_to_H

        transitioned_H_to_S = H * rate_H_to_S
        transitioned_H_to_I = H * rate_H_to_I
        transitioned_H_to_R = H * rate_H_to_R

        transitioned_S_to_C = S * rate_S_to_C
        transitioned_C_to_R = C * rate_C_to_R

        S = S - (transitioned_S_to_I + transitioned_S_to_R + transitioned_S_to_H + transitioned_S_to_C) + transitioned_H_to_S
        C = C + transitioned_S_to_C - transitioned_C_to_R
        H = H + (transitioned_S_to_H + transitioned_I_to_H) - (transitioned_H_to_S + transitioned_H_to_I + transitioned_H_to_R)
        I = I + (transitioned_S_to_I + transitioned_H_to_I) - transitioned_I_to_R - transitioned_I_to_H
        R = R + transitioned_S_to_R + transitioned_I_to_R + transitioned_H_to_R + transitioned_C_to_R
        
        add S to s_list
        add C to c_list
        add H to h_list
        add I to i_list
        add R to r_list
    
        add t to current_time[]
        
    return(S, C, H, I, R, Time)
'''

ALPHA   = 0.018   # (Susceptible becomes Infected)
BETA    = 0.008   # (Infected becomes Removed)
GAMMA   = 0.001   # (Susceptible becomes Removed)

OMEGA   = 0.010   # (Susceptible becomes Hybrid)
EPSILON = 0.003   # (Infected becomes Hybrid)

DELTA   = 0.020   # (Hybrid recovers to Susceptible)
ETA     = 0.012   # (Hybrid becomes Infected)
ZETA    = 0.005   # (Hybrid becomes Removed)

THETA   = 0.006   # (Susceptible becomes Carrier)
IOTA    = 0.003   # (Carrier becomes Removed)

def expected_statistics(S, C, H, I, R, Time):
    # plotting list
    current_time = [0]
    s_count = [S]
    c_count = [C]
    h_count = [H]
    i_count = [I]
    r_count = [R]
    
    for t in range(Time + 1):
        # base transitions
        aTrans = S * ALPHA
        bTrans = I * BETA
        gTrans = S * GAMMA
          
        # to hybrid transitions
        oTrans = S * OMEGA
        epTrans = I * EPSILON
        
        # from hybrid transitions
        dTrans = H * DELTA
        etTrans = H * ETA
        zTrans = H * ZETA
        
        # carrier transition
        tTrans = S * THETA
        iTrans = C * IOTA 
        
        S = max(S - (aTrans + gTrans + oTrans + tTrans) + dTrans, 0)
        C = max(C + tTrans - iTrans, 0)
        H = max(H + (oTrans + epTrans) - (dTrans + etTrans + zTrans), 0)
        I = max(I + (aTrans + etTrans) - bTrans - epTrans, 0)
        R = max(R + bTrans + gTrans + zTrans + iTrans, 0)
        
        # update list
        current_time.append(t)
        s_count.append(S)
        c_count.append(C)
        h_count.append(H)
        i_count.append(I)
        r_count.append(R)
        
    # create plot 
    plt.plot(current_time, s_count, color= 'blue', label='Susceptible')
    plt.plot(current_time, c_count, color= 'yellow', label='Carrier')
    plt.plot(current_time, h_count, color= 'orange', label='Hybrid')
    plt.plot(current_time, i_count, color= 'green', label='Infected')
    plt.plot(current_time, r_count, color= 'red', label='Removed')
    
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title("Expected Statistics")
    plt.legend()
    plt.show()
  
    return (int(S), int(C), int(H), int(I), int(R), t)

'''
function find_person_in(state, name)
    index = 0
    
    for each person in a state:
        if person's name is equal to name:
            return index
        
        index += 1
        
   else:
        return none
'''

def find_person_in(state_list, name):
    index = 0
    
    for person in state_list:
        if person.name == name:
            return index
        
        index += 1
        
    return None

'''
function find_person(name)
    for each state in [susceptible, carrier, hybrid, infected, removed]:
        index = 0
        for each person in state:
            if person's name is equal to name:
                return (state, index)
            index += 1

    if no person was found:
        return none
'''

def find_person(name):
    states = [
        ("susceptible", susceptible_list),
        ("carrier", carrier_list),
        ("hybrid", hybrid_list),
        ("infected", infected_list),
        ("removed", removed_list),
    ]

    for state_name, state_list in states:
        # enumerate provides both index AND a object
        for index, person in enumerate(state_list):
            if person.name == name:
                return state_name, index  # string name and index

    return None

''' 
procedure manhattan(a,b)
    return (a.x_pos - b.x_pos) + (a.y_pos - b.y_pos))
'''

def manhattan(a, b): # return distance between two people
    # use abs to account for negative position
    return abs(a.x_pos - b.x_pos) + abs(a.y_pos - b.y_pos)

'''
CLASS Person
    Attributes: 
        Name
        Health 
        Energy
        Strength
        x_pos
        y_pos
        
    Constructors(inputName):
        name = inputName
        health = 100
        energy = 100
        strength = null
        x_pos = random integer between 0 and 200
        y_pos = random integer between 0 and 200
        
    Methods:
        procedure move:
            x_pos = random integer between 0 and 200
            y_pos = random integer between 0 and 200
            
        procedure attack(target):
            if this person's energy >= 5:
                output that this person is attacking target
                lower target's health
                subtract 5 from this person's energy
                
            else:
                output that this person doesnt have enough energy to attack
            
        procedure takeDamage(attacker):
            subtract attacker's strength from this person's health
            
            if this person's health <= 0:
                this person's health = 0
                call transition()
            
        procedure rest:
            output that this Person is resting
            energy += 10
'''

class Person(object):
    def __init__(self, name): # constructors
        self.name = name
        self.health = 100
        self.energy = 100
        self.strength = None
        self.x_pos = random.randint(0,200)
        self.y_pos = random.randint(0,200)
        
    def move(self): # move to new location
        self.x_pos = random.randint(0,200)
        self.y_pos = random.randint(0,200)
        
    def attack(self, target): 
        if self.energy >= 5:
            print(self.name, "attacks", target.name, "!")
            target.takeDamage(self)
            self.energy -= 5
            
        else:
            print(self.name, "is too tired to attack", target.name)
            
    def takeDamage(self, attacker):
        self.health -= attacker.strength
        
        if self.health <= 0:
            self.health = 0
            self.transition()
        
    def rest(self):
        print(self.name, " is resting.")
        self.energy += 10
        
'''
CLASS Susceptible inherits Person
    Attributes:
        infection

    Constructors:
        add to susceptible list
        strength = random integer between 5 and 15
        infection = 0
        
    Methods:
        procedure move:
            x_pos = random integer between 0 and 200
            y_pos = random integer between 0 and 200

            if distance to any infected person is <= 10:
                call encounter(infectedPerson)

        procedure run:
            output that this susceptible is running
            call move()
            energy = energy - 25

        procedure encounter(target):
            if this susceptible has less than 50 energy:
                call attack(target)
            
            else:
                call run()

        procedure takeDamage(attacker):
            subtract attacker's strength from this susceptible's health

            if this susceptibles's health <= 0:
                this susceptibles's health = 0
                call transition()
                
            else if attacker is Infected or attacker is Carrier:
                if infection >= 100:
                    infection = 100
                    call transition()

        procedure transition:
            if infection == 0 and this susceptible's health is above 0:
                return

            else if infection > 75 and health > 0:
                move this susceptible to Infected
                return

            else if this susceptible's health == 0:
                move this susceptible to Removed
                return
            
            else:
                convert infection (0–100) into a decimal:
                    scale = infection / 100
    
                if infection >= 50 and infection < 75:
                    if random number between 0.0 and 1.0 is less than rate_S_to_I * (scale * 4):
                        move this susceptible to Infected
                        return
                otherwise:
                    if random number between 0.0 and 1.0 is less than rate_S_to_I * scale:
                        move this susceptible to Infected
                        return
    
                if infection >= 25 and infection < 50:
                    if random number between 0.0 and 1.0 is less than rate_S_to_H * (scale * 3):
                        move this susceptible to Hybrid
                        return
                otherwise:
                    if random number between 0.0 and 1.0 is less than rate_S_to_H * scale:
                        move this susceptible to Hybrid
                        return
    
                if infection >= 10 and infection < 25:
                    if random number between 0.0 and 1.0 is less than rate_S_to_C * (scale * 2):
                        move this susceptible to Carrier
                        return
                otherwise:
                    if random number between 0.0 and 1.0 is less than rate_S_to_C * scale:
                        move this susceptible to Carrier
                        return
'''

class Susceptible(Person):
    def __init__(self, name): # constructors
        super().__init__(name)
        susceptible_list.append(self)
        self.strength = random.randint(5,15)
        self.infection = 0
        
    def move(self): # move to new location
        self.x_pos = random.randint(0,200)
        self.y_pos = random.randint(0,200)
        
        for i in infected_list: # trigger encounter w/ nearby infected
            if manhattan(self, i) <= 10:
                self.encounter(i)

    def run(self): # escape encounter
        print(self.name, "runs!")
        self.move()
        self.energy -= 25

    def encounter(self, target): # decides if Suceptible can run
        if self.energy < 50:
            self.attack(target)
        
        else:
            self.run()
            
    def takeDamage(self, attacker):
        self.health -= attacker.strength
        
        if self.health <= 0:
            self.health = 0
            self.transition()
        
        elif isinstance(attacker, Infected) or isinstance(attacker,Carrier):
            if self.infection >= 100:
                self.infection = 100
                self.transition()
        
    def transition(self):
        if self.infection == 0 and self.health > 0:
            return
        
        elif self.infection > 75 and self.health > 0:
            new = Infected(self.name)
            susceptible_list.remove(self)
            return
            
        elif self.health == 0:
            new = Removed(self.name, "Susceptible", "Killed")
            susceptible_list.remove(self)
            return
            
        else:
            scale = self.infection / 100  # infection 0–100 → 0.0–1.0
        
            # random.random() = number between 0.0 and 1.0
            
            # S -> I (Alpha)
            # boosted infection chance
            if self.infection >= 50 and self.infection < 75:
                if random.random() < ALPHA * (scale * 4):
                    new = Infected(self.name)
                    susceptible_list.remove(self)
                    return
            else:
                if random.random() < ALPHA * scale:
                    new = Infected(self.name)
                    susceptible_list.remove(self)
                    return
            
            # S -> H (Omega)
            # boosted hybrid chance
            if self.infection >= 25 and self.infection < 50:
                if random.random() < OMEGA * (scale * 3):
                    new = Hybrid(self.name)
                    susceptible_list.remove(self)
                    return
            else:
                if random.random() < OMEGA * scale:
                    new = Hybrid(self.name)
                    susceptible_list.remove(self)
                    return
            
            # S -> C (Theta)
            # boosted carrier chance
            if self.infection >= 10 and self.infection < 25:
                if random.random() < THETA * (scale * 2):
                    new = Carrier(self.name)
                    susceptible_list.remove(self)
                    return
        
            else:
                if random.random() < THETA * scale:
                    new = Carrier(self.name)
                    susceptible_list.remove(self)
                    return
                
'''        
CLASS Carrier inherits Person
    Attributes:
        progression
        basePotency
        severity

    Constructors:
        add to carrier list
        strength    = random integer between 10 and 20
        basePotency = random integer between 5 and 10
        progression = 1
        severity    = 0.1

    Methods:
        procedure infect(target):
            currentPotency = basePotency + progression
            increase target's infection by currentPotency

        procedure attack(target):
            if this carrier's energy >= 5:
                output that this carrier is attacking target
                lower target's health by this carrier's strength
                subtract 5 from this carrier's energy
                
                if target is Susceptible or target is Hybrid:
                    call infect(target)
                
            else:
                output that this carrier doesnt have enough energy to attack

        procedure takeDamage(attacker):
            subtract attacker's strength from this carrier's health
            
            if this carriers's health <= 0:
                this carriers's health = 0
                call transition()

            if attacker is Infected:
                scaledPotency = attacker's potency / 100
                increase this carrier's progression by scaledPotency
                
                if progression >= 10:
                    progression = 10
                    call transition()

        procedure progressionIncrease:
            progression = progression + severity
            
            if severity < 0.5:
                severity = severity + 0.1

            if progression >= 10:
                progression = 10
                call transition()

        procedure transition:
            if this carrier's health == 0:
                move this carrier to Removed
                return

            else if progression == 10:
                move this carrier to Removed
                return

            else if random number between 0.0 and 1.0 is less than rate_C_to_R + severity:
                move this carrier to Removed
                return
            
            return   
'''

class Carrier(Person):
    def __init__(self, name): # constructors
        super().__init__(name)
        carrier_list.append(self)
        self.strength = random.randint(10,20)
        self.basePotency = random.randint(5,10)
        self.progression = 1
        self.severity    = 0.1
        
    def infect(self, target):
        currentPotency = self.basePotency + self.progression
        target.infection += currentPotency
        
    def attack(self, target): 
        if self.energy >= 5:
            print(self.name, "attacks", target.name, "!")
            target.takeDamage(self)
            self.energy -= 5
            
            if isinstance(target, Susceptible) or isinstance(target, Hybrid):
                self.infect(target)
        
        else: 
            print(self.name, "is too tired to attack", target.name)
            
    def takeDamage(self, attacker):
        self.health -= attacker.strength
        
        if self.health <= 0:
            self.health = 0
            self.transition()
        
        if isinstance(attacker, Infected):
            scaledPotency = attacker.potency/100 # scales to carrier progression
            self.progression = min(10, self.progression + scaledPotency) # caps progression at 10
            
            if self.progression >= 10:
                self.progression = 10
                self.transition()
            
    def progressionIncrease(self): 
        self.progression = self.progression + self.severity
        
        if self.severity < 0.5:
            self.severity = self.severity + 0.1

        if self.progression >= 10:
            self.progression = 10
            self.transition()
            
    def transition(self):
        if self.health == 0:
            new = Removed(self.name, "Carrier", "Killed")
            carrier_list.remove(self)
            return

        elif self.progression >= 10:
            new = Removed(self.name, "Carrier", "Disease")
            carrier_list.remove(self)
            return

        elif random.random() < IOTA + self.severity:
            new = Removed(self.name, "Carrier", "Disease")
            carrier_list.remove(self)
            return

        return   

'''
CLASS Hybrid inherits Person
    Attributes:
        recoveryChance
        infection
        
    Constructors:
        add to hybrid list
        strength = random integer between 15 and 25
        infection = 30
        recoveryChance = 100 - infection 
        
    Methods:
        procedure takeDamage(attacker):
            subtract attacker's strength from this hybrids's health
            
            if this hybrid's health <= 0:
                this hybrid's health = 0
                call transition()
            
            else if attacker is Infected or attacker is Carrier:
                if infection >= 100:
                    infection = 100
                    call transition()
                    
                recoveryChance = 100 - infection 
                
        procedure infectionGrowth:
            infection += 5
            
            if infection >= 100:
                infection = 100
                call transition()
            
        procedure transition:
            recoveryChance = 100 - infection  
            rScale = recoveryChance / 100
            iScale = infection / 100
            
            if this hybrid's health == 0:
                move this hybrid to Removed
                return
            
            else if a random number between 0.0 and 1.0 is less than rScale * rate_H_to_S:
                move this hybrid to Susceptible
                return
            
            else if a random number between 0.0 and 1.0 is less than iScale * rate_H_to_I:
                move this hybrid to Infected
                return
            
            return
'''

class Hybrid(Person):
    def __init__(self, name): # constructors
        super().__init__(name)
        hybrid_list.append(self)
        self.strength = random.randint(15,25)
        self.infection = 30
        self.recoveryChance = 100 - self.infection
        
    def takeDamage(self, attacker):
        self.health -= attacker.strength
        
        if self.health <= 0:
            self.health = 0
            self.transition()
            
        elif isinstance(attacker, Infected) or isinstance(attacker,Carrier):
            if self.infection >= 100:
                self.infection = 100
                self.transition()
                
            self.recoveryChance = 100 - self.infection
                
    def infectionGrowth(self):
        self.infection += 5
        
        if self.infection >= 100:
            self.infection = 100
            self.transition()
            
    def transition(self):
        self.recoveryChance = 100 - self.infection
        rScale = self.recoveryChance / 100
        iScale = self.infection / 100
                
        if self.health == 0:
            new = Removed(self.name, "Hybrid", "Killed")
            hybrid_list.remove(self)
            return
        
        elif random.random() < rScale * DELTA:
            new = Susceptible(self.name)
            hybrid_list.remove(self)
            return
        
        elif random.random() < iScale * ETA:
            new = Infected(self.name)
            hybrid_list.remove(self)
            return
        
        return
        
'''
CLASS Infected inherits Person
    Attributes:
        potency
        
    Constructors:
        add to infected list
        strength = random integer between 18 and 28
        potency = 25
    
    Methods:
        procedure infect(target):
            increase target's infection by potency
         
        procedure attack(target):
           if this infected's energy >= 5:
               output that this infected is attacking target
               lower target's health by this infected's strength
               subtract 5 from this infected's energy
               
               if target is Susceptible or target is Hybrid:
                   call infect(target)
                   
           else:
               output that this infected doesnt have enough energy to attack
            
            
        procedure transition:
            if this infected's health == 0:
                move this infected to Removed
                return
        
            else if a random number between 0.0 and 1.0 is less than rate_I_to_H:
                move this infected to Hybrid
                return
            
            return
'''

class Infected(Person):
    def __init__(self, name): # constructors
        super().__init__(name)
        infected_list.append(self)
        self.strength = random.randint(18,28)
        self.potency = 25
        
    def infect(self, target):
        target.infection += self.potency
        
    def attack(self, target): 
        if self.energy >= 5:
            print(self.name, "attacks", target.name, "!")
            target.takeDamage(self)
            self.energy -= 5
            
            if isinstance(target, Susceptible) or isinstance(target, Hybrid):
                self.infect(target)
        
        else: 
            print(self.name, "is too tired to attack", target.name)
            
            
    def transition(self):
        if self.health == 0:
            new = Removed(self.name, "Infected", "Killed")
            infected_list.remove(self)
            return
        
        elif random.random() < EPSILON:
            new = Hybrid(self.name)
            infected_list.remove(self)
            return
        
        return
        
''' 
CLASS Removed
    Attributes:
        name
        time_of_death
        cause_of_death
        origin_state
        
    Constructors(inputName, origin_state_input, cause_of_death_input):
        add to removed list
        name = inputName
        time_of_death = Day: " + day + ", time: " + time_of_day
        origin_state = origin_state_input
        cause_of_death = cause_of_death_input
        
    Methods:
        procedure getTOD:
            return time_of_death
        
        procedure getOrigin:
            return origin_state
        
        procedure setCOD(input):
            cause_of_death = input
            
         procedure getCOD:
             return cause_of_death
'''

class Removed(object):
    def __init__(self, name, origin_state, cause_of_death):
        removed_list.append(self)
        self.name = name
        self.time_of_death = f"Day: {day}, time: {time_of_day}"
        self.origin_state = origin_state
        self.cause_of_death = cause_of_death
        
    def getTOD(self):
        return self.time_of_death
    
    def getOrigin(self):
        return self.origin_state
    
    def setCOD(self, new_cause):
        self.cause_of_death = new_cause
        
    def getCOD(self):
        return self.cause_of_death

'''
procedure runSim(max_days)
    set time_of_day = 0
    set day = 0

    WHILE day < max_days:

        for each person in susceptible_list:
            call person.move()

        for each carrier in carrier_list:
            call carrier.move()

            for each infected in infected_list:
                set distance = |carrier.x_pos - infected.x_pos| 
                               + |carrier.y_pos - infected.y_pos|
                if distance <= 10:
                    call carrier.attack(infected)
                    call infected.attack(carrier)

            for each susceptible in susceptible_list:
                set distance = |carrier.x_pos - susceptible.x_pos| 
                               + |carrier.y_pos - susceptible.y_pos|
                if distance <= 10:
                    call carrier.attack(susceptible)
                    call susceptible.attack(carrier)

            for each hybrid in hybrid_list:
                set distance = |carrier.x_pos - hybrid.x_pos| 
                               + |carrier.y_pos - hybrid.y_pos|
                if distance <= 10:
                    call carrier.attack(hybrid)
                    call hybrid.attack(carrier)

        for each hybrid in hybrid_list:
            call hybrid.move()

            for each infected in infected_list:
                set distance = |hybrid.x_pos - infected.x_pos|
                               + |hybrid.y_pos - infected.y_pos|
                if distance <= 10:
                    call hybrid.attack(infected)
                    call infected.attack(hybrid)

            for each carrier in carrier_list:
                set distance = |hybrid.x_pos - carrier.x_pos|
                               + |hybrid.y_pos - carrier.y_pos|
                if distance <= 10:
                    call hybrid.attack(carrier)
                    call carrier.attack(hybrid)

        for each infected in infected_list:
            call infected.move()

            for each susceptible in susceptible_list:
                set distance = |infected.x_pos - susceptible.x_pos|
                               + |infected.y_pos - susceptible.y_pos|
                if distance <= 10:
                    call infected.attack(susceptible)
                    call susceptible.attack(infected)

            for each carrier in carrier_list:
                set distance = |infected.x_pos - carrier.x_pos|
                               + |infected.y_pos - carrier.y_pos|
                if distance <= 10:
                    call infected.attack(carrier)
                    call carrier.attack(infected)

            for each hybrid in hybrid_list:
                set distance = |infected.x_pos - hybrid.x_pos|
                               + |infected.y_pos - hybrid.y_pos|
                if distance <= 10:
                    call infected.attack(hybrid)
                    call hybrid.attack(infected)

        set time_of_day = time_of_day + 1
        if time_of_day == 24:
            set time_of_day = 0
            set day = day + 1

        for each person in a copy of susceptible_list:
            call person.transition()

        for each person in a copy of carrier_list:
            call person.transition()

        for each person in a copy of hybrid_list:
            call person.transition()

        for each person in a copy of infected_list:
            call person.transition()
'''

def runSim(max_days):
    global time_of_day, day
    time_of_day = 0
    day = 0
    
    # plotting list
    day_count = []
    susceptible_count = []
    carrier_count = []
    hybrid_count = []
    infected_count = []
    removed_count = []
    
    # base num for list
    day_count.append(0)
    susceptible_count.append(len(susceptible_list))
    carrier_count.append(len(carrier_list))
    hybrid_count.append(len(hybrid_list))
    infected_count.append(len(infected_list))
    removed_count.append(len(removed_list))

    while day < max_days:
        # 1. susceptible's move, interaction predefined 
        for person in susceptible_list:
            person.move()
        
        # 2. carrier move, then interact
        for person in carrier_list:
            person.move()
            
            # carrier meets infected
            for i in infected_list:
                if manhattan(person, i) <= 10:
                    person.attack(i)
                    i.attack(person)
            
            # carrier meets susceptible
            for s in susceptible_list:
                if manhattan(person, s) <= 10:
                    person.attack(s)
                    s.attack(person)
            
            # carrier meets hybrid
            for h in hybrid_list:
                if manhattan(person, h) <= 10:
                    person.attack(h)
                    h.attack(person)
        
        # 3. hybrid move, then interact
        for person in hybrid_list:
            person.move()
            
            # hybrid meets infected
            for i in infected_list:
                if manhattan(person, i) <= 10:
                    person.attack(i)
                    i.attack(person)
            
            # hybrid meets carrier
            for c in carrier_list:
                if manhattan(person, c) <= 10:
                    person.attack(c)
                    c.attack(person)
        
        # 4. infected move, then interact
        for person in infected_list:
            person.move()
            
            # infected meets susceptible
            for s in susceptible_list:
                if manhattan(person, s) <= 10:
                    person.attack(s)
                    s.attack(person)
            
            # infected meets carrier
            for c in carrier_list:
                if manhattan(person, c) <= 10:
                    person.attack(c)
                    c.attack(person)
            
            # infected meets hybrid
            for h in hybrid_list:
                if manhattan(person, h) <= 10:
                    person.attack(h)
                    h.attack(person)
            
        # 5. update time
        time_of_day += 1
        if time_of_day == 24:
            time_of_day = 0
            day += 1
            
            # plotting list
            day_count.append(day)
            susceptible_count.append(len(susceptible_list))
            carrier_count.append(len(carrier_list))
            hybrid_count.append(len(hybrid_list))
            infected_count.append(len(infected_list))
            removed_count.append(len(removed_list))

        
        # 6. Updates
        for person in carrier_list[:]:
            person.progressionIncrease()
            
        for person in hybrid_list[:]:
            person.infectionGrowth()
            
        # 7. transition 
        # [:] = copy of list, protects against skipping due to removing & adding objects
        for person in susceptible_list[:]:
            person.transition()
        for person in carrier_list[:]:
            person.transition()
        for person in hybrid_list[:]:
            person.transition()
        for person in infected_list[:]:
            person.transition()
        
        time.sleep(0.01)
        
    # create plot 
    plt.plot(day_count, susceptible_count, color='blue', label='Susceptible')
    plt.plot(day_count, carrier_count, color='yellow', label='Carrier')
    plt.plot(day_count, hybrid_count, color='orange', label='Hybrid')
    plt.plot(day_count, infected_count, color='green', label='Infected')
    plt.plot(day_count, removed_count, color='red', label='Removed')
    
    plt.xlabel("Time (days)")
    plt.ylabel("Population")
    plt.title("Simulation Statistics")
    plt.legend()
    plt.show()

        
''' 
Starters:

sam   = Susceptible("Sam")
sara  = Susceptible("Sara")
sid   = Susceptible("Sid")

# Carrier
cora  = Carrier("Cora")
cole  = Carrier("Cole")
cami  = Carrier("Cami")

# Hybrid
hyde  = Hybrid("Hyde")
hana  = Hybrid("Hana")
hugh  = Hybrid("Hugh")

# Infected
ivan  = Infected("Ivan")
iris  = Infected("Iris")
ian   = Infected("Ian")

'''


