# =========================================================
# Professional Pakistan-Specific Household Electricity Dataset Generator
# (Updated: house_size_marla now generates exact numeric marla values)
# =========================================================

import pandas as pd
import numpy as np

np.random.seed(42)
n = 15000  # number of rows

# ------------------- House Size (Exact Numeric Marlas) -------------------
# Original ranges with probabilities
ranges = {
    (0,5): 0.10,
    (5,10): 0.15,
    (10,15): 0.15,
    (15,20): 0.10,
    (20,30): 0.15,
    (30,40): 0.10,
    (40,50): 0.08,
    (50,60): 0.05,
    (60,70): 0.05,
    (70,80): 0.07
}

range_list = list(ranges.keys())
range_probs = list(ranges.values())

selected_ranges = np.random.choice(
    len(range_list),
    size=n,
    p=range_probs
)

# Generate an exact marla value inside the selected range
house_size_marla = np.array([
    np.random.randint(range_list[idx][0], range_list[idx][1])
    for idx in selected_ranges
])

# ------------------- Household Features -------------------
num_residents = np.random.randint(3, 9, n)
working_residents = np.array([np.random.randint(1, min(4,r+1)) for r in num_residents])

urban_rural = np.random.choice(['Urban','Rural'], size=n, p=[0.75,0.25])
energy_saving_appliances = np.random.choice([0,1], size=n, p=[0.7,0.3])  # 1 = Yes, 0 = No

# ------------------- Appliance Counts -------------------
num_lights = np.random.randint(5, 21, n)
num_fans = np.random.randint(1, 7, n)
num_AC = np.random.randint(0, 4, n)
num_fridge = np.random.randint(1, 3, n)
num_washing_machine = np.random.randint(0, 3, n)
num_TV = np.random.randint(1, 5, n)
num_computer = np.random.randint(0, 4, n)
num_water_heater = np.random.randint(0, 3, n)
num_oven = np.random.randint(0, 2, n)
num_microwave = np.random.randint(0, 2, n)
num_iron = np.random.randint(0, 2, n)
num_water_pump = np.random.randint(0, 2, n)

# ------------------- Adjust Appliances by House Size -------------------
for i, size in enumerate(house_size_marla):
    if size >= 10:
        num_lights[i] += 2
        num_fans[i] += 1
        num_AC[i] += 1
        num_water_heater[i] += 1
    if size >= 20:
        num_lights[i] += 3
        num_AC[i] += 1
        num_TV[i] += 1
        num_oven[i] += 1
        num_microwave[i] += 1

# ------------------- Daily Usage Hours -------------------
hours_lights = np.round(np.random.uniform(3, 8, n), 1)
hours_fans = np.round(np.random.uniform(4, 12, n), 1)
hours_AC = np.round(np.random.uniform(0, 12, n), 1)
hours_washing_machine = np.round(np.random.uniform(0, 1, n), 1)
hours_TV = np.round(np.random.uniform(1, 8, n), 1)
hours_computer = np.round(np.random.uniform(0, 8, n), 1)
hours_water_heater = np.round(np.random.uniform(0, 4, n), 1)
hours_oven = np.round(np.random.uniform(0, 2, n), 1)
hours_microwave = np.round(np.random.uniform(0, 2, n), 1)
hours_iron = np.round(np.random.uniform(0, 1, n), 1)
hours_water_pump = np.round(np.random.uniform(0, 3, n), 1)

# ------------------- Month & Temperature -------------------
month = np.random.randint(1, 13, n)

avg_temp_month = {
    1: 14, 2: 16, 3: 22, 4: 28, 5: 33, 6: 36,
    7: 34, 8: 33, 9: 32, 10: 28, 11: 22, 12: 16
}

temperature = np.array([np.random.normal(avg_temp_month[m], 3) for m in month])

# ------------------- Weekend/Holiday Effects -------------------
weekend = np.random.choice([0,1], size=n, p=[5/7,2/7])
weekend_factor = 1 + 0.1*weekend
holiday_factor = np.random.choice([0.9,1.0,1.1], size=n, p=[0.1,0.8,0.1])

