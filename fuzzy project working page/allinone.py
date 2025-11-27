import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------- Fuzzy I/O variables ----------

# Inputs
temperature = ctrl.Antecedent(np.arange(-44, 86, 1), 'temperature')  # °C
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')         # %
feeling = ctrl.Antecedent(np.arange(0, 11, 1), 'feeling')            # 0=cold ... 10=hot
ecology = ctrl.Antecedent(np.arange(0, 11, 1), 'ecology')            # 0=eco ... 10=not eco

# Output
heat = ctrl.Consequent(np.arange(10, 45, 1), 'heat')                 # heating level °C

# ---------- Membership functions ----------

def temp_membership_func(var, b1, c1, s1, m1, s2, m2, s3 ,m3, b2, c2):
    var['too cold']     = fuzz.sigmf(var.universe, b=b1,  c=-c1)
    var['chilly']       = fuzz.gaussmf(var.universe, sigma=s1, mean=m1)
    var['comfortable']  = fuzz.gaussmf(var.universe, sigma=s2, mean=m2)
    var['rather hot']   = fuzz.gaussmf(var.universe, sigma=s3, mean=m3)
    var['too hot']      = fuzz.sigmf(var.universe, b=b2, c=c2)

# Default membership functions (example for living room)
temp_membership_func(temperature, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 1.49, 26.77, 29.50, 4.66)
temp_membership_func(heat, 13.00, 3.16, 2.67, 17.62, 2.91, 21.07, 1.49, 26.77, 29.50, 4.66)

humidity['low']  = fuzz.trapmf(humidity.universe, [0, 0, 0, 45])
humidity['ok']   = fuzz.trimf(humidity.universe, [0, 45, 100])
humidity['high'] = fuzz.trapmf(humidity.universe, [45, 100, 100, 100])

feeling['too cold'] = fuzz.trapmf(feeling.universe, [0, 0, 0, 5])
feeling['okay']     = fuzz.trimf(feeling.universe, [0, 5, 10])
feeling['too hot']  = fuzz.trapmf(feeling.universe, [5, 10, 10, 10])

ecology['eco']     = fuzz.trapmf(ecology.universe, [0, 0, 0, 5])
ecology['medium']  = fuzz.trimf(ecology.universe, [0, 5, 10])
ecology['not eco'] = fuzz.trapmf(ecology.universe, [5, 10, 10, 10])

# ---------- Rules ----------
r1  = ctrl.Rule(temperature['too hot'], heat['chilly'])
r2  = ctrl.Rule(temperature['too cold'], heat['rather hot'])
r3  = ctrl.Rule(temperature['chilly'] & feeling['too cold'], heat['rather hot'])
r4  = ctrl.Rule(temperature['chilly'] & feeling['too hot'], heat['too cold'])
r5  = ctrl.Rule(temperature['rather hot'] & feeling['too cold'], heat['too hot'])
r6  = ctrl.Rule(temperature['rather hot'] & feeling['too hot'], heat['chilly'])
r7  = ctrl.Rule(temperature['chilly'] & feeling['okay'], heat['chilly'])
r8  = ctrl.Rule(temperature['rather hot'] & feeling['okay'], heat['rather hot'])
r9  = ctrl.Rule(temperature['comfortable'] & feeling['too hot'], heat['chilly'])
r10 = ctrl.Rule(temperature['comfortable'] & feeling['okay'], heat['comfortable'])
r11 = ctrl.Rule(temperature['comfortable'] & feeling['too cold'], heat['rather hot'])
r12 = ctrl.Rule((temperature['too cold'] | temperature['chilly']) & ecology['eco'], heat['chilly'])
r13 = ctrl.Rule((temperature['too hot'] | temperature['rather hot']) & ecology['eco'], heat['rather hot'])
r14 = ctrl.Rule((temperature['too cold'] | temperature['chilly']) & ecology['medium'], heat['comfortable'])
r15 = ctrl.Rule((temperature['too hot'] | temperature['rather hot']) & ecology['medium'], heat['comfortable'])
r16 = ctrl.Rule((temperature['too cold'] | temperature['chilly']) & ecology['not eco'], heat['rather hot'])
r17 = ctrl.Rule((temperature['too hot'] | temperature['rather hot']) & ecology['not eco'], heat['chilly'])

heating_ctrl = ctrl.ControlSystem([r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15,r16,r17])
heating_sim = ctrl.ControlSystemSimulation(heating_ctrl)

# ---------- Fuzzy compute function ----------
def fuzzy_compute(t, h, feeling, ecology, room=None):
    """
    Computes heating output based on inputs.
    """
    heating_sim.input['temperature'] = t
    heating_sim.input['humidity'] = h
    heating_sim.input['feeling'] = feeling
    heating_sim.input['ecology'] = ecology

    heating_sim.compute()
    return heating_sim.output['heat']
