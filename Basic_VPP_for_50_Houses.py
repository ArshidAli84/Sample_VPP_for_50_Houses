import numpy as np
import matplotlib.pyplot as plt

# Simulate data for 50 houses
num_houses = 50
monthly_consumption = np.random.uniform(150, 300, num_houses)  # kWh

# Introduce peak and off-peak hours
hours_in_month = 30 * 24  # Assuming 30 days in a month
peak_hours = np.random.choice(np.arange(hours_in_month), int(0.2 * hours_in_month), replace=False)
off_peak_hours = np.setdiff1d(np.arange(hours_in_month), peak_hours)

# Define pricing for peak and off-peak hours
peak_price = 0.15  # per kWh
off_peak_price = 0.10  # per kWh

# Calculate total monthly consumption for all houses during peak and off-peak hours
total_monthly_consumption = np.sum(monthly_consumption)  # Total consumption for the month
peak_consumption = total_monthly_consumption * 0.3  # 30% during peak hours
off_peak_consumption = total_monthly_consumption * 0.7  # 70% during off-peak hours

# Design a virtual power plant based on renewable sources
# Assume solar power generation for the virtual power plant
solar_capacity = total_monthly_consumption * 1.2  # Overcapacity for efficiency
solar_capacity_peak = 300  # Capacity of the installed solar plant during peak hours
solar_capacity_off_peak = 250  # Capacity of the installed solar plant during off-peak hours

# Battery storage system
battery_capacity = 1000  # kWh
battery_charge = 0.5 * battery_capacity  # Initial charge (50% of full capacity)
battery_efficiency = 0.9  # Charging and discharging efficiency

# Calculate total solar generation for peak and off-peak hours
solar_generation_peak = np.random.uniform(0.8, 1.2, num_houses) * (solar_capacity_peak * 0.3)
solar_generation_off_peak = np.random.uniform(0.8, 1.2, num_houses) * (solar_capacity_off_peak * 0.7)

# Calculate the total solar generation for the virtual power plant during peak and off-peak hours
total_solar_generation_peak = np.sum(solar_generation_peak)
total_solar_generation_off_peak = np.sum(solar_generation_off_peak)

# Calculate the total consumption during peak and off-peak hours
total_consumption_peak = np.sum(monthly_consumption * 0.3)
total_consumption_off_peak = np.sum(monthly_consumption * 0.7)

# Use solar generation during peak hours to provide full load demand
solar_to_peak_demand_ratio = total_solar_generation_peak / total_consumption_peak
if solar_to_peak_demand_ratio >= 1:
    print("Solar generation during peak hours can fully meet the demand.")
    battery_discharge = 0  # No battery discharge during peak hours
else:
    print("Solar generation during peak hours is insufficient. Using battery storage.")
    battery_discharge = np.minimum(battery_capacity, peak_consumption - total_solar_generation_peak) / battery_efficiency

# Rule-based strategy for off-peak hours
if total_solar_generation_off_peak >= off_peak_consumption:
    print("Solar generation during off-peak hours can fully meet the demand.")
    battery_discharge_off_peak = 0  # No battery discharge during off-peak hours
else:
    print("Solar generation during off-peak hours is insufficient. Using battery and solar.")
    shortage = off_peak_consumption - total_solar_generation_off_peak
    battery_discharge_off_peak = np.minimum(battery_capacity, shortage) / battery_efficiency

# Load-shifting strategy: Shift non-essential tasks to off-peak hours
shifted_consumption = np.clip(monthly_consumption - total_consumption_peak, 0, None)
solar_generation_off_peak += np.random.uniform(0.8, 1.2, num_houses) * shifted_consumption * 0.7

# Charge the battery during periods of excess solar generation
excess_solar = total_solar_generation_off_peak - off_peak_consumption
battery_charge += np.clip(excess_solar * battery_efficiency, 0, battery_capacity - battery_charge)

# Discharge the battery during peak hours to meet the demand
battery_charge -= battery_discharge

# Discharge the battery during off-peak hours to meet the demand
battery_charge -= battery_discharge_off_peak

# Recalculate total solar generation for off-peak hours after battery discharge
total_solar_generation_off_peak = np.sum(solar_generation_off_peak) + battery_discharge + battery_discharge_off_peak

# Check if the virtual power plant can meet the demand during peak and off-peak hours
peak_demand_met = total_solar_generation_peak >= total_consumption_peak
off_peak_demand_met = total_solar_generation_off_peak >= total_consumption_off_peak

# Determine load shedding hours based on demand during peak hours
load_shedding_hours_peak = max(0, int(total_consumption_peak - total_solar_generation_peak))

# Determine load shedding hours based on demand during off-peak hours
load_shedding_hours_off_peak = max(0, int(total_consumption_off_peak - total_solar_generation_off_peak))

# Implement a strategy to reduce load shedding by shifting non-essential tasks to off-peak hours
if not peak_demand_met:
    print(f"Load shedding expected during peak hours. Consider shifting non-essential tasks to off-peak hours.")
    print(f"Load shedding hours during peak: {load_shedding_hours_peak}")
else:
    print("Virtual power plant can meet the demand during peak hours.")

if not off_peak_demand_met:
    print(f"Load shedding expected during off-peak hours. Consider using a rule-based strategy to meet demand.")
    print(f"Load shedding hours during off-peak: {load_shedding_hours_off_peak}")
else:
    print("Virtual power plant can meet the demand during off-peak hours.")

# Visualize the data
fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axes[0].bar(range(num_houses), monthly_consumption, label='Monthly Consumption')
axes[0].bar(range(num_houses), solar_generation_peak, label='Solar Generation (Peak)', alpha=0.5)
axes[0].set_ylabel('Energy (kWh)')
axes[0].legend()
axes[0].set_title('Energy Consumption and Solar Generation during Peak Hours')

axes[1].bar(range(num_houses), monthly_consumption, label='Monthly Consumption')
axes[1].bar(range(num_houses), solar_generation_off_peak, label='Solar Generation (Off-Peak)', alpha=0.5)
axes[1].set_ylabel('Energy (kWh)')
axes[1].legend()
axes[1].set_title('Energy Consumption and Solar Generation during Off-Peak Hours')

axes[2].bar(range(num_houses), monthly_consumption, label='Monthly Consumption')
axes[2].bar(range(num_houses), shifted_consumption, label='Shifted Consumption (Off-Peak)', alpha=0.5)
axes[2].set_xlabel('House')
axes[2].set_ylabel('Energy (kWh)')
axes[2].legend()
axes[2].set_title('Energy Consumption with Load Shifting during Off-Peak Hours')

# Save the plot as a JPG file
plt.savefig('energy_management_plot_with_solar_250kwh.jpg')

# Show the plot
plt.show()