hours_washing_machine *= weekend_factor * holiday_factor
hours_TV *= weekend_factor * holiday_factor
hours_oven *= weekend_factor * holiday_factor

# ------------------- Seasonal AC/Fan Effect -------------------
hot_months = [5,6,7,8]
ac_fan_factor = np.array([1.2 if m in hot_months else 1.0 for m in month])
hours_AC *= ac_fan_factor
hours_fans *= ac_fan_factor

# ------------------- Daily kWh Calculation -------------------
lights_kwh = num_lights * hours_lights * 0.06
fans_kwh = num_fans * hours_fans * 0.075
AC_kwh = num_AC * hours_AC * 1.5 * (1 + (temperature-25)/50)
fridge_kwh = num_fridge * 1.2
washing_machine_kwh = num_washing_machine * hours_washing_machine * 0.5
TV_kwh = num_TV * hours_TV * 0.1
computer_kwh = num_computer * hours_computer * 0.1
water_heater_kwh = num_water_heater * hours_water_heater * 4
oven_kwh = num_oven * hours_oven * 1.5
microwave_kwh = num_microwave * hours_microwave * 1.2
iron_kwh = num_iron * hours_iron * 1.0
water_pump_kwh = num_water_pump * hours_water_pump * 3.0

total_daily_kwh = (lights_kwh + fans_kwh + AC_kwh + fridge_kwh + washing_machine_kwh +
                   TV_kwh + computer_kwh + water_heater_kwh + oven_kwh +
                   microwave_kwh + iron_kwh + water_pump_kwh)

# ------------------- Energy-Saving Appliances Adjustment -------------------
monthly_kwh = total_daily_kwh * 30 * np.random.uniform(0.95,1.05,n)
monthly_kwh = monthly_kwh * np.where(energy_saving_appliances==1, np.random.uniform(0.85,0.9,n), 1.0)
monthly_kwh = np.round(monthly_kwh,1)

# ------------------- Derived Features -------------------
total_appliances = (num_lights + num_fans + num_AC + num_fridge + num_washing_machine +
                    num_TV + num_computer + num_water_heater + num_oven + num_microwave +
                    num_iron + num_water_pump)

avg_daily_kwh = np.round(monthly_kwh / 30,1)
kwh_per_resident = np.round(monthly_kwh / num_residents,1)

# ------------------- Create DataFrame -------------------
data = pd.DataFrame({
    'house_size_marla': house_size_marla,
    'num_residents': num_residents,
    'working_residents': working_residents,
    'urban_rural': urban_rural,
    'energy_saving_appliances': energy_saving_appliances,
    'weekend': weekend,
    'month': month,
    'temperature': np.round(temperature,1),
    'num_lights': num_lights,
    'hours_lights': hours_lights,
    'num_fans': num_fans,
    'hours_fans': hours_fans,
    'num_AC': num_AC,
    'hours_AC': hours_AC,
    'num_fridge': num_fridge,
    'num_washing_machine': num_washing_machine,
    'hours_washing_machine': hours_washing_machine,
    'num_TV': num_TV,
    'hours_TV': hours_TV,
    'num_computer': num_computer,
    'hours_computer': hours_computer,
    'num_water_heater': num_water_heater,
    'hours_water_heater': hours_water_heater,
    'num_oven': num_oven,
    'hours_oven': hours_oven,
    'num_microwave': num_microwave,
    'hours_microwave': hours_microwave,
    'num_iron': num_iron,
    'hours_iron': hours_iron,
    'num_water_pump': num_water_pump,
    'hours_water_pump': hours_water_pump,
    'total_appliances': total_appliances,
    'avg_daily_kwh': avg_daily_kwh,
    'kwh_per_resident': kwh_per_resident,
    'monthly_kwh': monthly_kwh
})

# ------------------- Save CSV -------------------
data.to_csv("household_energy_pakistan_professional_numeric.csv", index=False)
print("✅ Dataset generated with numeric marla values (no ranges). Saved as 'household_energy_pakistan_professional_numeric.csv'")
print(data.head())
# =========================================================
