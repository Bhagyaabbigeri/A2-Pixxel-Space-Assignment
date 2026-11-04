# ==========================================
# Pixxel Mission Operations - Assignment A2
# Exploratory Data Analysis (EDA) Script
# Author: Bhagyashree Reddy
# ==========================================

import pandas as pd
import numpy as np

print("--- 1. LOADING DATA ---")
# Load the 48-hour telemetry CSV file
df = pd.read_csv('telemetry_48h.csv')

print(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nColumn Names & Data Types:")
print(df.dtypes)

print("\n--- 2. DATA CLEANING & PREPROCESSING ---")
# Convert timestamp column to datetime objects
df['dt'] = pd.to_datetime(df['timestamp_utc'])

# Sort by time and remove duplicate timestamps (handling log anomalies)
original_len = len(df)
df = df.sort_values('dt').drop_duplicates(subset=['timestamp_utc']).reset_index(drop=True)
cleaned_len = len(df)
print(f"Removed {original_len - cleaned_len} duplicate timestamp rows.")

# Check time step cadences (expected 10 seconds)
time_diffs = df['dt'].diff().dt.total_seconds()
print("\nTime step diff value counts (seconds):")
print(time_diffs.value_counts().head(5))

print("\n--- 3. ORBIT PERIOD ANALYSIS ---")
# Identify eclipse entries (transition from sunlight '0' to shadow '1')
df['eclipse_diff'] = df['eclipse'].diff()
eclipse_entries = df[df['eclipse_diff'] == 1].copy()

# Compute time difference between consecutive eclipse entries
eclipse_entries['period_min'] = eclipse_entries['dt'].diff().dt.total_seconds() / 60.0
orbit_periods = eclipse_entries['period_min'].dropna()

print(f"Total Orbits Measured: {len(orbit_periods)}")
print(f"Mean Orbit Period: {orbit_periods.mean():.2f} minutes")
print(f"Min Orbit Period: {orbit_periods.min():.2f} minutes")
print(f"Max Orbit Period: {orbit_periods.max():.2f} minutes")
print(f"Std Dev Orbit Period: {orbit_periods.std():.3f} minutes")

print("\n--- 4. ECLIPSE DURATION & FRACTION ---")
# Group consecutive eclipse rows to measure shadow duration
df['eclipse_block'] = (df['eclipse'] != df['eclipse'].shift()).cumsum()
eclipse_blocks = df[df['eclipse'] == 1].groupby('eclipse_block')

eclipse_durations = []
for _, group in eclipse_blocks:
    duration_min = (len(group) * 10) / 60.0  # 10-second cadence per row
    eclipse_durations.append(duration_min)

eclipse_durations = pd.Series(eclipse_durations)
mean_eclipse = eclipse_durations.mean()
eclipse_fraction = mean_eclipse / orbit_periods.mean()

print(f"Mean Eclipse Duration: {mean_eclipse:.2f} minutes")
print(f"Eclipse Duration Range: {eclipse_durations.min():.2f} to {eclipse_durations.max():.2f} minutes")
print(f"Eclipse Fraction: {eclipse_fraction:.4f} ({eclipse_fraction * 100:.2f}% of orbit)")

print("\n--- 5. STATE-OF-CHARGE (SoC) DEPTH & ANOMALY DETECTION ---")
# Track battery drain per eclipse
depths = []
for _, group in eclipse_blocks:
    ent_idx = group.index[0]
    entry_soc = df.loc[ent_idx, 'batt_soc_pct']

    # Find lowest SoC before battery starts charging again (batt_current_a > 0)
    sub = df.loc[ent_idx : ent_idx + len(group) + 10]
    charging = sub[sub['batt_current_a'] > 0]
    end_check_idx = charging.index[0] if len(charging) > 0 else group.index[-1]

    min_soc = df.loc[ent_idx : end_check_idx, 'batt_soc_pct'].min()
    depths.append(entry_soc - min_soc)

depths = pd.Series(depths)
print(f"Mean SoC Drain Depth per Eclipse: {depths.mean():.2f}%")
print(f"SoC Depth Range: {depths.min():.2f}% to {depths.max():.2f}%")

# Check starting SoC vs ending SoC to show battery decay
print(f"Battery SoC at Start (Orbit 1): {df['batt_soc_pct'].iloc[0]:.2f}%")
print(f"Battery SoC at End (Orbit 30): {df['batt_soc_pct'].iloc[-1]:.2f}%")

print("\n--- EDA ANALYSIS COMPLETE ---")